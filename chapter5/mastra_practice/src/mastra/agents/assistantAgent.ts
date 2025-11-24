import { Agent } from "@mastra/core/agent";
import { bedrock } from "@ai-sdk/amazon-bedrock";
import { getBedrockModel } from "../../../lib/aws-config";

const model = await getBedrockModel();

export const assistantAgent = new Agent(
  {
    name: "assistant",
    instructions: "あなたは親切で知識豊富なAIアシスタントです。ユーザーの質問に対して、わかりやすく丁寧に回答してください。",
    // model: bedrock("us.anthropic.claude-3-5-haiku-20241022-v1:0"),
    model: model,
  }
);

// export const assistantAgent = new Agent({
//   name: "assistant",
//   instructions: "あなたは親切で知識豊富なAIアシスタントです。ユーザーの質問に対して、わかりやすく丁寧に回答してください。",
//   model: bedrock("us.anthropic.claude-3-7-sonnet-20250219-v1:0"),
// });
