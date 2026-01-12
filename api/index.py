from flask import Flask, request, jsonify
import os
from google import genai

app = Flask(__name__)

# This line asks Vercel for your Secret API Key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/api/scan", methods=["POST"])
def scan():
    # This receives the photo you upload
    file = request.files['document']
    
    # This sends it to Gemini to read
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=["Read this. What is the due date and amount?", file]
    )
    
    return jsonify({"result": response.text})
