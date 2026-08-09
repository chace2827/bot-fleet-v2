#!/usr/bin/env python3
"""A-series drift detector — the greenfield family's Phase C arm-distinctness machinery.

⛔ STANDALONE. NOT wired into scripts/daily.sh. A `daily.sh` wiring snippet is emitted as a
COMMENT (see WIRING_SNIPPET / --emit-wiring); wiring is a Day-0-adjacent decision
(reactivation-runbook.md §4 Step 4(b)) and this tool does not edit daily.sh.

WHY IT EXISTS. The seven greenfield bots run on Architecture E: three SHARED Library automations
(ScannerA/ScannerB/Backstop) attached to all seven, plus one differing exit mechanic per arm. An
edit to a shared object changes all seven at once and fails identically on all seven — which the
arms cannot detect by diffing each other (greenfield-family-spec.md §8.3 A7 box). §8.3 specifies a
nine-assert nightly detector A1–A9; §8.2 a 21-pair capture-diff. Nothing in scripts/ implemented
them (memo N-3); this is that build (decision-card-2026-08-06 slot-4 item 7).

WHAT IT REPRODUCES. The asserts were hand-run once at n=7 bots on 2026-08-07; the reference is
data/captures/2026-08-07-greenfield/ASSERTS-A1-A9-and-capture-diff.txt. `--validate` asserts this
tool reproduces it EXACTLY: A1 21/21 · A2 7/7 · A3 7/7 · A7 3/3 · A8 7/7 · A9 7/7; A4 MOOT;
A4b/A6 NOT-RUNNABLE pre-Day-0; A5 NOT-RUN. Any divergence is a defect in the tool, not the record.

NEVER HARDCODE OA OBJECT IDS. A post-restore re-creates objects with new BOT…/RT…/IN… ids. All ids
are read from the captures/CSV at runtime; family membership keys on the STABLE bot NAME
(GF-QQQ-IC-<Arm>), never on an id.

OPS-CLASS SCOPING (E-3, exploratory-bots-design-2026-08-07 §3.3 item 6, RULED 2026-08-07).
The two LEDGER-reading asserts — A4b and A6 — iterate every row in the ledger and are NOT scoped
to the family. A single `TESTOPS-LAB-*` row would turn them red for reasons that have nothing to
do with arm distinctness: A6 flags any quantity != 1 (an ops bot sized 3 for the dstop unit test
trips it on its first fill), and A4b's `cfg_stop` returns False for any bot outside the seven-arm
dict, so an ops bot's ≥2 fast same-day closes read as a broken input link forever. Guardrail G3:
"no A-series assert may read them." Both now take the ops set — declared in data/bots_meta.csv's
`ops_class` column, never a tag and never a bot name — and SKIP those bots with the skip REPORTED.
A detector that answers "no findings" while structurally blind is worse than no detector.

THE G2 RIDER (§1.2, load-bearing). The Open-Position action stores a REFERENCE
({"type":"input","nid":"root",…}) identical on every arm; `oldValue` is a stale pre-link snapshot.
Config is read ONLY from the BOT INPUT OBJECT's decoded value (the per-bot end of the chain). This
tool reads that end and ignores the action reference and oldValue — the diff that reads the action
alone "will look like a clean pass and prove nothing."
"""
import argparse, csv, hashlib, json, os, re, sys

VERSION = "0.1.0-DRAFT"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
BOTS_META = os.path.join(DATA, "bots_meta.csv")

# --- E-3 §3.3 — the ops-class (Lab) exclusion, mirrored from build_ledger.py --
OPS_CLASS_COL   = "ops_class"
OPS_CLASS_VALUE = "lab-ops"

# --- the seven arms, keyed by STABLE bot name (never an id) ----------------
RIDE   = "GF-QQQ-IC-Ride"      # PR-14 · control (base only)
PT50   = "GF-QQQ-IC-PT50"      # PR-15
TRAIL  = "GF-QQQ-IC-Trail"     # PR-16
TOUCH0 = "GF-QQQ-IC-Touch0"    # PR-17
SL100  = "GF-QQQ-IC-SL100"     # PR-18
SL200  = "GF-QQQ-IC-SL200"     # PR-19
CANARY = "GF-QQQ-IC-Canary"    # PR-20
FAMILY = [RIDE, PT50, TRAIL, TOUCH0, SL100, SL200, CANARY]
ARM_PR = {RIDE: "PR-14", PT50: "PR-15", TRAIL: "PR-16", TOUCH0: "PR-17",
          SL100: "PR-18", SL200: "PR-19", CANARY: "PR-20"}
SHARED_AUTOMATIONS = ["GF-ScannerA-PutSpread", "GF-ScannerB-CallSpread", "GF-Backstop-1552-FlatClose"]

# --- field taxonomy (§8.2 step 3 / the decoded exit bundle) ----------------
MECHANIC_TRIGGERS = ["profits", "dprofit", "stoploss", "dstop", "tstop", "touch",
                     "price", "xevents", "epsdays"]
PRICING_SUBFIELDS = ["smprofits", "smdprofit", "smstoploss", "smdstop", "smtstop", "smtouch"]
BASE_FIELDS       = ["expdays", "smexpdays", "dtype"]   # equal on all; never a mechanic
KNOWN_FIELDS      = MECHANIC_TRIGGERS + PRICING_SUBFIELDS + BASE_FIELDS + ["text"]

# --- A3 pre-registration (§9 MECHANISM lines). SOLE verdict source; config-independent, so it
# catches all-arms-mistyped-identically. Amending a PR is a gated "amend the plan" edit here. ----
PRE_REGISTRATION = {
    RIDE:   {},                                          # base only — the control
    PT50:   {"profits": 0.5},                            # + smprofits speedy
    TRAIL:  {"tstop": {"type": "tstop", "target": 40, "trail": 15}},   # + smtstop normal
    TOUCH0: {"touch": {"type": "usd", "value": 0}},      # + smtouch normal
    SL100:  {"stoploss": 1.0},                           # % of credit (C1)
    SL200:  {"stoploss": 2.0},                           # % of credit (C1)
    CANARY: {"profits": 0.05},                           # + smprofits speedy
}

# --- the hand-run reference verdicts this tool must reproduce (§ ASSERTS file) --
REFERENCE = {"A1": (21, 21), "A2": (7, 7), "A3": (7, 7), "A7": (3, 3), "A8": (7, 7), "A9": (7, 7),
             "A4": "MOOT", "A4b": "NOT-RUNNABLE", "A5": "NOT-RUN", "A6": "NOT-RUNNABLE"}
# recorded Notes UTF-16 lengths (ASSERTS file "NOTES BYTE-EXACTNESS" line) — spot-checked in A3
# ⛔ RE-BASELINED 2026-08-09 (S2-R3, Andy's ruling option A): the Day-0 signing edits lengthened
# every §9 entry, so the §9-vs-recorded check now baselines on the SIGNED §9 lengths. The bots'
# in-app Notes remain the build-time snapshot (old values, kept below for the record):
# build-time: {RIDE: 2339, PT50: 1722, TRAIL: 5412, TOUCH0: 2917, SL100: 4389, SL200: 4546, CANARY: 3018}
RECORDED_NOTE_LEN = {RIDE: 6258, PT50: 4005, TRAIL: 7698, TOUCH0: 5206,
                     SL100: 7494, SL200: 6832, CANARY: 5418}


# ===========================================================================
# Parsing
# ===========================================================================
def _clean(line):
    """Strip a capture line's trailing annotation (`<- …`), bold markers and trailing 'OK'."""
    line = line.split("<-")[0].split("^")[0]
    line = line.replace("**", "")
    return re.sub(r"\s+OK\b.*$", "", line).rstrip()


def _read_value(s):
    """Read one decoded value from string `s` starting after a field name: '' | {json} | "str" | token.
    Returns (normalized_value, rest_of_string)."""
    s = s.lstrip()
    if s.startswith('""'):
        return "", s[2:]
    if s.startswith("{"):
        depth, i = 0, 0
        for i, ch in enumerate(s):
            depth += (ch == "{") - (ch == "}")
            if depth == 0:
                break
        blob = s[:i + 1]
        try:
            return json.loads(blob), s[i + 1:]
        except json.JSONDecodeError:
            return blob, s[i + 1:]
    if s.startswith('"'):
        j = s.find('"', 1)
        return s[1:j] if j > 0 else s[1:], s[j + 1:] if j > 0 else ""
    tok = s.split()[0] if s.split() else ""
    return tok, s[len(tok):]


_FIELD_RE = re.compile(r"\b(" + "|".join(sorted(KNOWN_FIELDS, key=len, reverse=True)) + r")\b")

def parse_decoded_fieldset(block):
    """Parse a DECODED FIELD SET block -> {field: value}. A line qualifies iff its first token is a
    known field; on it EVERY known field is located (finditer) and its value read, so multiple
    fields per line survive any separator — the empties line `profits "" dprofit "" price ""` and
    the terse `expdays 0.01 · smexpdays {…}` both parse (known field names never occur inside these
    captures' value payloads/labels, verified)."""
    fields = {}
    for raw in block.splitlines():
        line = _clean(raw)
        toks = line.split()
        if not toks or toks[0] not in KNOWN_FIELDS:
            continue
        for m in _FIELD_RE.finditer(line):
            val, _ = _read_value(line[m.end():])
            fields.setdefault(m.group(1), val)
    return fields


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return v


def norm_val(v):
    """Normalize a decoded value for COMPARISON. Drops the 'text' LABEL key from JSON payloads
    (§1.2 rule 3 / N-4: OA re-serialises labels while payloads are byte-identical — compare
    decoded values, never rendered labels), and coerces numeric strings to float."""
    if isinstance(v, dict):
        return tuple(sorted((k, norm_val(v[k])) for k in v if k != "text"))
    return _num(v) if isinstance(v, str) else v


def mechanic_map(fieldset):
    """The arm's mechanic map: {trigger_field: normalized_value} for NON-EMPTY triggers only."""
    return {f: norm_val(fieldset[f]) for f in MECHANIC_TRIGGERS
            if fieldset.get(f, "") not in ("", None, {})}


def parse_bot_capture(text):
    """Parse one GF-QQQ-IC-* bot capture file -> structured dict (ids read from the file)."""
    def find(pat, default=None, flags=0):
        m = re.search(pat, text, flags)
        return m.group(1).strip() if m else default

    name = find(r"^BOT\s+(GF-QQQ-IC-\S+)", flags=re.M)
    bot = {"name": name, "bot_id": find(r"^BOT_ID\s+(\S+)", flags=re.M), "kind": "bot"}

    # bot-level settings (A2) — tolerant of BOTH the verbose ("seed  2500") and terse
    # ("seed 2500 OK · posLimit 2 OK") capture formats; values matched by content, searched anywhere.
    s = {}
    for key, pat in {
        "seed": r"\bseed\s+(\d+)", "posLimitDay": r"\bposLimitDay\s+(\d+)",
        "posLimit": r"\bposLimit\s+(\d+)", "scanrate": r"\bscanrate\s+(\d+)",
        "exitrate": r"\bexitrate\s+(\d+)", "nopdt": r"\bnopdt\s+(\d+)",
        "status": r'\bstatus\s+"?([A-Za-z]+)"?', "disableExits": r"\bdisableExits\s+(\d+)",
        "icon": r"\bicon\s+(fas-robot\s+bg-\w+)",
        "group": r'\bgroup\s+(?:\{[^}]*"name":"([^"]+)"|(\w+))',
        "tags": r'\btags\s+"([^"]*)"',
    }.items():
        m = re.search(pat, text)
        if m:
            s[key] = next((g for g in m.groups() if g), "").strip()
    # accountId ("account  accountId = \"sim\"" verbose | "account sim" terse) and symbols
    # ("[]" | "(none)") render differently per format — normalize both.
    m = re.search(r'accountId\s*=\s*"([^"]+)"', text) or re.search(r"\baccount\s+(\w+)", text)
    s["accountId"] = m.group(1) if m else None
    m = re.search(r"\bsymbols\s+(\[\]|\(?none\)?|\S+)", text)
    s["symbols"] = "0" if (m and re.sub(r"[^a-z]", "", (m.group(1) or "").lower()) in ("", "none")) else (m.group(1) if m else None)
    bot["settings"] = s

    # bot inputs + decoded field set (A1/A3/A8/A9). "type exits" is present in verbose captures
    # and absent in terse ones -> optional.
    inputs = {}
    for side, lbl in (("PUT", "GF_EXITS_PUT"), ("CALL", "GF_EXITS_CALL")):
        m = re.search(rf"{lbl}\s+id\s+(IN\S+)(?:\s+type\s+exits)?\s+posType\s+(\S+)", text)
        inputs[side] = {"label": lbl, "id": m.group(1) if m else None,
                        "posType": m.group(2) if m else None}
    ds_m = re.search(r"DECODED FIELD SET.*?\n(.*?)(?:\n\s*ARM MECHANIC|\n##|\Z)", text, re.S)
    fieldset = parse_decoded_fieldset(ds_m.group(1)) if ds_m else {}
    bot["fieldset"] = fieldset
    bot["inputs"] = inputs
    bot["mechanics"] = mechanic_map(fieldset)
    bot["a8_recorded_equal"] = "IDENTICAL on both" in text and "A8 PASS" in text

    # attached automations: rids + trigger config (A2 amended — trigger lives at the bot).
    # Value-based, format-tolerant: rids, ntime/freq/holidays, and the weekday value arrays
    # (scanner [1,2,3,4,5] ×2 + backstop byweekday [0,1,2,3,4]) — identical across all seven.
    bot["rids"] = sorted(set(re.findall(r"\b(RT\w+)", text)))
    def g1(pat):
        m = re.search(pat, text)
        return m.group(1) if m else None
    bot["trigger"] = {
        "backstop_ntime": g1(r"\bntime\s+(\d+)"), "backstop_freq": g1(r"\bfreq\s+(\d+)"),
        "backstop_holidays": g1(r'\bholidays\s+"?(\w+)"?'),
        "weekday_arrays": tuple(sorted(re.findall(r"\[[\d,]+\]", text))),
    }

    # notes record (A3 cross-check)
    nl = re.search(r"length\s+(\d+)\s+UTF-16", text)
    fd = re.search(r"firstDiff\s*=\s*(-?\d+)", text)
    bot["notes"] = {"utf16_len": int(nl.group(1)) if nl else None,
                    "firstDiff": int(fd.group(1)) if fd else None,
                    "raw": _extract_raw_notes(text)}
    return bot


def _extract_raw_notes(text):
    """Return the bot's raw NOTES bytes if the capture carries them (post-restore full captures may;
    the build-time summary captures record only length+firstDiff, so this is usually None)."""
    m = re.search(r"NOTES_TEXT\s*<<<\n(.*?)\n>>>", text, re.S)
    return m.group(1) if m else None


def parse_shared_capture(text):
    """Parse a shared-automation capture -> {name, rid, version, current_hash}. The current
    (adopted) hash is the LAST sha256(JSON{name,inputs,root}) in the file (a re-baseline appends a
    NEW A7 BASELINE below the original, which is left standing but superseded)."""
    name = re.search(r"^AUTOMATION\s+(GF-\S+)", text, re.M)
    hashes = re.findall(r"sha256\(JSON\{name,inputs,root\}\)\s+([0-9a-f]{64})", text)
    ver = re.findall(r"(?:^VERSION|version)\s+(\d+)", text, re.M)
    return {"kind": "shared", "name": name.group(1) if name else None,
            "current_hash": hashes[-1] if hashes else None,
            "all_hashes": hashes, "version": ver[-1] if ver else None}


def classify_and_parse(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if re.search(r"^BOT_ID\s", text, re.M) and re.search(r"^BOT\s+GF-QQQ-IC-", text, re.M):
        return parse_bot_capture(text)
    if re.search(r"^AUTOMATION\s+GF-", text, re.M):
        return parse_shared_capture(text)
    return None


def load_captures(roots):
    bots, shared = {}, {}
    for root in roots:
        for dirpath, _dirs, files in os.walk(root):
            for fn in files:
                if not fn.endswith(".txt") or "ASSERTS" in fn:
                    continue
                obj = classify_and_parse(os.path.join(dirpath, fn))
                if obj is None or not obj.get("name"):
                    continue
                (bots if obj["kind"] == "bot" else shared)[obj["name"]] = obj
    return bots, shared


def load_config_a7(config_path):
    """Read a7_hash baselines for shared_automation rows from bots_config_v2.csv (skip # comments)."""
    out = {}
    with open(config_path, encoding="utf-8") as f:
        rows = list(csv.reader(r for r in f if not r.lstrip().startswith("#")))
    if not rows:
        return out
    hdr = rows[0]
    idx = {c: i for i, c in enumerate(hdr)}
    for r in rows[1:]:
        if len(r) <= idx.get("a7_hash", 99):
            continue
        if r[idx["object_kind"]] == "shared_automation":
            out[r[idx["name"]]] = {"a7_hash": r[idx["a7_hash"]].strip(),
                                   "version": r[idx["version"]].strip()}
    return out


# ===========================================================================
# The asserts
# ===========================================================================
class Result:
    def __init__(self, name, status, k=None, n=None, detail="", lines=None):
        self.name, self.status, self.k, self.n = name, status, k, n
        self.detail, self.lines = detail, lines or []

    def ok(self):
        return self.status in ("PASS", "MOOT", "NOT-RUNNABLE", "NOT-RUN")

    def count(self):
        return f"{self.k}/{self.n}" if self.k is not None else ""


def _identify_control(bots):
    """The control = the bot with an EMPTY mechanic map; cross-checked as Ride/PR-14 by name."""
    empties = [b for b in bots.values() if not b["mechanics"]]
    ctrl = empties[0]["name"] if len(empties) == 1 else RIDE
    return ctrl


def a1_pairwise(bots):
    """A1 (amended): arm-vs-control expect 1 differing mechanic; arm-vs-arm expect 2 (each its own);
    shared-field-different-value expect 1. Base fields EQUAL in every pair. -> 21/21."""
    names = [n for n in FAMILY if n in bots]
    ctrl = _identify_control(bots)
    pairs, ok = [], 0
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            ma, mb = bots[a]["mechanics"], bots[b]["mechanics"]
            diff = {f for f in set(ma) | set(mb) if ma.get(f) != mb.get(f)}
            base_equal = all(norm_val(bots[a]["fieldset"].get(f, "")) == norm_val(bots[b]["fieldset"].get(f, ""))
                             for f in BASE_FIELDS)
            if a == ctrl or b == ctrl:
                ptype, expect = "arm-vs-control", 1
            elif set(ma) == set(mb):
                ptype, expect = "shared-field", 1
            else:
                ptype, expect = "arm-vs-arm", 2
            own = set(ma) | set(mb) if ptype == "arm-vs-arm" else diff
            passed = (len(diff) == expect and base_equal
                      and (ptype != "arm-vs-arm" or diff == own))
            ok += passed
            pairs.append((a, b, ptype, sorted(diff), expect, passed))
    n = len(pairs)
    lines = [f"    {'✓' if p else '✗'} {a} / {b:22} {ptype:15} diff={d} expect {e}"
             for a, b, ptype, d, e, p in pairs]
    return Result("A1", "PASS" if ok == n else "FAIL", ok, n,
                  "pairwise mechanic distinctness (amended)", lines), pairs, ctrl


def a2_nonbundle(bots):
    """A2 (amended): every non-bundle field + trigger config + rid list EQUAL across all seven
    (excluding name and the arm/pr-specific tag). -> 7/7."""
    names = [n for n in FAMILY if n in bots]
    fields = ["accountId", "seed", "posLimit", "posLimitDay", "scanrate", "exitrate", "nopdt",
              "status", "disableExits", "group", "icon", "symbols"]
    vec = {}
    for n in names:
        b = bots[n]
        v = tuple(b["settings"].get(f) for f in fields)
        v += (tuple(b["rids"]), b["trigger"].get("backstop_ntime"),
              b["trigger"].get("backstop_freq"), b["trigger"].get("backstop_holidays"),
              b["trigger"].get("weekday_arrays"))
        vec[n] = v
    consensus = max((v for v in vec.values()), key=lambda v: sum(1 for x in vec.values() if x == v))
    ok = sum(1 for n in names if vec[n] == consensus)
    lines = []
    for n in names:
        if vec[n] != consensus:
            diffs = [fields[i] for i in range(len(fields)) if vec[n][i] != consensus[i]]
            lines.append(f"    ✗ {n}: diverges on {diffs or 'trigger/rid'}")
    nfields = len(fields) + 4
    return Result("A2", "PASS" if ok == len(names) else "FAIL", ok, len(names),
                  f"{nfields} non-bundle fields incl. trigger config + rid list, equal across the family",
                  lines)


def a3_prereg(bots, spec_blocks):
    """A3 (LOAD-BEARING): decoded mechanic set == the hardcoded §9 PRE_REGISTRATION table (the SOLE
    verdict source, config-independent). Companion Notes cross-check = byte-compare vs the §9 block
    (raw notes) OR recorded firstDiff==-1 + UTF-16 length == the §9 block's length. -> 7/7."""
    names = [n for n in FAMILY if n in bots]
    ok, lines = 0, []
    for n in names:
        want = {f: norm_val(v) for f, v in PRE_REGISTRATION[n].items()}
        got = bots[n]["mechanics"]
        passed = got == want
        ok += passed
        # companion notes cross-check (never a prose value-parse)
        note = _a3_notes_check(bots[n], spec_blocks.get(n))
        lines.append(f"    {'✓' if passed else '✗'} {n:22} mechanics {sorted(got)} "
                     f"vs §9 {sorted(want)}   [notes: {note}]")
    return Result("A3", "PASS" if ok == len(names) else "FAIL", ok, len(names),
                  "decoded set == §9 pre-registration (table = sole verdict; notes byte-compared)",
                  lines)


def _a3_notes_check(bot, block):
    raw = bot["notes"].get("raw")
    if raw is not None and block is not None:
        return "byte-exact vs §9" if raw == block else "⚠ DRIFT vs §9"
    rec_len, fd = bot["notes"].get("utf16_len"), bot["notes"].get("firstDiff")
    if rec_len is None:
        return "no notes record"
    spec_len = len(block.encode("utf-16-le")) // 2 if block is not None else None
    len_ok = (spec_len is None) or (rec_len == spec_len)
    return (f"recorded firstDiff={fd}, utf16={rec_len}"
            + ("" if len_ok else f" ≠ §9 len {spec_len}"))


def a7_hashes(shared, config_a7):
    """A7: each shared automation's adopted payload hash == its CSV a7_hash baseline (by name).
    On mismatch, a drift report names the object, old/new hash, versions and a best-effort delta."""
    ok, lines, drift = 0, [], []
    for name in SHARED_AUTOMATIONS:
        cur = shared.get(name)
        base = config_a7.get(name)
        if cur is None or base is None:
            lines.append(f"    ? {name}: missing {'capture' if cur is None else 'CSV baseline'}")
            continue
        passed = cur["current_hash"] == base["a7_hash"]
        ok += passed
        lines.append(f"    {'✓' if passed else '✗'} {name:28} v{cur['version']} "
                     f"{(cur['current_hash'] or '')[:16]}… vs baseline {base['a7_hash'][:16]}…")
        if not passed:
            drift.append({"object": name, "baseline_hash": base["a7_hash"],
                          "current_hash": cur["current_hash"],
                          "version_baseline": base["version"], "version_current": cur["version"],
                          "field_delta": "hash-only (prior structured capture needed for field delta)"})
    r = Result("A7", "PASS" if ok == len(SHARED_AUTOMATIONS) else "FAIL", ok, len(SHARED_AUTOMATIONS),
               "shared-automation payload hash vs recorded baseline", lines)
    r.drift = drift
    return r


def a8_symmetry(bots):
    """A8: decoded(PUT)==decoded(CALL) per bot. These summary captures record one decoded set
    labelled 'IDENTICAL on both (A8 PASS)'; verified from that dual-side record (a full re-derivation
    needs both raw serialized payloads, available live). -> 7/7."""
    names = [n for n in FAMILY if n in bots]
    ok, lines = 0, []
    for n in names:
        passed = bots[n]["a8_recorded_equal"]
        ok += passed
        lines.append(f"    {'✓' if passed else '✗'} {n}: PUT≡CALL "
                     f"({'recorded identical' if passed else 'NOT recorded equal'})")
    return Result("A8", "PASS" if ok == len(names) else "FAIL", ok, len(names),
                  "decoded(GF_EXITS_PUT) == decoded(GF_EXITS_CALL), per bot (from dual-side record)",
                  lines)


def a9_bound(bots):
    """A9: both bot inputs BOUND (id present) and NON-EMPTY (decoded set has ≥ expdays). -> 7/7."""
    names = [n for n in FAMILY if n in bots]
    ok, lines = 0, []
    for n in names:
        ins = bots[n]["inputs"]
        bound = all(ins[s].get("id") for s in ("PUT", "CALL"))
        nonempty = bool(bots[n]["fieldset"].get("expdays"))
        passed = bound and nonempty
        ok += passed
        lines.append(f"    {'✓' if passed else '✗'} {n}: PUT {ins['PUT'].get('id')} / "
                     f"CALL {ins['CALL'].get('id')}  non-empty={nonempty}")
    return Result("A9", "PASS" if ok == len(names) else "FAIL", ok, len(names),
                  "every GF_EXITS_PUT/CALL bot input BOUND and NON-EMPTY (14/14 inputs)", lines)


def load_ops_set(path):
    """The declared ops set (E-3 §3.3 item 1). Classification is the `ops_class` COLUMN and
    nothing else — never the export's `tags` string (lossy: OA normalises tags) and never the
    bot name. A missing file or missing column yields an EMPTY set, which is the pre-Lab state;
    build_ledger.py is the surface that REFUSES on a missing column, and it is the one that
    guards the ledger. This tool only needs to know who to skip."""
    if not path or not os.path.exists(path):
        return set()
    return {(r.get("bot") or "").strip()
            for r in csv.DictReader(open(path))
            if (r.get(OPS_CLASS_COL) or "").strip().lower() == OPS_CLASS_VALUE} - {""}


def _ops_scope(ledger_rows, ops_set):
    """Split the ledger on the class axis and return (kept, report_line_or_None).
    The line is emitted whenever an ops set is DECLARED — including at zero matched rows —
    so the scoping is never invisible (§3.3 item 6, Tier-C SKIPPED discipline)."""
    if not ops_set:
        return ledger_rows, None
    kept    = [r for r in ledger_rows if (r.get("bot") or "") not in ops_set]
    skipped = [r for r in ledger_rows if (r.get("bot") or "") in ops_set]
    seen = sorted({r.get("bot") for r in skipped})
    return kept, (f"    ⏸ OPS-CLASS SCOPED OUT (E-3 §3.3): {len(skipped)} of {len(ledger_rows)} "
                  f"ledger row(s) skipped, {len(ops_set)} bot(s) declared "
                  f"{OPS_CLASS_COL}={OPS_CLASS_VALUE} in data/bots_meta.csv; "
                  f"present in this ledger: {seen if seen else 'none'}. "
                  f"Guardrail G3 — reported, never silent.")


def a4_a5_a6(ledger_rows, bots, ops_set=None):
    """A4 MOOT (F-4). A4b/A6 ledger-dependent (NOT-RUNNABLE without post-cutover rows). A5 NOT-RUN
    (no account-settings capture) — printed with last recorded values, not skipped silently."""
    r4 = Result("A4", "MOOT", detail="F-4 ruling — SENTINEL-SL1 struck; superseded by A9")
    if ledger_rows:
        r4b = _a4b(ledger_rows, bots, ops_set)
        r6 = _a6(ledger_rows, bots, ops_set)
    else:
        r4b = Result("A4b", "NOT-RUNNABLE", detail="no post-cutover ledger rows (broken-link stop-out needs a ledger)")
        r6 = Result("A6", "NOT-RUNNABLE", detail="no ledger rows; sizing primitive is fixed quantity:1 in the shared action")
    r5 = Result("A5", "NOT-RUN",
                detail="no account-settings capture supplied; last recorded itmpaper=market, "
                       "itmlive=auto, maxexits=0 — D2 is the Day-0 gate (stated, not skipped)")
    return [r4, r4b, r5, r6]


def _a4b(ledger_rows, bots, ops_set=None):
    """A4b: an arm whose config carries no stoploss but shows a day of stop-outs within minutes of
    open (the runtime fell back to the Default while the stored config still reads correct).

    ⛔ OPS-SCOPED (E-3 §3.3 item 6). TESTOPS-LAB-OPS *is* this signature by design — a deliberately
    loose entry rule plus daily closes — and it carries no stoploss in the seven-arm dict, so an
    unscoped A4b FAILs every day it trades with no broken link anywhere, permanently destroying the
    detector it exists to be."""
    flags = []
    ledger_rows, ops_line = _ops_scope(ledger_rows, ops_set)
    cfg_stop = {n: bool(bots[n]["mechanics"].get("stoploss")) for n in bots}
    by_bot_day = {}
    parse_errors = []
    for r in ledger_rows:
        # FIXED 2026-08-08 (self-test O4; authorized by Andy, orchestrator chat): was
        # `(_ts(c) - _ts(o)) <= 300` — a timedelta compared to an int raises TypeError
        # into a bare `except`, so every row read "not fast" and A4b could never fire.
        # Now: .total_seconds(); a missing/blank close_date (an OPEN position) is
        # legitimately not-fast; a PRESENT-but-unparseable date is a LOUD flag, never
        # a silent skip.
        od, cd = (r.get("open_date") or "").strip(), (r.get("close_date") or "").strip()
        if len(cd) < 19 or len(od) < 19:
            fast = False
        else:
            try:
                fast = (_ts(cd) - _ts(od)).total_seconds() <= 300
            except (ValueError, TypeError) as e:
                parse_errors.append(f"UNPARSEABLE date on {r.get('bot')} "
                                    f"open={od!r} close={cd!r} ({e}) — row NOT evaluated")
                fast = False
        if r.get("open_date", "")[:10] == r.get("close_date", "")[:10] and fast:
            by_bot_day.setdefault((r.get("bot"), r.get("open_date", "")[:10]), 0)
            by_bot_day[(r.get("bot"), r.get("open_date", "")[:10])] += 1
    for (bot, day), c in by_bot_day.items():
        if c >= 2 and not cfg_stop.get(bot, False):
            flags.append(f"{bot} {day}: {c} fast stop-outs, no stoploss in config")
    flags = parse_errors + flags   # unparseable dates are findings, never silence
    return Result("A4b", "FAIL" if flags else "PASS", 0 if flags else 1, 1,
                  "broken-input-link stop-out detector",
                  ([ops_line] if ops_line else []) + flags)


def _a6(ledger_rows, bots, ops_set=None):
    """⛔ OPS-SCOPED (E-3 §3.3 item 6). This iterates ALL ledger rows, not just GF-QQQ-IC-*; one
    TESTOPS-LAB-DSTOP row at qty 3 — the size its own unit test REQUIRES — turns the family's
    mandated sizing guard red on its first fill."""
    ledger_rows, ops_line = _ops_scope(ledger_rows, ops_set)
    bad = [f"{r.get('bot')} {r.get('open_date','')[:10]} qty={r.get('quantity')}"
           for r in ledger_rows if _num(r.get("quantity")) not in (1.0, 1)]
    return Result("A6", "FAIL" if bad else "PASS", 0 if bad else 1, 1,
                  "exactly 1 contract per leg per arm per day",
                  ([ops_line] if ops_line else []) + bad[:20])


def _ts(s):
    import datetime
    return datetime.datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")


# ===========================================================================
# §8.2 capture-diff (21 pairs, both G2 hops)
# ===========================================================================
def capture_diff_report(bots, pairs, ctrl):
    lines = ["  §8.2 CAPTURE-DIFF — 21 unordered pairs. Both G2 hops resolved on every arm:",
             "    hop1 action→automation-input {nid:root} = a REFERENCE, NOT read for config.",
             "    hop2 automation-input→BOT input {nid:bot, input:IN<this bot>} = the read end.",
             "    oldValue IGNORED everywhere (§1.2 rule 2)."]
    # prove hop2 resolves to this bot's own input id on each arm
    for n in [x for x in FAMILY if x in bots]:
        ids = [bots[n]["inputs"][s].get("id") for s in ("PUT", "CALL")]
        lines.append(f"    {n:22} bot inputs {ids} (read end; action ref & oldValue ignored)")
    lines.append(f"    control = {ctrl} (empty mechanic map)")
    by_type = {"arm-vs-control": 0, "shared-field": 0, "arm-vs-arm": 0}
    for _a, _b, ptype, _d, _e, p in pairs:
        by_type[ptype] += p
    lines.append(f"    PASS: arm-vs-control {by_type['arm-vs-control']}/6 · "
                 f"shared-field {by_type['shared-field']}/2 · arm-vs-arm {by_type['arm-vs-arm']}/13")
    return lines


# ===========================================================================
# §9 block extraction (for the A3 notes cross-check)
# ===========================================================================
def load_spec_blocks(spec_path):
    """Extract each arm's fenced §9 block (### GF-QQQ-IC-<Arm> … up to the closing ```)."""
    if not os.path.exists(spec_path):
        return {}
    text = open(spec_path, encoding="utf-8").read()
    blocks = {}
    for n in FAMILY:
        m = re.search(rf"(### {re.escape(n)}\n.*?)\n```", text, re.S)
        if m:
            blocks[n] = m.group(1)
    return blocks


# ===========================================================================
# Orchestration + reporting
# ===========================================================================
def run(captures, config, spec, ledger=None, as_json=False, bots_meta=None):
    bots, shared = load_captures(captures)
    config_a7 = load_config_a7(config) if config and os.path.exists(config) else {}
    spec_blocks = load_spec_blocks(spec) if spec else {}
    ledger_rows = None
    if ledger and os.path.exists(ledger):
        ledger_rows = [r for r in csv.DictReader(open(ledger))
                       if (r.get("status") or "").lower() == "closed"]
    ops_set = load_ops_set(bots_meta if bots_meta is not None else BOTS_META)
    missing = [n for n in FAMILY if n not in bots]

    r1, pairs, ctrl = a1_pairwise(bots)
    results = [r1, a2_nonbundle(bots), a3_prereg(bots, spec_blocks)]
    results += a4_a5_a6(ledger_rows, bots, ops_set)[:1]             # A4
    results += [a7_hashes(shared, config_a7), a8_symmetry(bots), a9_bound(bots)]
    a4b, a5, a6 = a4_a5_a6(ledger_rows, bots, ops_set)[1:]
    results += [a4b, a5, a6]
    order = {"A1": 0, "A2": 1, "A3": 2, "A4": 3, "A4b": 4, "A5": 5, "A6": 6, "A7": 7, "A8": 8, "A9": 9}
    results.sort(key=lambda r: order[r.name])
    diff_lines = capture_diff_report(bots, pairs, ctrl)

    # --- print ---
    print(f"A-SERIES DRIFT DETECTOR v{VERSION}  ⛔ STANDALONE / NOT WIRED into daily.sh")
    print(f"  captures: {len(bots)}/7 bots, {len(shared)}/3 shared automations"
          + (f"   ⚠ MISSING BOTS: {missing}" if missing else ""))
    if ops_set:
        print(f"  ops-class scoping ACTIVE (E-3 §3.3): {len(ops_set)} bot(s) excluded from "
              f"A4b/A6 — {sorted(ops_set)}")
    print()
    for r in results:
        tag = {"PASS": "✅", "FAIL": "🛑", "MOOT": "⚪", "NOT-RUNNABLE": "⏸", "NOT-RUN": "⏸"}[r.status]
        print(f"  {tag} {r.name:4} {r.status:12} {r.count():7} {r.detail}")
        for ln in r.lines:
            print(ln)
        drift = getattr(r, "drift", None)
        if drift:
            print("    ⛔ A7 DRIFT REPORT:")
            for d in drift:
                print(f"      {d['object']}: baseline {d['baseline_hash'][:16]}… (v{d['version_baseline']}) "
                      f"-> current {(d['current_hash'] or '')[:16]}… (v{d['version_current']}); "
                      f"delta: {d['field_delta']}")
    print()
    for ln in diff_lines:
        print(ln)

    red = [r for r in results if r.status == "FAIL"]
    print()
    if red:
        print(f"  🛑 FAMILY RED — {len(red)} assert(s) FAIL: {[r.name for r in red]}. "
              f"The family's ranking is VOID until re-based (§9 family-level kill).")
    else:
        print("  ✅ FAMILY GREEN — every runnable assert passes; A4 moot, A4b/A5/A6 pre-Day-0.")

    if as_json:
        print(json.dumps({"engine_version": VERSION, "wired": False,
                          "results": {r.name: {"status": r.status, "k": r.k, "n": r.n} for r in results},
                          "a7_drift": getattr(results[order["A7"]], "drift", [])}, indent=2))
    return 1 if red else 0


def validate(captures, config, spec):
    """Reproduce the hand-run reference EXACTLY, or fail loudly (a defect in the tool)."""
    bots, shared = load_captures(captures)
    config_a7 = load_config_a7(config)
    spec_blocks = load_spec_blocks(spec)
    r1, _pairs, _c = a1_pairwise(bots)
    got = {
        "A1": (r1.k, r1.n), "A2": _kn(a2_nonbundle(bots)), "A3": _kn(a3_prereg(bots, spec_blocks)),
        "A7": _kn(a7_hashes(shared, config_a7)), "A8": _kn(a8_symmetry(bots)), "A9": _kn(a9_bound(bots)),
    }
    rest = a4_a5_a6(None, bots)
    got["A4"], got["A4b"], got["A5"], got["A6"] = (rest[0].status, rest[1].status,
                                                   rest[2].status, rest[3].status)
    print(f"A-SERIES --validate  (reproduce data/captures/…/ASSERTS-A1-A9-and-capture-diff.txt)\n")
    fails = 0
    for key, want in REFERENCE.items():
        g = got[key]
        ok = g == want
        fails += not ok
        print(f"  {'PASS' if ok else 'FAIL'}  {key:4} got {g}  want {want}")
    # spot-checks: exitrate==1 all seven, Backstop ntime==1552, §9 note lengths
    spot = []
    spot.append(("exitrate==1 on all seven",
                 all(bots[n]["settings"].get("exitrate") == "1" for n in FAMILY if n in bots)))
    spot.append(("Backstop ntime==1552 on all seven",
                 all(bots[n]["trigger"].get("backstop_ntime") == "1552" for n in FAMILY if n in bots)))
    len_ok = all(spec_blocks.get(n) is not None
                 and (len(spec_blocks[n].encode("utf-16-le")) // 2) == RECORDED_NOTE_LEN[n]
                 for n in FAMILY if n in bots)
    spot.append(("§9 fenced-block UTF-16 lengths == recorded notes lengths", len_ok))
    for label, ok in spot:
        fails += not ok
        print(f"  {'PASS' if ok else 'FAIL'}  spot: {label}")
    print(f"\n  {'✅ REPRODUCED THE REFERENCE EXACTLY' if not fails else f'🛑 {fails} DIVERGENCE(S) — tool defect'}")
    return 1 if fails else 0


def _kn(r):
    return (r.k, r.n)


# ===========================================================================
# SELF-TEST — E-3 §3.3 item 6 ops-class scoping of A4b / A6.
# ⛔ SEPARATE FROM --validate ON PURPOSE. --validate reproduces the hand-run
# 2026-08-07 reference and its output must not move; these are new asserts
# about new behaviour and get their own flag.
# ===========================================================================
def _st_ledger(bot, day, qty="1", opened="09:46:00", closed="15:50:00"):
    return {"bot": bot, "quantity": qty, "status": "closed",
            "open_date": f"{day} {opened}", "close_date": f"{day} {closed}"}


def selftest():
    OPSBOT, DSTOP = "TESTOPS-LAB-OPS", "TESTOPS-LAB-DSTOP"
    fake_bots = {n: {"mechanics": {}} for n in FAMILY}          # control-like: no stoploss
    fails, results = 0, []

    def check(name, got, want):
        nonlocal fails
        ok = got == want
        fails += not ok
        results.append((ok, name, got, want))

    # A6 fixture: the family sized 1 (legal) + an ops bot sized 3 (its unit test REQUIRES 3)
    a6_rows = [_st_ledger(RIDE, "2026-09-01"), _st_ledger(PT50, "2026-09-01"),
               _st_ledger(DSTOP, "2026-09-01", qty="3")]
    # A4b fixture: the ops bot's own signature — 2 fast same-day closes, no stoploss in config
    a4b_rows = [_st_ledger(RIDE, "2026-09-01", closed="15:50:00"),
                _st_ledger(OPSBOT, "2026-09-01", opened="09:46:00", closed="09:48:00"),
                _st_ledger(OPSBOT, "2026-09-01", opened="10:10:00", closed="10:12:00")]
    ops = {OPSBOT, DSTOP}

    # ---- O1: the ops set comes from the COLUMN, never a tag or a name -----
    import tempfile, os as _os
    fd, mp = tempfile.mkstemp(suffix=".csv"); _os.close(fd)
    with open(mp, "w", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(["bot", "pillar", "role", "notes", OPS_CLASS_COL])
        w.writerow([OPSBOT, "Lab", "ops", "tags: experiment ops lab", OPS_CLASS_VALUE])
        w.writerow(["TESTOPS-LOOKALIKE", "IC", "experiment", "ops in the notes", ""])
        w.writerow([RIDE, "IC", "control", "", ""])
    try:
        check("O1  load_ops_set keys on the ops_class COLUMN only (name/notes ignored)",
              load_ops_set(mp), {OPSBOT})
        check("O1b a missing bots_meta.csv yields an empty set (pre-Lab state)",
              load_ops_set(mp + ".nope"), set())
    finally:
        _os.unlink(mp)

    # ---- O2/O3: A6 ---------------------------------------------------------
    r = _a6(a6_rows, fake_bots, None)
    check("O2  UNSCOPED A6 FAILs on the ops bot's qty=3 row (the defect E-3 names)",
          (r.status, any(DSTOP in l for l in r.lines)), ("FAIL", True))
    r = _a6(a6_rows, fake_bots, ops)
    check("O3  SCOPED A6 PASSes — the family's sizing guard survives",
          r.status, "PASS")
    check("O3b …and REPORTS the skip (never silent)",
          any("OPS-CLASS SCOPED OUT" in l and DSTOP in l for l in r.lines), True)

    # ---- O4/O5: A4b --------------------------------------------------------
    # O4 HISTORY: as written 2026-08-08 (Worker B) this test RECORDED a pre-existing
    # defect — timedelta<=int swallowed by a bare except made A4b structurally blind,
    # ("PASS", []) on rows it should have flagged. FIXED same day by the orchestrator
    # session at Andy's explicit "fix O4": predicate uses .total_seconds(), blank
    # close_date (open position) is legitimately not-fast, unparseable dates are LOUD
    # flags. O4 is now the POSITIVE control: the detector MUST fire on this fixture.
    r = _a4b(a4b_rows, fake_bots, None)
    check("O4  unscoped A4b FIRES on 2 fast same-day closes with no stoploss in config "
          "(predicate fixed 2026-08-08 — was structurally blind since birth)",
          (r.status, len(r.lines) == 1 and OPSBOT in r.lines[0]), ("FAIL", True))
    r = _a4b(a4b_rows, fake_bots, ops)
    check("O5  SCOPED A4b removes the ops rows from what the detector examines",
          any("2 of 3 ledger row(s) skipped" in l for l in r.lines), True)
    check("O5b …and REPORTS the skip, naming the bot (never silent)",
          any("OPS-CLASS SCOPED OUT" in l and OPSBOT in l for l in r.lines), True)

    # ---- O6: declared but absent from the ledger is still reported ---------
    r = _a6([_st_ledger(RIDE, "2026-09-01")], fake_bots, ops)
    check("O6  ops set declared with no ops rows in the ledger STILL reports the scoping",
          (r.status, any("OPS-CLASS SCOPED OUT" in l and "none" in l for l in r.lines)),
          ("PASS", True))

    # ---- O7: scoping must not blind the detector to the FAMILY -------------
    r = _a6(a6_rows + [_st_ledger(TRAIL, "2026-09-02", qty="2")], fake_bots, ops)
    check("O7  a REAL family violation still FAILs after scoping (not blinded)",
          (r.status, any(TRAIL in l for l in r.lines)), ("FAIL", True))
    r = _a4b(a4b_rows + [_st_ledger(SL100, "2026-09-02", opened="09:46:00", closed="09:47:00"),
                         _st_ledger(SL100, "2026-09-02", opened="10:00:00", closed="10:01:00")],
             fake_bots, ops)
    check("O7b scoping drops ONLY the ops rows — every family row still reaches A4b "
          "(2 of 5 skipped, the 3 family rows kept)",
          any("2 of 5 ledger row(s) skipped" in l for l in r.lines), True)

    # ---- O8: the pre-Day-0 / --validate path is untouched by ops scoping ---
    a = a4_a5_a6(None, fake_bots, ops)
    check("O8  ledger-less run is NOT-RUNNABLE for A4b/A6 regardless of ops set "
          "(--validate reference unmoved)",
          [x.status for x in a], ["MOOT", "NOT-RUNNABLE", "NOT-RUN", "NOT-RUNNABLE"])
    check("O8b an EMPTY ops set changes nothing (identical to the pre-E-3 behaviour)",
          (_a6(a6_rows, fake_bots, set()).status, _a6(a6_rows, fake_bots, None).status,
           _a6(a6_rows, fake_bots, set()).lines == _a6(a6_rows, fake_bots, None).lines),
          ("FAIL", "FAIL", True))

    print("SELF-TEST — E-3 §3.3 item 6 OPS-CLASS SCOPING (a_series.py A4b / A6)")
    print("=" * 74)
    for ok, name, got, want in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"        got  {got!r}\n        want {want!r}")
    print("-" * 74)
    print(f"{len(results) - fails}/{len(results)} passed")
    return 1 if fails else 0


# ===========================================================================
# ⬇⬇⬇  daily.sh WIRING SNIPPET — EMITTED AS A COMMENT ONLY. NOT APPLIED. ⬇⬇⬇
# Wiring is a Day-0-adjacent decision (reactivation-runbook.md §4 Step 4(b)); this tool does not
# edit daily.sh. When Andy rules to wire it, insert as a stage AFTER the numeric stages, fail RED:
# ---------------------------------------------------------------------------
WIRING_SNIPPET = r"""
# === stage N of N: A-SERIES ARM-DISTINCTNESS + A7 DRIFT (greenfield family) ===
# Runbook §4 Step 4(b): A7 is the ONLY detector of a shared-automation edit. No baseline / no
# runner = no detector for the whole sample -> those bots stay OFF.
echo "== A-series drift detector =="
if python3 scripts/a_series.py \
        --captures "$LATEST_CAPTURES_DIR" \
        --config data/bots_config_v2.csv \
        --spec docs/greenfield-family-spec.md \
        --ledger data/trades.csv ; then
    echo "A-SERIES: GREEN"
else
    echo "A-SERIES: 🛑 RED — family ranking VOID, arms held. See brief." >&2
    BRIEF_RED=1                 # surface RED in the three-verdict brief
fi
"""
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="A-series greenfield drift detector (STANDALONE, not wired).")
    ap.add_argument("--captures", nargs="+", default=[os.path.join(DATA, "captures")])
    ap.add_argument("--config", default=os.path.join(DATA, "bots_config_v2.csv"))
    ap.add_argument("--spec", default=os.path.join(ROOT, "docs", "greenfield-family-spec.md"))
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--bots-meta", default=BOTS_META,
                    help="ops-class declaration source (E-3 §3.3); scopes A4b/A6")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--selftest", action="store_true",
                    help="run the E-3 §3.3 ops-scoping tests and exit")
    ap.add_argument("--emit-wiring", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.emit_wiring:
        print(WIRING_SNIPPET)
        sys.exit(0)
    if a.selftest:
        sys.exit(selftest())
    if a.validate:
        sys.exit(validate(a.captures, a.config, a.spec))
    sys.exit(run(a.captures, a.config, a.spec, a.ledger, a.json, a.bots_meta))
