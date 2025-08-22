#!/usr/bin/env python3
"""
Production Flask API server for QuintAI
Optimized for Render deployment
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Add current directory to Python path to import QuintAI modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Configure CORS for production
CORS(app, origins=[
    "https://quintai-website.onrender.com",
    "https://quintai-api.onrender.com",
    "http://localhost:8000",
    "http://localhost:3000"
])

# Import QuintAI modules
try:
    from agent1 import responses1
    from agent2 import responses2
    from agent3 import responses3
    from agent4 import responses4
    from judgellm import responses5
    logger.info("✅ All QuintAI modules imported successfully")
except ImportError as e:
    logger.error(f"❌ Error importing QuintAI modules: {e}")
    logger.error("Make sure all required dependencies are installed and API keys are set")

@app.route('/')
def home():
    return jsonify({
        "message": "QuintAI API Server",
        "status": "running",
        "environment": "production",
        "endpoints": {
            "ask": "/ask",
            "health": "/health",
            "test": "/test-agents"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    try:
        # Test if we can import the modules
        from agent1 import responses1
        from agent2 import responses2
        from agent3 import responses3
        from agent4 import responses4
        from judgellm import responses5
        
        return jsonify({
            "status": "healthy",
            "message": "QuintAI API server is running",
            "modules_loaded": True
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": f"Error loading modules: {str(e)}",
            "modules_loaded": False
        }), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Main endpoint to ask a question and get responses from all agents"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Question is required"}), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400
        
        logger.info(f"🤖 Processing question: {question}")
        
        # Get responses from all agents
        responses = []
        agent_functions = [
            ("Agent 1: PDF Expert", responses1),
            ("Agent 2: Groq Specialist", responses2),
            ("Agent 3: Wikipedia Tool", responses3),
            ("Agent 4: Gemini AI", responses4)
        ]
        
        # Process each agent
        for agent_name, agent_func in agent_functions:
            try:
                logger.info(f"🔄 Processing with {agent_name}...")
                response = agent_func(question)
                
                # Clean up response if it's a LangChain object
                if hasattr(response, 'content'):
                    response = response.content
                elif hasattr(response, 'text'):
                    response = response.text
                elif hasattr(response, 'output'):
                    response = response.output
                
                responses.append({
                    "agent": agent_name,
                    "response": str(response),
                    "status": "success"
                })
                logger.info(f"✅ {agent_name} completed successfully")
                
            except Exception as e:
                error_msg = f"Error in {agent_name}: {str(e)}"
                logger.error(f"❌ {error_msg}")
                responses.append({
                    "agent": agent_name,
                    "response": error_msg,
                    "status": "error"
                })
        
        # Get judge's decision
        try:
            logger.info("⚖️ Getting judge's decision...")
            judge_response = responses5(question, [r["response"] for r in responses])
            
            # Clean up judge response
            if hasattr(judge_response, 'content'):
                judge_response = judge_response.content
            elif hasattr(judge_response, 'text'):
                judge_response = judge_response.text
            elif hasattr(judge_response, 'output'):
                judge_response = judge_response.output
                
            logger.info("✅ Judge decision completed")
            
        except Exception as e:
            error_msg = f"Error in Judge LLM: {str(e)}"
            logger.error(f"❌ {error_msg}")
            judge_response = error_msg
        
        # Prepare final response
        result = {
            "question": question,
            "agent_responses": responses,
            "judge_decision": str(judge_response),
            "status": "completed"
        }
        
        logger.info("🎉 Question processing completed successfully")
        return jsonify(result)
        
    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        logger.error(f"❌ {error_msg}")
        logger.error(traceback.format_exc())
        return jsonify({"error": error_msg}), 500

@app.route('/test-agents', methods=['GET'])
def test_agents():
    """Test endpoint to check if all agents are working"""
    test_question = "What is artificial intelligence?"
    results = {}
    
    try:
        # Test each agent individually
        agents = [
            ("Agent 1 (PDF)", responses1),
            ("Agent 2 (Groq)", responses2),
            ("Agent 3 (Wikipedia)", responses3),
            ("Agent 4 (Gemini)", responses4)
        ]
        
        for name, func in agents:
            try:
                response = func(test_question)
                if hasattr(response, 'content'):
                    response = response.content
                elif hasattr(response, 'text'):
                    response = response.text
                results[name] = {
                    "status": "success",
                    "response": str(response)[:200] + "..." if len(str(response)) > 200 else str(response)
                }
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return jsonify({
            "test_question": test_question,
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": f"Test failed: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Starting QuintAI Production API Server on port {port}")
    
    # Test if we can import the modules
    try:
        from agent1 import responses1
        from agent2 import responses2
        from agent3 import responses3
        from agent4 import responses4
        from judgellm import responses5
        logger.info("✅ All modules imported successfully!")
    except Exception as e:
        logger.error(f"❌ Import error: {e}")
        logger.warning("The server will start but may not function properly")
    
    app.run(host='0.0.0.0', port=port, debug=False) 