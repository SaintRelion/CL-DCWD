import requests


def get_historical_weather(lat, lon, date_str):
    # date_str format: "YYYY-MM-DD"
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date_str}&end_date={date_str}&daily=rain_sum,temperature_2m_max&timezone=Asia%2FSingapore"
    response = requests.get(url).json()

    if "daily" in response:
        return {
            "rain": response["daily"]["rain_sum"][0],  # in mm
            "temp": response["daily"]["temperature_2m_max"][0],
        }
    return {"rain": 0, "temp": 25}
