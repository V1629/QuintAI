# QuintAI Website

A beautiful, modern, and futuristic website showcasing the QuintAI multi-agent AI question-answering system with **LIVE DEMO** functionality!

## 🎨 Design Features

- **Dark Blue Futuristic Theme**: Modern gradient backgrounds with glowing blue accents
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Interactive Elements**: Hover effects, smooth animations, and parallax scrolling
- **Professional Layout**: Clean sections highlighting all project features and capabilities
- **🚀 LIVE DEMO**: Interactive demonstration of the QuintAI system in action!

## 🚀 Quick Start

### Option 1: Using Python Server (Recommended)
```bash
python serve.py
```
This will:
- Start a local web server on port 8000
- Automatically open your default browser
- Display the website at `http://localhost:8000`

### Option 2: Using Built-in Python Server
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

### Option 3: Direct File Opening
Simply double-click `index.html` to open it directly in your browser.

## 🌟 Website Sections

### 1. **Hero Section**
- Eye-catching title with glowing animation
- Project description and call-to-action button
- Animated grid background

### 2. **Core Features**
- Multi-Agent Architecture
- Intelligent Judging System
- Retrieval-Augmented Generation
- Advanced Tool Integration
- Extensible Framework
- Security & Reliability

### 3. **Technology Stack**
- Python 3.12+
- LangChain & LangGraph
- ChromaDB Vector Database
- Multiple LLM Providers (Ollama, Groq, Gemini)
- Wikipedia API Integration

### 4. **System Architecture**
- Visual workflow diagram
- Agent specializations
- System flow explanation

### 5. **🚀 LIVE DEMO - Experience QuintAI**
- **Interactive Question Input**: Type any question and watch the magic happen
- **Real-time Workflow Animation**: See all 5 AI agents process your question simultaneously
- **Live Agent Responses**: Get real responses from each specialized agent
- **Judge LLM Analysis**: Watch the intelligent judge select the best answer
- **Real QuintAI Integration**: Connect to the actual Python backend for authentic responses

### 6. **Setup Guide**
- Step-by-step installation instructions
- Code examples for each step
- Environment configuration

## 🎯 Key Features

- **Smooth Scrolling Navigation**: Click any nav item to smoothly scroll to that section
- **Scroll Progress Indicator**: Blue bar at the top showing scroll progress
- **Fade-in Animations**: Elements appear as you scroll down
- **Interactive Cards**: Hover effects on feature and tech stack cards
- **Responsive Grid Layouts**: Automatically adjusts to different screen sizes
- **Modern Typography**: Clean, readable fonts with proper contrast
- **🚀 LIVE AI DEMO**: Real-time interaction with the QuintAI system!

## 🚀 Live Demo Functionality

### **How the Demo Works:**

1. **Input Your Question**: Type any question in the demo input field
2. **Watch the Workflow**: See a beautiful animation showing all 5 AI agents processing your question
3. **Real Agent Responses**: Get actual responses from:
   - **Agent 1**: PDF Expert (Ollama + ChromaDB)
   - **Agent 2**: Groq Specialist (High-speed LLM)
   - **Agent 3**: Wikipedia Tool (Ollama + Wikipedia API)
   - **Agent 4**: Gemini AI (Google's advanced AI)
4. **Judge LLM Analysis**: Watch the intelligent judge evaluate all responses and select the best answer
5. **Complete Results**: See the final decision with justification

### **Two Modes:**

- **🎯 Real Mode**: Connect to the QuintAI API server for authentic responses
- **🎭 Demo Mode**: Fallback to simulated responses if API is unavailable

## 🔧 Backend API Server

For the live demo to work with real responses, you need to run the API server:

### **Start the API Server:**
```bash
python api_server.py
```

This will:
- Start a Flask server on port 5000
- Import and run the actual QuintAI system
- Provide real-time responses to the website
- Handle all agent processing and judging

### **API Endpoints:**
- `POST /ask` - Submit a question and get responses from all agents
- `GET /health` - Check server health
- `GET /test-agents` - Test individual agent functionality

## 🛠️ Technical Details

- **Pure HTML/CSS/JavaScript**: No external dependencies except Font Awesome icons
- **CSS Variables**: Easy color scheme customization
- **CSS Grid & Flexbox**: Modern layout techniques
- **Intersection Observer API**: Efficient scroll-based animations
- **CSS Transitions**: Smooth hover and interaction effects
- **Fetch API**: Real-time communication with Python backend
- **Error Handling**: Graceful fallback to simulated responses

## 🎨 Customization

The website uses CSS custom properties (variables) for easy theming:

```css
:root {
    --primary-blue: #0a192f;      /* Main background */
    --secondary-blue: #112240;    /* Secondary background */
    --accent-blue: #64ffda;       /* Accent color */
    --text-primary: #ccd6f6;      /* Primary text */
    --text-secondary: #8892b0;    /* Secondary text */
}
```

## 📱 Browser Compatibility

- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🚀 Deployment

To deploy this website:

1. **GitHub Pages**: Push to a GitHub repository and enable GitHub Pages
2. **Netlify**: Drag and drop the `index.html` file
3. **Vercel**: Connect your repository for automatic deployment
4. **Traditional Hosting**: Upload files to any web server

**Note**: For the live demo to work in production, you'll need to:
- Deploy the `api_server.py` to a cloud service (Heroku, AWS, etc.)
- Update the API endpoint URL in the JavaScript code
- Ensure all dependencies and API keys are configured

## 🔧 Troubleshooting

### Website not loading?
- Make sure you're running the server from the correct directory
- Check if port 8000 is available
- Try a different port by editing `serve.py`

### Live demo not working?
- Ensure the API server is running (`python api_server.py`)
- Check if port 5000 is available
- Verify all QuintAI dependencies are installed
- Check browser console for error messages

### Styling issues?
- Ensure all CSS is loaded properly
- Check browser console for errors
- Verify Font Awesome CDN is accessible

### Mobile responsiveness?
- Test on different devices
- Check viewport meta tag is present
- Verify CSS media queries are working

## 📋 Prerequisites for Live Demo

To run the live demo with real responses:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API Keys** in `.env` file:
   ```
   groq_api_key=YOUR_GROQ_API_KEY
   groq1_api_key=YOUR_GROQ_API_KEY_FOR_JUDGE
   gemini_api_key=YOUR_GEMINI_API_KEY
   ```

3. **Download Ollama Models:**
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

4. **Ensure PDF File**: Make sure `A Psycho-Cybernetics__-_Maxwell_Maltz.pdf` is in the project directory

5. **Start API Server:**
   ```bash
   python api_server.py
   ```

6. **Start Website:**
   ```bash
   python serve.py
   ```

## 📞 Support

If you encounter any issues:
1. Check the browser console for error messages
2. Verify all files are in the same directory
3. Ensure Python 3.6+ is installed for the server script
4. Check that the API server is running for live demo functionality
5. Verify all API keys and dependencies are properly configured

## 🎉 What You'll Experience

With the enhanced QuintAI website, you can:

- **🎨 View**: A beautiful, professional presentation of your AI project
- **🚀 Interact**: Use the live demo to ask real questions
- **🤖 Experience**: Watch 5 AI agents work together in real-time
- **⚖️ Judge**: See the intelligent judging system in action
- **📱 Share**: Showcase your project to others with an impressive interface

---

**Experience the future of AI with QuintAI's interactive website! 🚀🤖✨** 