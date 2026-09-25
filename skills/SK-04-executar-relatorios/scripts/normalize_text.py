#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import re, sys

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.hidden = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in {"script","style","noscript"}:
            self.hidden += 1
        elif tag in {"p","div","section","article","header","footer","li","h1","h2","h3","h4","h5","h6","br","tr"}:
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in {"script","style","noscript"} and self.hidden:
            self.hidden -= 1
        elif tag in {"p","div","section","article","li","h1","h2","h3","h4","h5","h6","tr"}:
            self.parts.append("\n")
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

def normalize(text):
    text = unescape(text).replace("\r\n","\n").replace("\r","\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: normalize_text.py INPUT [OUTPUT]")
    src = Path(sys.argv[1])
    raw = src.read_text(encoding="utf-8", errors="replace")
    if src.suffix.lower() in {".html",".htm"}:
        parser = VisibleText()
        parser.feed(raw)
        raw = "".join(parser.parts)
    out = normalize(raw)
    if len(sys.argv) >= 3:
        Path(sys.argv[2]).write_text(out, encoding="utf-8")
    else:
        print(out, end="")

if __name__ == "__main__":
    main()
