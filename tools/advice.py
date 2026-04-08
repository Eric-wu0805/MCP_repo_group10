import requests

def get_advice_data() -> str:
    """旅行前的人生建議"""
    try:
        url = "https://api.adviceslip.com/advice"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        advice = data.get("slip", {}).get("advice", "保持好心情！")
        return f"人生建議：{advice}"
    except Exception as e:
        return f"無法取得建議: {str(e)}"
