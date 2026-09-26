#!/usr/bin/env python3
"""Build the public site: wrap page.html (artifact-format body) into a full index.html.
page.html is the single source: it also publishes as the private Claude preview artifact."""
import re, pathlib
root = pathlib.Path(__file__).parent
page = (root / "page.html").read_text()
title = re.search(r"<title>(.*?)</title>", page).group(1)
page = re.sub(r"<title>.*?</title>\n?", "", page, count=1)
desc = "The Ark is where you come to live your purpose. In community. Founding 100, by invitation."
favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230a0a0a'/%3E"
           "%3Cpath d='M6 11a10 10 0 0 0 20 0' fill='none' stroke='%23f2f1ee' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E")
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#fffdf7">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://joinarknow.com/">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="https://joinarknow.com/">
<link rel="icon" href="{favicon}">
"""
# move the <link>/<style> head material into <head>; the rest is body
split = page.index("</style>") + len("</style>")
html = head + page[:split].strip() + "\n</head>\n<body>\n" + page[split:].strip() + "\n</body>\n</html>\n"
(root / "index.html").write_text(html)
print("built index.html", len(html), "bytes")
