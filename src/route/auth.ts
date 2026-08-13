import { AuthorizationCode } from 'simple-oauth2';
import { randomBytes } from 'crypto';
import { apiServer } from '../lib/api-server.js';
import { config, logger } from '../config.js';

export const randomString = () => randomBytes(4).toString('hex');

apiServer.defineRoute({
  method: 'GET',
  url: '/auth',
  handler: function () {
    const host = this.headers.host;
    const url = new URL(`https://${host}/${this.url}`);
    const provider = url.searchParams.get('provider');
    const githubHost = url.searchParams.get('github_host') || config.githubHost;
    logger.logMethodArgs?.('get-auth', { host, url, provider, githubHost });

    if (provider !== 'github') {
      return {
        ok: false,
        statusCode: 400,
        errorCode: 'invalid_provider',
      };
    }

    // Use custom GitHub host if provided, otherwise fall back to config
    const authConfig = {
      tokenHost: githubHost,
      tokenPath: config.auth.tokenPath,
      authorizePath: config.auth.authorizePath,
    };

    const client = new AuthorizationCode({
      client: config.client,
      auth: authConfig,
    });

    const authorizationUri = client.authorizeURL({
      redirect_uri: `https://${host}/callback?provider=${provider}&github_host=${encodeURIComponent(githubHost)}`,
      scope: config.scope,
      state: randomString(),
    });

    logger.logProperty?.('authorizationUri', authorizationUri);

    this.serverResponse.raw_.setHeader('Location', authorizationUri);
    return {
      ok: true,
      statusCode: 301,
      data: {},
    };
  },
});
