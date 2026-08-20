import sys, re, io
# Locate a quote fragment in a hard-wrapped Markdown file.
# Prints the TIGHTEST line window containing it: earliest end, then latest start.
# Normalisation, in this order -- each one was added because it produced a false ABSENT
# in the wave-3 pilot, not on theory:
#   1. whitespace collapsed      (source docs hard-wrap at ~105 cols; quotes span lines)
#   2. markdown emphasis dropped (* _ ` -- the catalog moves ** around inside a quote)
#   3. quote characters unified  (" ' and the typographic variants -- the catalog renders
#                                 the source's " as ' because the cell is itself quoted)
QUOTES = dict.fromkeys(map(ord, "‘’“”'"), '"')
def norm(s):
    s = s.translate(QUOTES)
    s = re.sub(r'[*_`]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

frag = norm(sys.argv[1])
lines = io.open(sys.argv[2], encoding='utf-8').read().split('\n')
for end in range(len(lines)):
    for start in range(end, max(-1, end - 6), -1):
        if frag in norm(' '.join(lines[start:end + 1])):
            print("FOUND start_line=%d end_line=%d wrapped=%s" % (start + 1, end + 1, start != end))
            raise SystemExit(0)
print("ABSENT")
raise SystemExit(1)
