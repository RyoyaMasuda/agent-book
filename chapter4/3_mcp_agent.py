import asyncio # 非同期処理を扱うためのモジュールをインポートします。
import operator # オペレータ関数（例: operator.add）をインポートします。
import os # オペレーティングシステムと対話するためのモジュールをインポートします。
from langchain.chat_models import init_chat_model # LangChainのチャットモデルを初期化する関数をインポートします。
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage # LangChainのメッセージタイプ（任意、AI、人間、システム）をインポートします。
from langchain_mcp_adapters.client import MultiServerMCPClient # MultiServerMCPClientをインポートします。
from langgraph.graph import StateGraph, START, END # LangGraphのStateGraph、開始ノード、終了ノードをインポートします。
from langgraph.prebuilt import ToolNode # LangGraphの事前構築済みツールノードをインポートします。
from pydantic import BaseModel # PydanticのBaseModelをインポートし、データモデルを定義します。
from typing import Annotated, Dict, List, Union # 型ヒントのためのAnnotated, Dict, List, Unionをインポートします。

from dotenv import load_dotenv # .envファイルから環境変数をロードする関数をインポートします。
load_dotenv() # 環境変数をロードします。

mcp_client = None # MCPクライアントを格納するためのグローバル変数をNoneで初期化します。
tools = None # ツールを格納するためのグローバル変数をNoneで初期化します。
llm_with_tools = None # ツールにバインドされたLLMを格納するためのグローバル変数をNoneで初期化します。

async def initialize_llm(): # LLMを初期化するための非同期関数を定義します。
    """MCPクライアントとツールを初期化する""" # 関数のdocstringです。
    global mcp_client, tools, llm_with_tools # グローバル変数を関数内で使用することを宣言します。
    
    mcp_client = MultiServerMCPClient( # MultiServerMCPClientのインスタンスを作成します。
        { # MCPサーバーの設定を辞書形式で定義します。
            # FileSystem MCPサーバー # ファイルシステムMCPサーバーの設定を開始します。
            "file-system": { # 「file-system」という名前のサーバーを設定します。
                "command": "npx", # 実行するコマンドはnpxです。
                "args": [ # npxコマンドに渡す引数をリストで定義します。
                    "-y", # npxのプロンプトに自動的にyesと答えるための引数です。
                    "@modelcontextprotocol/server-filesystem", # 実行するパッケージ名です。
                    "./" # ファイルシステムサーバーがカレントディレクトリを対象とすることを示します。
                ],
                "transport": "stdio", # サーバーとの通信に標準入出力（stdio）を使用します。
            },
            # AWS Knowledge MCPサーバー # AWSナレッジMCPサーバーの設定を開始します。
            "aws-knowledge-mcp-server": { # 「aws-knowledge-mcp-server」という名前のサーバーを設定します。
                "url": "https://knowledge-mcp.global.api.aws", # サーバーのエンドポイントURLです。
                "transport": "streamable_http", # サーバーとの通信にストリーミング可能なHTTPを使用します。
            }
        }
    )
    # MCPサーバーをLangChainツールとして取得 # 取得したMCPサーバーをLangChainのツールとして利用します。
    tools = await mcp_client.get_tools() # MCPクライアントからツールを取得し、グローバル変数toolsに格納します。
    
    # LLMの初期化 # 大規模言語モデル（LLM）の初期化を行います。
    llm_with_tools = init_chat_model( # LangChainのチャットモデルを初期化します。
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0", # 使用するモデルのIDを指定します。
        model_provider="bedrock_converse", # モデルプロバイダーとしてBedrock Converseを指定します。
    ).bind_tools(tools) # 初期化されたLLMに取得したツールをバインドします。


# ステートの定義 # エージェントの状態を定義します。
class AgentState(BaseModel): # PydanticのBaseModelを継承してAgentStateクラスを定義します。
    messages: Annotated[list[AnyMessage], operator.add] # メッセージのリストを定義し、新しいメッセージが追加されると結合されるようにします。


system_prompt = """ # LLMに与えるシステムプロンプトを定義します。
あなたの責務はAWSドキュメントを検索し、Markdown形式としてファイル出力することです。 # エージェントの主な責務を説明します。
- 検索後、Markdown形式に変換してください。 # 検索結果をMarkdown形式に変換するよう指示します。
- 検索は最大で2回までとし、その時点での情報を出力してください。 # 検索回数を最大2回に制限し、その時点での情報を出力するよう指示します。
"""
async def agent(state: AgentState) -> Dict[str, List[AIMessage]]: # エージェントの主要なロジックを実装する非同期関数を定義します。
    response = await llm_with_tools.ainvoke( # ツールにバインドされたLLMを非同期で呼び出します。
       [SystemMessage(system_prompt)] + state.messages # システムプロンプトと現在のメッセージ履歴を結合してLLMに渡します。
    )

    return {"messages": [response]} # LLMからの応答をメッセージリストとして返します。

# ルーティング関数：toolsノードかENDノードへ遷移する # グラフの次のステップを決定するルーティング関数です。
def route_node(state: AgentState) -> Union[str]: # エージェントの状態を受け取り、次に遷移するノード名を文字列で返します。
    last_message = state.messages[-1] # メッセージ履歴の最後のメッセージを取得します。
    if not isinstance(last_message, AIMessage): # 最後のメッセージがAIMessage型でない場合、エラーを発生させます。
	    raise ValueError("「AIMessage」以外のメッセージです。遷移が不正な可能性があります。") # 不正なメッセージタイプに対するエラーメッセージです。
    if not last_message.tool_calls: # 最後のAIメッセージにツール呼び出しが含まれていない場合、
        return END # ENDノードへ遷移します。
    return "tools" # ツール呼び出しがある場合は、"tools"ノードへ遷移します。

async def main(): # メイン処理を行う非同期関数を定義します。
    # MCPクライアントとツールを初期化 # MCPクライアントとツールの初期化を行います。
    await initialize_llm() # initialize_llm関数を呼び出してMCPクライアントとツール、LLMを初期化します。
    
    # グラフを構築 # LangGraphのグラフを構築します。
    builder = StateGraph(AgentState) # AgentStateを状態として持つStateGraphのビルダーを作成します。
    builder.add_node("agent", agent) # "agent"という名前でagent関数をノードとして追加します。
    builder.add_node("tools", ToolNode(tools)) # "tools"という名前でToolNodeにツールをバインドしてノードとして追加します。
    
    builder.add_edge(START, "agent") # グラフの開始（START）から"agent"ノードへのエッジを追加します。
    builder.add_conditional_edges( # 条件付きエッジを追加します。
        "agent", # "agent"ノードから条件付き遷移を開始します。
        route_node, # route_node関数を使って次のノードを決定します。
    )
    builder.add_edge("tools", "agent") # "tools"ノードから"agent"ノードへのエッジを追加します。
    
    graph = builder.compile(name="ReAct Agent") # グラフをコンパイルし、"ReAct Agent"という名前を付けます。
    
    question = "Bedrockで利用可能なモデルプロパイダーを教えて！" # エージェントに尋ねる質問を定義します。
    response = await graph.ainvoke( # グラフを非同期で実行し、質問に対する応答を取得します。
        {"messages": # メッセージを含む辞書を渡します。
            [HumanMessage(question)] # 質問をHumanMessageとしてメッセージリストに追加します。
        }
    )
    print(response) # エージェントからの応答を表示します。
    return response # 応答を返します。

asyncio.run(main()) # main関数を非同期で実行します。