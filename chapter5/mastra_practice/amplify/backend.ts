import { defineBackend } from '@aws-amplify/backend';
import { auth } from './auth/resource';
import { data } from './data/resource';
import { ManagedPolicy } from 'aws-cdk-lib/aws-iam';

/**
 * @see https://docs.amplify.aws/react/build-a-backend/ to add storage, functions, and more
 */

const backend = defineBackend({
  auth
});

const authecticatedUserIamRole = backend.auth.resources.authenticatedUserIamRole;

authecticatedUserIamRole.addManagedPolicy(
  ManagedPolicy.fromAwsManagedPolicyName("AmazonBedrockFullAccess")
);