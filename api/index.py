from flask import Flask, request, jsonify
import os
from google import genai

app = Flask(__name__)

@app.route("/api/scan", methods=["POST"])
def scan():
    try:
        # Check if the key exists in Vercel's memory
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return jsonify({"error": "Missing API Key in Vercel Settings"}), 500
            
        client = genai.Client(api_key=api_key)
        
        if 'document' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['document']
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=["Identify this document. If it is a bill, give the amount and due date.", file]
        )
        
        return jsonify({"result": response.text})
    except Exception as e:
        # This will tell us the EXACT error on the screen
        return jsonify({"error": str(e)}), 500
