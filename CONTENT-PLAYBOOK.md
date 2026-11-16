# She Talks Business: weekly content playbook

This is the instruction file for the weekly content agent (and for Lynn). Every week one topic becomes:
a blog post on the site, a Flodesk newsletter, a reel script for Instagram and TikTok, captions, and a free guide.
**Every piece has one job: get people to sign up for the newsletter or the free guide.**

## Who we write for
Creatives and small business owners who want to use AI (and Canva) to create more in less time. Not developers.
Teams and brands are served on /work-with-me; don't pitch training in the weekly content.

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
- Turn one blog post into 10 social posts in 15 minutes
- Build a Claude Project / custom GPT for your brand
- AI product photos from one phone photo (hero, detail, mood)
- Canva Magic Studio: the 5 tools worth your time ⚠️ verify current names
- Plan a month of content with one prompt
- Repurpose a reel into a carousel with AI
- Write a sales page section by section with AI
- AI for client emails: templates that don't sound robotic
- Colour variations of a product image, step by step
- My weekly AI content workflow, start to finish
- Prompts to audit your Instagram bio and highlights
