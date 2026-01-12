from flask import Flask, request, jsonify
import os
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route("/api/scan", methods=["POST"])
def scan():
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        file = request.files['document']
        
        # This tells the AI exactly what kind of file it's looking at
        response = client.models.generate_content(
            model="gemini-1.5-flash",
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
