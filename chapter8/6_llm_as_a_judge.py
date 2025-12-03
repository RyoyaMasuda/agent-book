# RAGAS（RAG評価フレームワーク）のインポート
# SingleTurnSample: 評価用のサンプルデータを格納するクラス
from ragas.dataset_schema import SingleTurnSample
# LangchainLLMWrapper: LangChainのLLMをRAGASで使用できるようにラップするクラス
from ragas.llms import LangchainLLMWrapper
# AspectCritic: LLMを評価者（judge）として使用し、回答の品質を評価するメトリクス
from ragas.metrics import AspectCritic
# LangChainのチャットモデルを初期化する関数
from langchain.chat_models import init_chat_model
# 環境変数を.envファイルから読み込むためのライブラリ
from dotenv import load_dotenv

# .envファイルから環境変数（APIキーなど）を読み込む
load_dotenv()

# 評価したい質問を設定
user_input = "日本の首都はどこでしょうか？"
# 別の質問例（コメントアウト済み）
# user_input = "日本の首都はどこでしょうか？質問に端的に回答してください。"

# AWS BedrockのClaudeモデルを初期化
# model: 使用するモデルの名前（Claude 3.7 Sonnet）
# model_provider: モデルプロバイダー（bedrock_converseはAWS BedrockのAPI）
llm = init_chat_model(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    model_provider="bedrock_converse",
)

# LLMに質問を送信して回答を取得
# invoke(): LLMにメッセージを送信するメソッド
# ("human", user_input): 人間からの入力として質問を送信
# .content: レスポンスからテキストコンテンツを取得
response = llm.invoke(("human", user_input)).content
print("response :" + response)

# 評価用のサンプルデータを作成
# SingleTurnSample: 1回の対話（質問と回答）を表すデータ構造
# user_input: ユーザーの質問
# response: LLMが生成した回答
# reference: 正解（参照データ）。評価の基準となる正しい回答
sample = SingleTurnSample(
    user_input=user_input,
    response=response,
    reference="東京都"
)

# 評価基準の定義（プロンプト）
# AspectCriticが評価を行う際に使用する指示文
# この定義に基づいて、LLMが評価者として回答の品質を判断する
definition="""
参照データと回答を比較し、正確性を評価してください。
参照データに対して、冗長でなく端的かつ関連した回答ができた場合のみ、評価値を1としてください。
"""

# 評価者（AspectCritic）を作成
# name: 評価メトリクスの名前
# definition: 評価基準の定義（上記のプロンプト）
# llm: 評価に使用するLLM（LangchainLLMWrapperでラップしてRAGASで使用可能にする）
evaluator = AspectCritic(
    name="relevance_score", 
    definition=definition,
    llm=LangchainLLMWrapper(llm)
)

# サンプルデータを評価してスコアを取得
# single_turn_score(): 1つのサンプルを評価し、スコア（0-1の値）を返す
# スコアが1に近いほど、回答が評価基準を満たしていることを意味する
score = evaluator.single_turn_score(sample)
print("Score: " + str(score))
