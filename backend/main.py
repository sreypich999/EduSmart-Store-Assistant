from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
import sqlite3
import chromadb
import uuid
from datetime import datetime
import logging
import base64
from gtts import gTTS
import io
import tempfile
from typing import Optional
from dotenv import load_dotenv

# LangChain imports (compatible versions)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.schema import HumanMessage
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    logger.warning(f"LangChain imports failed: {e}")
    LANGCHAIN_AVAILABLE = False
    ChatGoogleGenerativeAI = None
    HumanMessage = None

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Education Store Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key and LANGCHAIN_AVAILABLE:
    genai.configure(api_key=gemini_api_key)
    # Initialize LangChain Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_api_key,
        temperature=0.7
    )
else:
    if gemini_api_key and not LANGCHAIN_AVAILABLE:
        logger.warning("LangChain not available, using direct Gemini API")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
    else:
        logger.warning("GEMINI_API_KEY not found or LangChain unavailable. AI features will be disabled.")
        model = None
    llm = None

class UserMessage(BaseModel):
    message: str
    user_id: str
    session_id: Optional[str] = None
    response_type: str = "both"
    language: str = "en"

class AssistantResponse(BaseModel):
    text: str
    audio_data: Optional[str] = None
    session_id: str
    response_type: str
    timestamp: str

class TextToSpeechService:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def text_to_speech(self, text: str, lang: str = 'en') -> Optional[str]:
        try:
            clean_text = self.clean_text_for_speech(text)
            tts_lang = 'km' if lang == 'km' else 'en'
            tts = gTTS(text=clean_text, lang=tts_lang, slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
            return audio_base64
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            return None
    
    def clean_text_for_speech(self, text: str) -> str:
        import re
        clean_text = re.sub(r'[**]', '', text)
        clean_text = re.sub(r'[*]', '', clean_text)
        clean_text = re.sub(r'#+', '', clean_text)
        clean_text = re.sub(r'\[.*?\]\(.*?\)', '', clean_text)
        clean_text = re.sub(r'\n+', '. ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        return clean_text.strip()

class ConversationMemory:
    def __init__(self):
        self.max_history = 10
    
    def store_conversation(self, user_id: str, session_id: str, user_message: str, assistant_response: str):
        try:
            conn = get_db_connection()
            if conn is None:
                logger.warning("No database connection. Skipping conversation storage.")
                return
                
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO conversation_history 
                (user_id, session_id, user_message, assistant_response, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, session_id, user_message, assistant_response, datetime.utcnow()))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
    
    def get_conversation_history(self, user_id: str, session_id: str, limit: int = 5):
        try:
            conn = get_db_connection()
            if conn is None:
                logger.warning("No database connection. Returning empty history.")
                return []
                
            cur = conn.cursor()
            cur.execute("""
                SELECT user_message, assistant_response 
                FROM conversation_history 
                WHERE user_id = ? AND session_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (user_id, session_id, limit))
            results = cur.fetchall()
            cur.close()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []

class ChromaProductSearch:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(path="./chroma_db")
            self.collection = self.client.get_collection("education_products")
            logger.info("✅ ChromaDB connected successfully")
        except Exception as e:
            logger.error(f"❌ ChromaDB connection failed: {e}")
            self.collection = None
    
    def search_products(self, query: str, n_results: int = 5):
        if not self.collection:
            logger.warning("ChromaDB not available, returning demo products")
            return self.get_demo_products()
        
        try:
            # Search in ChromaDB
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            products = []
            if results['metadatas']:
                for metadata in results['metadatas'][0]:
                    products.append({
                        'name': metadata.get('product_name', ''),
                        'description': metadata.get('description', ''),
                        'price': metadata.get('price', 0),
                        'category': metadata.get('category', ''),
                        'stock': metadata.get('stock', 0),
                        'age_range': metadata.get('age_range', ''),
                        'brand': metadata.get('brand', ''),
                        'features': metadata.get('features', '')
                    })
            
            return products if products else self.get_demo_products()
            
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            return self.get_demo_products()
    
    def get_demo_products(self):
        """Return demo products when ChromaDB is not available"""
        return [
            {
                'name': 'STEM Robotics Kit Pro',
                'description': 'Advanced robotics kit with coding capabilities for teens',
                'price': 149.99,
                'category': 'STEM',
                'stock': 35,
                'age_range': '14-18 years',
                'brand': 'RoboTech Pro',
                'features': 'AI programming, Multiple sensors, Machine learning'
            },
            {
                'name': 'Digital Microscope Pro',
                'description': 'High-precision digital microscope with 2000x magnification',
                'price': 129.99,
                'category': 'Science',
                'stock': 25,
                'age_range': '12+ years',
                'brand': 'ScienceVision',
                'features': '2000x magnification, 4K imaging, Computer connectivity'
            }
        ]

class EducationStoreRAG:
    def __init__(self):
        self.memory = ConversationMemory()
        self.tts_service = TextToSpeechService()
        self.product_search = ChromaProductSearch()
        self.llm = llm
        self.model = model if not LANGCHAIN_AVAILABLE else None
    
    def get_context(self, query: str, language: str = "en"):
        products = self.product_search.search_products(query)
        
        if not products:
            if language == "km":
                return "មិនមានផលិតផលជាក់លាក់ត្រូវនឹងសំណើររបស់អ្នកទេ។ ខ្ញុំអាចជួយឆ្លើយសំណួរទូទៅអំពីហាងផ្គត់ផ្គង់អប់រំបាន។"
            else:
                return "No specific products found matching your query. I can help with general education store questions."
        
        if language == "km":
            context = "ផលិតផលអប់រំពាក់ព័ន្ធ៖\n"
        else:
            context = "Relevant Education Products:\n"
            
        for i, product in enumerate(products, 1):
            name = product['name']
            desc = product['description']
            price = product['price']
            category = product['category']
            stock = product['stock']
            age_range = product['age_range']
            brand = product['brand']
            features = product.get('features', '')
            
            if language == "km":
                context += f"""{i}. {name} ({brand})
   ការពិពណ៌នា៖ {desc}
   លក្ខណៈពិសេស៖ {features}
   ប្រភេទ៖ {category} | អាយុ៖ {age_range}
   តម្លៃ៖ ${price} | ស្តុក៖ {stock} ឯកតា
   
"""
            else:
                context += f"""{i}. {name} ({brand})
   Description: {desc}
   Features: {features}
   Category: {category} | Age: {age_range}
   Price: ${price} | Stock: {stock} units
   
"""
        return context

    def generate_response(self, user_message: str, user_id: str, session_id: str, response_type: str = "both", language: str = "en"):
        try:
            # If neither Gemini nor LangChain is configured, use a simple response
            if not self.llm and not self.model:
                if language == "km":
                    simple_response = "ខ្ញុំនៅទីនេះដើម្បីជួយអ្នកជាមួយផលិតផលហាងអប់រំ! បច្ចុប្បន្នដំណើរការក្នុងរបៀបសាកល្បង។ សូមកំណត់ GEMINI_API_KEY សម្រាប់ការឆ្លើយតប AI។"
                else:
                    simple_response = "I'm here to help with education store products! Currently running in demo mode. Please configure GEMINI_API_KEY for AI responses."
                
                audio_data = self.tts_service.text_to_speech(simple_response, language) if response_type in ["voice", "both"] else None
                return {
                    "text": simple_response,
                    "audio_data": audio_data,
                    "response_type": response_type
                }
            
            # Get conversation history
            history = self.memory.get_conversation_history(user_id, session_id)
            
            # Get product context using ChromaDB
            product_context = self.get_context(user_message, language)
            
            # Create conversation context
            conversation_context = ""
            for user_msg, assistant_resp in reversed(history):
                conversation_context += f"User: {user_msg}\nAssistant: {assistant_resp}\n"
            
            # Create language-specific prompts
            if language == "km":
                system_prompt = """អ្នកគឺជាជំនួយការដែលមានចំណេះដឹង និងរួសរាយសម្រាប់ "ហាង EduSmart" ដែលជាហាងលក់ផលិតផលអប់រំ។ 
ជួយអតិថិជនជាមួយនឹងការស្វែងរកផលិតផល ការណែនាំ និងដំបូន្មានអប់រំ។

ព័ត៌មានហាង៖
- យើងឯកទេសក្នុងការផ្គត់ផ្គង់សម្ភារៈអប់រំសម្រាប់អាយុគ្រប់ប្រភេទ
- ផលិតផលរួមមានឧបករណ៍ STEM សៀវភៅ គ្រឿងសិល្បៈ ឧបករណ៍បន្ទប់រៀន
- យើងផ្តល់ផលិតផលសម្រាប់គ្រូ ឪពុកម្តាយ និងសិស្ស
- ជួរតម្លៃ៖ ៥$ - ៥០០$

{product_context}

{conversation_context}

សូមឆ្លើយតបជាភាសាខ្មែរ និងប្រើប្រាស់ព័ត៌មានផលិតផលខាងលើដើម្បីផ្តល់ចម្លើយដែលមានប្រយោជន៍។
រក្សាការសន្ទនាធម្មជាតិ និងលើកទឹកចិត្តអំពីការរៀនសូត្រ។"""
            else:
                system_prompt = """You are a friendly and knowledgeable assistant for "EduSmart Store", an education supplies retailer. 
Help customers with product inquiries, recommendations, and educational advice.

STORE INFORMATION:
- We specialize in educational materials for all ages
- Products include STEM kits, books, art supplies, classroom equipment
- We offer products for teachers, parents, and students
- Price range: $5 - $500

{product_context}

{conversation_context}

Please respond in English and use the product information above to provide helpful responses.
Maintain natural conversation flow and be positive about learning and education."""
            
            # Create the final prompt
            prompt = system_prompt.format(
                product_context=product_context,
                conversation_context=conversation_context
            )
            
            response_text = ""
            
            # Use LangChain if available, otherwise use direct Gemini
            if self.llm and LANGCHAIN_AVAILABLE:
                # Use LangChain with Gemini
                messages = [
                    HumanMessage(content=f"User question: {user_message}\n\nContext: {prompt}")
                ]
                response = self.llm.invoke(messages)
                response_text = response.content
            elif self.model:
                # Use direct Gemini API
                full_prompt = f"{prompt}\n\nCurrent user question: {user_message}\n\nResponse:"
                response = self.model.generate_content(full_prompt)
                response_text = response.text
            else:
                raise Exception("No AI model available")
            
            # Store conversation
            self.memory.store_conversation(user_id, session_id, user_message, response_text)
            
            # Generate audio if needed
            audio_data = None
            if response_type in ["voice", "both"]:
                audio_data = self.tts_service.text_to_speech(response_text, language)
            
            return {
                "text": response_text,
                "audio_data": audio_data,
                "response_type": response_type
            }
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            if language == "km":
                error_text = "សូមអភ័យទោស ខ្ញុំមានបញ្ហាក្នុងការដំណើរការសំណើរបស់អ្នកឥឡូវនេះ។ សូមព្យាយាមម្តងទៀត។"
            else:
                error_text = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
            
            audio_data = None
            if response_type in ["voice", "both"]:
                audio_data = self.tts_service.text_to_speech(error_text, language)
            
            return {
                "text": error_text,
                "audio_data": audio_data,
                "response_type": response_type
            }

def get_db_connection():
    """Get SQLite database connection"""
    try:
        conn = sqlite3.connect('education_store.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"SQLite connection error: {e}")
        return None

# Initialize RAG system
rag_system = EducationStoreRAG()

@app.post("/chat", response_model=AssistantResponse)
async def chat_endpoint(user_message: UserMessage):
    try:
        if not user_message.session_id:
            user_message.session_id = str(uuid.uuid4())
        
        response_data = rag_system.generate_response(
            user_message.message, 
            user_message.user_id, 
            user_message.session_id,
            user_message.response_type,
            user_message.language
        )
        
        # Ensure audio_data is not None for the response model
        audio_data = response_data["audio_data"] or ""
        
        return AssistantResponse(
            text=response_data["text"],
            audio_data=audio_data,
            session_id=user_message.session_id,
            response_type=user_message.response_type,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        error_text = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
        if user_message.language == "km":
            error_text = "សូមអភ័យទោស ខ្ញុំមានបញ្ហាក្នុងការដំណើរការសំណើរបស់អ្នកឥឡូវនេះ។ សូមព្យាយាមម្តងទៀត។"
        
        return AssistantResponse(
            text=error_text,
            audio_data="",
            session_id=user_message.session_id or str(uuid.uuid4()),
            response_type=user_message.response_type,
            timestamp=datetime.utcnow().isoformat()
        )

@app.get("/")
async def serve_frontend():
    return FileResponse('../frontend/index.html')

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/test-db")
async def test_database():
    """Test endpoint to check database connections"""
    # Test SQLite
    sqlite_conn = get_db_connection()
    sqlite_status = "connected" if sqlite_conn else "disconnected"
    
    # Test ChromaDB
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = chroma_client.get_collection("education_products")
        chroma_status = "connected"
        product_count = chroma_collection.count()
    except Exception as e:
        chroma_status = f"error: {str(e)}"
        product_count = 0
    
    return {
        "sqlite_status": sqlite_status,
        "chromadb_status": chroma_status,
        "vector_products_count": product_count,
        "gemini_configured": (llm is not None) or (model is not None),
        "langchain_available": LANGCHAIN_AVAILABLE
    }

# Mount static files
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '../frontend')

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
else:
    logger.warning(f"Frontend directory not found: {frontend_dir}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)