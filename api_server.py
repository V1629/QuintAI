#!/usr/bin/env python3
"""
Flask API server for QuintAI website demo
This server runs the actual QuintAI system and provides real responses
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path to import QuintAI modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# FIX: agents are imported lazily inside request handlers, not at module level.
# Top-level imports were causing all agents to initialize (and fail) on startup
# before requests were even received.

@app.route('/')
def home():
    return jsonify({
        "message": "QuintAI API Server",
        "status": "running",
        "endpoints": {
            "ask": "/ask",
            "health": "/health",
            "test_agents": "/test-agents"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "QuintAI API server is running"
    })

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

        print(f"🤖 Processing question: {question}")

        # FIX: import agents here so initialization happens per-request context
        from agent1 import responses1
        from agent2 import responses2
        from agent3 import responses3
        from agent4 import responses4
        from judgellm import responses5

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
                print(f"🔄 Processing with {agent_name}...")
                response = agent_func(question)

                # Clean up response if it's still a LangChain/Gemini object
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
                print(f"✅ {agent_name} completed successfully")

            except Exception as e:
                error_msg = f"Error in {agent_name}: {str(e)}"
                print(f"❌ {error_msg}")
                responses.append({
                    "agent": agent_name,
                    "response": error_msg,
                    "status": "error"
                })

        # Get judge's decision
        try:
            print("⚖️ Getting judge's decision...")
            judge_response = responses5(question, [r["response"] for r in responses])

            # Clean up judge response
            if hasattr(judge_response, 'content'):
                judge_response = judge_response.content
            elif hasattr(judge_response, 'text'):
                judge_response = judge_response.text
            elif hasattr(judge_response, 'output'):
                judge_response = judge_response.output

            print("✅ Judge decision completed")

        except Exception as e:
            error_msg = f"Error in Judge LLM: {str(e)}"
            print(f"❌ {error_msg}")
            judge_response = error_msg

        # Prepare final response
        result = {
            "question": question,
            "agent_responses": responses,
            "judge_decision": str(judge_response),
            "status": "completed"
        }

        print("🎉 Question processing completed successfully")
        return jsonify(result)

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        return jsonify({"error": error_msg}), 500

@app.route('/test-agents', methods=['GET'])
def test_agents():
    """Test endpoint to check if all agents are working"""
    test_question = "What is artificial intelligence?"
    results = {}

    try:
        from agent1 import responses1
        from agent2 import responses2
        from agent3 import responses3
        from agent4 import responses4

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

if __name__ == '__main__':
    print("🚀 Starting QuintAI API Server...")
    print("📝 Make sure you have:")
    print("   - All required API keys in .env file")
    print("   - Ollama models downloaded (llama3.2, nomic-embed-text)")
    print("   - All dependencies installed")
    print("   - PDF file in the project directory")
    print()
    print(f"🌐 Server will be available at: http://localhost:5000")
    print(f"🔗 API endpoint: http://localhost:5000/ask")
    print(f"📊 Health check: http://localhost:5000/health")
    print(f"🧪 Test agents: http://localhost:5000/test-agents")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)