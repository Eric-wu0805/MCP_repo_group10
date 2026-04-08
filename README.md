# MCP Server + AI agent 分組實作

> 課程：AI Agent 開發 — MCP（Model Context Protocol）
> 主題：旅遊顧問 MCP Server

---



## Server 功能總覽

| Tool 名稱      | 功能說明               | 負責組員 |
| -------------- | ---------------------- | -------- |
| `get_weather`  | 查詢世界各地的即時天氣 | 吳宸宇   |
| `get_fun_fact` | 取得隨機趣味冷知識     | 林富閎   |
| `get_advice`   | 取得旅行前的人生建議   | 張承新   |


---

## 組員與分工

| 姓名   | 負責功能                 | 檔案                  | 使用的 API |
| ------ | ------------------------ | --------------------- | ------------------- |
| 吳宸宇 | 天氣工具 (Tool)          | `tools/weather.py`  | `https://wttr.in/{city}?format=j1` |
| 林富閎 | 冷知識工具 (Tool)        | `tools/fun_fact.py` | `https://uselessfacts.jsph.pl/api/v2/facts/random` |
| 林富閎 | 推薦活動 (Tool)        | `tools/actuvuty.py` | `https://bored-api.appbrewery.com/random` |
| 林富閎 | 搜尋景點、美食 (Tool)        | `tools/search.py` 、`tools/food.py` | `duckduckgo-search` |
| 張承新 | 建議工具 (Tool)          | `tools/advice.py`   | `https://api.adviceslip.com/advice` |
| 全組   | 共同維護 Resource + Prompt | `server.py`         | —                  |
| 全組   | 共同維護 Agent（用 AI 產生） | `agent.py`          | Gemini API          |


---

## 專案架構
```
├── server.py              # MCP Server 主程式（包含 Resource 與 Prompt）
├── agent.py               # MCP Client + Gemini Agent（用 AI 產生並擴充進階指令）
├── tools/                 # 各組員負責開發的 Tools 目錄
│   ├── weather.py         # 天氣查詢工具（吳宸宇負責）
│   ├── fun_fact.py        # 冷知識獲取工具（林富閎負責）
│   └── advice.py          # 人生建議工具（張承新負責）
├── requirements.txt       # 專案依賴套件表
├── .env                   # 實際讀取金鑰的環境變數檔（不該推上 GitHub）
├── .env.example           # 環境變數範例檔
├── .gitignore             # Git 忽略檔案設定
└── README.md              # 專案說明文件
```

---

## 使用方式

```bash
# 1. 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定 API Key
cp .env.example .env
# 編輯 .env，填入你的 GEMINI_API_KEY

# 4. 用 MCP Inspector 測試 Server
mcp dev server.py

# 5. 用 Agent 對話
python agent.py
```

---

## 測試結果

### MCP Inspector 截圖

> 貼上 Inspector 的截圖（Tools / Resources / Prompts 三個分頁都要有）

### Agent 對話截圖

> 貼上 Agent 對話的截圖（顯示 Gemini 呼叫 Tool 的過程，以及使用 /use 呼叫 Prompt 的結果）

---<img width="942" height="858" alt="image" src="https://github.com/user-attachments/assets/4cafbde2-7aef-4a51-ad3e-cf9f30ea23e1" />


## 各 Tool 說明

### `get_weather`（負責：吳宸宇）
- **功能**：查詢世界各地指定城市的即時天氣觀測結果與氣溫。
- **使用 API**：`https://wttr.in/{city}?format=j1`
- **參數**：`city` (字串 str) — 欲查詢的城市英文名稱（例如："Taipei", "Tokyo"）
- **回傳範例**：`"Taipei 目前天氣：Partly cloudy，氣溫 25°C"` 或 `"無法取得 Taipei 的天氣資訊: [錯誤原因]"`
```python
@mcp.tool()
def get_weather(city: str) -> str:
    """查詢目的地天氣"""
    return get_weather_data(city)
```

### `get_fun_fact`（負責：林富閎）
- **功能**：隨機取得一個冷知識或趣味小百科。
- **使用 API**：`https://uselessfacts.jsph.pl/api/v2/facts/random`
- **參數**：無
- **回傳範例**：`"趣味冷知識：The shortest commercial flight is in Scotland..."`

```python
@mcp.tool()
def get_fun_fact() -> str:
    """旅途趣味冷知識"""
    return get_fun_fact_data()
```

### `get_advice`（負責：張承新）
- **功能**：取得隨機的勵志語錄或人生建議。
- **使用 API**：`https://api.adviceslip.com/advice`
- **參數**：無
- **回傳範例**：`"人生建議：Don't be afraid to ask questions."`

```python
@mcp.tool()
def get_advice() -> str:
    """旅行前的人生建議"""
    return get_advice_data()
```



## 心得

### 遇到最難的問題

最困難的地方在於實作 `agent.py` 時，遇到了「非同步事件迴圈阻塞」與 TaskGroup 崩潰的問題，以及處理 MCP Inspector 連線方式的衝突。當時因為使用了同步的 `input()` 或一般版的 Gemini `chat.send_message()`，導致卡死了非同步的 MCP SSE 連線，頻繁發生 `ExceptionGroup` 報錯。
**解決方式**：我們將讀取輸入的指令改為 `await asyncio.to_thread(input)`，並且升級使用非同步版本的 `client.aio.chats.create` 來避免主執行緒卡死，再加上實作解析 ExceptionGroup 錯誤樹的機制，成功抓出深層的 API Key 容量上限等 API 問題。另外在 Inspector 方面，也學會了正確將網頁端的 Transport 設定切換成 SSE 並搭配 Localhost 埠號，順利排除了開發上的阻礙。

### MCP 跟上週的 Tool Calling 有什麼不同？

上週學的傳統 Tool Calling 是將「工具邏輯」與「AI Agent」的程式碼高度綁定（Coupled），這代表我們若換一個大語言模型，可能就需要重新調整一遍工具的參數與呼叫細節。
而 **MCP (Model Context Protocol) 最大的好處在於「解耦（Decoupling）」與「標準化」**：
這週我們是開發一個功能獨立的「伺服器（Server）」，將工具、資源、和 Prompt 全部封裝。任何支援 MCP 協定的客戶端（包含我們寫的 Agent、官方 Inspector、甚至是 Claude Desktop 等）都能直接連線並無縫取用我們的天氣與冷知識工具。這種 Client-Server 架構大幅提升了工具的共用性、跨平台能力與擴充性！
