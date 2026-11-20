# She Talks Business: weekly content playbook

This is the instruction file for the weekly content agent (and for Lynn). Every week one topic becomes:
a blog post on the site, a Flodesk newsletter, a reel script for Instagram and TikTok, captions, and a free guide.
**Every piece has two jobs: get people to sign up for the newsletter or the free guide, and show that Lynn knows AI for marketing and sales so business owners hire her.**

## Who we write for
Owners and marketers of service businesses and (luxury) brands: beauty, hair & skin, interior design, real estate, home services & construction, hospitality. Busy, not technical, care about more clients and less admin. Not developers.

## Positioning
Lynn builds AI systems that fix where a business leaks customers: websites that book, online booking and AI assistants, missed-call text-back, automatic follow-up, review requests, marketing automation. Each issue teaches one of these systems (or one part of it) so readers can try it themselves.
End every article and reel script with a soft line that she builds this for businesses ("Rather have this built for you? Tell me about your business: shetalksbusiness.co/contact"). One line only; the main CTA stays the free guide.
Show what the system does in real life (a salon, an interior designer, a builder), not abstract theory. Never invent statistics or client results; if a number is useful, find a real source and cite it in sources.md, or leave it out.

## Voice
- Lynn, first person, warm and direct. Short sentences. British spelling (colour, centre).
- Show the "how": exact steps, exact prompts. No theory, no hype words ("game-changer", "unlock", "revolutionise").
- No em dashes. Use commas, colons or full stops.
- Never promote C-School.
- Fact-check every AI tool feature, name and price live before writing it. If something can't be verified, mark it with ⚠️ in the draft for Lynn to check. Prefer tool-agnostic advice.

## Weekly steps (for the agent)
1. **Topic.** Read `NEXT-TOPIC.md`. If it has a topic, use it (and its notes). If it's empty, pick the next unused topic from the topic bank below and say so in the pull request. Remove the topic you used from the bank, and reset `NEXT-TOPIC.md` to an empty `Topic:` line in the same pull request.
2. **Research.** Check current features and wording of any tool mentioned. Note sources in `drops/<date>-<slug>/sources.md`.
3. **Article.** Write `content/posts/<date>-<slug>.md` (date = next Thursday) with `status: draft`. 800 to 1,200 words. Structure:
   - Problem in 2 to 3 short paragraphs
   - The method, as numbered steps
   - At least one fenced prompt block (```Copy prompt) that readers can copy
   - `<!--guide-->` on its own line after the first prompt (the free guide box appears there)
   - "Your turn" with one small task and "hit reply"
   - One line teasing next week
   Front matter fields: title, slug, date, issue, description (max 155 chars), dek, guide_title, guide_segment, guide_pitch, guide_points (3 to 4), reel_instagram, reel_tiktok, status.
4. **Email.** `drops/<date>-<slug>/email.md`: 3 subject lines, preview text, then Flodesk blocks (text, prompt box, button to the post, button to the guide `#guide`, sign-off "Lynn", P.S. with reel links).
5. **Reel.** `reel-script.md`: 30 to 45 s, hook in the first 3 s, a table of time / on screen / you say / text on screen, a shot list, 3 alternative hooks. The CTA is always "Comment KEYWORD".
6. **Captions.** `captions.md`: Instagram caption (hook, value list, comment CTA, save CTA, 5 to 8 hashtags), TikTok caption (short), and the DM reply with the link to `/newsletter/<slug>#guide`.
7. **Guide.** `guide.md`: 1 to 2 page cheat sheet content, the Flodesk segment name (kebab-case), and the delivery email. Reuse an existing guide if the topic fits.
8. **Build check.** Run `python3 tools/build.py` and make sure it finishes without errors.
9. **Hand over.** Commit on a branch `drop/<date>-<slug>`, open a pull request titled "Issue #N: <title>" and summarise what Lynn needs to do. Don't merge.

## What Lynn does each week
1. Review the pull request (edit the article right on GitHub if needed).
2. Make the guide PDF in Canva, upload it to Flodesk, create the segment and the workflow (see README).
3. Film the reel from the script, post it, and paste the reel links into the post's front matter.
4. Change `status: draft` to `status: published` and merge. Netlify publishes the post automatically.
5. Build the email in Flodesk from `email.md` and schedule it.
6. Set the comment keyword in ManyChat (or reply by hand) with the DM text.

## Topic bank
- Find where your business leaks customers: a 10-minute self-audit with AI
- The missed-call text-back: what it is and how to set it up
- Get more Google reviews on autopilot (and reply to them with AI)
- Follow up on every quote without remembering to
- An AI assistant that answers questions and books appointments on your website
- Win back past clients with one automated message
- Cut no-shows with smart reminders
- What a website that books actually needs (checklist)
- Turn one client project into a month of content with AI
- Write all your client emails in your brand voice with AI
- Luxury brand voice: make automated messages feel personal
- AI product and portfolio photos for service businesses
