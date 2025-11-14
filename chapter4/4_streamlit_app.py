import uuid # UUID（Universally Unique Identifier）を生成するためのモジュールをインポートします。
import streamlit as st # Streamlitライブラリをstというエイリアスでインポートします。
from langchain_core.messages import HumanMessage # LangChainのHumanMessageクラスをインポートします。
from langgraph.types import Command # LangGraphのCommandクラスをインポートします。

# core.pyからエージェントをインポート # 別ファイルで定義されたエージェントをインポートするコメントです。
from x_agent_core import agent # x_agent_coreモジュールからagentオブジェクトをインポートします。

def init_session_state(): # Streamlitのセッション状態を初期化する関数を定義します。
    """セッション状態を初期化する""" # 関数のdocstringです。
    if 'messages' not in st.session_state: # セッション状態に'messages'がない場合、
        st.session_state.messages = [] # 空のリストとして'messages'を初期化します。
    if 'waiting_for_approval' not in st.session_state: # セッション状態に'waiting_for_approval'がない場合、
        st.session_state.waiting_for_approval = False # Falseとして'waiting_for_approval'を初期化します。
    if 'final_result' not in st.session_state: # セッション状態に'final_result'がない場合、
        st.session_state.final_result = None # Noneとして'final_result'を初期化します。
    if "thread_id" not in st.session_state: # セッション状態に'thread_id'がない場合、
        st.session_state.thread_id = None # Noneとして'thread_id'を初期化します。

def reset_session(): # セッション状態をリセットする関数を定義します。
    """セッション状態をリセットする""" # 関数のdocstringです。
    st.session_state.messages = [] # メッセージリストを空にリセットします。
    st.session_state.waiting_for_approval = False # 承認待ちフラグをFalseにリセットします。
    st.session_state.final_result = None # 最終結果をNoneにリセットします。
    st.session_state.thread_id = None # スレッドIDをNoneにリセットします。

# セッション状態の初期化を実行 # アプリケーション起動時にセッション状態を初期化するコメントです。
init_session_state() # セッション状態の初期化関数を呼び出します。

def run_agent(input_data): # エージェントを実行し、結果を処理する関数を定義します。
    """エージェントを実行し、結果を処理する""" # 関数のdocstringです。
    # AIエージェント呼び出しに使うconfigurationの作成 # AIエージェント呼び出しのための設定を作成するコメントです。
    config = {"configurable": # 設定情報を格納する辞書を定義します。
        {"thread_id": st.session_state.thread_id} # スレッドIDをconfigに追加します。
    }
        
    # 結果を処理 # エージェントの実行結果を処理するコメントです。
    with st.spinner("処理中...", show_time=True): # Streamlitのスピナーを表示し、処理中であることをユーザーに伝えます。
        for chunk in agent.stream(input_data, stream_mode="updates", config=config): # エージェントからのストリーム更新をループ処理します。
            for task_name, result in chunk.items(): # 各チャンク内のタスク名と結果を反復処理します。
                # interruptの場合 # エージェントが中断された場合の処理を示すコメントです。
                if task_name == "__interrupt__": # タスク名が"__interrupt__"の場合、
                    st.session_state.tool_info = result[0].value # ツール情報をセッション状態に保存します。
                    st.session_state.waiting_for_approval = True # 承認待ち状態をTrueに設定します。
                # 最終回答の場合 # エージェントが最終回答を生成した場合の処理を示すコメントです。
                elif task_name == "agent": # タスク名が"agent"の場合、
                    if result is not None:
                        st.session_state.final_result = result.content # 最終結果をセッション状態に保存します。
                    else:
                        st.session_state.final_result = None # resultがNoneの場合はNoneを保存
                # LLM推論の場合 # LLM（大規模言語モデル）が推論を行った場合の処理を示すコメントです。
                elif task_name == "invoke_llm": # タスク名が"invoke_llm"の場合、
                    if isinstance(chunk["invoke_llm"].content, list): # LLMの応答内容がリストの場合、
                        for content in result.content: # リスト内の各コンテンツを反復処理します。
                            if content["type"] == "text": # コンテンツのタイプが"text"の場合、
                                st.session_state.messages.append({"role": "assistant", "content": content["text"]}) # アシスタントメッセージとしてセッション状態に追加します。
                # ツール実行の場合 # ツールが実行された場合の処理を示すコメントです。
                elif task_name == "use_tool": # タスク名が"use_tool"の場合、
                    st.session_state.messages.append({"role": "assistant", "content": "ツールを実行！"}) # 「ツールを実行！」というアシスタントメッセージをセッション状態に追加します。
        st.rerun() # Streamlitアプリケーションを再実行し、UIを更新します。
                
def feedback(): # ユーザーからのフィードバックを取得し、エージェントに通知する関数を定義します。
    """フィードバックを取得し、エージェントに通知する関数""" # 関数のdocstringです。
    approve_column, deny_column = st.columns(2) # 承認ボタンと拒否ボタンを配置するための2つのカラムを作成します。

    feedback_result = None # フィードバックの結果をNoneで初期化します。
    with approve_column: # 承認カラム内で、
        if st.button("APPROVE", width="stretch"): # 「APPROVE」ボタンが押された場合、
            st.session_state.waiting_for_approval = False # 承認待ち状態をFalseに設定します。
            feedback_result = "APPROVE" # フィードバック結果を「APPROVE」に設定します。
    with deny_column: # 拒否カラム内で、
        if st.button("DENY", width="stretch"): # 「DENY」ボタンが押された場合、
            st.session_state.waiting_for_approval = False # 承認待ち状態をFalseに設定します。
            feedback_result = "DENY" # フィードバック結果を「DENY」に設定します。
                
    # いずれかのボタンが押された場合 # いずれかのフィードバックボタンが押された場合の処理を示すコメントです。
    return feedback_result # フィードバック結果を返します。

def app(): # Streamlitアプリケーションのメイン関数を定義します。
    # タイトルの設定 # アプリケーションのタイトルを設定するコメントです。
    st.title("Webリサーチエージェント") # アプリケーションのタイトルを「Webリサーチエージェント」に設定します。

    # メッセージ表示エリア # メッセージを表示するエリアのコメントです。
    for msg in st.session_state.messages: # セッション状態のメッセージリストを反復処理します。
        if msg["role"] == "user": # メッセージの役割が「user」の場合、
            st.chat_message("user").write(msg["content"]) # ユーザーのチャットメッセージとして内容を表示します。
        else: # メッセージの役割が「assistant」の場合、
            st.chat_message("assistant").write(msg["content"]) # アシスタントのチャットメッセージとして内容を表示します。
            
    # ツール承認の確認 # ツール承認が必要かどうかの確認を示すコメントです。
    if st.session_state.waiting_for_approval \
       and st.session_state.tool_info: # 承認待ち状態であり、ツール情報がある場合、
        st.info(st.session_state.tool_info["args"]) # ツール引数を情報として表示します。
        if st.session_state.tool_info["name"] == "write_file": # ツール名が"write_file"の場合、
            with st.container(height=400): # 高さ400ピクセルのコンテナを作成し、その中で、
                st.html(st.session_state.tool_info["html"], width="stretch") # ツール情報に含まれるHTMLコンテンツを表示します。
        feedback_result = feedback() # feedback関数を呼び出してフィードバック結果を取得します。
        if feedback_result: # フィードバック結果がある場合、
            st.chat_message("user").write(feedback_result) # ユーザーのチャットメッセージとしてフィードバック結果を表示します。
            st.session_state.messages.append({"role": "user", "content": feedback_result}) # フィードバック結果をユーザーメッセージとしてセッション状態に追加します。
            run_agent(Command(resume=feedback_result)) # エージェントを再開し、フィードバック結果を渡します。
            st.rerun() # Streamlitアプリケーションを再実行し、UIを更新します。

    # 最終結果の表示 # 最終結果を表示するエリアのコメントです。
    if st.session_state.final_result \
       and not st.session_state.waiting_for_approval: # 最終結果があり、かつ承認待ち状態でない場合、
        st.subheader("最終結果") # 「最終結果」というサブヘッダーを表示します。
        st.success(st.session_state.final_result) # 最終結果を成功メッセージとして表示します。

    # ユーザー入力エリア # ユーザーがメッセージを入力するエリアのコメントです。
    if not st.session_state.waiting_for_approval: # 承認待ち状態でない場合、
        user_input = st.chat_input("メッセージを入力してください") # ユーザー入力用のチャット入力ボックスを表示します。
        if user_input: # ユーザーが何か入力した場合、
            reset_session() # セッション状態をリセットします。
            # スレッドIDを設定 # 新しいスレッドIDを設定するコメントです。
            st.session_state.thread_id = str(uuid.uuid4()) # 新しいUUIDを生成し、スレッドIDとして設定します。
            # ユーザーメッセージを追加 # ユーザーメッセージをチャットに追加するコメントです。
            st.chat_message("user").write(user_input) # ユーザーの入力内容をチャットメッセージとして表示します。
            st.session_state.messages.append({"role": "user", "content": user_input}) # ユーザーの入力内容をセッション状態のメッセージリストに追加します。
            
            # エージェントを実行 # エージェントを実行するコメントです。
            messages = [HumanMessage(content=user_input)] # ユーザーの入力内容をHumanMessageとしてリストに格納します。
            if run_agent(messages): # run_agent関数を呼び出してエージェントを実行します。
                st.rerun() # run_agentがTrueを返した場合（通常は再実行されるため）、Streamlitアプリケーションを再実行し、UIを更新します。
    else: # 承認待ち状態の場合、
        st.info("ツールの承認待ちです。上記のボタンで応答してください。") # ツール承認待ちであることをユーザーに通知します。

# メインの実行 # アプリケーションのメイン実行ブロックのコメントです。
if __name__ == "__main__": # スクリプトが直接実行された場合、
    app() # app関数を呼び出してStreamlitアプリケーションを開始します。
