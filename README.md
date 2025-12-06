# AI-Driven E-Book Platform 📚🤖

[![GitHub](https://img.shields.io/badge/GitHub-Uzairrrrrr%2Fhackathon--1-blue)](https://github.com/Uzairrrrrr/hackathon-1)

An interactive e-book platform with AI-powered chatbot assistance, user authentication, personalized content, and Urdu translation capabilities. Built for hackathon with modern tech stack.

## 🚀 Features

### Core Features
- **📖 Interactive E-Book**: Beautiful Docusaurus-powered book interface with purple gradient theme
- **🤖 AI Chatbot**: Intelligent RAG-based chatbot powered by Google Gemini (FREE tier)
- **🔐 Authentication**: Complete signup/login system with JWT tokens
- **👤 User Profiling**: Capture user background (software/hardware experience, programming languages, industry, learning goals)
- **✨ Content Personalization**: AI adapts content based on user profile
- **🌐 Urdu Translation**: Translate content to Urdu with caching for performance
- **🎨 Modern UI**: Purple gradient design with smooth animations

### Tech Stack
**Frontend:**
- Docusaurus 3.9.2 (TypeScript)
- React with Context API
- Custom CSS with animations

**Backend:**
- FastAPI (Python)
- SQLAlchemy with SQLite
- Google Gemini 1.5 Flash API
- Qdrant Vector Database (RAG)
- JWT Authentication

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+
- **Google Gemini API Key** (FREE - get from https://aistudio.google.com/apikey)

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
\`\`\`bash
git clone https://github.com/Uzairrrrrr/hackathon-1.git
cd hackathon-1
\`\`\`

### 2️⃣ Get Gemini API Key (FREE)
1. Visit https://aistudio.google.com/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

### 3️⃣ Backend Setup
\`\`\`bash
cd chatbot-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment - Edit .env and add:
# GEMINI_API_KEY=your_key_here
# DATABASE_URL=sqlite:///./app.db

# Initialize database and index book content
python scripts/index_book_content.py

# Start backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

Backend will run on http://localhost:8000

### 4️⃣ Frontend Setup
\`\`\`bash
# In a new terminal
cd book

# Install dependencies
npm install

# Start development server
npm start
\`\`\`

Frontend will open at http://localhost:3000

## 🎯 Usage

### Sign Up & Login
1. Navigate to http://localhost:3000
2. Click **Sign Up** in navbar
3. Fill in your details and profile questions
4. Login with your credentials
5. Start reading and using the chatbot!

### Using the Chatbot
- Click the chat icon in bottom right
- Ask questions about the book content
- Get AI-powered answers from Gemini

### Personalized Content
- Content adapts based on your experience level
- Examples relevant to your programming languages
- Industry-specific use cases

### Translation
- Click translate button on any chapter
- Get instant Urdu translation
- Cached for fast repeated access

## 📁 Project Structure

\`\`\`
hackathon-1/
├── book/                          # Frontend (Docusaurus)
│   ├── docs/                      # Book content
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/             # Login/Signup forms
│   │   │   ├── ChatBot/          # AI chatbot widget
│   │   │   └── ChapterControls/  # Translation controls
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx   # Auth state management
│   │   └── css/
│   │       └── custom.css        # Purple gradient theme
│   ├── docusaurus.config.ts      # Docusaurus configuration
│   └── package.json
│
└── chatbot-backend/               # Backend (FastAPI)
    ├── app/
    │   ├── api/
    │   │   ├── auth.py           # Auth endpoints
    │   │   ├── chat.py           # Chatbot endpoints
    │   │   └── content.py        # Personalization/translation
    │   ├── models/
    │   │   ├── auth.py           # User models
    │   │   └── database.py       # Database setup
    │   ├── services/
    │   │   ├── rag_agent.py      # Gemini RAG chatbot
    │   │   ├── auth.py           # JWT authentication
    │   │   ├── personalization.py
    │   │   └── translation.py
    │   ├── config.py
    │   └── main.py
    ├── scripts/
    │   └── index_book_content.py # Initialize vector DB
    ├── requirements.txt
    └── .env
\`\`\`

## 🔑 Environment Variables

### Backend (.env)
\`\`\`env
# AI Configuration (FREE - Get from https://aistudio.google.com/apikey)
GEMINI_API_KEY=your_gemini_api_key_here
AI_PROVIDER=gemini
GEMINI_MODEL=gemini-1.5-flash

# Database (SQLite for local development)
DATABASE_URL=sqlite:///./app.db

# JWT Authentication
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Qdrant Vector Database (Optional - has defaults)
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
QDRANT_COLLECTION_NAME=book_content
\`\`\`

## 🎨 UI Theme

The platform features a beautiful purple gradient theme:
- Primary: \`#667eea\` → \`#764ba2\`
- Smooth animations and transitions
- Custom scrollbar with gradient
- Responsive design
- Modern card-based layout

## 🏆 Hackathon Bonus Points

This project implements several bonus features:
- ✅ **Authentication System** (Signup/Login with JWT)
- ✅ **User Profiling** (Background questions for personalization)
- ✅ **Content Personalization** (Adapts to user experience level)
- ✅ **Translation Support** (Urdu translation with caching)
- ✅ **Modern UI/UX** (Purple gradient theme, animations)
- ✅ **FREE AI Integration** (Google Gemini instead of paid OpenAI)

## 🧪 Testing

### Test Backend
\`\`\`bash
cd chatbot-backend
source venv/bin/activate

# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "What is this book about?"}'
\`\`\`

### Test Frontend
- Navigate to http://localhost:3000
- Check navbar buttons (Login/Signup/GitHub)
- Test signup flow
- Test login flow
- Test chatbot
- Test translation

## 🚀 Deployment

### GitHub Pages (Frontend)
\`\`\`bash
cd book
npm run build
npm run deploy
\`\`\`

### Backend Deployment
Deploy to platforms like:
- Railway.app
- Render.com
- Heroku
- DigitalOcean

Update environment variables and DATABASE_URL for production.

## 📝 API Documentation

Once backend is running, visit:
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Backend won't start
- Check Python virtual environment is activated
- Verify all dependencies installed: \`pip list\`
- Check .env file has valid Gemini API key
- Ensure port 8000 is not in use

### Frontend won't start
- Clear npm cache: \`npm cache clean --force\`
- Delete node_modules and reinstall: \`rm -rf node_modules && npm install\`
- Check Node.js version: \`node --version\` (should be 18+)

### Chatbot not working
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Verify Gemini API key is valid
- Check backend logs for errors

### Database errors
- Delete app.db and rerun: \`python scripts/index_book_content.py\`
- Verify DATABASE_URL in .env is correct
- Check SQLite is installed

## 📄 License

This project is built for hackathon purposes.

## 🙏 Acknowledgments

- **Docusaurus** - Beautiful documentation framework
- **FastAPI** - Modern Python web framework
- **Google Gemini** - FREE AI API with generous limits
- **Qdrant** - Vector database for RAG
- **Spec-Kit Plus** - Project scaffolding

---

Built with ❤️ using Docusaurus, FastAPI, and Google Gemini
