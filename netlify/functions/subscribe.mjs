// POST /api/subscribe  {email, first_name?, segment?, source?}
// Adds the subscriber to Flodesk, then to the segment for the newsletter or guide.
// Needs two environment variables in Netlify (Site configuration > Environment variables):
//   FLODESK_API_KEY   your Flodesk API key (Flodesk > Account settings > Integrations > API keys)
//   FLODESK_SEGMENTS  JSON map of segment names to Flodesk segment ids, e.g.
//                     {"newsletter":"64ab...","sas-prompt-guide":"64cd..."}
// Without a key it answers 503 and the form on the site falls back to the Flodesk signup page.

const API = 'https://api.flodesk.com/v1';
// Throwaway inbox services that bots and freebie hunters use.
const DISPOSABLE = new Set(`mailinator.com guerrillamail.com guerrillamail.net sharklasers.com grr.la 10minutemail.com
10minutemail.net temp-mail.org tempmail.com tempmail.net tempmailo.com yopmail.com yopmail.net trashmail.com
trashmail.de getnada.com nada.email dispostable.com maildrop.cc mailnesia.com throwawaymail.com fakeinbox.com
mintemail.com mohmal.com emailondeck.com spamgourmet.com mytemp.email tempr.email discard.email moakt.com
burnermail.io inboxkitten.com mail.tm mail.gw byom.de fexpost.com tmpmail.org tmpmail.net emailfake.com
33mail.com spambox.us getairmail.com tempinbox.com mailcatch.com`.split(/\s+/));
const json = (status, body) => new Response(JSON.stringify(body), {
  status, headers: { 'content-type': 'application/json' },
});

export default async (req) => {
  if (req.method !== 'POST') return json(405, { error: 'Method not allowed' });
  const key = process.env.FLODESK_API_KEY;
  if (!key) return json(503, { error: 'Signup is not configured yet' });

  let data;
  try { data = await req.json(); } catch { return json(400, { error: 'Invalid request' }); }
  const email = String(data.email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) {
    return json(400, { error: 'Please enter a valid email address' });
  }
  // Spam checks. Suspicious requests get a fake "ok" so bots don't learn what blocked them.
  const fake = (why) => { console.log('Blocked signup:', why); return json(200, { ok: true }); };
  if (data.website) return fake('honeypot filled');
  const origin = req.headers.get('origin') || req.headers.get('referer') || '';
  if (!/^https:\/\/([a-z0-9-]+--)?(shetalksbusiness\.co|shetalksbusiness\.netlify\.app)(\/|$)/i.test(origin)) {
    return fake('wrong origin ' + origin.slice(0, 80));
  }
  const elapsed = Number(data.t);
  if (!Number.isFinite(elapsed) || elapsed < 2000) return fake('too fast or no timer');
  const domain = email.split('@')[1];
  if (DISPOSABLE.has(domain)) return fake('disposable domain ' + domain);
  if (/^[a-z0-9]{20,}@/.test(email) && !/[aeiou]{1}/.test(email.split('@')[0].slice(0, 12))) {
    return fake('random-looking address');
  }

  let segments = {};
  try { segments = JSON.parse(process.env.FLODESK_SEGMENTS || '{}'); } catch {}
  const name = String(data.segment || 'newsletter').replace(/[^a-z0-9-]/gi, '').slice(0, 60);
  const ids = [...new Set([segments.newsletter, segments[name]].filter(Boolean))];

  const headers = {
    authorization: 'Basic ' + Buffer.from(key + ':').toString('base64'),
    'content-type': 'application/json',
    'user-agent': 'She Talks Business website (shetalksbusiness.co)',
  };

  const sub = await fetch(`${API}/subscribers`, {
    method: 'POST', headers,
    body: JSON.stringify({
      email,
      ...(data.first_name ? { first_name: String(data.first_name).slice(0, 80) } : {}),
    }),
  });
  if (!sub.ok) {
    console.error('Flodesk subscriber error', sub.status, await sub.text());
    return json(502, { error: 'Could not sign you up right now' });
  }

  // The subscriber now exists in Flodesk. Add them to the segments, using the id Flodesk returned.
  let subId = email;
  try { const s = await sub.json(); subId = s.id || email; } catch {}
  if (ids.length) {
    const seg = await fetch(`${API}/subscribers/${encodeURIComponent(subId)}/segments`, {
      method: 'POST', headers, body: JSON.stringify({ segment_ids: ids }),
    });
    if (!seg.ok) {
      // Don't fail the signup: the person is already on the list. Log what went wrong.
      console.error('Flodesk segment error', seg.status, await seg.text(), 'ids tried:', ids.join(','));
      try {
        const list = await fetch(`${API}/segments?per_page=100`, { headers });
        const body = await list.json();
        const segs = (body.data || body || []).map((s) => `${s.name}=${s.id}`).join(' | ');
        console.error('Flodesk segments available:', list.status, segs);
      } catch (e) { console.error('Could not list segments', e); }
    }
  }
  return json(200, { ok: true });
};

export const config = {
  path: '/api/subscribe',
  // Max 5 signups per minute from the same IP address; extra requests get a 429.
  rateLimit: { windowLimit: 5, windowSize: 60, aggregateBy: ['ip', 'domain'] },
};
