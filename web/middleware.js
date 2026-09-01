/* ============================================================================
   middleware.js — the actual gate.

   Runs at the edge, before any static file is served. This is what makes the
   internal pages genuinely private: without it, /internal/changelog is just a
   file on a public CDN and the locks in the sidebar are decoration.

   Two tiers:
     /internal/*  any verified @gushwork.ai account
     /admin/*     only the ADMIN_EMAILS allowlist

   The matcher below is deliberately narrow. Everything else — the Overview
   page, /foundation/tokens.css, the fonts, and critically
   /exports/dashboard/component-registry.json, which every dashboard the
   plugin builds fetches on load to check for drift — never reaches this
   function and stays public.
   ========================================================================= */

import { COOKIE, verify, readCookie, sessionSecret, authModes } from './api/_session.js';

export const config = {
  matcher: ['/internal/:path*', '/admin/:path*']
};

function forbidden(email) {
  return new Response(
    '<!doctype html><meta charset="utf-8"><title>Not your tier</title>' +
    '<link rel="stylesheet" href="/foundation/tokens.css">' +
    '<body style="margin:0;min-height:100vh;display:grid;place-items:center;' +
    'background:var(--gw-color-neutral-25);font-family:Inter,system-ui,sans-serif;' +
    'color:var(--gw-color-neutral-900)">' +
    '<div style="max-width:420px;padding:32px;background:#fff;border-radius:16px;' +
    'border:1px solid var(--gw-color-neutral-100);text-align:center">' +
    '<h1 style="margin:0 0 8px;font-size:22px">Admins only</h1>' +
    '<p style="margin:0 0 24px;font-size:14px;color:var(--gw-color-neutral-600)">' +
    'The review sheet and the catalogue are limited to the design system admins. ' +
    'You are signed in as ' + String(email || '').replace(/[<>&"]/g, '') + '.</p>' +
    '<a href="/" style="font-size:14px;color:var(--gw-color-primary-500)">' +
    'Back to Gushwork Design</a></div></body>',
    { status: 403, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
  );
}

function toSignIn(url) {
  const to = new URL('/', url);
  to.searchParams.set('signin', 'required');
  to.searchParams.set('next', url.pathname + url.search);
  return new Response(null, { status: 302, headers: { Location: to.toString() } });
}

export default async function middleware(request) {
  const url = new URL(request.url);
  const modes = authModes();

  /* Fail closed if there is no way in at all — an unconfigured gate must not
     quietly serve the private pages to everyone. In practice the password
     path has a default, so this only fires if SITE_PASSWORD is explicitly
     blanked before Google auth is configured. */
  if (!modes.google && !modes.password) {
    return new Response(
      '<!doctype html><meta charset="utf-8"><title>Sign-in not configured</title>' +
      '<body style="margin:0;min-height:100vh;display:grid;place-items:center;' +
      'font-family:Inter,system-ui,sans-serif;background:#f7f8f9;color:#262a2e">' +
      '<div style="max-width:460px;padding:32px;background:#fff;border-radius:16px;' +
      'border:1px solid #e7e8e9;text-align:center">' +
      '<h1 style="margin:0 0 8px;font-size:22px">Sign-in is not configured yet</h1>' +
      '<p style="margin:0 0 24px;font-size:14px;color:#6a7077">These pages stay closed ' +
      'until either SITE_PASSWORD or the three Google variables are set on the Vercel ' +
      'project.</p>' +
      '<a href="/" style="font-size:14px;color:#0070ff">Back to Gushwork Design</a>' +
      '</div></body>',
      { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
    );
  }

  /* One cookie, either door — the password route signs the same payload the
     Google callback does, so nothing here needs to know which was used. */
  const session = await verify(
    readCookie(request.headers.get('cookie'), COOKIE), sessionSecret()
  );
  if (!session) return toSignIn(url);

  if (url.pathname.startsWith('/admin') && !session.admin) {
    return forbidden(session.email);
  }

  /* Returning nothing continues to the next handler, which serves the file. */
  return undefined;
}
