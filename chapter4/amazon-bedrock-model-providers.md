# Amazon Bedrockで利用可能なモデルプロバイダー

Amazon Bedrockは、AWS上の基盤モデル（FM: Foundation Model）を利用できるサービスです。以下のプロバイダーから様々なモデルを利用できます。

## 利用可能なモデルプロバイダー一覧

Amazon Bedrockでは、以下の主要なAI企業から提供される多数の基盤モデルにアクセスできます：

1. **AI21 Labs**
   - 長い文脈長に対する効率的な処理と接地された生成を提供

2. **Amazon**
   - Amazonの独自モデル「Titan」および「Nova」シリーズ
   - テキスト、画像、ドキュメント、ビデオ理解、画像・ビデオ生成、インタラクティブ音声、コード生成などの機能を提供

3. **Anthropic**
   - 複雑な推論、コード生成、指示に従うことに優れるClaude モデル

4. **Cohere**
   - 高度な検索と取得による効率的な多言語AIエージェントを提供

5. **DeepSeek**
   - 複雑な問題を段階的に解決する高度な推論モデル

6. **Luma AI**
   - 自然で一貫性のある動きと超リアルな細部を持つ高品質ビデオ生成

7. **Meta**
   - 高度な画像・言語推論を提供するLlamaモデル

8. **Mistral AI**
   - エージェント推論とマルチモーダルタスク向けの特化型エキスパートモデル

9. **OpenAI**
   - オープンソース版GPTモデル

10. **Qwen**
    - 中国Alibabaが開発したモデル

11. **Stability AI**
    - 画像生成のStable Diffusionモデル

12. **TwelveLabs**
    - ビデオ理解・分析モデル

13. **Writer**
    - テキスト生成に特化したモデル

## 主な特徴

Amazon Bedrockを通じて提供されるモデルは、以下のような特徴を備えています：

- **複数のモダリティ対応**：テキスト、画像、音声、ビデオなど様々な入出力形式をサポート
- **ストリーミング対応**：一部のモデルではリアルタイムのレスポンス生成が可能
- **リージョン間推論**：特定のモデルでは複数のAWSリージョンにまたがる推論が可能
- **埋め込み（Embeddings）対応**：多くのプロバイダーがベクトル埋め込みモデルを提供

## 入出力モダリティ

Amazon Bedrockのモデルは以下の入出力モダリティをサポートしています：

- **入力**：テキスト、画像、音声、ビデオ
- **出力**：テキスト、画像、音声、ビデオ、埋め込みベクトル

## その他の機能

Amazon Bedrockでは、モデル選択以外にも以下の機能が提供されています：

- **モデル評価**：異なるモデルやRAG（検索拡張生成）ワークフローからのレスポンスを比較・検証
- **カスタムモデルインポート**：独自のモデルをBedrockにインポートして既存のモデルと併用
- **Amazon Bedrock Marketplace**：100以上の一般的、新興、特化型の基盤モデルを発見、テスト、使用

## 詳細情報

各プロバイダーの詳細情報は以下のリンクから確認できます：

- [Amazon Nova](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html)
- [AI21 Labs](https://docs.ai21.com/)
- [Anthropic](https://docs.anthropic.com/)
- [Cohere](https://docs.cohere.com/docs)
- [DeepSeek](https://www.deepseek.com/)
- [Luma AI](https://lumalabs.ai/learning-hub)
- [Meta](https://ai.meta.com/llama/get-started)
- [Mistral AI](https://docs.mistral.ai/)
- [OpenAI](https://openai.com/api/)
- [Qwen](https://www.alibabacloud.com)
- [Stability AI](https://platform.stability.ai/docs/getting-started)
- [TwelveLabs](https://docs.twelvelabs.io/docs/get-started/introduction)
- [Writer AI](https://writer.com/llms/)