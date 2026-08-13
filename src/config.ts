import { createLogger } from '@alwatr/logger';

const clientId = process.env.OAUTH_GITHUB_CLIENT_ID;
const clientSecret = process.env.OAUTH_GITHUB_CLIENT_SECRET;
const scope = process.env.OAUTH_GITHUB_SCOPE;
const githubHost = process.env.OAUTH_GITHUB_HOST || 'https://github.com';
const tokenPath = process.env.OAUTH_GITHUB_TOKEN_PATH || '/login/oauth/access_token';
const authorizePath = process.env.OAUTH_GITHUB_AUTHORIZE_PATH || '/login/oauth/authorize';

if (clientId == undefined) {
  throw new Error('github client id required, OAUTH_GITHUB_CLIENT_ID="123_123_123" yarn start');
}
if (clientSecret == undefined) {
  throw new Error('github client secret required, OAUTH_GITHUB_CLIENT_SECRET="123_123_123" yarn start');
}

export const config = {
  client: {
    id: clientId as string,
    secret: clientSecret as string,
  },
  scope: scope || 'repo',
  githubHost: githubHost as string,
  auth: {
    tokenHost: githubHost,
    tokenPath: tokenPath,
    authorizePath: authorizePath,
  },
  nanoServer: {
    host: process.env.HOST ?? '0.0.0.0',
    port: process.env.PORT != null ? +process.env.PORT : 8000,
    healthRoute: true,
  },
};

export const logger = createLogger('decap-cms-backend');

logger.logProperty?.('config', config);
