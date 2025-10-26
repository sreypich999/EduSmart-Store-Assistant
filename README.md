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
- **ChromaDB**: Vector database for product embeddings (uses `all-MiniLM-L6-v2` embedding model)
- **SQLite**: Relational database for conversation history
- **gTTS**: Google Text-to-Speech for voice responses
- **LangChain**: Optional AI framework integration

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **Vanilla JavaScript**: No framework dependencies
- **ASR Integration**: Web Speech API for real-time speech recognition
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

```

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
- **ASR Input**: Click the voice button to speak your query using browser-based speech recognition
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

### EducationStoreRAG Class
Handles the core RAG (Retrieval-Augmented Generation) functionality:
- **RAG Pipeline**: Retrieves relevant products via ChromaDB vector search, then generates contextual responses using Gemini AI
- **Context Integration**: Combines product information with conversation history for personalized recommendations
- **Multilingual Support**: Generates responses in English and Khmer with appropriate TTS language selection
- **Fallback Mechanisms**: Graceful degradation when AI services are unavailable

### ChromaProductSearch Class
Manages vector-based product search:
- **Embedding Model**: Uses `all-MiniLM-L6-v2` (Sentence Transformers) for semantic text embeddings
- Semantic search through product catalog with vector similarity matching
- Fallback to demo products if ChromaDB unavailable
- Metadata filtering and ranking based on relevance scores

### ConversationMemory Class
Maintains chat history and context:
- SQLite-based persistent storage
- Session-based conversation tracking
- Automatic cleanup and management

## 🌐 Browser Support

### Recommended Browsers
- Google Chrome (full feature support)
- Microsoft Edge (full feature support)
- Firefox (limited voice features)

### Voice Features
- Speech recognition requires HTTPS in production
- Text-to-speech works in all modern browsers
- Khmer language support may vary by browser

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

### Optional LangChain Integration
The application supports both direct Gemini API and LangChain integration. LangChain provides additional features but requires compatible versions.

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




## 🙏 Acknowledgments

- Google Gemini AI for language model capabilities
- ChromaDB for vector database functionality
- FastAPI for the web framework
- gTTS for text-to-speech services


---

**Happy Learning with EduSmart Store Assistant! 🎓📚**
