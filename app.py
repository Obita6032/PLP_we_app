from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# OpenWeatherMap API key (replace with your own key)
API_KEY = 'your_openweathermap_api_key'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
            response = requests.get(complete_url)
            data = response.json()

            if data["cod"] == 200:
                # Extracting the data from the response
                weather_data = {
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"]
                }
            else:
                error_message = "City not found! Please try again."

    return render_template("index.html", weather_data=weather_data, error_message=error_message)


@app.route("/location/<lat>/<lon>")
def location(lat, lon):
    weather_data = None
    error_message = None

    complete_url = f"{BASE_URL}lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:
        weather_data = {
            "city": f"Latitude: {lat}, Longitude: {lon}",
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"]
        }
    else:
        error_message = "Unable to get weather for the given location."

    return render_template("index.html", weather_data=weather_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
