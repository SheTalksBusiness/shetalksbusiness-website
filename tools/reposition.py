"""One-time rewrite (Nov 2026): reposition the site around AI systems for marketing & sales.
Run once from the repo root: python3 tools/reposition.py
"""
import os, re, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from components import signup_form, prompt_card, EYEBROW, H2, WRAP

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site')
SERIF = "font-family: 'Editors Note', Georgia, serif; font-weight: 300;"
MUTED = 'color: #242424b3;'
BTN_DARK = 'background: #242424; color: #ffffff; text-decoration: none; padding: 18px 30px; border-radius: 2px; font-size: 13px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase;'
BTN_LINE = 'border: 1px solid #242424; color: #242424; text-decoration: none; padding: 17px 29px; border-radius: 2px; font-size: 13px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase;'
CARD = 'background: #ffffff; border-radius: 4px; box-shadow: 0 1px 2px #24242414, 0 8px 24px -12px #24242414;'


def rd(f): return open(os.path.join(SITE, f), encoding='utf-8').read()
def wr(f, t): open(os.path.join(SITE, f), 'w', encoding='utf-8').write(t)


def section(t, name):
    """Return the text of <!-- NAME --> up to the next section marker."""
    a = t.index(f'<!-- {name} -->')
    m = re.search(r'\n<!-- [A-Z &/-]+ -->', t[a + 5:])
    return t[a:a + 5 + m.start() + 1]


def replace_main(t, new):
    a = t.index('<!-- HERO -->') if '<!-- HERO -->' in t else t.index('<!-- CONTACT -->')
    b = t.index('<!-- FOOTER -->')
    return t[:a] + new + '\n' + t[b:]


def set_seo(t, title, desc):
    t = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', t, count=1)
    for p in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        t = re.sub(r'(<meta ' + p + r' content=")[^"]*', lambda m: m.group(1) + desc, t)
    for p in ('property="og:title"', 'name="twitter:title"'):
        t = re.sub(r'(<meta ' + p + r' content=")[^"]*', lambda m: m.group(1) + title, t)
    return t


# ---------------------------------------------------------------- shared content
LEAKS = [
    ('They can\'t find you', 'An outdated website, or none at all. People search, see a competitor that looks better, and book there.',
     'A website that sells', 'A fast, beautiful website built to turn visitors into bookings, with your reviews and work front and centre.'),
    ('They can\'t book', 'Booking means a DM, an email and three messages back and forth. Half of them give up.',
     'Booking around the clock', 'Online booking and an AI assistant that answers questions and books appointments, even at 11pm.'),
    ('You miss the call', 'You\'re with a client, on site or in the chair. The phone rings, and that customer calls the next business on the list.',
     'Missed-call text-back', 'Every missed call gets a friendly text within a minute, so the conversation keeps going until you\'re free.'),
    ('Leads go cold', 'Someone asks for a quote, you\'re busy, and by the time you follow up they\'ve moved on.',
     'Automatic follow-up', 'Quotes, enquiries and no-shows get a personal follow-up at the right moment, without you remembering to send it.'),
    ('Happy clients stay silent', 'Your clients love you, but you forget to ask for a review. New customers only see a handful.',
     'Review requests on autopilot', 'After every appointment, clients get a request to leave a Google review. Happy ones go public, unhappy ones come to you first.'),
    ('No time for marketing', 'Posting, newsletters and offers always come last, so your calendar has quiet weeks.',
     'Marketing that runs itself', 'Content, reminders and win-back messages to past clients, drafted by AI in your brand voice and sent on schedule.'),
]

INDUSTRIES = [
    ('Beauty, hair &amp; skin', 'Salons, clinics and studios: fewer no-shows, fuller books, more reviews.'),
    ('Interior design', 'Turn enquiries into consultations and keep every project lead warm.'),
    ('Real estate', 'Answer every viewing request fast and follow up with every lead.'),
    ('Home services &amp; construction', 'Never lose a job to a missed call while you\'re on site.'),
    ('Hospitality', 'Bookings, guest messages and reviews that keep tables and rooms full.'),
]

STEPS = [
    ('1', 'Leak check', 'We talk through how customers find you, contact you and book. I show you exactly where they slip away.'),
    ('2', 'Build', 'I design and build the systems, connected to the tools you already use: your calendar, phone, website and Google profile.'),
    ('3', 'Launch', 'We test everything together, I show you how it works, and it goes live. No tech skills needed on your side.'),
    ('4', 'Run &amp; improve', 'I monitor the systems every month, fix what needs fixing and improve what\'s working.'),
]


def leak_rows():
    rows = []
    for i, (leak, why, fix, how) in enumerate(LEAKS, 1):
        rows.append(f'''<div class="leak-row">
        <div class="leak-q"><span class="leak-n">{i:02d}</span><h3>{leak}</h3><p>{why}</p></div>
        <div class="leak-a"><span class="leak-tag">The fix</span><h3>{fix}</h3><p>{how}</p></div>
      </div>''')
    return '\n      '.join(rows)


LEAK_CSS = '''<style id="stb-leaks">
.leak-list{display:flex;flex-direction:column;border-top:1px solid #24242433}
.leak-row{display:grid;grid-template-columns:1fr 1fr;gap:24px 64px;padding:36px 0;border-bottom:1px solid #24242433}
.leak-row h3{margin:0;font-family:'Editors Note',Georgia,serif;font-weight:300;font-size:30px;line-height:1.15}
.leak-row p{margin:0;font-size:16px;line-height:1.65;color:#242424b3}
.leak-q,.leak-a{display:flex;flex-direction:column;gap:12px}
.leak-n{font-family:'Editors Note',Georgia,serif;font-style:italic;font-weight:300;font-size:22px;color:#7a715f}
.leak-tag{align-self:flex-start;font-size:11px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;background:#b9cfeb;color:#242424;padding:6px 10px;border-radius:2px}
.leak-a{padding-left:32px;border-left:1px solid #24242426}
@media (max-width:760px){.leak-row{grid-template-columns:1fr}.leak-a{padding-left:0;border-left:0;padding-top:20px;border-top:1px dashed #24242433}}
</style>'''


def industries_grid(dark=False):
    items = ''.join(f'''<div style="display: flex; flex-direction: column; gap: 10px; padding-top: 22px; border-top: 1px solid {'#ffffff40' if dark else '#242424'};">
        <h3 style="margin: 0; {SERIF} font-size: 28px; line-height: 1.15;">{n}</h3>
        <p style="margin: 0; font-size: 15px; line-height: 1.6; color: {'#ffffffb3' if dark else '#242424b3'};">{d}</p></div>''' for n, d in INDUSTRIES)
    return f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 40px 32px;">{items}</div>'


def steps_list():
    items = ''.join(f'''<li style="{CARD} padding: 32px; display: flex; flex-direction: column; gap: 14px;">
        <span style="{SERIF} font-size: 44px; line-height: 1;">{n}</span>
        <strong style="font-weight: 500; font-size: 18px;">{h}</strong>
        <span style="font-size: 15px; line-height: 1.6; {MUTED}">{d}</span></li>''' for n, h, d in STEPS)
    return f'<ol style="margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 24px;">{items}</ol>'


def head_block(eyebrow, h2, side=None, side_html=''):
    side_p = f'<p style="margin: 0; flex: 1 1 360px; max-width: 440px; font-size: 17px; line-height: 1.6; {MUTED}">{side}</p>' if side else side_html
    return f'''<div style="display: flex; flex-wrap: wrap; gap: 24px 64px; align-items: flex-end; justify-content: space-between;">
      <div style="display: flex; flex-direction: column; gap: 16px; flex: 1 1 520px; max-width: 700px;">
        <p style="{EYEBROW}">{eyebrow}</p>
        <h2 style="{H2}">{h2}</h2>
      </div>
      {side_p}
    </div>'''


def cta_dark(h2, p, primary=('Tell me about your business', '/contact#top'), secondary=('Get the free newsletter', '/newsletter/#top')):
    return f'''<!-- CTA -->
<section style="background: #242424; color: #ffffff;">
  <div style="max-width: 900px; margin: 0 auto; padding: 112px clamp(24px, 6vw, 96px); display: flex; flex-direction: column; gap: 28px; align-items: center; text-align: center;">
    <h2 style="margin: 0; {SERIF} font-size: clamp(40px, 5vw, 64px); line-height: 1.06;">{h2}</h2>
    <p style="margin: 0; max-width: 560px; font-size: 18px; line-height: 1.6; color: #ffffffcc;">{p}</p>
    <div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;">
      <a href="{primary[1]}" style="background: #ffffff; color: #242424; text-decoration: none; padding: 18px 30px; border-radius: 2px; font-size: 13px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase;">{primary[0]}</a>
      <a href="{secondary[1]}" style="border: 1px solid #ffffff; color: #ffffff; text-decoration: none; padding: 17px 29px; border-radius: 2px; font-size: 13px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase;">{secondary[0]}</a>
    </div>
  </div>
</section>
'''


NEWSLETTER_COPY = 'Every week I break down one AI system for marketing and sales: what it does, the tools, the prompts and the exact steps. Learn it yourself, or hand it to me.'


def newsletter_block():
    return f'''<!-- NEWSLETTER -->
<section id="newsletter" style="background: #b9cfeb;">
  <div style="max-width: 1240px; margin: 0 auto; padding: 112px clamp(24px, 6vw, 96px); display: flex; flex-wrap: wrap; gap: 48px 80px; align-items: center;">
    <div style="flex: 1 1 460px; display: flex; flex-direction: column; gap: 18px;">
      <p style="{EYEBROW}">Free · every week</p>
      <h2 style="margin: 0; {SERIF} font-size: clamp(44px, 5vw, 68px); line-height: 1.04;">The Resource Room</h2>
      <p style="margin: 0; max-width: 480px; font-size: 18px; line-height: 1.6;">{NEWSLETTER_COPY} Join 20,000+ readers.</p>
    </div>
    <div style="flex: 1 1 420px; display: flex; flex-direction: column; gap: 12px;">
      {signup_form('newsletter', 'Join for free')}
    </div>
  </div>
</section>
'''


# ---------------------------------------------------------------- homepage
def home():
    t = rd('index.html')
    brands = section(t, 'BRANDS')
    latest = section(t, 'LATEST')
    testimonial = section(t, 'TESTIMONIAL')
    latest = latest.replace('Read the <em>latest issues.</em>', 'Learn the systems <em>I build.</em>')
    latest = latest.replace('<p style="margin: 0; font-size: 13px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase;">The Resource Room</p>',
                            '<p style="margin: 0; font-size: 13px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase;">The Resource Room · free newsletter</p>')
    # keep the Adobe quote + three short ones
    figs = re.findall(r'<figure style="margin: 0; background: #ffffff;.*?</figure>', testimonial, re.S)
    keep = [f for f in figs if 'beehiiv' in f.lower() or 'Event organiser' in f or 'Sherry' in f]
    grid_start = testimonial.index('<div style="display: grid;')
    grid_end = testimonial.rindex('</div>\n  </div>\n</section>')
    testimonial = testimonial[:grid_start] + '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">\n      ' + '\n      '.join(keep) + '\n    ' + testimonial[grid_end:]

    hero = f'''<!-- HERO -->
<section style="background: #f7f4f0;">
  <div style="max-width: 1240px; margin: 0 auto; padding: 96px clamp(24px, 6vw, 96px) 112px; display: flex; flex-wrap: wrap; gap: 64px; align-items: center;">
    <div style="flex: 1 1 520px; min-width: 0; display: flex; flex-direction: column; gap: 28px;">
      <p style="{EYEBROW}">AI systems for marketing &amp; sales</p>
      <h1 style="margin: 0; {SERIF} font-size: clamp(50px, 6.2vw, 88px); line-height: 1.02; letter-spacing: -0.01em;">More clients.<br><em>Less chasing.</em></h1>
      <p style="margin: 0; max-width: 560px; font-size: 19px; line-height: 1.6; {MUTED}">I find where your business is leaking customers, and fix it with AI. Websites that book, missed calls that get answered, follow-ups that send themselves and reviews that keep coming in. Built for service businesses and luxury brands.</p>
      <div style="display: flex; flex-wrap: wrap; gap: 12px; padding-top: 4px;">
        <a class="btn-dark" href="/contact#top" style="{BTN_DARK}">Find my leaks</a>
        <a class="btn-line" href="/work-with-me#solutions" style="{BTN_LINE}">What I automate</a>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 8px 24px; padding-top: 24px; border-top: 1px solid #24242426; font-size: 14px; {MUTED}">
        <span>Worked with Adobe, Canva &amp; beehiiv</span>
        <span aria-hidden="true">·</span>
        <span>20,000+ newsletter readers</span>
        <span aria-hidden="true">·</span>
        <span>Based in the Netherlands, working globally</span>
      </div>
    </div>
    <div style="flex: 1 1 380px; min-width: 0; position: relative;">
      <img src="/assets/8eb0cbd47f56aec7fed3af8e9f463b54.webp" alt="Lynn Noppen, AI implementation specialist and founder of She Talks Business" style="width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 4px; display: block;">
      <p style="margin: 0; position: absolute; left: -28px; bottom: 36px; background: #ffffff; padding: 14px 22px; border-radius: 4px; box-shadow: 0 4px 12px -4px #24242414, 0 16px 40px -16px #24242414; font-family: 'Editors Hand', cursive; font-size: 30px; line-height: 1;">hey, I'm Lynn!</p>
    </div>
  </div>
</section>
'''
    leaks = f'''<!-- LEAKS -->
<section id="leaks" style="background: #ffffff;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    {head_block('Where you lose customers', 'Where is your business <em>leaking customers?</em>', 'Most small businesses don\'t need more followers. They need to stop losing the people who already wanted to buy. These are the six leaks I see most, and how I fix each one.')}
    <div class="leak-list">
      {leak_rows()}
    </div>
    <a class="btn-dark" href="/contact#top" style="align-self: flex-start; {BTN_DARK}">Tell me where it hurts</a>
  </div>
</section>
'''
    how = f'''<!-- HOW -->
<section style="background: #e5ddd2;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    {head_block('How it works', 'Done for you, <em>start to finish.</em>', 'You don\'t need to learn a single tool. I build the systems around the way you already work, and keep them running.')}
    {steps_list()}
  </div>
</section>
'''
    who = f'''<!-- INDUSTRIES -->
<section style="background: #242424; color: #ffffff;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    <div style="display: flex; flex-wrap: wrap; gap: 24px 64px; align-items: flex-end; justify-content: space-between;">
      <div style="display: flex; flex-direction: column; gap: 16px; flex: 1 1 520px; max-width: 700px;">
        <p style="{EYEBROW} color: #b9cfeb;">Who I work with</p>
        <h2 style="{H2}">For businesses where <em>every client counts.</em></h2>
      </div>
      <p style="margin: 0; flex: 1 1 360px; max-width: 440px; font-size: 17px; line-height: 1.6; color: #ffffffb3;">Premium service businesses and luxury brands, where one extra client a week makes a real difference, and where the experience has to feel as good as your work.</p>
    </div>
    {industries_grid(dark=True)}
  </div>
</section>
'''
    prompts = f'''<!-- PROMPTS -->
<section id="prompts" aria-label="Try a prompt" style="background: #f7f4f0;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    {head_block('Free prompts', 'Try it yourself. <em>See what AI can do.</em>', 'Copy a prompt, paste it into ChatGPT or Claude and fill in the brackets. New prompts land in the newsletter every week.')}
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
      {prompt_card('pr1', 'Find your customer leaks', 'Strategy', "You are a customer journey consultant for small service businesses. My business: [what you do, where, for whom]. This is how customers find me, contact me and book today: [describe every step]. List the 5 places where I'm most likely losing customers, why, and one simple fix for each. Start with the fix that would bring in the most clients this month.")}
      {prompt_card('pr2', 'Reply to a Google review', 'Reviews', "Write a reply to this Google review for my business [business name, type]. Review: [paste review]. Keep it under 60 words, warm and personal, mention one detail from the review, thank them by first name and invite them back. If the review is negative, apologise once, don't argue, and offer to continue the conversation by phone or email.")}
      {prompt_card('pr3', 'Write a missed-call text', 'Follow-up', "Write 3 versions of a text message my business sends automatically when I miss a call. Business: [name, what you do]. Tone: [e.g. warm and luxurious]. Each message under 300 characters, says I'm with a client right now, asks how I can help, and gives a link to book: [booking link]. No emojis.")}
    </div>
  </div>
</section>
'''
    about = f'''<!-- MEET -->
<section style="background: #ffffff;">
  <div style="{WRAP} display: flex; flex-wrap: wrap; gap: 56px 80px; align-items: center;">
    <div style="flex: 1 1 380px; min-width: 0;">
      <img loading="lazy" decoding="async" src="/assets/467fd1bc8b4af5589031648a0444ba0f.webp" alt="Lynn Noppen at work" style="width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 4px; display: block;">
    </div>
    <div style="flex: 1 1 480px; min-width: 0; display: flex; flex-direction: column; gap: 22px;">
      <p style="{EYEBROW}">Meet Lynn</p>
      <h2 style="{H2}">Marketing know-how, <em>built into AI.</em></h2>
      <p style="margin: 0; font-size: 18px; line-height: 1.7; color: #242424cc;">I've spent over ten years in marketing and communications: from government comms to building an online business with 200,000+ followers and 20,000 newsletter readers, and creating campaigns for brands like Adobe and Canva.</p>
      <p style="margin: 0; font-size: 18px; line-height: 1.7; color: #242424cc;">Now I put that experience into AI systems for small businesses. Not tech for the sake of tech, but simple automations that bring in clients and give you your evenings back. I run my own business on limited hours as a mum of two, so I know exactly how much time this saves.</p>
      <a class="btn-line" href="/about#top" style="align-self: flex-start; margin-top: 8px; {BTN_LINE}">More about me</a>
    </div>
  </div>
</section>
'''
    main = (hero + '\n' + brands + '\n' + leaks + '\n' + how + '\n' + who + '\n' + about + '\n' + testimonial + '\n' + latest + '\n' + prompts + '\n'
            + newsletter_block() + '\n' + cta_dark("Let's find <em>your leaks.</em>", 'Tell me a little about your business and how clients reach you now. I\'ll reply within 24 hours with where I\'d start.'))
    t = replace_main(t, main)
    t = set_seo(t, 'AI Systems That Bring You More Clients | She Talks Business',
                'Lynn Noppen builds AI systems for service businesses and luxury brands: websites that book, missed-call text-back, automatic follow-up and review requests. Stop losing customers.')
    if 'id="stb-leaks"' not in t:
        t = t.replace('</head>', LEAK_CSS + '\n</head>', 1)
    wr('index.html', t)


# ---------------------------------------------------------------- work with me -> services
def services():
    t = rd('work-with-me.html')
    sol_cards = ''.join(f'''<div style="{CARD} padding: 36px 32px; display: flex; flex-direction: column; gap: 14px;">
        <span style="{SERIF} font-style: italic; font-size: 22px; color: #7a715f;">{i:02d}</span>
        <h3 style="margin: 0; {SERIF} font-size: 32px; line-height: 1.12;">{fix}</h3>
        <p style="margin: 0; font-size: 16px; line-height: 1.6; {MUTED}">{how}</p>
        <p style="margin: auto 0 0; padding-top: 16px; border-top: 1px solid #24242426; font-size: 14px; line-height: 1.5;"><strong style="font-weight: 500;">Fixes:</strong> {leak.lower().replace("they ", "people ")}</p></div>'''
                        for i, (leak, why, fix, how) in enumerate(LEAKS, 1))
    faq_items = [
        ('What does it cost?', 'Every business leaks in different places, so I don\'t do one-size-fits-all packages. After a short call you get a clear proposal: a one-time setup fee to build your systems, and a small monthly fee for hosting, monitoring and improvements. No surprises.'),
        ('Do I need to be good with tech?', 'Not at all. I build everything, connect it to the tools you already use and show you how it works. Most clients only see the results: more bookings, more reviews, fewer missed leads.'),
        ('Will it still sound like me?', 'Yes. Every message, reply and post is written in your brand voice, and you approve the templates before anything goes live. For luxury brands especially, the tone matters as much as the timing.'),
        ('Which tools do you use?', 'It depends on what you already have. I work with your calendar, booking system, phone number, website and Google Business Profile, and add AI where it saves time. You never get locked into tools you don\'t need.'),
        ('How long does it take?', 'Most systems are live within one to three weeks, depending on how many leaks we fix and how quickly we can connect your accounts.'),
        ('Do you work outside the Netherlands?', 'Yes. I work with businesses in the Netherlands and internationally, in English and Dutch. Everything is set up online.'),
    ]
    faq = ''.join(f'''<details style="border-bottom: 1px solid #24242433; padding: 24px 0;">
        <summary style="display: flex; justify-content: space-between; gap: 24px; align-items: center; {SERIF} font-size: 26px;">{q}<span class="plus" aria-hidden="true" style="font-family: Avenir, sans-serif; font-size: 28px; line-height: 1;">+</span></summary>
        <p style="margin: 16px 0 0; font-size: 16px; line-height: 1.65; {MUTED}">{a}</p>
      </details>''' for q, a in faq_items)
    main = f'''<!-- HERO -->
<section style="background: #f7f4f0;">
  <div style="max-width: 1240px; margin: 0 auto; padding: 96px clamp(24px, 6vw, 96px) 112px; display: flex; flex-wrap: wrap; gap: 64px; align-items: center;">
    <div style="flex: 1 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 28px;">
      <p style="{EYEBROW}">Services</p>
      <h1 style="margin: 0; {SERIF} font-size: clamp(50px, 6.2vw, 88px); line-height: 1.02;">AI that brings in <em>clients.</em></h1>
      <p style="margin: 0; max-width: 560px; font-size: 19px; line-height: 1.6; {MUTED}">I build and run AI systems that fix the leaks in your marketing and sales: from the first search to the five-star review. You keep doing the work you love; the systems make sure no client slips through.</p>
      <div style="display: flex; flex-wrap: wrap; gap: 12px;">
        <a class="btn-dark" href="/contact#top" style="{BTN_DARK}">Tell me about your business</a>
        <a class="btn-line" href="#solutions" style="{BTN_LINE}">See the systems</a>
      </div>
    </div>
    <div style="flex: 1 1 360px; min-width: 0;">
      <img src="/assets/467fd1bc8b4af5589031648a0444ba0f.webp" alt="Lynn Noppen at work" style="width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 4px; display: block;">
    </div>
  </div>
</section>

<!-- SOLUTIONS -->
<section id="solutions" style="background: #ffffff;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    {head_block('The systems', 'Six ways I stop <em>the leaks.</em>', 'Start with the one that costs you the most clients, or combine them into one system that runs your whole customer journey.')}
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">{sol_cards}</div>
  </div>
</section>

<!-- INDUSTRIES -->
<section style="background: #e5ddd2;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    {head_block('Who I work with', 'Made for premium <em>service businesses.</em>', 'Especially luxury brands, where the experience before and after the appointment has to feel as good as the work itself.')}
    {industries_grid()}
  </div>
</section>

<!-- PROCESS -->
<section style="background: #ffffff;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    {head_block('How it works', 'From first call to <em>fully booked.</em>')}
    {steps_list()}
  </div>
</section>

<!-- TRAINING -->
<section style="background: #f7f4f0;">
  <div style="{WRAP} display: flex; flex-wrap: wrap; gap: 40px 80px; align-items: center;">
    <div style="flex: 1 1 480px; display: flex; flex-direction: column; gap: 18px;">
      <p style="{EYEBROW}">Also available</p>
      <h2 style="{H2}">AI training &amp; <em>speaking.</em></h2>
      <p style="margin: 0; max-width: 560px; font-size: 18px; line-height: 1.6; {MUTED}">Want your team to use AI for marketing themselves? I give hands-on workshops, masterclasses and keynotes on AI for marketing, content and design, online or on location. I still design and set up Canva for brands too.</p>
    </div>
    <a class="btn-line" href="/contact#top" style="{BTN_LINE}">Ask about training</a>
  </div>
</section>

<!-- FAQ -->
<section style="background: #ffffff;">
  <div style="max-width: 860px; margin: 0 auto; padding: 120px clamp(24px, 6vw, 96px); display: flex; flex-direction: column; gap: 40px;">
    <div style="display: flex; flex-direction: column; gap: 16px;">
      <p style="{EYEBROW}">Questions</p>
      <h2 style="margin: 0; {SERIF} font-size: clamp(36px, 4vw, 54px); line-height: 1.1;">Good to know</h2>
    </div>
    <div style="display: flex; flex-direction: column; border-top: 1px solid #24242433;">
      {faq}
    </div>
  </div>
</section>

''' + cta_dark("Let's find <em>your leaks.</em>", 'Tell me about your business and how clients reach you now. I\'ll reply within 24 hours with where I\'d start.', secondary=('See my work', '/portfolio#top'))
    t = replace_main(t, main)
    t = set_seo(t, 'AI Automation Services for Small Businesses | She Talks Business',
                'Websites that book, missed-call text-back, automatic follow-up, review requests and marketing automation for beauty, interior, real estate, home services and hospitality businesses.')
    wr('work-with-me.html', t)


# ---------------------------------------------------------------- about
def about():
    t = rd('about.html')
    rep = [
        ('AI educator, Official Canva Creator and the founder of She Talks Business. I help creatives, small business owners and teams use AI and Canva to create more, in less time, without the overwhelm.',
         'AI implementation specialist and the founder of She Talks Business. I build AI systems that help service businesses and luxury brands get more clients, by automating the marketing and sales work that slips through the cracks.'),
        ('tech should save you time, not take it.', 'more clients, less chasing.'),
        ('From government comms to <em>AI &amp; Canva educator.</em>', 'From government comms to <em>AI systems builder.</em>'),
        ('In 2018 I went all in on Canva. I started sharing tutorials and business tips online, and the community grew to more than 200,000 people on socials and 20,000 readers of my weekly newsletter.',
         'Then I started my own business. I taught myself design and online marketing, shared everything I learned, and built a community of more than 200,000 people on socials and 20,000 readers of my weekly newsletter.'),
    ]
    for a, b in rep:
        assert a in t, a[:40]
        t = t.replace(a, b)
    t = re.sub(r'<p style="margin: 0;">Along the way I became a Canva Verified Expert.*?</p>',
               '<p style="margin: 0;">Along the way I became an official Canva Creator and created campaigns for brands like Adobe and Canva. When AI arrived, I tested everything and used it to automate my own marketing. Then business owners started asking me to do the same for them: answer their leads, fill their calendars and collect their reviews. Today that\'s my main work: finding where a business is leaking customers, and fixing it with AI.</p>', t, flags=re.S)
    t = t.replace('Which is exactly why I care so much about workflows that save time.', 'Which is exactly why I build systems that run without you.')
    # credentials
    t = t.replace('>10 years in Canva<', '>10+ years in marketing<').replace('Designing, implementing and teaching since the early days.', 'Communications, content and online marketing, from government to global brands.')
    t = t.replace('>Former Canva Verified Expert<', '>200K+ community<').replace('Recognised by Canva for expert-level knowledge.', 'Followers learning AI, marketing and design from me every week.')
    # approach
    t = t.replace('Simple, practical, <em>and actually fun.</em>', 'Simple systems, <em>real results.</em>')
    t = t.replace('<h3 style="margin: 0; font-family: \'Editors Note\', Georgia, serif; font-weight: 300; font-size: 28px;">Practical over theory</h3>', '<h3 style="margin: 0; font-family: \'Editors Note\', Georgia, serif; font-weight: 300; font-size: 28px;">Results over tech</h3>')
    t = t.replace('Live demos and real examples from your own brand. Tips your team uses the same day, not slides they forget by Friday.', 'I only build what brings in clients or saves you hours. If a simple automation does the job, you won\'t get a complicated one.')
    t = t.replace('>Built for the whole team<', '>In your brand voice<')
    t = t.replace('Not just for designers. I set things up so anyone ( from comms to HR), can create on-brand work with confidence and ease.', 'Every message your customers get sounds like you. Warm, personal and on-brand, especially for luxury businesses.')
    t = t.replace('>Done once, used forever<', '>Built to keep running<')
    t = t.replace('Templates, Brand Kits and workflows designed to last, so you stop reinventing the wheel every week.', 'I monitor and improve your systems every month, so they keep working while you focus on your clients.')
    # CTA
    t = t.replace("Let's make AI <em>work for you.</em>", "Let's find <em>your leaks.</em>")
    t = t.replace("Whether you need templates, a team setup or a masterclass, I'd love to hear what you're working on.", 'Tell me about your business and how clients reach you now. I\'ll reply within 24 hours with where I\'d start.')
    t = t.replace('<a href="/newsletter/#top" style="background: #ffffff; color: #242424;', '<a href="/contact#top" style="background: #ffffff; color: #242424;', 1)
    t = t.replace('>Get the free newsletter</a>\n      <a href="/contact#top" style="border: 1px solid #ffffff;', '>Tell me about your business</a>\n      <a href="/newsletter/#top" style="border: 1px solid #ffffff;')
    t = t.replace('text-transform: uppercase;">Get in touch</a>', 'text-transform: uppercase;">Get the free newsletter</a>')
    t = set_seo(t, 'About Lynn Noppen, AI Implementation Specialist | She Talks Business',
                'Lynn Noppen builds AI systems that help service businesses and luxury brands get more clients. 10+ years in marketing, 200K+ community, campaigns for Adobe and Canva.')
    wr('about.html', t)


# ---------------------------------------------------------------- contact
def contact():
    t = rd('contact.html')
    t = t.replace("Planning a masterclass, need custom templates, or ready to get your whole team working smarter with AI and Canva? Tell me a bit about it and I'll get back to you within 24 hours.",
                  "Tell me about your business: what you do, how clients find and book you now, and where you feel you're losing them. I'll get back to you within 24 hours with where I'd start.")
    t = t.replace('placeholder="Company, municipality, community…"', 'placeholder="Business name and website"')
    t = t.replace('>Organisation <span', '>Business <span')
    old_topics = re.search(r'(<legend[^>]*>)I\'m interested in(</legend>\s*<div[^>]*>)(.*?)(</div>\s*</fieldset>)', t, re.S)
    lab = re.search(r'<label [^>]*><input type="checkbox" name="topic"[^>]*>', old_topics.group(3)).group(0)
    topics = ['A website that books', 'Online booking &amp; AI assistant', 'Missed-call text-back', 'Lead follow-up', 'Review requests', 'Marketing automation', 'AI training or speaking', 'Not sure yet']
    new = ''.join(f'\n          {lab}{x}</label>' for x in topics) + '\n        '
    t = t[:old_topics.start(3)] + new + t[old_topics.end(3):]
    t = t.replace('>I\'m interested in</legend>', '>What would help most?</legend>')
    t = t.replace('placeholder="What are you working on, how big is your team, and when would you like to start?"',
                  'placeholder="What kind of business do you run, how do clients book you now, and where do you think you\'re losing them?"')
    t = set_seo(t, "Contact | She Talks Business", "Tell Lynn about your business and where you're losing customers. She'll reply within 24 hours with where she'd start.")
    wr('contact.html', t)


# ---------------------------------------------------------------- every page: nav, footer
def global_changes():
    for f in glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True):
        t = open(f, encoding='utf-8').read()
        o = t
        # nav: Services first, For designers out, button to contact
        t = re.sub(r'\s*<a class="navlink" href="/for-designers#top"[^>]*>For designers</a>', '', t)
        t = re.sub(r'(<a class="navlink" href="/work-with-me#top"[^>]*>)Work with me(</a>)', r'\1Services\2', t)
        m = re.search(r'\s*<a class="navlink" href="/work-with-me#top"[^>]*>Services</a>', t)
        if m and '<a class="navlink" href="/about#top"' in t[:m.start()]:
            svc = m.group(0); t = t[:m.start()] + t[m.end():]
            t = re.sub(r'(<a class="navlink" href="/#top"[^>]*>Home</a>)', lambda mm: mm.group(1) + svc, t, count=1)
        t = re.sub(r'(<a class="btn-dark" href=")/newsletter/#top(" style="background: #242424; color: #ffffff; text-decoration: none; padding: 14px 22px;[^"]*">)Free newsletter</a>',
                   r'\1/contact#top\2Let’s talk</a>', t)
        t = t.replace('AI and Canva, made simple. Free prompts, guides and a weekly newsletter for creatives and small business owners, plus training and design for teams. Based in the Netherlands.',
                      'AI systems that bring service businesses and luxury brands more clients: websites, bookings, follow-up and reviews on autopilot. Plus a free weekly newsletter on AI for marketing. Based in the Netherlands, working globally.')
        t = re.sub(r'(<a [^>]*href="/work-with-me#top"[^>]*>)Work with me(</a>)', r'\1Services\2', t)
        if t != o:
            open(f, 'w', encoding='utf-8').write(t)


if __name__ == '__main__':
    home(); services(); about(); contact(); global_changes()
    print('done')
