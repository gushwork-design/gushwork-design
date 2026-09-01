/* Starts the Google sign-in flow.
   GET /api/auth/login?next=/internal/changelog  →  302 to Google */

import {
  serializeCookie, safeNext, redirectUri, missingConfig
} from '../_session.js';

const STATE_COOKIE = 'gw_oauth_state';

export default function handler(req, res) {
  const missing = missingConfig();
  if (missing.length) {
    res.status(503).setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.end(
      'Google sign-in is not configured yet.\n\n' +
      'Missing environment variables: ' + missing.join(', ') + '\n\n' +
      'Set them on the Vercel project, then redeploy. See web/README-auth.md.'
    );
  }

  const url = new URL(req.url, 'https://' + (req.headers['x-forwarded-host'] || req.headers.host));
  const next = safeNext(url.searchParams.get('next'));

  /* CSRF: a random nonce goes into both the state parameter and a
     short-lived cookie. The callback only proceeds if they match, so a
     response we did not initiate cannot complete a sign-in. */
  const nonce = crypto.randomUUID();
  const state = Buffer.from(JSON.stringify({ n: nonce, next }), 'utf8').toString('base64url');

  const authorize = new URL('https://accounts.google.com/o/oauth2/v2/auth');
  authorize.searchParams.set('client_id', process.env.GOOGLE_CLIENT_ID);
  authorize.searchParams.set('redirect_uri', redirectUri(req));
  authorize.searchParams.set('response_type', 'code');
  authorize.searchParams.set('scope', 'openid email profile');
  authorize.searchParams.set('state', state);
  authorize.searchParams.set('prompt', 'select_account');
  /* `hd` asks Google to show only Workspace accounts on this domain. It is a
     hint to the picker, NOT a security control — the callback re-checks the
     verified claim, because a determined user can strip this parameter. */
  authorize.searchParams.set('hd', process.env.ALLOWED_DOMAIN || 'gushwork.ai');

  res.setHeader('Set-Cookie', serializeCookie(STATE_COOKIE, nonce, { maxAge: 600 }));
  res.writeHead(302, { Location: authorize.toString() });
  res.end();
}
