// POST /api/subscribe  {email, first_name?, segment?, source?}
// Adds the subscriber to Flodesk, then to the segment for the newsletter or guide.
// Needs two environment variables in Netlify (Site configuration > Environment variables):
//   FLODESK_API_KEY   your Flodesk API key (Flodesk > Account settings > Integrations > API keys)
//   FLODESK_SEGMENTS  JSON map of segment names to Flodesk segment ids, e.g.
//                     {"newsletter":"64ab...","sas-prompt-guide":"64cd..."}
// Without a key it answers 503 and the form on the site falls back to the Flodesk signup page.

const API = 'https://api.flodesk.com/v1';
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
  if (data.website) return json(200, { ok: true }); // honeypot: pretend success

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

  if (ids.length) {
    const seg = await fetch(`${API}/subscribers/${encodeURIComponent(email)}/segments`, {
      method: 'POST', headers, body: JSON.stringify({ segment_ids: ids }),
    });
    if (!seg.ok) {
      console.error('Flodesk segment error', seg.status, await seg.text());
      return json(502, { error: 'Could not sign you up right now' });
    }
  }
  return json(200, { ok: true });
};

export const config = { path: '/api/subscribe' };
