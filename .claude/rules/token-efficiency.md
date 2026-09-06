## Editing & showing code

- **NEVER** reprint a whole file after an edit. Once `Edit`/`Write` succeeds, show only the changed lines (or just confirm the edit) — don't read the file back and paste it in full to "prove" the change worked.
- **ALWAYS** prefer a diff-style snippet over a full file listing when presenting a code change: quote the modified block plus 1-2 lines of surrounding context, not the entire file.
- **ALWAYS** reference existing code by `path:line` instead of pasting it verbatim when the user can open the file themselves.

## Planning & repeated context

- **NEVER** restate a plan the user already approved earlier in the same conversation before executing it — proceed directly, with at most a one-line "starting X."
- **NEVER** re-explain architecture, conventions, or decisions already established earlier in the conversation unless the user asks again or something actually changed.
- **NEVER** re-read a file already read earlier in the conversation unless it may have changed since (e.g. after an edit by another tool/process) — reuse what's already in context.

## Examples & tool output

- **ALWAYS** cap illustrative examples at 1 per concept, unless the user explicitly asks for more or a single example is genuinely ambiguous.
- **NEVER** paste raw, full command output (test runs, lint, build logs, `git diff` of unrelated files) into a response — extract and quote only the failing/relevant lines.
- **ALWAYS** keep exploratory searches targeted (`grep` for a symbol, `Read` with a line range) instead of opening whole directories or large files speculatively.
