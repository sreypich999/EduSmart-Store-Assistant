# EduSmart Store Assistant

![EduSmart Store Assistant Interface](https://github.com/sreypich999/EduSmart-Store-Assistant/blob/main/photo_2025-10-26_19-29-17.jpg)

An AI-powered educational store assistant with bilingual voice support, built with FastAPI, Gemini AI, and ChromaDB vector search. Features **Retrieval-Augmented Generation (RAG)**, **Automatic Speech Recognition (ASR)**, and **Text-to-Speech (TTS)** capabilities.

## 🎯 Overview

EduSmart Store Assistant is a sophisticated chatbot application designed to help customers discover and learn about educational products. The system combines:

- **AI-Powered Conversations**: Uses Google's Gemini AI for intelligent responses
- **Product Search**: Vector-based search through 50+ educational products using ChromaDB
- **Voice Support**: Text-to-speech and speech-to-text capabilities
- **Bilingual Interface**: Supports English and Khmer (Cambodian) languages
- **Conversation Memory**: Maintains context across chat sessions
- **Modern Web Interface**: Responsive chat UI with real-time interactions

## 🚀 Features

### Core Functionality
- **Intelligent Product Recommendations**: AI-driven suggestions based on user queries
- **Voice Input/Output**: Speak to the assistant and receive voice responses
- **Multilingual Support**: Full English and Khmer language support
- **Conversation History**: Persistent chat memory using SQLite
- **Real-time Chat Interface**: Modern, responsive web UI

### Product Categories
- **STEM & Science**: Robotics kits, microscopes, chemistry labs, physics equipment
- **Art & Creativity**: Professional art supplies, digital tablets, pottery tools
- **Books & Literature**: Classic literature, science encyclopedias, language learning
- **Electronics & Technology**: Educational tablets, coding laptops, VR headsets
- **Early Learning**: Montessori materials, phonics systems, math manipulatives
- **Classroom Equipment**: Smart boards, language labs, STEM classroom kits

### Technical Features
- **RAG (Retrieval-Augmented Generation)**: Combines vector search with AI generation for accurate product recommendations
- **ASR (Automatic Speech Recognition)**: Browser-based speech-to-text using Web Speech API
- **TTS (Text-to-Speech)**: Google gTTS integration for voice responses in multiple languages
- **Vector Search**: ChromaDB-powered semantic product search
- **AI Integration**: Google Gemini 2.5 Flash model for responses
- **CORS Support**: Cross-origin resource sharing enabled
- **Health Monitoring**: Built-in health check endpoints

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance async web framework
- **Google Gemini AI**: Advanced language model for responses
- **LangChain**: AI framework for streamlined Gemini integration and prompt management
- **ChromaDB**: Vector database for product embeddings (uses `all-MiniLM-L6-v2` embedding model)
- **SQLite**: Relational database for conversation history
- **gTTS**: Google Text-to-Speech for voice responses
- **python-dotenv**: Environment variable management for API keys

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **Vanilla JavaScript**: No framework dependencies
- **ASR Integration**: Web Speech API connecting to Google Cloud Speech (no API key required)
- **TTS Playback**: Web Audio API for voice response playback
- **Bilingual UI**: Dynamic language switching with Khmer and English support

### Development Tools
- **Python 3.10+**: Core programming language
- **Uvicorn**: ASGI server for FastAPI
- **python-dotenv**: Environment variable management
- **Pydantic**: Data validation and serialization

## 📋 Prerequisites

- Python 3.10 or higher
- Google Gemini API key
- Modern web browser with Web Speech API support (Chrome/Edge recommended)
- Internet connection for AI services

## 🔧 Installation



### 1. Set Up Python Environment
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Initialize Databases
```bash
cd backend
python init_database.py
```

This will:
- Create SQLite database for conversation history
- Initialize ChromaDB with 50 educational products
- Set up vector embeddings using `all-MiniLM-L6-v2` model for semantic search

## 🚀 Running the Application

### Start the Backend Server
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### Access the Application
Open your browser and navigate to: `http://localhost:5000`

The FastAPI backend serves the frontend automatically.

## 📖 API Endpoints

### Chat Endpoint
- **POST** `/chat`
- Accepts: `UserMessage` with message, user_id, session_id, response_type, language
- Returns: `AssistantResponse` with text, audio_data, session_id, response_type, timestamp

### Health Check
- **GET** `/health`
- Returns system status and timestamp

### Database Test
- **GET** `/test-db`
- Returns database connection status and product counts

## 🎨 Usage

### Basic Interaction
1. Open the web interface
2. Choose your preferred response type (Text & Voice, Text Only, Voice Only)
3. Select language (English/Khmer)
4. Type or speak your question about educational products
5. Receive AI-powered responses with product recommendations

### Voice Features (ASR & TTS)
- **ASR Input**: Click the voice button to speak your query using Web Speech API (connects to Google Cloud Speech automatically - no API key needed)
- **TTS Output**: Responses can include audio playback with gTTS-generated voice synthesis
- **Language Detection**: Automatic language detection for speech recognition (English/Khmer)
- **Voice Response Types**: Choose between text-only, voice-only, or combined text+voice responses

### Example Queries
- "Show me STEM kits for teenagers"
- "What art supplies do you have for beginners?"
- "Recommend books for learning programming"
- "Find science equipment for middle school"

## 🗂️ Project Structure

```
education-store/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── init_database.py        # Database initialization
│   ├── requirements.txt        # Python dependencies
│   ├── education_store.db      # SQLite database
│   ├── chroma_db/              # Vector database
│   └── .env                    # Environment variables
├── frontend/
│   └── index.html              # Web interface
├── pyproject.toml              # Project configuration
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## 🔍 Key Components

### EducationStoreRAG Class - **RAG Implementation**
Handles the core RAG (Retrieval-Augmented Generation) functionality:
- **Retrieval**: Uses ChromaDB vector search with `all-MiniLM-L6-v2` embeddings to find relevant educational products
- **Augmentation**: Combines retrieved product data with conversation history for context
- **Generation**: Leverages Google Gemini AI to create personalized, accurate responses
- **Multilingual Support**: Generates responses in English and Khmer with appropriate TTS language selection
- **Fallback Mechanisms**: Graceful degradation when AI services are unavailable

### ChromaProductSearch Class - **Vector Search Engine**
Manages vector-based product search:
- **Embedding Model**: Uses `all-MiniLM-L6-v2` (Sentence Transformers) for 384-dimensional semantic text embeddings
- **Semantic Search**: Vector similarity matching through 50+ educational products
- **Fallback System**: Returns demo products if ChromaDB is unavailable
- **Metadata Filtering**: Ranks results based on relevance scores and product attributes

### TextToSpeechService Class - **TTS Implementation**
Handles text-to-speech conversion:
- **TTS Engine**: Google gTTS (Google Text-to-Speech) for high-quality voice synthesis
- **Language Support**: English and Khmer voice generation
- **Text Cleaning**: Removes markdown, links, and formatting for clean speech output
- **Audio Format**: Base64-encoded audio for web playback

### ConversationMemory Class
Maintains chat history and context:
- SQLite-based persistent storage
- Session-based conversation tracking
- Automatic cleanup and management

### Frontend ASR Integration - **Speech Recognition**
Browser-based automatic speech recognition:
- **API**: Web Speech API (browser-native, no API key required)
- **Provider**: Google Cloud Speech (automatic browser integration)
- **Languages**: English (`en-US`) and Khmer (`km-KH`) support
- **Features**: Real-time transcription, continuous mode, error handling

## 🌐 Browser Support

### Recommended Browsers
- Google Chrome (full feature support)
- Microsoft Edge (full feature support)
- Firefox (limited voice features)

### Voice Features
- **ASR**: Uses Web Speech API (browser-native, connects to Google Cloud Speech automatically - no API key needed)
- **TTS**: Uses Google gTTS service for voice synthesis
- Speech recognition requires HTTPS in production
- Text-to-speech works in all modern browsers
- Khmer language support may vary by browser

## 🔄 **Complete RAG + ASR + TTS Integration Flow**

### **Step-by-Step Process:**

1. **🎤 ASR Input** (Web Speech API)
   - User clicks voice button → Browser requests microphone permission
   - Speech captured → Sent to Google Cloud Speech (automatic, no API key)
   - Audio transcribed to text in real-time (English/Khmer support)
   - Text inserted into chat input field

2. **🔍 RAG Retrieval** (ChromaDB + Sentence Transformers)
   - User text query processed using `all-MiniLM-L6-v2` embeddings
   - Semantic search through 50+ educational products in vector database
   - Top relevant products retrieved based on similarity scores
   - Product metadata (name, description, price, category) extracted

3. **🤖 RAG Generation** (Google Gemini AI)
   - Retrieved product data + conversation history → Context creation
   - Multilingual prompts generated (English/Khmer)
   - Gemini AI generates personalized, contextual responses
   - Response stored in conversation memory (SQLite)

4. **🔊 TTS Output** (Google gTTS)
   - AI response text cleaned (remove markdown, formatting)
   - Language detected (English/Khmer) for appropriate voice
   - Text converted to speech audio via Google gTTS
   - Audio encoded as Base64 for web playback

5. **🎧 Audio Playback** (Web Audio API)
   - Base64 audio decoded and played in browser
   - Voice response synchronized with text display
   - Multiple audio responses can play sequentially

### **Technology Integration:**
- **ASR**: Browser-native (Web Speech API) → Google Cloud Speech
- **RAG**: ChromaDB (embeddings) + Gemini AI (generation)
- **TTS**: Google gTTS service
- **Storage**: SQLite (conversations) + ChromaDB (vectors)

## 🛡️ Security Considerations

- API keys stored in environment variables
- CORS enabled for development
- Input validation using Pydantic models
- No user authentication implemented (add as needed)

## 🔧 Configuration

### Environment Variables
```env
GEMINI_API_KEY=your_api_key_here
```

### LangChain Integration
The application uses LangChain as the primary framework for Gemini AI integration, providing:
- Structured prompt management
- Conversation chain handling
- Seamless API abstraction
- Fallback to direct Gemini API if LangChain is unavailable

### Database Configuration
- SQLite database path: `education_store.db`
- ChromaDB path: `./chroma_db`
- Embedding model: `all-MiniLM-L6-v2` (384-dimensional sentence embeddings)
- Conversation history retention: Configurable in ConversationMemory class

## 🐛 Troubleshooting

### Common Issues

**AI responses not working:**
- Check GEMINI_API_KEY in .env file
- Verify internet connection
- Check API key validity

**Voice features not working:**
- Ensure HTTPS in production
- Check browser compatibility
- Verify microphone permissions

**Database errors:**
- Run `python init_database.py` to reinitialize
- Check file permissions
- Verify ChromaDB installation

**Port already in use:**
- Change port in uvicorn command
- Kill existing processes on port 5000



## 🔗 **External Services & APIs Used**

### **AI & Language Models:**
- **Google Gemini AI**: https://ai.google.dev/ (for RAG text generation)
- **LangChain**: https://python.langchain.com/ (AI framework for Gemini integration)
- **Google Cloud Speech-to-Text**: https://cloud.google.com/speech-to-text (ASR backend)
- **Google Text-to-Speech (gTTS)**: https://pypi.org/project/gTTS/ (TTS service)

### **Browser APIs:**
- **Web Speech API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API (ASR)
- **Web Audio API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API (audio playback)

### **Vector Search & Embeddings:**
- **ChromaDB**: https://www.trychroma.com/ (vector database)
- **Sentence Transformers (all-MiniLM-L6-v2)**: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 (embeddings)



---

**Happy Learning with EduSmart Store Assistant! 🎓📚**
