from flask import Flask, request, jsonify
import os
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route("/api/scan", methods=["POST"])
def scan():
    try:
        # We are being very specific about finding the key here
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return jsonify({"error": "The app can't find your GEMINI_API_KEY in Vercel settings."}), 500
            
        client = genai.Client(api_key=api_key)
        
        file = request.files['document']
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-latest", 
            contents=[
                types.Part.from_bytes(
                    data=file.read(),
                    mime_type=file.content_type
                ),
                "Identify this document. If it is a bill, give the amount and due date."
            ]
        )
        
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
