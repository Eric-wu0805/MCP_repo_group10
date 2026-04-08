import asyncio
import os
import traceback
from dotenv import load_dotenv
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from google import genai
from google.genai import types

# 載入環境變數
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("找不到 GEMINI_API_KEY，請確認 .env 檔案設定。")

client = genai.Client(api_key=API_KEY)

async def main():
    print("正在連接到 MCP Server (http://localhost:8000/sse)...")
    try:
        async with sse_client("http://localhost:8000/sse") as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("連線成功！")
                
                # 取得工具清單
                tools_response = await session.list_tools()
                tools = tools_response.tools
                
                # 轉換工具給 Gemini
                gemini_tools = []
                for t in tools:
                    properties = {}
                    required = []
                    schema = t.inputSchema
                    if schema and "properties" in schema:
                        for prop_name, prop_details in schema["properties"].items():
                            properties[prop_name] = {
                                "type": prop_details.get("type", "STRING").upper(),
                                "description": prop_details.get("description", "")
                            }
                        if "required" in schema:
                            required = schema["required"]
                    
                    gemini_tools.append({
                        "name": t.name,
                        "description": t.description,
                        "parameters": {
                            "type": "OBJECT",
                            "properties": properties,
                            "required": required
                        }
                    })
                    
                print(f"從 Server 取得 {len(gemini_tools)} 個工具")

                # 改用 aio 非同步客戶端，避免阻塞事件迴圈
                chat = client.aio.chats.create(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(
                        tools=[{"function_declarations": gemini_tools}] if gemini_tools else None,
                        temperature=0.7,
                    )
                )

                print("開始對話 (輸入 'exit' 結束) :")
                print("您可以輸入 /prompts 查詢可用提示詞，或輸入 /use <名稱> [參數] 使用提示詞")
                
                while True:
                    user_msg = await asyncio.to_thread(input, "你: ")
                    if user_msg.strip() == '':
                        continue
                    if user_msg.lower() == 'exit':
                        break
                    
                    # 處理擴充指令
                    if user_msg.startswith("/prompts"):
                        prompts_resp = await session.list_prompts()
                        print("\n[可用 Prompts]")
                        for p in prompts_resp.prompts:
                            print(f"- {p.name}: {p.description}")
                        continue
                        
                    if user_msg.startswith("/use "):
                        parts = user_msg.split()
                        if len(parts) >= 2:
                            prompt_name = parts[1]
                            prompt_args = {"city": parts[2]} if len(parts) > 2 else {}
                            try:
                                print(f"[Debug] 取得 Prompt: {prompt_name}")
                                prompt_result = await session.get_prompt(name=prompt_name, arguments=prompt_args)
                                user_msg = prompt_result.messages[0].content.text
                                print(f"[系統為您送出]: {user_msg}")
                            except Exception as e:
                                print(f"取得 prompt 失敗: {e}")
                                continue
                        else:
                            print("用法: /use <名稱> [參數]")
                            continue

                    print("Gemini 思考中...")
                    response = await chat.send_message(user_msg)
                    
                    # 處理 Function Calls
                    while response.function_calls:
                        for function_call in response.function_calls:
                            tool_name = function_call.name
                            args = dict(function_call.args) if function_call.args else {}
                            print(f"[Debug] 呼叫工具：{tool_name}")
                            print(f"[Debug] 參數：{args}")
                            
                            tool_result = await session.call_tool(tool_name, arguments=args)
                            result_text = tool_result.content[0].text if tool_result.content else str(tool_result)
                            print(f"[Debug] 工具結果：{result_text}")
                            
                            print("Gemini 根據結果思考中...")
                            try:
                                response = await chat.send_message(
                                    types.Part.from_function_response(
                                        name=tool_name,
                                        response={"result": result_text}
                                    )
                                )
                            except Exception as e:
                                print(f"[Debug] 傳送工具結果時發生錯誤：{e}")
                                break
                    
                    if response.text:
                        print(f"Gemini: {response.text}")

    except Exception as e:
        print("連線或執行時發生錯誤 (詳細內容如下):")
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e) or "TaskGroup" in str(e):
            print("\n❌ 錯誤提示：如果您看到一堆錯誤，這通常是因為 .env 內的 GEMINI_API_KEY 是無效的金鑰或額度已用盡！請務必到 Google AI Studio 申請您自己的金鑰並貼到 .env 中。")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
