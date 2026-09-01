/* Clears the session cookie and sends you back to a page on this site. */

import { COOKIE, serializeCookie, safeNext } from '../_session.js';

export default function handler(req, res) {
  const url = new URL(req.url, 'https://' + (req.headers['x-forwarded-host'] || req.headers.host));
  res.setHeader('Set-Cookie', serializeCookie(COOKIE, '', { maxAge: 0 }));
  res.writeHead(302, { Location: safeNext(url.searchParams.get('next')) });
  res.end();
}
