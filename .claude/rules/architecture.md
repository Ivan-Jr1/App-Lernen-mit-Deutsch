## Git

- **ALWAYS** use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`).
- **ALWAYS** summarize what changed as a bullet list in the commit body when the change touches more than one file or concern — one bullet per distinct change, each starting with a verb. Skip the body for small, single-concern commits where the subject line already says it all.
- **NEVER** add a Claude/AI co-author line to commits.
- **NEVER** commit changes without the user's explicit permission. Always wait until the user requests the commit.


## General code quality principles

- **ALWAYS** write Clean Code: optimize for readability and a low-effort read over cleverness or brevity.
- **ALWAYS** use type hints/type annotations for function parameters and return values, in languages that support them.
- **ALWAYS** keep function-level comments to a single sentence, max 2 lines — comments explain *why*, not *what*.
- **ALWAYS** write identifiers (function/variable names) in English, even in files or commit messages written in another language.
- **ALWAYS** apply SOLID as guidance for individual functions and modules (single responsibility, small well-named surfaces) — **not** as a mandate to add service/repository/use-case layers where the codebase's established pattern doesn't already have them. Match the shape the codebase already uses rather than imposing a different architectural style during an unrelated change.
- **ALWAYS** apply DRY *within* a single codebase or independently-deployed service. This does **not** mean forcing a shared import across codebases that deploy independently (e.g. a monorepo's separate services/packages) — duplication across those boundaries is often intentional, not a violation; each side keeps its own copy.
- **ALWAYS** use KISS — prefer the direct, obvious implementation over a generic/configurable one built for requirements that don't exist yet. No speculative abstraction "for later," no premature optimization.
- **ALWAYS** aim for performance, but only as a side effect of simplification (e.g., removing a redundant loop or an extra round-trip) — never a micro-optimization that trades away readability for a marginal gain.
- **NEVER** let conditional/loop nesting run more than 2–3 levels deep; prefer early returns instead.
- **ALWAYS** split a function when it clearly does more than one separable thing — but don't split purely to shrink line count if it fragments a linear, top-to-bottom read. Match the codebase's existing decomposition style rather than over-decomposing.
- **ALWAYS** unify duplicated logic *within* a codebase into one shared function/module instead of copy-pasting a near-identical second version next to it.
- **ALWAYS** simplify expressions and use language idioms (comprehensions, safe-navigation/optional chaining, f-strings/template literals, etc.) when they reduce actual logical complexity — not merely character count.
- **Prioritization**: when these principles compete, or time is limited, weigh maintenance impact × regression risk and take the highest-return, lowest-risk change first.


## Change scope

- **NEVER** change business rules, contracts (request/response shapes, permission checks), or directory structure as a side effect of an unrelated cleanup or refactor — those require an explicit, separate ask.
- **NEVER** add a new external dependency without stating the justification (what it replaces, why an existing dependency or the stdlib doesn't already cover it).


## Codebase boundaries (monorepos)

- **NEVER** import across codebases/services that deploy independently within a monorepo. If two independently-deployed parts need the same logic, duplicate the module rather than sharing one import — a shared import creates an accidental deploy-time coupling between things meant to ship separately.


## API routes & request handlers

- **ALWAYS** parse/validate incoming request bodies through the project's existing parsing/validation helper rather than reading raw request data ad hoc in each handler.
- **ALWAYS** update any explicit route registry/config the framework requires (a router table, gateway route, `urls.py`, etc.) in the same change that adds a handler — a handler with no matching registration fails silently (404/whatever the framework's default is) instead of erroring loud.
- **ALWAYS** perform authorization/permission checks as the first statement in a request handler, returning the failure response immediately — don't bury access checks after other logic has already run.


## Documentation

- **ALWAYS** keep documentation in lockstep with the code it describes — a change that alters documented behavior (a route, an env var, a config key, a business rule) updates the relevant doc in the same change, not as a follow-up.
- **ALWAYS** favor a spec-driven shape for non-trivial design work — write the problem statement and requirements down *before* the implementation, not as a changelog written after the fact.
