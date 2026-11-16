"""One-time rewrite of the site for the AI-educator positioning. Run once from the repo root."""
import re, glob, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from components import signup_form, prompt_card, EYEBROW, H2, WRAP

SITE = 'site'
STYLES = open('partials/site-styles.html').read()
SCRIPT = open('partials/signup-script.html').read()


def sub1(t, old, new, label):
    if old not in t:
        raise SystemExit(f'missing: {label}')
    return t.replace(old, new, 1)


def section(t, name):
    a = t.index(f'<!-- {name} -->')
    b = t.index('<!-- ', a + 5)
    return a, b

# ---------------------------------------------------------------- all pages
for f in glob.glob(f'{SITE}/*.html'):
    t = open(f).read()
    # absolute asset paths so pages under /newsletter/ work too
    t = re.sub(r'(src|href)="assets/', r'\1="/assets/', t)
    t = t.replace('url("assets/', 'url("/assets/')
    # shared styles + signup script
    if 'id="stb-shared"' not in t:
        t = t.replace('</head>', STYLES + '\n</head>', 1)
    if 'id="stb-signup"' not in t:
        t = t.replace('</body>', SCRIPT + '\n</body>', 1)
    # nav: Newsletter link + newsletter button instead of Templates
    t = re.sub(r'(<a class="navlink" href="/about#top"[^>]*>About</a>)',
               r'\1\n      <a class="navlink" href="/newsletter/#top" style="color: #242424;">Newsletter</a>', t, count=1)
    t = re.sub(r'<a class="btn-dark" href="/for-designers#top"( style="[^"]*")>Templates</a>',
               r'<a class="btn-dark" href="/newsletter/#top"\1>Free newsletter</a>', t, count=1)
    # footer
    t = t.replace('Canva design, implementation and education for brands and business owners around the globe. Based in the Netherlands.',
                  'AI and Canva, made simple. Free prompts, guides and a weekly newsletter for creatives and small business owners, plus training and design for teams. Based in the Netherlands.')
    t = t.replace('<a href="/about#top">About</a><a href="/work-with-me#top">',
                  '<a href="/about#top">About</a><a href="/newsletter/#top">Newsletter</a><a href="/work-with-me#top">', 1)
    t = t.replace('<a href="https://she-talks-business.myflodesk.com/freetemplates">The Resource Room</a>',
                  '<a href="/newsletter/#top">The Resource Room</a>')
    open(f, 'w').write(t)

# ---------------------------------------------------------------- homepage
p = f'{SITE}/index.html'
t = open(p).read()

hero_old = t[t.index('<p style="margin: 0; font-size: 13px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase;">Canva educator'):
             t.index('<div style="flex: 1 1 380px; min-width: 0; position: relative;">')]
hero_new = f'''<p style="{EYEBROW}">AI educator · Official Canva Creator</p>
      <h1 style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: clamp(52px, 6.4vw, 92px); line-height: 1.02; letter-spacing: -0.01em;">AI, made<br><em>simple.</em></h1>
      <p style="margin: 0; max-width: 540px; font-size: 19px; line-height: 1.6; color: #242424b3;">Free prompts, step-by-step guides and a weekly newsletter for creatives and small business owners. I show you exactly how I use AI and Canva to create more, in less time.</p>
      <div style="display: flex; flex-direction: column; gap: 10px; padding-top: 4px;">
        {signup_form('newsletter', 'Get the free newsletter', note=False)}
        <p class="nl-note">Join 20,000+ readers. Free, every week. Unsubscribe anytime.</p>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 8px 24px; padding-top: 24px; border-top: 1px solid #24242426; font-size: 14px; color: #242424b3;">
        <span>Official Canva Creator</span>
        <span aria-hidden="true">·</span>
        <span>200K+ creative community</span>
        <span aria-hidden="true">·</span>
        <a href="/newsletter/#issues" style="color: inherit;">Read the latest issues →</a>
      </div>
    </div>
    '''
t = sub1(t, hero_old, hero_new, 'hero')

t = t.replace('Canva creatives in my social community', 'Creatives in my social community')
t = t.replace('Readers of my weekly newsletter', 'Readers of my weekly newsletter')
t = t.replace('Designing, building and teaching in Canva', 'Teaching creatives to work smarter')
t = t.replace('Business owners worldwide working faster', 'People trained around the globe')

PROMPTS = [
    ('prompt-week', 'Turn one idea into a week of posts', 'Content',
     "You are my content strategist. My business: [what you do and who you help].\n\n"
     "Turn this one idea into 5 social media posts for the coming week: [your idea].\n\n"
     "For each post, give me a hook of max 10 words, 3 short lines of body text and one call to action. "
     "Write in a warm, simple tone. No hashtags, no emojis."),
    ('prompt-image', 'Write an on-brand AI image prompt', 'Visuals',
     "Write one image prompt for [your AI image tool] in this exact order:\n"
     "subject, how the objects relate in space, the role of my reference image, materials and textures, "
     "colours ([your brand colours]), setting, lighting, camera and lens, mood, and what to avoid.\n\n"
     "What I want to show: [describe your product or scene]."),
    ('prompt-voice', 'Make AI sound like you', 'Writing',
     "Here are 3 posts or emails I wrote myself:\n[paste them]\n\n"
     "First, describe my writing style in 5 short bullet points. "
     "Then rewrite the draft below in that style, in under 120 words:\n[paste your draft]"),
]
cards = '\n      '.join(prompt_card(*x) for x in PROMPTS)
prompts_sec = f'''<!-- PROMPTS -->
<section id="prompts" aria-label="Try a prompt" style="background: #f7f4f0;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    <div style="display: flex; flex-wrap: wrap; gap: 24px 64px; align-items: flex-end; justify-content: space-between;">
      <div style="display: flex; flex-direction: column; gap: 16px; max-width: 640px;">
        <p style="{EYEBROW}">Free prompts</p>
        <h2 style="{H2}">Try a prompt. <em>See what happens.</em></h2>
      </div>
      <p style="margin: 0; max-width: 420px; font-size: 17px; line-height: 1.6; color: #242424b3;">Copy one, paste it into ChatGPT or Claude, and fill in the brackets. New prompts land in your inbox every week.</p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
      {cards}
    </div>
  </div>
</section>

<!-- LATEST -->
<section id="latest" aria-label="Latest issues" style="background: #ffffff;">
  <div style="{WRAP} display: flex; flex-direction: column; gap: 56px;">
    <div style="display: flex; flex-wrap: wrap; gap: 24px 64px; align-items: flex-end; justify-content: space-between;">
      <div style="display: flex; flex-direction: column; gap: 16px; max-width: 640px;">
        <p style="{EYEBROW}">The Resource Room</p>
        <h2 style="{H2}">Read the <em>latest issues.</em></h2>
      </div>
      <a class="btn-line" href="/newsletter/#issues" style="border: 1px solid #242424; color: #242424; text-decoration: none; padding: 17px 29px; border-radius: 2px; font-size: 13px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase;">See all issues</a>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 40px;">
<!--LATEST:START--><!--LATEST:END-->
    </div>
  </div>
</section>

'''
a, _ = section(t, 'BRANDS')
b = t.index('<!-- IMAGE BREAK -->')
# place prompts + latest right after the brands strip (before the image band)
t = t[:b] + prompts_sec + t[b:]

# pillars reframed for teams
a, b = section(t, 'PILLARS')
pil = t[a:b]
pil2 = pil
for old, new in [
    ('How I can help', 'For teams &amp; brands'),
    ('Design it. Implement it. <em>Teach it.</em>', 'Bring AI and Canva <em>into your team.</em>'),
    ('Three ways to work together: pick one, or combine them for a Canva setup your whole team will actually use.',
     'Three ways to work together: training, design and implementation, so your whole team creates on-brand work faster with AI and Canva.'),
    ('Live and online masterclasses, keynotes and workshops that make Canva click, for teams, events and communities.',
     'Live and online masterclasses, keynotes and workshops that make AI and Canva click, for teams, events and communities.'),
    ('Masterclasses: online &amp; live', 'AI &amp; Canva masterclasses'),
    ('Custom Canva templates that match your brand and save your team hours. Done once, used forever. Pair it with training to get the most out of it.',
     'Custom Canva templates and AI visuals that match your brand and save your team hours. Done once, used forever.'),
    ('I set up your brand inside Canva and build a workflow your team can follow, so every design stays on-brand without the back-and-forth.',
     'I set up your brand in Canva and build AI workflows your team can follow, so every design stays on-brand without the back-and-forth.'),
]:
    if old in pil2:
        pil2 = pil2.replace(old, new)
    else:
        print('pillars: not found ->', old[:60])
t = t[:a] + pil2 + t[b:]

# drop the B2B industries block from the homepage
a, b = section(t, 'INDUSTRIES')
t = t[:a] + t[b:]

# final newsletter block with a real form
a, b = section(t, 'NEWSLETTER')
nl = f'''<!-- NEWSLETTER -->
<section id="newsletter" style="background: #b9cfeb;">
  <div style="{WRAP} display: flex; flex-wrap: wrap; gap: 48px 80px; align-items: center;">
    <div style="flex: 1 1 460px; display: flex; flex-direction: column; gap: 18px;">
      <p style="{EYEBROW}">Free · every week</p>
      <h2 style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: clamp(44px, 5vw, 68px); line-height: 1.04;">The Resource Room</h2>
      <p style="margin: 0; max-width: 480px; font-size: 18px; line-height: 1.6;">One AI or Canva workflow every week, explained step by step, with the prompts to copy. Join 20,000+ creatives and small business owners.</p>
    </div>
    <div style="flex: 1 1 420px; display: flex; flex-direction: column; gap: 12px;">
      {signup_form('newsletter', 'Join for free')}
    </div>
  </div>
</section>

'''
t = t[:a] + nl + t[b:]

# SEO
T = 'AI Made Simple for Creatives &amp; Small Businesses | She Talks Business'
D = 'Free AI prompts, step-by-step guides and a weekly newsletter from Lynn Noppen, Official Canva Creator. Learn to use AI and Canva to create more in less time.'
t = re.sub(r'<title>.*?</title>', f'<title>{T}</title>', t, count=1)
t = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + D, t, count=1)
t = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + D, t, count=1)
t = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + T, t, count=1)
open(p, 'w').write(t)

# ---------------------------------------------------------------- about
p = f'{SITE}/about.html'
t = open(p).read()
for old, new in [
    ("Canva educator, designer and implementation partner, and the founder of She Talks Business. For the past ten years I've helped brands, teams and business owners make Canva their fastest, most reliable design tool.",
     "AI educator, Official Canva Creator and the founder of She Talks Business. I help creatives, small business owners and teams use AI and Canva to create more, in less time, without the overwhelm."),
    ('design should save you time, not take it.', 'tech should save you time, not take it.'),
    ('From government comms to <em>global Canva expert.</em>', 'From government comms to <em>AI &amp; Canva educator.</em>'),
    ('Along the way I became a Canva Verified Expert, an official Canva Creator, and partnered with brands like Canva and Adobe. Today I design custom templates, implement Canva for teams (from Dutch municipalities to international brands), and host masterclasses for audiences around the globe.',
     'Along the way I became a Canva Verified Expert, an official Canva Creator, and partnered with brands like Canva and Adobe. When AI tools arrived, I did what I always do: tested everything, kept what actually saves time, and started teaching it in plain language. Today I share AI workflows, prompts and guides every week, train teams, and design for brands from Dutch municipalities to international companies.'),
    ("Let's make Canva <em>work for you.</em>", "Let's make AI <em>work for you.</em>"),
]:
    if old in t: t = t.replace(old, new)
    else: print('about: not found ->', old[:60])
t = t.replace('<a href="/work-with-me#top" style="background: #ffffff; color: #242424;', '<a href="/newsletter/#top" style="background: #ffffff; color: #242424;', 1)
t = t.replace('>See how I can help</a>', '>Get the free newsletter</a>', 1)
D = 'Meet Lynn Noppen: AI educator and Official Canva Creator with a 200K+ creative community, teaching creatives, small business owners and teams to work smarter with AI and Canva.'
t = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + D, t, count=1)
t = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + D, t, count=1)
t = re.sub(r'<title>.*?</title>', '<title>About Lynn Noppen, AI Educator &amp; Canva Creator | She Talks Business</title>', t, count=1)
open(p, 'w').write(t)

# ---------------------------------------------------------------- work with me
p = f'{SITE}/work-with-me.html'
t = open(p).read()
for old, new in [
    ('Three ways to make Canva <em>work harder for you.</em>', 'Bring AI and Canva <em>into your team.</em>'),
    ("Whether you're a solo business owner, a Canva designer or an organisation with a whole team to onboard, there's a way to work together that fits.",
     "Training, design and implementation for teams, events and communities, so everyone creates on-brand work faster with AI and Canva."),
    ('Live demos, real coaching, zero boring theory. I make Canva click for your team, community or clients, with tips they\'ll use the same day.',
     'Live demos, real coaching, zero boring theory. I make AI and Canva click for your team, community or clients, with workflows they\'ll use the same day.'),
    ('Online or live, keynote or hands-on workshop. Every session is tailored to your audience, from complete beginners to seasoned marketers.',
     'AI for content and visuals, Canva for teams, or both. Online or live, keynote or hands-on workshop, tailored to your audience, from complete beginners to seasoned marketers.'),
    ('Canva for teams, set up properly. I bring your brand into Canva and build a workflow everyone can follow, so your comms team, your colleagues and your partners create on-brand work without the back-and-forth.',
     'AI and Canva for teams, set up properly. I bring your brand into Canva, add the AI workflows that make sense, and build a process everyone can follow, so your team creates on-brand work without the back-and-forth.'),
    ('We talk through your team, your brand and where Canva is slowing you down.', 'We talk through your team, your brand and where content is slowing you down.'),
]:
    if old in t: t = t.replace(old, new)
    else: print('wwm: not found ->', old[:60])
D = 'AI and Canva training, custom design and implementation for teams, events and communities. Masterclasses, keynotes and team setups by Lynn Noppen.'
t = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + D, t, count=1)
t = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + D, t, count=1)
t = re.sub(r'<title>.*?</title>', '<title>AI &amp; Canva Training, Design and Implementation | She Talks Business</title>', t, count=1)
open(p, 'w').write(t)

# ---------------------------------------------------------------- contact
p = f'{SITE}/contact.html'
t = open(p).read()
t = t.replace('>Canva for my team</label>', '>AI or Canva for my team</label>')
t = t.replace('ready to get your whole team working smarter in Canva?', 'ready to get your whole team working smarter with AI and Canva?')
t = t.replace("Let's talk <em>Canva.</em>", "Let's <em>talk.</em>")
t = t.replace('Join The Resource Room: weekly Canva hacks and templates, for free.', 'Join The Resource Room: one AI or Canva workflow every week, with the prompts to copy. Free.')
t = t.replace('href="https://she-talks-business.myflodesk.com/freetemplates" style="background: #242424', 'href="/newsletter/#top" style="background: #242424')
open(p, 'w').write(t)

# ---------------------------------------------------------------- privacy: newsletter now signs up on this site
p = f'{SITE}/privacy.html'
t = open(p).read()
old = 'If you sign up for my newsletter, you do so on a sign-up page hosted by Flodesk.'
new = 'If you sign up for my newsletter on this website, your email address is sent securely to Flodesk, my email provider.'
if old in t: t = t.replace(old, new)
else: print('privacy: not found')
open(p, 'w').write(t)

# any remaining direct Flodesk links on pages -> on-site newsletter page
for f in glob.glob(f'{SITE}/*.html'):
    t = open(f).read()
    t2 = re.sub(r'href="https://she-talks-business\.myflodesk\.com/freetemplates"(?![^<]*nl-form)', 'href="/newsletter/#top"', t)
    open(f, 'w').write(t2)
print('restructure done')
