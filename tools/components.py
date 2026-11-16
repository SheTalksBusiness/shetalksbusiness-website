"""Small HTML building blocks shared by the one-time restructure and the weekly build."""
import html as _h

FLODESK_PAGE = 'https://she-talks-business.myflodesk.com/freetemplates'


def signup_form(segment='newsletter', button='Get the free newsletter', dark=False,
                success=None, note=True, placeholder='Your email address'):
    cls = 'nl-form on-dark' if dark else 'nl-form'
    succ = f' data-success="{_h.escape(success)}"' if success else ''
    out = (f'<form class="{cls}" data-segment="{segment}" action="{FLODESK_PAGE}" method="get" novalidate{succ}>'
           f'<input class="nl-email" type="email" name="email" placeholder="{placeholder}" aria-label="Email address" autocomplete="email" required>'
           '<input class="nl-hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">'
           f'<button type="submit" class="nl-btn">{button}</button>'
           '<p class="nl-msg" role="status" aria-live="polite"></p></form>')
    if note:
        out += ('<p class="nl-note">Free, every week. Unsubscribe anytime. '
                '<a href="/privacy#top">Privacy</a></p>')
    return out


def prompt_card(pid, title, use, prompt):
    return f'''<div class="prompt-card">
        <p style="margin: 0; font-size: 12px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #7a715f;">{use}</p>
        <h3 style="margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: 30px; line-height: 1.15;">{title}</h3>
        <p class="prompt-text" id="{pid}">{_h.escape(prompt)}</p>
        <button type="button" class="copy-btn" data-copy="{pid}">Copy prompt</button>
      </div>'''


EYEBROW = 'margin: 0; font-size: 13px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase;'
H2 = "margin: 0; font-family: 'Editors Note', Georgia, serif; font-weight: 300; font-size: clamp(40px, 4.6vw, 62px); line-height: 1.06;"
WRAP = 'max-width: 1240px; margin: 0 auto; padding: 112px clamp(24px, 6vw, 96px);'
