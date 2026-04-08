import random
from tools.search import web_search_data

def get_food_data(city: str = None) -> str:
    """推薦在地美食"""
    if not city:
        common_foods = [
            "珍珠奶茶 - 台灣最具代表性的飲品",
            "牛肉麵 - 濃郁湯頭與軟嫩牛肉的完美結合",
            "滷肉飯 - 簡單卻不簡單的在地靈魂美味",
            "小籠包 - 皮薄多汁、口感細緻的國民美食",
            "蚵仔煎 - 風味獨特的傳統夜市小吃"
        ]
        selected = random.sample(common_foods, k=3)
        return "在此推薦您幾項經典美食：\n- " + "\n- ".join(selected)
    
    # 如果有指定城市，我們嘗試使用 web_search 來尋找更精確的在地美食
    try:
        search_query = f"{city} 必吃美食 推薦"
        search_results = web_search_data(search_query, max_results=3)
        return f"【{city} 在地美食推薦】\n{search_results}"
    except Exception as e:
        return f"暫時無法取得 {city} 的美食資訊：{str(e)}"

if __name__ == "__main__":
    # 測試程式碼
    # print(get_food_data("台中"))
    pass
