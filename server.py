"""
W8 分組實作：MCP Server
主題：主題 A：旅遊顧問 MCP Server

分工說明：
- 整合了天氣、常識、建議的工具
- 加入了旅行提示的 resource
- 加入了旅行計畫的 prompt
"""

from mcp.server.fastmcp import FastMCP
from tools.weather import get_weather_data
from tools.fun_fact import get_fun_fact_data
from tools.advice import get_advice_data

mcp = FastMCP("旅遊顧問 Server")

# ════════════════════════════════
#  Tools
# ════════════════════════════════

@mcp.tool()
def get_weather(city: str) -> str:
    """查詢目的地天氣"""
    return get_weather_data(city)

@mcp.tool()
def get_fun_fact() -> str:
    """旅途趣味冷知識"""
    return get_fun_fact_data()

@mcp.tool()
def get_advice() -> str:
    """旅行前的人生建議"""
    return get_advice_data()

# ════════════════════════════════
#  Resource
# ════════════════════════════════

@mcp.resource("info://travel-tips")
def get_travel_tips() -> str:
    """旅行必帶物品與注意事項清單"""
    return (
        "旅行必帶物品：\n"
        "- 護照 / 身分證\n"
        "- 當地貨幣或信用卡\n"
        "- 備用藥品\n"
        "- 充電器與轉接頭\n\n"
        "出發前注意：\n"
        "- 確認當地天氣，準備適當衣物\n"
        "- 查詢當地緊急電話\n"
        "- 備份重要文件"
    )

# ════════════════════════════════
#  Prompt
# ════════════════════════════════

@mcp.prompt()
def plan_trip(city: str) -> str:
    """產生旅遊行前簡報的提示詞"""
    return (
        f"我要去 {city} 旅行，請幫我準備一份完整的行前簡報：\n"
        f"1. 查詢 {city} 的天氣，判斷需要帶什麼衣物\n"
        f"2. 給我一則旅遊相關的冷知識或趣味資訊\n"
        f"3. 給我一則旅行前的人生建議\n"
        f"4. 推薦 2-3 個在 {city} 可以做的活動\n"
        f"請用繁體中文，語氣活潑。"
    )

if __name__ == "__main__":
    print("MCP Server 啟動中... http://localhost:8000")
    mcp.run(transport="sse")
