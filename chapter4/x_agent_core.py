# streamlitはめんどくさいのでターミナルで実行できるようにソースを変更した

from langchain_core.messages.ai import AIMessage
from botocore.config import Config
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_tavily import TavilySearch
from langchain_core.messages import (
    BaseMessage, 
    SystemMessage, 
    AIMessage, 
    ToolMessage, 
    ToolCall
)
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages
from rich import print

# .envから環境変数ファイルを読みだし
from dotenv import load_dotenv
load_dotenv(override=True)

# ツールの定義
# Web検索ツール
web_search = TavilySearch(max_results=2, topic="general")

working_directory = "report"
# ローカルファイルを扱うツールキット
file_toolkit = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=["write_file"], # ファイル書き込みツールを指定
)
write_file = file_toolkit.get_tools()[0]

# 使用するツールのリスト
tools = [web_search, write_file]
tools_by_name = {tool.name: tool for tool in tools}

# LLMの初期化
cfg = Config(
    read_timeout=300,
)
llm_with_tools = init_chat_model(
    # model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    model_provider="bedrock_converse",
    config=cfg,
).bind_tools(tools)

# システムプロンプト
system_prompt = """
あなたの責務はユーザからのリクエストを調査し、調査結果をファイル出力することです。
- ユーザーのリクエスト調査にWeb検索が必要であれば、Web検索ツールを使ってください。
- 必要な情報が集まったと判断したら検索は終了して下さい。
- 検索は最大2回までとしてください。
- ファイル出力はHTML形式(.html)に変換して保存してください。
  * Web検索が拒否された場合、Web検索を中止してレポート作成してください。
  * レポート保存を拒否された場合、レポート作成を中止し、内容をユーザーに直接伝えて下さい。
"""

# LLMを呼び出すタスク
@task
def invoke_llm(messages: list[BaseMessage]) -> AIMessage:
    response = llm_with_tools.invoke(
       [SystemMessage(content=system_prompt)] + messages
    )
    return response

# ツールを実行するタスク
@task
def use_tool(tool_call):
    tool = tools_by_name[tool_call["name"]]
    observation = tool.invoke(tool_call["args"])

    return ToolMessage(content=observation, tool_call_id=tool_call["id"])

# ユーザーにツール実行の承認を求める
def ask_human(tool_call: ToolCall):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    tool_data = {"name": tool_name}
    if tool_name == web_search.name:
        args =  f'* ツール名\n'
        args += f'  * {tool_name}\n'
        args += "* 引数\n"
        for key, value in tool_args.items():
            args += f'  * {key}\n'
            args += f'    * {value}\n'

        tool_data["args"] = args
    elif tool_name == write_file.name:
        args =  f'* ツール名\n'
        args += f'  * {tool_name}\n'
        args += f'* 保存ファイル名\n'
        args += f'  * {tool_args["file_path"]}'
        tool_data["html"] = tool_args["text"]
    tool_data["args"] = args

    feedback = interrupt(tool_data)

    if feedback == "y": # ユーザーがツール利用を承認したとき
        return tool_call
    
    # ユーザーがツール利用を承認しなかったとき
    return ToolMessage(
        content="ツール利用が拒否されたため、処理を終了してください。", 
        name=tool_name, 
        tool_call_id=tool_call["id"]
    )
    
# チェックポインターの設定
checkpointer = MemorySaver()
@entrypoint(checkpointer)
def agent(messages):
    # LLMを呼び出し
    llm_response = invoke_llm(messages).result()
    print("-------------x_agent_core.py 最初の呼び出し-----------------")
    print(llm_response)
    print("--------------------------------------------------------")


    # ツール呼び出しがある限り繰り返す
    while True:
        if not llm_response.tool_calls:
            break

        approve_tools = []
        tool_results = []
        
        print("---------------llm_response.tool_calls---------------")
        print(llm_response.tool_calls)
        print("--------------------------------------------------------")
        # 各ツール呼び出しに対してユーザーの承認を求める
        for tool_call in llm_response.tool_calls:
            feedback = ask_human(tool_call)
            if isinstance(feedback, ToolMessage):
                tool_results.append(feedback)
            else:
                approve_tools.append(feedback)
        print("---------------tool_results---------------")
        print(tool_results)
        print("--------------------------------------------------------")

        print("---------------approve_tools---------------")
        print(approve_tools)
        print("--------------------------------------------------------")

        # 承認されたツールを実行
        tool_futures = []
        for tool_call in approve_tools:
            future = use_tool(tool_call)   # 非同期実行を開始
            tool_futures.append(future)

        print("---------------tool_futures---------------")
        print(tool_futures)
        print("--------------------------------------------------------")

        # Future が完了するのを待って結果だけを集める
        tool_use_results = []
        for future in tool_futures:
            result = future.result()       # 完了まで待ち、結果を取得
            tool_use_results.append(result)

        print("---------------tool_use_results---------------")
        print(tool_use_results)
        print("--------------------------------------------------------")

        # メッセージリストに追加
        messages = add_messages(
            messages,
            [llm_response, *tool_use_results, *tool_results]
        )

        print("---------------messages---------------")
        print(messages)
        print("--------------------------------------------------------")

        # モデルを再度呼び出し
        llm_response = invoke_llm(messages).result()
    
    # 最終結果を返す
    return llm_response


if __name__ == "__main__":
    import asyncio
    import uuid
    from langchain_core.messages import HumanMessage
    from langgraph.types import Command

    async def test_agent():
        content = input("メッセージを入力してください: ")
        messages = [HumanMessage(content=content)]
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        print("エージェント実行中...")
        result = agent.invoke(messages, config=config)

        ## interrputが走るとresutlに中断されたという情報が一回出力される
        ## resultに入る内容↓
        # {
        #     '__interrupt__': [
        #         Interrupt(
        #             value={
        #                 'name': 'tavily_search',
        #                 'args': '* ツール名\n  * tavily_search\n* 引数\n  * query\n    * GPT-5.1 recent announcement OpenAI\n  * time_range\n    * 
        # month\n  * search_depth\n    * advanced\n'
        #             },
        #             id='0b6b13bd32a0a7c9c9231a994207bf1a'
        #         )
        #     ]
        # }

        print("---------------結果---------------")
        print(result)
        print("------------------------------------")

        while True:
            # 最終的にはAIMessageが返ってくるのでAIMessageでない場合はHuman-in-the-loopでツール実行をするかしないか判断する
            if not isinstance(result, AIMessage):
                # 上記のように'__interrupt__'があった場合はユーザーにツール実行をするかしないか判断する
                if "__interrupt__" in result.keys():
                
                    feedback_result = input("ツールを実行しますか？ (Y/n): ")
                    feedback_result = feedback_result.lower()
                    
                    # Command(resume=feedback_result)とすると止まっていたところから再開できる。
                    # 今回の場合はask_humanのfeedback = interrupt(tool_data)のところから再開
                    # feedbackにfeedback_resultの値が入る
                    result = agent.invoke(Command(resume=feedback_result), config=config)

                    print("---------------結果---------------")
                    print(result)
                    print("------------------------------------")
            else:
                return result

        return result   # 最終結果を返す

    asyncio.run(test_agent())