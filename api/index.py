from flask import Flask, request, jsonify
import os
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route("/api/scan", methods=["POST"])
def scan():
    try:
        # 1. Get your secret key from Vercel
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        # 2. Grab the photo from your phone
        if 'document' not in request.files:
            return jsonify({"error": "No photo detected"}), 400
            
        file = request.files['document']
        
        # 3. Send to Gemini (using the latest 2026 model)
        response = client.models.generate_content(
            model="gemini-2.0-flash-latest", 
            contents=[
                types.Part.from_bytes(
                    data=file.read(),
                    mime_type=file.content_type
                ),
                "Identify this document. If it is a bill, give the amount and due date. If it is an ID, summarize the info."
            ]
        )
        
        # 4. Send the answer back to your phone screen
        return jsonify({"result": response.text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
