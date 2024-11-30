from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get API key from environment variables
API_KEY = os.getenv("API_KEY")

# Function to map weather description to emoji
def get_weather_emoji(description):
    description = description.lower()
    if "rain" in description or "drizzle" in description:
        return "🌧️"
    elif "clear" in description:
        return "☀️"
    elif "cloud" in description or "overcast" in description:
        return "☁️"
    elif "snow" in description:
        return "❄️"
    elif "storm" in description or "thunder" in description:
        return "🌩️"
    elif "fog" in description or "mist" in description or "haze" in description:
        return "🌫️"
    elif "wind" in description:
        return "💨"
    else:
        return "🌈"  # Default emoji for unclassified weather

# Function to provide weather-specific advice
def get_weather_advice(temp, condition):
    advice = ""
    if temp <= 0:
        advice = "It's freezing! Wear a heavy jacket, gloves, and a hat."
    elif 0 < temp <= 10:
        advice = "It's cold. A warm jacket and a scarf would be helpful."
    elif 10 < temp <= 20:
        advice = "The weather is cool. Consider wearing a light jacket."
    elif 20 < temp <= 30:
        advice = "The weather is mild. A T-shirt and comfortable clothes will do."
    elif temp > 30:
        advice = "It's hot! Stay hydrated and wear light clothing."
    if "rain" in condition.lower():
        advice += " It's raining. Don't forget an umbrella or a raincoat."
    if "snow" in condition.lower():
        advice += " Snowfall expected. Drive carefully and dress warmly."
    return advice or "Enjoy the weather!"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city = request.form['city'].strip()
        
        if city:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                data = response.json()

                if data['cod'] == 200:
                    advice = get_weather_advice(data['main']['temp'], data['weather'][0]['description'])
                    emoji = get_weather_emoji(data['weather'][0]['description'])
                    weather_data = {
                        'city': data['name'],
                        'country': data['sys']['country'],
                        'temperature': round(data['main']['temp'], 2),  # Rounded for better readability
                        'description': data['weather'][0]['description'].capitalize(),
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'emoji': emoji,  # Include the emoji here
                        'advice': advice
                    }
                else:
                    error_message = data.get('message', "City not found. Please enter a valid city name.")
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"

    return render_template("index.html", weather_data=weather_data, error_message=error_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

