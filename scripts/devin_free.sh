#!/usr/bin/env bash
# devin-free v2 — the ONLY sanctioned way this project invokes Devin.
#
# WHY THIS EXISTS (v1)
# --------------------
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
# WHAT v2 ADDS (step 6 ruling, 2026-08-19)
# -----------------------------------------
# Devin refuses untrusted workspaces, which blocked every /tmp clone. The ruling
# was NOT to disable trust globally and NOT to touch Andy's real Devin config.
# Instead the config is hardcoded the same way the model is: this wrapper writes
# and passes its OWN scratch config carrying skip_workspace_trust, and --config
# stays refused from argv. Callers can set neither.
#
# ⛔ AND THE POINT OF v2, NOT A SIDE EFFECT — THE CWD GUARD.
# Workspace trust was the ONLY thing standing between a wrapper invocation and a
# Devin session loose in the live repo: /Users/andrewchace/bot-fleet-v2 is
# ALREADY in trusted_paths. The moment skip_workspace_trust is in play that
# protection is gone. So v2 refuses, above exec, exit 2, to run anywhere inside
# the live tree or the git store. Turning a guard off requires replacing it.
#
# CONFIG SEPARATION — stated here so it is reviewable without reading the code
# ---------------------------------------------------------------------------
#   THIS WRAPPER'S config, created if absent, repaired only if the trust key is
#   missing, and the only config this script ever opens:
#       ~/.local/share/devin-free-lane/config.json
#   ANDY'S REAL Devin config and state — NEVER read, NEVER written, NEVER passed
#   by this script. They appear below only inside self-check refusals:
#       ~/.config/devin/config.json        (global CLI config)
#       ~/.local/share/devin/              (CLI state, incl. trusted_workspaces.json,
#                                           which is SHARED ACROSS LANES — another
#                                           lane restoring it has silently un-trusted
#                                           this lane's clone mid-run before)
#   The scratch config lives outside the repo AND outside both of the above. The
#   script asserts that at run time rather than trusting this comment.
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
#   devin-free [flags...] -- "prompt"        # -p, --model and --config are supplied
#   devin-free --workspace DIR [flags] -- "prompt"
#   devin-free --selfhash                    # print sha256 of this file and exit 0
#
# --workspace exists because the permission grant is a PREFIX match on this
# script's path: `cd DIR && devin-free ...` does not match it and falls through
# to the classifier. So the wrapper owns the chdir too, and the cwd guard is
# applied to the RESOLVED target — pointing --workspace at the live tree is
# refused exactly like standing in it.
#
# REFUSES, without invoking anything, if argv contains --model, -r/--resume, or
# --config, in either spelling (`--flag value` or `--flag=value`).
set -euo pipefail

DEVIN_BIN="/Applications/Devin.app/Contents/Resources/app/extensions/windsurf/devin/bin/devin"
MODEL="swe-1-7"          # SWE-1.7 Max. Free. The only model this wrapper will run.
SELF="${BASH_SOURCE[0]}"

FREE_CONFIG_DIR="$HOME/.local/share/devin-free-lane"
FREE_CONFIG="$FREE_CONFIG_DIR/config.json"
FREE_CONFIG_BODY='{"skip_workspace_trust": true}'

REAL_CONFIG="$HOME/.config/devin/config.json"   # never opened by this script
REAL_CONFIG_DIR="$HOME/.config/devin"           # never opened by this script
REAL_STATE_DIR="$HOME/.local/share/devin"       # never opened by this script

# Directories this wrapper will not run in, at any depth. The first two are the
# step-6 ruling. The third is added by this script's author: ~/bot-fleet is the
# permanent READ-ONLY archive (CLAUDE.md §8) and the same argument applies.
GUARDED_ROOTS="$HOME/bot-fleet-v2
$HOME/gitstore
$HOME/bot-fleet"

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
WORKSPACE=""
ARGS=()
while [ $# -gt 0 ]; do
    case "$1" in
        --model|--model=*)
            die "REFUSED: --model is not yours to set. This wrapper runs ${MODEL} (free) and nothing else.
       Passing a model is how paid inference gets billed by accident: swe-1-7-lightning is
       \$2.5/\$12.5 per MTok and any claude-*/gpt-* alias is banned outright by dispatch §2." ;;
        -r|--resume|--resume=*)
            die "REFUSED: -r/--resume is prohibited. Resuming re-enters a session whose model and
       permission mode were fixed elsewhere, so this wrapper's guarantee would not apply to it." ;;
        --config|--config=*)
            die "REFUSED: --config is not yours to set. This wrapper supplies its own scratch config
       (${FREE_CONFIG}). A caller-supplied config can redirect credentials, model
       defaults and workspace trust, which would silently reopen everything this wrapper closes." ;;
        --workspace)
            [ $# -ge 2 ] || die "REFUSED: --workspace needs a directory argument."
            WORKSPACE="$2"; shift 2 ;;
        --workspace=*)
            WORKSPACE="${1#--workspace=}"; shift ;;
        *)
            ARGS+=("$1"); shift ;;
    esac
done

# ---------------------------------------------------------------- cwd guard
# Resolved with `pwd -P` on both sides so /tmp -> /private/tmp, symlinked homes
# and `..` cannot walk a caller into the live tree behind the guard's back.
if [ -n "$WORKSPACE" ]; then
    [ -d "$WORKSPACE" ] || die "REFUSED: --workspace is not a directory: $WORKSPACE"
    TARGET="$(cd "$WORKSPACE" && pwd -P)"
else
    TARGET="$(pwd -P)"
fi

while IFS= read -r root; do
    [ -n "$root" ] || continue
    if [ -d "$root" ]; then root_p="$(cd "$root" && pwd -P)"; else root_p="$root"; fi
    case "$TARGET" in
        "$root_p"|"$root_p"/*)
            die "REFUSED: this wrapper will not run inside ${root_p}.
       Target was: ${TARGET}
       v2 passes skip_workspace_trust, so Devin's own workspace-trust check — which is what
       has been stopping runs in the live tree — no longer fires. ${root_p} is already in
       trusted_paths, so nothing else stands between this invocation and a Devin session
       loose in it. Run in a disposable clone and open a PR; that is the only sanctioned path." ;;
    esac
done <<GUARDS
$GUARDED_ROOTS
GUARDS

[ -x "$DEVIN_BIN" ] || die "devin binary missing or not executable: $DEVIN_BIN"

# ------------------------------------------------- this wrapper's own config
# Self-check first: prove the path we are about to write is not Andy's. This is
# an assertion, not a comment — if someone edits FREE_CONFIG to point at the
# real config, the script refuses instead of clobbering it.
case "$FREE_CONFIG" in
    "$REAL_CONFIG"|"$REAL_CONFIG_DIR"/*|"$REAL_STATE_DIR"/*)
        die "REFUSED (self-check): scratch config path ${FREE_CONFIG} is inside Andy's real Devin
       config/state. This script never reads or writes those." ;;
esac
for root in $HOME/bot-fleet-v2 $HOME/gitstore $HOME/bot-fleet; do
    case "$FREE_CONFIG" in
        "$root"/*) die "REFUSED (self-check): scratch config ${FREE_CONFIG} is inside ${root}.
       It must live outside every repo so no agent can reach the thing that constrains it." ;;
    esac
done

# Idempotent: created if absent, otherwise left alone unless the trust key is
# missing or false.
#
# It is deliberately NOT rewritten whenever its content differs from the literal
# above, which is what the first draft of v2 did. Observed on the first real run
# (session brook-trilby, 2026-08-19): the CLI WRITES BACK into whatever config it
# is handed, adding version / devin.org_id / shell.setup_complete / theme_mode.
# Resetting that every run would re-trigger the CLI's first-run banner
# ("Welcome to Devin CLI! ... You're all set.") into the stdout of every single
# dispatch, where a fleet parser reads it as agent output.
mkdir -p "$FREE_CONFIG_DIR"
if [ ! -f "$FREE_CONFIG" ]; then
    printf '%s\n' "$FREE_CONFIG_BODY" > "$FREE_CONFIG"
    chmod 600 "$FREE_CONFIG"
elif ! grep -q '"skip_workspace_trust"[[:space:]]*:[[:space:]]*true' "$FREE_CONFIG"; then
    # The one thing this wrapper guarantees about the file has been lost. Repair
    # it to the minimum; the CLI will re-add its own state on the next run.
    printf '%s\n' "$FREE_CONFIG_BODY" > "$FREE_CONFIG"
    chmod 600 "$FREE_CONFIG"
fi

# Provenance goes to stderr on every run, so any transcript that contains a
# dispatch also contains proof of which wrapper version produced it. It is the
# LAST thing above exec on purpose: its absence from a transcript is a per-run
# marker that no invocation occurred.
cd "$TARGET"
printf 'devin-free: v2 sha256 %s | model %s (free) | config %s | workspace %s\n' \
    "$(self_sha)" "$MODEL" "$FREE_CONFIG" "$TARGET" >&2

exec "$DEVIN_BIN" -p --model "$MODEL" --config "$FREE_CONFIG" ${ARGS[@]+"${ARGS[@]}"}
