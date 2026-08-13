import { apiServer } from '../lib/api-server.js';

apiServer.defineRoute({
  method: 'GET',
  url: '/',
  handler: function () {
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Origin', '*');
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    this.serverResponse.raw_.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    this.serverResponse.replyJson({
      ok: true,
      data: {
        app: '..:: Decap CMS Backend Microservice ::..',
        message: 'Hello',
      },
    });
  },
});

// Add OPTIONS support for CORS preflight
apiServer.defineRoute({
  method: 'OPTIONS',
  url: '/',
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
