import { AuthFetchAuthSessionServer } from "./amplify-server-utils";

export async function getBedrockModel() {
    try {
        const { createAmazonBedrock } = await import("@ai-sdk/amazon-bedrock");

        const modelId = "us.anthropic.claude-3-7-sonnet-20250219-v1:0";

        const region = process.env.AWS_REGION || "us-west-2";

        const session = await AuthFetchAuthSessionServer();

        if (!session || !session.credentials) {
            throw new Error("Failed to get authentication session");
        }

        const bedrock = createAmazonBedrock({
            region,
            accessKeyId: session.credentials.accessKeyId,
            secretAccessKey: session.credentials.secretAccessKey,
            sessionToken: session.credentials.sessionToken,
        });

        const model = bedrock(modelId);

        return model;
    } catch (error) {
        throw error;
    }
}