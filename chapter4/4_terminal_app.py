import uuid
import asyncio
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from x_agent_core import agent as agent_entrypoint_func # agent 関数を別の名前にインポート
from x_agent_core import checkpointer # checkpointer もインポート

# agent_entrypoint_func を呼び出して、実際のグラフインスタンスを取得
agent = agent_entrypoint_func(checkpointer)

# Streamlitのst.session_stateの代わりに通常のPython変数を使用
session_state = {
    "messages": [],
    "waiting_for_approval": False,
    "final_result": None,
    "thread_id": None,
    "tool_info": None,
}

def init_session_state():
    """セッション状態を初期化する (ターミナル版)"""
    session_state['messages'] = []
    session_state['waiting_for_approval'] = False
    session_state['final_result'] = None
    session_state['thread_id'] = None
    session_state['tool_info'] = None

def reset_session():
    """セッション状態をリセットする (ターミナル版)"""
    init_session_state()

async def run_agent_terminal(input_data):
    """エージェントを実行する (ターミナル版)"""
    config = {"configurable": {"thread_id": session_state['thread_id']}}
    async for chunk in agent.stream(input_data, stream_mode="updates", config=config):
        pass

# async def run_agent_terminal(input_data):
#     """エージェントを実行し、結果を処理する (ターミナル版)"""
#     config = {"configurable": {"thread_id": session_state['thread_id']}}
        
#     print("処理中...")
#     # エージェントからのストリーム更新をループ処理します。
#     async for chunk in agent.stream(input_data, stream_mode="updates", config=config):
#         # 各チャンク内のタスク名と結果を反復処理します。
#         for task_name, result in chunk.items():
#             # エージェントが中断された場合の処理
#             if task_name == "__interrupt__":
#                 session_state['tool_info'] = result[0].value
#                 session_state['waiting_for_approval'] = True
#                 print(f"\n--- ツール承認待ち ---")
#                 print(f"ツール引数: {session_state['tool_info']['args']}")
#                 if session_state['tool_info']['name'] == "write_file":
#                     print(f"HTMLコンテンツ:\n{session_state['tool_info']['html']}")
                
#                 # ユーザーからのフィードバックを input() で受け取る
#                 feedback_input = input("ツールを実行しますか？ (APPROVE/DENY): ").upper()
#                 session_state['messages'].append({"role": "user", "content": feedback_input})
#                 print(f"User: {feedback_input}")
                
#                 # ユーザーからのフィードバックをエージェントに渡して再開
#                 session_state['waiting_for_approval'] = False # 承認待ち状態を解除
#                 await run_agent_terminal(Command(resume=feedback_input))
#                 return # 承認後の再帰呼び出しで処理が完了したら元のループを抜ける
#             # エージェントが最終回答を生成した場合の処理
#             elif task_name == "agent":
#                 if result is not None:
#                     session_state['final_result'] = result.content
#                 else:
#                     session_state['final_result'] = None
#             # LLM（大規模言語モデル）が推論を行った場合の処理
#             elif task_name == "invoke_llm":
#                 if isinstance(chunk["invoke_llm"].content, list):
#                     for content in result.content:
#                         if content["type"] == "text":
#                             session_state['messages'].append({"role": "assistant", "content": content["text"]})
#                             print(f"Assistant: {content["text"]}")
#                 else:
#                     session_state['messages'].append({"role": "assistant", "content": result.content})
#                     print(f"Assistant: {result.content}")
#             # ツールが実行された場合の処理
#             elif task_name == "use_tool":
#                 session_state['messages'].append({"role": "assistant", "content": "ツールを実行！"})
#                 print("Assistant: ツールを実行！")
    
#     # 最終結果があり、かつ承認待ち状態でない場合
#     if session_state['final_result'] and not session_state['waiting_for_approval']:
#         print("\n--- 最終結果 ---")
#         print(session_state['final_result'])
    
#     return session_state['final_result']

async def app_terminal():
    """アプリケーションのメイン関数 (ターミナル版)"""
    print("--- Webリサーチエージェント (ターミナル版) ---")

    init_session_state()

    while True:
        # 承認待ち状態でない場合
        if not session_state['waiting_for_approval']:
            user_input = input("\nメッセージを入力してください (終了する場合は 'exit'): ")
            if user_input.lower() == 'exit':
                break

            reset_session()
            # 新しいUUIDを生成し、スレッドIDとして設定します。
            session_state['thread_id'] = str(uuid.uuid4())
            # ユーザーの入力内容をセッション状態のメッセージリストに追加します。
            session_state['messages'].append({"role": "user", "content": user_input})
            print(f"User: {user_input}")

            messages = [HumanMessage(content=user_input)]
            await run_agent_terminal(messages)
        else:
            # run_agent_terminal内でユーザー入力処理が行われるため、ここでは何もしない
            pass

# スクリプトが直接実行された場合
if __name__ == "__main__":
    asyncio.run(app_terminal())
