from flask import Flask, request, jsonify
import os
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route("/api/scan", methods=["POST"])
def scan():
    try:
        # 1. Grab the API Key from your Vercel Settings
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return jsonify({"error": "Missing GEMINI_API_KEY in Vercel"}), 500
            
        client = genai.Client(api_key=api_key)
        
        # 2. Grab the photo sent from your phone
        if 'document' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
            
        file = request.files['document']
        
        # 3. Send the photo to Gemini 1.5 Flash
        # We use 1.5-flash because it is the most compatible with 'v1beta'
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=[
                types.Part.from_bytes(
                    data=file.read(),
                    mime_type=file.content_type
                ),
                "Identify this document. If it is a bill, give the amount and due date. If it is an ID, summarize the info."
            ]
        )
        
        # 4. Return the AI's answer to your website
        return jsonify({"result": response.text})
        
    except Exception as e:
        # If anything goes wrong, this tells us exactly what
        return jsonify({"error": str(e)}), 500
