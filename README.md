# shetalksbusiness.co

The She Talks Business website: static HTML in `site/`, newsletter issues in `content/posts/`, built by `tools/build.py` and hosted on Netlify.

## Folders
| Folder | What's in it |
|---|---|
| `site/` | The published website. Edit pages here directly. |
| `content/posts/` | One Markdown file per newsletter issue. `status: published` puts it live. |
| `drops/` | The weekly content pack: email, reel script, captions, guide. Not published. |
| `netlify/functions/subscribe.mjs` | Sends signups from the website to Flodesk. |
| `tools/` | `build.py` (runs on every deploy), `md.py`, `components.py`. |
| `CONTENT-PLAYBOOK.md` | How the weekly content is made. |

## One-time setup

### 1. GitHub + Netlify
1. Create an empty **private** repository on GitHub, e.g. `shetalksbusiness-website`.
2. Push this folder to it.
3. In Netlify, open the site **shetalksbusiness** → Site configuration → Build & deploy → Link repository → GitHub → pick the repo. Netlify reads `netlify.toml` (publish `site`, build `python3 tools/build.py`).

### 2. Flodesk signups
1. Flodesk → Account settings → Integrations → API keys → create a key.
2. Flodesk → Audience → Segments: create **Newsletter** and **Guide: SAS Prompt Method**. Open each segment; the id is the last part of the address bar URL.
3. Netlify → Site configuration → Environment variables:
   - `FLODESK_API_KEY` = your key
   - `FLODESK_SEGMENTS` = `{"newsletter":"<newsletter segment id>","sas-prompt-guide":"<guide segment id>"}`
4. Redeploy. Until the key is set, the forms send people to your Flodesk signup page instead, so nothing breaks.

### 3. Deliver each guide
Flodesk → Workflows → new workflow, trigger **Subscriber added to segment** → pick the guide segment → email with the download link. Add one segment + workflow per new guide, and add the segment to `FLODESK_SEGMENTS`.

### 4. Comment keywords
Use ManyChat (Instagram + TikTok) or reply by hand with the DM text in each drop's `captions.md`.

## Adding a new guide segment name
The `guide_segment` in a post's front matter must match a key in `FLODESK_SEGMENTS`. Everyone who signs up for a guide is also added to the newsletter segment.
