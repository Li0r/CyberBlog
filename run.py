#!/usr/bin/env python3
"""Run from the CyberBlog repo root AFTER fix_blog.py:  python3 build_sidebar.py

Edit POSTS below, then rerun to regenerate the sidebar on every page.
Each platform becomes its own collapsible group; the group of the page you're
on opens automatically and the current post is highlighted.
Format: "Platform name": [("Link text", "file name inside writeup/"), ...]"""
import pathlib, re

POSTS = {
    "pwnable.kr": [
        ("fd", "fd.html"),
        ("horcruxes", "horcruxes.html"),
    ],
    "picoCTF": [
        ("babygame01", "babygame01.html"),
    ],
    "ShabakCTF-2021": [
        ("BabyRISC", "babyrisc.html")
    ],
    # "HackTheBox": [("some-box", "some-box.html")],
    # "Projects":   [("my-project", "my-project.html")],
}

CSS_MARK = "/* sidebar groups */"
CSS_ADD = f"""
{CSS_MARK}
.sidebar details.sub{{margin:4px 0 4px 8px}}
.sidebar details.sub summary{{font-weight:600;font-size:.95rem}}
.sidebar a.current{{color:var(--link);font-weight:700}}
"""

root = pathlib.Path('.')
css = root / 'static' / 'style.css'
if not css.exists():
    raise SystemExit("static/style.css not found - run fix_blog.py first.")
if CSS_MARK not in css.read_text():
    css.write_text(css.read_text() + CSS_ADD)
    print("added sidebar styles to static/style.css")


def sidebar_html(prefix, current):
    out = ['<div class="sidebar">', '    <details open>', '        <summary>Writeups</summary>']
    for platform, posts in POSTS.items():
        is_open = any(f == current for _, f in posts)
        out.append(f'        <details class="sub"{" open" if is_open else ""}>')
        out.append(f'            <summary>{platform}</summary>')
        out.append('            <ul>')
        for title, fname in posts:
            cls = ' class="current"' if fname == current else ''
            out.append(f'                <li><a href="{prefix}{fname}"{cls}>{title}</a></li>')
        out.append('            </ul>')
        out.append('        </details>')
    out += ['    </details>', '</div>']
    return '\n'.join(out)


for f in sorted(root.glob('**/*.html')):
    if '.git' in f.parts:
        continue
    s = f.read_text()
    if '<div class="sidebar">' not in s:
        continue
    in_writeup = f.parent.name == 'writeup'
    prefix = '' if in_writeup else 'writeup/'
    new = sidebar_html(prefix, f.name if in_writeup else None)
    s2 = re.sub(r'<div class="sidebar">.*?</div>\n?', new + '\n', s, count=1, flags=re.S)
    f.write_text(s2)
    print("sidebar updated:", f)
