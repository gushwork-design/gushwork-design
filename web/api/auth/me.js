/* Who is signed in, and which doors are open? shell.js calls this to decide
   whether to draw the locks, the ADMIN group and the user card — and whether
   the modal offers Google, a password field, or both.

   Always 200 — "nobody" is a valid answer, not an error. */

import { COOKIE, verify, readCookie, sessionSecret, authModes, GATE_ENABLED }
  from '../_session.js';

export default async function handler(req, res) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  /* The answer differs per cookie, so it must never be cached by the CDN. */
  res.setHeader('Cache-Control', 'no-store, private');

  const modes = authModes();
  const payload = await verify(readCookie(req.headers.cookie, COOKIE), sessionSecret());

  if (!payload) {
    return res.status(200).end(JSON.stringify({ signedIn: false, admin: false, modes,
                                                gate: GATE_ENABLED }));
  }

  res.status(200).end(JSON.stringify({
    signedIn: true,
    email: payload.email || null,
    name: payload.name || payload.email,
    picture: payload.picture || null,
    admin: !!payload.admin,
    via: payload.via || 'google',
    modes,
    gate: GATE_ENABLED
  }));
}
