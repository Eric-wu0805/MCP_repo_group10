from duckduckgo_search import DDGS
import time

def web_search_data(query: str, max_results: int = 5) -> str:
    """搜尋網頁資訊"""
    # 增加重試機制與稍微的延遲，增加穩定性
    for attempt in range(2):
        try:
            with DDGS() as ddgs:
                # 移除 region 參數以確保回傳結果穩定，直接搜尋 query
                results = list(ddgs.text(query, max_results=max_results))
                
                if not results:
                    if attempt == 0:
                        time.sleep(1) # 第一次失敗就等一下再重試
                        continue
                    return f"搜尋 '{query}' 時未找到相關結果（目前可能連線受限或無對應資訊）。"
                
                output = [f"關於 '{query}' 的搜尋結果："]
                for i, r in enumerate(results, 1):
                    title = r.get('title', '無標題')
                    body = r.get('body', '無內容摘要')
                    href = r.get('href', '#')
                    output.append(f"{i}. {title}\n   {body}\n   連結: {href}")
                
                return "\n\n".join(output)
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
                continue
            return f"搜尋服務暫時無法使用：{str(e)}"

if __name__ == "__main__":
    # 測試程式碼
    # print(web_search_data("台北 美食"))
    pass
