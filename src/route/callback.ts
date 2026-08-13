import { AuthorizationCode } from 'simple-oauth2';
import { config, logger } from '../config.js';
import { apiServer } from '../lib/api-server.js';

apiServer.defineRoute({
  method: 'GET',
  url: '/callback',
  handler: async function () {
    const host = this.headers.host;
    const url = new URL(`https://${host}/${this.url}`);
    const provider = url.searchParams.get('provider');
    const code = url.searchParams.get('code');
    const githubHost = url.searchParams.get('github_host') || config.githubHost;
    logger.logMethodArgs?.('get-callback', { host, url, provider, githubHost });

    if (provider !== 'github') {
      return {
        ok: false,
        statusCode: 400,
        errorCode: 'invalid_provider',
      };
    }

    if (!code) {
      return {
        ok: false,
        statusCode: 400,
        errorCode: 'require_code',
      };
    }

    // Use custom GitHub host if provided, otherwise fall back to config
    const authConfig = {
      tokenHost: githubHost,
      tokenPath: config.auth.tokenPath,
      authorizePath: config.auth.authorizePath,
    };

    const client = new AuthorizationCode({
      auth: authConfig,
      client: config.client,
    });
    const tokenParams = {
      code,
      redirect_uri: `https://${host}/callback?provider=${provider}&github_host=${encodeURIComponent(githubHost)}`,
    };

    const accessToken = await client.getToken(tokenParams);
    const token = accessToken.token['access_token'] as string;

    // Set CORS headers to allow communication with Decap CMS
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Origin', '*');
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    this.serverResponse.reply(renderBody('success', token, githubHost));

    return {
      ok: true,
      data: {},
    };
  },
});

// Add OPTIONS support for CORS preflight
apiServer.defineRoute({
  method: 'OPTIONS',
  url: '/callback',
  handler: function () {
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Origin', '*');
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    this.serverResponse.raw_.setHeader('Access-Control-Max-Age', '86400');
    
    return {
      ok: true,
      statusCode: 204,
      data: {},
    };
  },
});

function renderBody(status: string, token?: string, githubHost?: string) {
  const payload = token ? { token, githubHost } : { githubHost: githubHost || config.githubHost };
  return `
    <script>
      window.opener.postMessage(
        'authorization:github:${status}:${JSON.stringify(payload)}',
        "*"
      );
      window.close();
    </script>
  `;
}
