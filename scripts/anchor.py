#!/usr/bin/env python3
"""anchor.py -- locate a rules-catalog quote in its hard-wrapped source doc.

    python3 anchor.py <source_doc> "<raw Source quote/anchor cell>"

The RAW CELL goes in. The tool derives the fragment itself, so that "every agent runs
the identical script" is true of the input as well as the code -- a hand-derived input
makes an identical tool produce non-identical answers.

Output (always FRAGMENT= first, so the derivation is visible in the transcript):
    FRAGMENT=<what was actually searched for>
    FOUND start_line=N end_line=M wrapped=<b> trimmed=<n>  exit 0  -- exactly one match
    AMBIGUOUS n=<k> lines=<n1,n2,...>                      exit 2  -- MORE THAN ONE match
    ABSENT                                                 exit 1  -- no match
    TOO_SHORT longest=<n>                                  exit 3  -- no part reaches 25 chars
    TRIM_EXCEEDED trimmed=<n> limit=<n>                    exit 4  -- matched only after
                                                                      trimming too much to trust

AMBIGUOUS and TOO_SHORT are both UNRESOLVED verdicts. Never pick one of several
matches: first-match-wins with no signal is exactly the miscite class this wave exists
to find, and it silently makes anchor_line a coin flip.

Normalisation -- each rule was added because it produced a FALSE ABSENT on real data:
  1. whitespace collapsed      source docs hard-wrap at ~105 cols; quotes span lines
  2. markdown emphasis dropped the catalog moves ** around inside a quote
  3. quote characters unified  the catalog renders the source's " as ' because the
                               cell is itself quoted
"""
import sys, re, io

MIN_FRAGMENT = 25          # was 40; 250 of 2310 rows (10.8%) could never reach 40, measured at
                           # normalised length with this file's own fragment(). An earlier
                           # "239 / 10.3%" was measured with a reimplementation, not with this
                           # tool -- the same class of error this tool exists to prevent.
MAX_TRIM_ABS = 15          # a match found only after dropping more than this is not the quote
MAX_TRIM_FRAC = 0.20       # ... nor is one that dropped more than a fifth of it
QUOTES = dict.fromkeys(map(ord, "‘’“”'"), '"')

def norm(s):
    s = s.translate(QUOTES)
    s = re.sub(r'[*_`]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def fragment(cell):
    """Longest quoted span, split on ellipsis, longest surviving part.

    The cell is written `"<source text>" -- <section name>`; everything outside the
    quotes is the catalog's own anchor note and is not in the source doc. A string
    still containing an ellipsis is never searched for -- the ellipsis stands for text
    that was elided, so the literal can never match."""
    spans = re.findall(r'"([^"]+)"', cell)
    best = max(spans, key=len) if spans else cell
    parts = [p.strip() for p in re.split(r'\.\.\.|…', best) if p.strip()]
    return max(parts, key=len) if parts else ""

def main():
    src, cell = sys.argv[1], sys.argv[2]
    frag_raw = fragment(cell)
    frag = norm(frag_raw)
    print("FRAGMENT=%s" % frag_raw)
    if len(frag) < MIN_FRAGMENT:
        print("TOO_SHORT longest=%d" % len(frag)); return 3

    lines = io.open(src, encoding='utf-8').read().split('\n')
    joined, starts = [], []          # starts[i] = offset at which line i begins
    pos = 0
    for l in lines:
        n = norm(l)
        starts.append(pos)
        joined.append(n)
        pos += len(n) + 1            # single separator space, always
    text = " ".join(joined)

    # Longest-matching-prefix backoff. The catalog routinely ends a quote with terminal
    # punctuation the source does not have -- it quotes "...never fired**." where the source
    # reads "...never fired** in 22 days". Searching only the full fragment reports ABSENT on
    # text that is plainly present, which is the same false-negative class as the wrap defect.
    # So: try the whole fragment, then drop trailing punctuation, then drop trailing words,
    # never going below MIN_FRAGMENT. Report how much was dropped.
    def occurrences(f):
        out, i = [], text.find(f)
        while i != -1:
            out.append(i); i = text.find(f, i + 1)
        return out

    cand, hits, trimmed = frag, occurrences(frag), 0
    if not hits:
        probe = frag.rstrip(' .,;:!?"\')-')
        while len(probe) >= MIN_FRAGMENT:
            h = occurrences(probe)
            if h:
                cand, hits, trimmed = probe, h, len(frag) - len(probe)
                break
            cut = probe.rfind(' ')
            if cut <= 0: break
            probe = probe[:cut].rstrip(' .,;:!?"\')-')
    if not hits:
        print("ABSENT"); return 1

    # Cap the backoff. Added 2026-08-20 after a full-catalog dry run showed 355 of 2114 matches
    # (15.4%) resolving ONLY through the backoff, with a maximum of 120 characters dropped -- a
    # 120-char trim is not "the same quote with its full stop removed", it is a different string.
    # Uncapped, those rows were recorded identically to exact matches.
    if trimmed:
        limit = max(MAX_TRIM_ABS, int(MAX_TRIM_FRAC * len(frag)))
        if trimmed > MAX_TRIM_ABS or trimmed > MAX_TRIM_FRAC * len(frag):
            print("TRIM_EXCEEDED trimmed=%d limit=%d" % (trimmed, limit)); return 4
    frag = cand

    def line_of(off):
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= off: lo = mid
            else: hi = mid - 1
        return lo + 1

    spans = [(line_of(h), line_of(h + len(frag) - 1)) for h in hits]
    uniq = sorted(set(spans))
    if len(uniq) > 1:
        print("AMBIGUOUS n=%d lines=%s" % (len(uniq), ",".join(str(s) for s, _ in uniq)))
        return 2
    s, e = uniq[0]
    print("FOUND start_line=%d end_line=%d wrapped=%s trimmed=%d" % (s, e, s != e, trimmed))
    return 0

if __name__ == "__main__":
    sys.exit(main())
