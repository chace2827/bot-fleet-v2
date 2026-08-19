#!/usr/bin/env bash
# devin-free — the ONLY sanctioned way this project invokes Devin.
#
# WHY THIS EXISTS
# ---------------
# On 2026-08-19 a narrow permission rule was granted in the form
#   Bash(/Applications/.../devin/bin/devin -p --model swe-1-7:*)
# on the theory that it would permit the free model and deny paid ones. It does
# neither reliably. Two invocations were SEEN to pass that rule:
#   devin -p --model swe-1-7-lightning   ($2.5 / $12.5 per MTok)
#   devin -p --model claude-opus-5       ($5 / $25 per MTok, banned outright)
# The first slips through because "swe-1-7-lightning" begins with "swe-1-7", so
# it satisfies a prefix match. The second shares no prefix at all and passed
# anyway, which means the matcher does not bind the --model argument. A rule
# that has not been seen to deny something is not a guard.
#
# The fix is structural, not behavioural: the model is not an argument any more.
# This wrapper hardcodes it, and the raw binary is not granted. The guarantee no
# longer depends on anyone typing the right flag.
#
# INSTALL
#   canonical (committed):  scripts/devin_free.sh
#   installed (executable): ~/bin/devin-free
# The installed copy lives OUTSIDE the repo on purpose: fleet agents edit /tmp
# clones and cannot reach ~/bin, so an agent cannot edit the thing that
# constrains it. The two copies must be byte-identical -- assert before every
# wave with `devin-free --selfhash` against `shasum -a 256 scripts/devin_free.sh`.
#
# USAGE
#   devin-free [flags...] -- "prompt"     # -p and --model swe-1-7 are supplied
#   devin-free --selfhash                 # print sha256 of this file and exit 0
#
# REFUSES, without invoking anything, if argv contains --model, -r/--resume, or
# --config, in either spelling (`--flag value` or `--flag=value`).
set -euo pipefail

DEVIN_BIN="/Applications/Devin.app/Contents/Resources/app/extensions/windsurf/devin/bin/devin"
MODEL="swe-1-7"          # SWE-1.7 Max. Free. The only model this wrapper will run.
SELF="${BASH_SOURCE[0]}"

die() { printf 'devin-free: %s\n' "$*" >&2; exit 2; }

self_sha() { shasum -a 256 "$SELF" | awk '{print $1}'; }

if [ "${1:-}" = "--selfhash" ]; then
    printf '%s  %s\n' "$(self_sha)" "$SELF"
    exit 0
fi

# ---------------------------------------------------------------- refusals
# Checked BEFORE anything is invoked. Each blocked flag is matched in both
# spellings, because `--model=opus` is a single argv token that is not equal to
# `--model` and would sail past a naive equality test.
for arg in "$@"; do
    case "$arg" in
        --model|--model=*)
            die "REFUSED: --model is not yours to set. This wrapper runs ${MODEL} (free) and nothing else.
       Passing a model is how paid inference gets billed by accident: swe-1-7-lightning is
       \$2.5/\$12.5 per MTok and any claude-*/gpt-* alias is banned outright by dispatch §2." ;;
        -r|--resume|--resume=*)
            die "REFUSED: -r/--resume is prohibited. Resuming re-enters a session whose model and
       permission mode were fixed elsewhere, so this wrapper's guarantee would not apply to it." ;;
        --config|--config=*)
            die "REFUSED: --config can redirect credentials, model defaults and workspace-trust
       settings, which would silently reopen everything this wrapper closes." ;;
    esac
done

[ -x "$DEVIN_BIN" ] || die "devin binary missing or not executable: $DEVIN_BIN"

# Provenance goes to stderr on every run, so any transcript that contains a
# dispatch also contains proof of which wrapper version produced it.
printf 'devin-free: sha256 %s | model %s (free)\n' "$(self_sha)" "$MODEL" >&2

exec "$DEVIN_BIN" -p --model "$MODEL" "$@"
