"""Build newsletter issues into the static site.

Reads content/posts/*.md and writes:
  site/newsletter/<slug>.html   one page per published issue
  site/newsletter/index.html    the newsletter page with the full archive (/newsletter/)
  site/index.html               the 3 latest issues between <!--LATEST:START--> and <!--LATEST:END-->
  site/sitemap.xml              issue URLs between <!--POSTS:START--> and <!--POSTS:END-->

Run from the repo root:  python3 tools/build.py
Netlify runs the same command on every deploy.
"""
import os, re, sys, glob, json, html, datetime
sys.path.insert(0, os.path.dirname(__file__))
from md import convert, front_matter
from components import signup_form, EYEBROW, H2, WRAP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
DOMAIN = 'https://shetalksbusiness.co'
MONTHS = 'January February March April May June July August September October November December'.split()


def fmt_date(d):
    y, m, dd = map(int, d.split('-'))
    return f'{dd} {MONTHS[m - 1]} {y}'


def read_minutes(text):
    return max(1, round(len(re.findall(r'\w+', text)) / 220))


def shell():
    """Header and footer from the About page, with no active menu item."""
    t = open(os.path.join(SITE, 'about.html')).read()
    head = t[:t.index('<!-- HERO')]
    tail = t[t.index('<!-- FOOTER'):]
    head = re.sub(r'(href="/about#top"[^>]*?) border-bottom: 1px solid #242424; padding-bottom: 2px;', r'\1', head)
    head = head.replace(' aria-current="page"', '')
    return head, tail


def set_meta(head, title, desc, path, image=None, extra=''):
    e = html.escape
    head = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(desc), head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(desc), head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(title), head, count=1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + DOMAIN + path, head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + DOMAIN + path, head, count=1)
    if image:
        head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + DOMAIN + image, head, count=1)
    if extra:
        head = head.replace('</head>', extra + '\n</head>', 1)
    return head


def load_posts():
    posts = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'content', 'posts', '*.md'))):
        meta, body = front_matter(open(f, encoding='utf-8').read())
        if meta.get('status', 'published') != 'published':
            continue
        meta['body'] = body
        meta['slug'] = meta.get('slug') or os.path.basename(f)[:-3].split('-', 3)[-1]
        meta['minutes'] = read_minutes(body)
        posts.append(meta)
    posts.sort(key=lambda p: p['date'], reverse=True)
    return posts


def card(p):
    e = html.escape
    issue = f"Issue {p['issue']} · " if p.get('issue') else ''
    return (f'<a class="issue-card" href="/newsletter/{p["slug"]}#top">'
            f'<span class="issue-meta">{issue}{fmt_date(p["date"])}</span>'
            f'<h3>{e(p["title"])}</h3>'
            f'<p style="margin: 0; font-size: 16px; line-height: 1.6; color: #242424b3;">{e(p.get("description", ""))}</p>'
            '<span style="font-size: 13px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase;">Read the issue →</span></a>')


def guide_box(p):
    if not p.get('guide_title'):
        return ''
    e = html.escape
    pts = p.get('guide_points') or []
    lis = ''.join(f'<li style="padding-top: 10px; border-top: 1px solid #24242426;">{e(x)}</li>' for x in pts)
    ul = f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 16px;">{lis}</ul>' if lis else ''
    form = signup_form(p.get('guide_segment', 'newsletter'), 'Send me the guide',
                       success="Check your inbox, your guide is on its way!")
    return f'''<aside id="guide" aria-label="Free guide" style="background: #e5ddd2; border-radius: 4px; padding: clamp(28px, 5vw, 48px); display: flex; flex-direction: column; gap: 18px; margin: 48px 0;">
      <p style="{EYEBROW} color: #5f584a;">Free download</p>
      <h2 style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: clamp(30px, 3.4vw, 42px); line-height: 1.1;">{e(p['guide_title'])}</h2>
      <p style="margin: 0; font-size: 17px; line-height: 1.6;">{e(p.get('guide_pitch', 'Get the exact steps and prompts from this issue, plus a new workflow in your inbox every week.'))}</p>
      {ul}
      {form}
    </aside>'''


def reel_links(p):
    links = [(k, p.get(f'reel_{k}')) for k in ('instagram', 'tiktok', 'youtube')]
    links = [(k, u) for k, u in links if u]
    if not links:
        return ''
    names = {'instagram': 'Instagram', 'tiktok': 'TikTok', 'youtube': 'YouTube'}
    a = ' · '.join(f'<a href="{html.escape(u)}" style="color: #242424;">{names[k]}</a>' for k, u in links)
    return f'<p style="margin: 32px 0 0; font-size: 16px; color: #242424b3;">Prefer to watch? See the how-to on {a}.</p>'


def post_page(p, head, tail, others):
    e = html.escape
    path = f'/newsletter/{p["slug"]}'
    ld = {
        '@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'],
        'description': p.get('description', ''), 'datePublished': p['date'],
        'author': {'@type': 'Person', 'name': 'Lynn Noppen', 'url': DOMAIN + '/about'},
        'publisher': {'@type': 'Organization', 'name': 'She Talks Business', 'url': DOMAIN + '/'},
        'mainEntityOfPage': DOMAIN + path,
    }
    if p.get('image'): ld['image'] = DOMAIN + p['image']
    extra = '<script type="application/ld+json">' + json.dumps(ld) + '</script>'
    h = set_meta(head, f"{p['title']} | She Talks Business", p.get('description', ''), path, p.get('image'), extra)
    issue = f"Issue {p['issue']} · " if p.get('issue') else ''
    cover = (f'<img src="{e(p["image"])}" alt="{e(p.get("image_alt", ""))}" style="width: 100%; border-radius: 4px; display: block; margin: 0 0 48px;">'
             if p.get('image') else '')
    body_html = convert(p['body'])
    # place the guide box after the first h2-section block if marked, else at the end of the article
    box = guide_box(p)
    if '<!--guide-->' in p['body']:
        body_html = body_html.replace('<p>&lt;!--guide--&gt;</p>', box)
        box = ''
    more = ''.join(card(o) for o in others[:2])
    more_sec = f'''<section aria-label="More issues" style="background: #ffffff; border-top: 1px solid #24242426;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 48px;">
    <h2 style="{H2}">Keep <em>reading.</em></h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 40px;">{more}</div>
  </div>
</section>
''' if more else ''
    main = f'''<!-- ARTICLE -->
<article>
<section style="background: #f7f4f0;">
  <div style="max-width: 860px; margin: 0 auto; padding: 96px clamp(24px, 6vw, 96px) 72px; display: flex; flex-direction: column; gap: 24px;">
    <a href="/newsletter/#issues" style="{EYEBROW} color: #242424; text-decoration: none;">← The Resource Room</a>
    <p style="margin: 0; font-size: 13px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #7a715f;">{issue}{fmt_date(p['date'])} · {p['minutes']} min read</p>
    <h1 style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: clamp(44px, 5.6vw, 76px); line-height: 1.04;">{e(p['title'])}</h1>
    <p style="margin: 0; font-size: 21px; line-height: 1.55; color: #242424b3;">{e(p.get('dek', p.get('description', '')))}</p>
    <p style="margin: 8px 0 0; font-size: 15px;">By <a href="/about#top" style="color: #242424;">Lynn Noppen</a></p>
  </div>
</section>
<section style="background: #ffffff;">
  <div style="max-width: 860px; margin: 0 auto; padding: 72px clamp(24px, 6vw, 96px) 96px;">
    {cover}
    <div class="prose">
{body_html}
    </div>
    {box}
    {reel_links(p)}
  </div>
</section>
</article>

<!-- NEWSLETTER -->
<section style="background: #242424; color: #ffffff;">
  <div style="max-width: 900px; margin: 0 auto; padding: 112px clamp(24px, 6vw, 96px); display: flex; flex-direction: column; gap: 24px; align-items: center; text-align: center;">
    <p style="{EYEBROW} color: #b9cfeb;">Free · every week</p>
    <h2 style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: clamp(40px, 5vw, 64px); line-height: 1.06;">Get the next issue <em>in your inbox.</em></h2>
    <p style="margin: 0; max-width: 540px; font-size: 18px; line-height: 1.6; color: #ffffffcc;">One AI or Canva workflow every week, explained step by step, with the prompts to copy.</p>
    <div style="width: 100%; max-width: 540px; display: flex; flex-direction: column; gap: 10px; align-items: center;">{signup_form('newsletter', 'Join for free', dark=True)}</div>
  </div>
</section>

{more_sec}'''
    return h + main + tail


def newsletter_page(posts, head, tail):
    h = set_meta(head, 'The Resource Room: Free Weekly AI Newsletter | She Talks Business',
                 'One AI or Canva workflow every week, explained step by step, with the prompts to copy and a free guide. Join 20,000+ creatives and small business owners.',
                 '/newsletter/')
    cards = '\n'.join(card(p) for p in posts) or (
        '<p style="margin: 0; font-size: 18px; color: #242424b3;">The first issue is on its way. Sign up above so you don\'t miss it.</p>')
    items = [
        ('01', 'One workflow, step by step', 'Every week I test one AI or Canva workflow and show you exactly how it works, from the first prompt to the finished result.'),
        ('02', 'Prompts to copy', 'No theory. The exact prompts I use, ready to paste into ChatGPT, Claude or your favourite image tool.'),
        ('03', 'Free guides', 'Cheat sheets, prompt packs and templates that go with the issue, free for readers.'),
    ]
    what = ''.join(f'''<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 24px; border-top: 1px solid #242424;">
        <p style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-style: italic; font-weight: 300; font-size: 28px; color: #7a715f;">{n}</p>
        <h3 style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: 28px; line-height: 1.15;">{t}</h3>
        <p style="margin: 0; font-size: 16px; line-height: 1.65; color: #242424b3;">{d}</p></div>''' for n, t, d in items)
    main = f'''<!-- HERO -->
<section style="background: #f7f4f0;">
  <div style="max-width: 1240px; margin: 0 auto; padding: 112px clamp(24px, 6vw, 96px) 120px; display: flex; flex-wrap: wrap; gap: 64px; align-items: center;">
    <div style="flex: 1 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 28px;">
      <p style="{EYEBROW}">Free weekly newsletter</p>
      <h1 style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: clamp(52px, 6.4vw, 92px); line-height: 1.02;">The Resource <em>Room.</em></h1>
      <p style="margin: 0; max-width: 560px; font-size: 19px; line-height: 1.6; color: #242424b3;">Every week I pick one AI or Canva workflow, test it, and explain it step by step. You get the exact prompts, the steps, and a free guide to keep.</p>
      <div style="display: flex; flex-direction: column; gap: 10px;">
        {signup_form('newsletter', 'Get the free newsletter', note=False)}
        <p class="nl-note">Join 20,000+ readers. Free, every week. Unsubscribe anytime. <a href="/privacy#top">Privacy</a></p>
      </div>
    </div>
    <div style="flex: 1 1 320px; min-width: 0;">
      <img src="/assets/8eb0cbd47f56aec7fed3af8e9f463b54.webp" alt="Lynn Noppen, founder of She Talks Business" style="width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 4px; display: block;">
    </div>
  </div>
</section>

<!-- WHAT -->
<section style="background: #ffffff;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 48px;">
    <h2 style="{H2}">What you <em>get.</em></h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 40px;">{what}</div>
  </div>
</section>

<!-- ISSUES -->
<section id="issues" style="background: #f7f4f0;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 48px;">
    <div style="display: flex; flex-direction: column; gap: 16px;">
      <p style="{EYEBROW}">Archive</p>
      <h2 style="{H2}">All <em>issues.</em></h2>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 40px;">
{cards}
    </div>
  </div>
</section>

'''
    return h + main + tail


def replace_between(t, start, end, new):
    a = t.index(start) + len(start)
    b = t.index(end)
    return t[:a] + new + t[b:]


def main():
    posts = load_posts()
    head, tail = shell()
    os.makedirs(os.path.join(SITE, 'newsletter'), exist_ok=True)
    # remove pages of issues that were unpublished or renamed
    keep = {p['slug'] + '.html' for p in posts} | {'index.html'}
    for f in glob.glob(os.path.join(SITE, 'newsletter', '*.html')):
        if os.path.basename(f) not in keep:
            os.remove(f)
    for p in posts:
        others = [o for o in posts if o is not p]
        open(os.path.join(SITE, 'newsletter', p['slug'] + '.html'), 'w', encoding='utf-8').write(post_page(p, head, tail, others))
    open(os.path.join(SITE, 'newsletter', 'index.html'), 'w', encoding='utf-8').write(newsletter_page(posts, head, tail))

    idx = os.path.join(SITE, 'index.html')
    t = open(idx, encoding='utf-8').read()
    latest = '\n'.join(card(p) for p in posts[:3]) or (
        '<p style="margin: 0; font-size: 18px; color: #242424b3;">The first issue is on its way. Sign up so you don\'t miss it.</p>')
    t = replace_between(t, '<!--LATEST:START-->', '<!--LATEST:END-->', latest)
    open(idx, 'w', encoding='utf-8').write(t)

    sm = os.path.join(SITE, 'sitemap.xml')
    s = open(sm).read()
    if '<!--POSTS:START-->' not in s:
        s = s.replace('</urlset>', '  <!--POSTS:START--><!--POSTS:END-->\n</urlset>')
    urls = ''.join(f'\n  <url><loc>{DOMAIN}/newsletter/{p["slug"]}</loc><lastmod>{p["date"]}</lastmod><priority>0.7</priority></url>' for p in posts)
    if f'{DOMAIN}/newsletter/<' not in s:
        urls = f'\n  <url><loc>{DOMAIN}/newsletter/</loc><lastmod>{datetime.date.today()}</lastmod><priority>0.9</priority></url>' + urls
    s = replace_between(s, '<!--POSTS:START-->', '<!--POSTS:END-->', urls + '\n  ')
    open(sm, 'w').write(s)
    print(f'built {len(posts)} issue(s)')


if __name__ == '__main__':
    main()
