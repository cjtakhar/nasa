from flask import Flask, render_template, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def fetch_nasa_iod(api_key):
    # Define the URL for NASA API
    api_url = "https://api.nasa.gov/planetary/apod"
   
    # Set up the parameters for the API request
    params = {
        "api_key": api_key
    }

    # Make the API request
    response = requests.get(api_url, params=params)

    # Check if response was successful 
    if response.status_code == 200:
        #Pase the JSON response
        data = response.json()

        #Extract relevant information
        image_url = data.get("url")
        title = data.get("title")
        explanation = data.get("explanation")

        # Return the information
        return {
            "title": title,
            "image_url": image_url,
            "explanation": explanation
        }
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")

@app.route('/')
def index():
    api_key = os.getenv("NASA_API_KEY")
    try:
        data = fetch_nasa_iod(api_key)
        return render_template('index.html', data=data)
    except Exception as e:
        return str(e)

app.route('/api/iod')
def iod():
    api_key = os.getenv("NASA_API_KEY")
    try:
        data = fetch_nasa_iod(api_key)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)