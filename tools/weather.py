import requests

def get_weather_data(city: str) -> str:
    """查詢目的地天氣"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data['current_condition'][0]
        temp = current['temp_C']
        desc = current['weatherDesc'][0]['value']
        return f"{city} 目前天氣：{desc}，氣溫 {temp}°C"
    except Exception as e:
        return f"無法取得 {city} 的天氣資訊: {str(e)}"
