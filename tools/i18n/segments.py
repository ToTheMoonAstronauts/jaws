"""Shared segment logic for the Lithuanian build.
A *segment* is a piece of user-facing English: a text node, a translatable attribute value,
or a string literal (or a literal part of a template literal) inside JavaScript.
extract.py lists them; build_lt.py replaces each one with its Lithuanian version from lt.json."""
import re, html

ATTRS = ("alt", "title", "placeholder", "aria-label", "content", "data-ttl")
WORD = re.compile(r"[A-Za-z]{2,}")
# things that look like code, ids, urls, colours, css -- never translated
SKIP = re.compile(r"^(https?:|mailto:|#|\.[a-z]|/|[a-z0-9_-]+\.(html|js|css|webp|png|jpg|svg|ico)\b|[a-z]+(-[a-z0-9]+)+$|[a-z]+[A-Z]\w*$|[a-z_]+$)|[{}]|;(?! )|=>|\$\(|var\(--")

def is_text(s):
    t = html.unescape(s).strip()
    if len(t) < 2 or not WORD.search(t): return False
    if SKIP.search(t): return False
    return True

TAG = re.compile(r"(<script\b[^>]*>)(.*?)(</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)|(<[^>]+>)|([^<]+)", re.S | re.I)
ATTR = re.compile(r'(\s(?:' + "|".join(ATTRS) + r')=")([^"]*)(")')
# JS literals: "..." '...' `...` (no nesting of ${} with backticks inside, which our code avoids)
JSLIT = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'|`((?:[^`\\]|\\.)*)`', re.S)
TPL = re.compile(r"\$\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}")

def js_segments(code, fn):
    """call fn(text) for each translatable literal part; return code with replacements."""
    def lit(m):
        q = '"' if m.group(1) is not None else ("'" if m.group(2) is not None else "`")
        body = m.group(1) if q == '"' else (m.group(2) if q == "'" else m.group(3))
        if q == "`":
            parts = TPL.split(body); exprs = TPL.findall(body)
            out = []
            for i, p in enumerate(parts):
                out.append(html_or_text(p, fn))
                if i < len(exprs): out.append(js_segments_in_expr(exprs[i], fn))
            return "`" + "".join(out) + "`"
        return q + html_or_text(body, fn, js=True) + q
    return JSLIT.sub(lit, code)

def js_segments_in_expr(expr, fn):
    return "${" + js_segments(expr[2:-1], fn) + "}"

def html_or_text(s, fn, js=False):
    """a JS string may hold HTML markup: translate its text nodes + attrs; else the whole string."""
    if "<" in s and ">" in s: return html_segments(s, fn, in_js=True)
    if not is_text(s): return s
    lead = len(s) - len(s.lstrip()); trail = len(s) - len(s.rstrip())
    core = s.strip()
    return s[:lead] + fn(core) + s[len(s) - trail:] if trail else s[:lead] + fn(core)

def html_segments(doc, fn, in_js=False):
    def tag(m):
        if m.group(1):  # script
            if 'type="application/ld+json"' in m.group(1): return m.group(0)
            return m.group(1) + js_segments(m.group(2), fn) + m.group(3)
        if m.group(4) or m.group(5): return m.group(0)
        if m.group(6):
            t = m.group(6)
            if t.startswith("<meta") and 'name="description"' not in t and 'property="og:' not in t: return t
            return ATTR.sub(lambda a: a.group(1) + (fn(a.group(2)) if is_text(a.group(2)) and "${" not in a.group(2) else a.group(2)) + a.group(3), t)
        txt = m.group(7)
        if not is_text(txt) or (in_js and "${" in txt): return txt
        lead = txt[:len(txt) - len(txt.lstrip())]; trail = txt[len(txt.rstrip()):]
        return lead + fn(txt.strip()) + trail
    return TAG.sub(tag, doc)
