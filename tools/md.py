"""Tiny Markdown to HTML converter for newsletter issues (no dependencies).

Supports: ## / ### headings, paragraphs, - and 1. lists, > quotes, --- rules,
```fenced blocks``` (rendered as a copyable prompt), images, links, **bold**, *italic*, `code`.
"""
import html, re

_n = [0]


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', r'<img src="\2" alt="\1" loading="lazy">', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<em>\1</em>', s)
    return s


def convert(md):
    lines = md.replace('\r\n', '\n').split('\n')
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>')
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith('```'):
            flush()
            label = s[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                buf.append(lines[i])
                i += 1
            _n[0] += 1
            pid = f'p{_n[0]}'
            out.append(f'<pre id="{pid}"><code>{html.escape(chr(10).join(buf))}</code></pre>'
                       f'<button type="button" class="copy-btn" data-copy="{pid}">{html.escape(label) if label else "Copy prompt"}</button>')
        elif not s:
            flush()
        elif s.startswith('### '):
            flush(); out.append('<h3>' + inline(s[4:]) + '</h3>')
        elif s.startswith('## '):
            flush(); out.append('<h2>' + inline(s[3:]) + '</h2>')
        elif s in ('---', '***'):
            flush(); out.append('<hr>')
        elif s.startswith('> '):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append('<blockquote>' + inline(' '.join(buf)) + '</blockquote>')
            continue
        elif re.match(r'^(-|\*) ', s) or re.match(r'^\d+\. ', s):
            flush()
            ordered = bool(re.match(r'^\d+\. ', s))
            tag = 'ol' if ordered else 'ul'
            items = []
            while i < len(lines):
                t = lines[i].strip()
                m = re.match(r'^\d+\. (.*)', t) if ordered else re.match(r'^(?:-|\*) (.*)', t)
                if not m: break
                items.append('<li>' + inline(m.group(1)) + '</li>'); i += 1
            out.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
            continue
        elif s.startswith('!['):
            flush(); out.append(inline(s))
        else:
            para.append(s)
        i += 1
    flush()
    return '\n'.join(out)


def front_matter(text):
    """Simple YAML-ish front matter: key: value, and lists as '- item' under a key."""
    if not text.startswith('---'):
        return {}, text
    end = text.index('\n---', 3)
    meta, key = {}, None
    for ln in text[3:end].strip().split('\n'):
        if re.match(r'^\s+- ', ln) or (ln.startswith('- ') and key):
            meta.setdefault(key, [])
            if not isinstance(meta[key], list): meta[key] = []
            meta[key].append(ln.strip()[2:].strip().strip('"'))
        elif ':' in ln:
            key, v = ln.split(':', 1)
            key = key.strip(); v = v.strip().strip('"')
            meta[key] = v
    return meta, text[end + 4:].lstrip('\n')
