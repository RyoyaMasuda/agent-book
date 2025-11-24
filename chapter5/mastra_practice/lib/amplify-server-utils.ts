import { cookies } from "next/headers";
import { createServerRunner } from "@aws-amplify/adapter-nextjs";
import { fetchAuthSession } from "aws-amplify/auth/server";

import outputs from "../amplify_outputs.json";

const serverRunner = createServerRunner(
    {
        config: outputs,
    }
)

export const { runWithAmplifyServerContext } = serverRunner;

export async function AuthFetchAuthSessionServer() {
    try {
        const session = await runWithAmplifyServerContext(
            {
                nextServerContext: { cookies },
                operation: (contextSpec: any) => fetchAuthSession(contextSpec)
            }
        )
        return session;
    } catch (error) {
        return null;
    }
}

