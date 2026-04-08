import requests

def get_fun_fact_data() -> str:
    """旅途趣味冷知識"""
    try:
        url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        fact = data.get("text", "沒有冷知識可提供")
        return f"趣味冷知識：{fact}"
    except Exception as e:
        return f"無法取得冷知識: {str(e)}"
