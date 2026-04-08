import random

def get_activity_data(city: str = None) -> str:
    """推薦旅遊活動"""
    activities = [
        "參觀當地的歷史博物館，了解當地的文化底蘊",
        "在市中心的老街或創意市集散步，尋找在地特色",
        "品嚐著名的在地美食或特色小吃",
        "到知名的城市公園或森林步道健行，放鬆身心",
        "參加當地的文化體驗課程（如手作、烹飪）",
        "尋找當地的景觀咖啡廳，享受悠閒的午後時光",
        "逛逛當地的傳統市場，體驗最道地的生活氣息",
        "如果是晚上的話，可以前往觀景台欣賞璀璨夜景",
        "參觀當地的指標性建築或古蹟景點",
        "到當地的特色書店或藝廊進行一場文藝之旅"
    ]
    
    # 隨機選取 2-3 個活動
    selected = random.sample(activities, k=random.randint(2, 3))
    activities_list = "\n- ".join(selected)
    
    prefix = f"在 {city} 的推薦活動：" if city else "推薦的旅遊活動："
    return f"{prefix}\n- {activities_list}"

if __name__ == "__main__":
    # 測試程式碼
    print(get_activity_data("台北"))
