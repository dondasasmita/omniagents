# omniagents-unknowns

The map is not the territory. Your prompt is the map; the codebase or domain is
the territory; the gap between them is made of unknowns — and the expensive
kind, the unknown unknowns, cannot be reached by asking you questions, because
you don't know to ask them. This plugin packages two counter-moves, each a pass
that runs before the work and ends in a prompt you couldn't have written
without it:

- a **blindspot pass**, which surveys the territory first and reports back what
  you didn't know to ask;
- a **depth pass**, which asks what a top professional in the field would do
  with your task — and rewrites it to ask for exactly that, deeper rather than
  bigger.

## Skills

| Skill                                | Invocation                                          |
| ------------------------------------ | --------------------------------------------------- |
| `omniagents-unknowns:blindspot-pass` | `/blindspot-pass <task or area> + your familiarity` |
| `omniagents-unknowns:depth-pass`     | `/depth-pass <the prompt or task to deepen>`        |

Both also trigger on their own. The blindspot pass answers "blindspot pass",
"unknown unknowns", "what am I missing", or "I'm new to this codebase/domain —
help me prompt you better." The depth pass answers "I want a deeper version of
this, not a bigger one", "what would a top professional do here", or "upgrade
my prompt before I run it."

## Blindspot pass

A blindspot pass is reconnaissance, not implementation:

- Fixes the frame: what you're trying to do and how familiar you already are.
- Surveys the territory — codebase (modules, history, conventions, tests) or
  domain (vocabulary, tooling, what good looks like) — before asking you
  anything.
- Reports 3–7 blindspots, deltas only, ranked by whether they would change what
  you ask for — each as a card you keep or drop, grounded in a cited file, with
  the question it unlocks.
- Ends with the payoff: a rewritten prompt you couldn't have written before the
  pass.

It distinguishes the four quadrants of unknowns — known knowns, known unknowns,
unknown knowns, unknown unknowns — because each needs a different move:
interviews only reach what you already know to ask; prototypes surface what
you'd recognize on sight; only surveying the territory reaches the rest.

By default the pass stops at planning. When the work moves into the build, a
review, or a merge, the same lens extends through an optional companion — a
deviation log, a buy-in doc, a merge-readiness quiz — in
`references/after-the-pass.md`.

## Depth pass

Most prompts arrive pre-digested: they name a deliverable and inherit a
generalist's picture of how to produce it. Asked to do better, a model's reflex
is to do more — more sections, more features, more caveats. A depth pass keeps
the deliverable and changes how it is made. Before rewriting your prompt it
answers four questions:

1. What would a top professional in this field do here that you're not asking
   for? — a named practitioner and the moves routine to them, not "be
   rigorous".
2. What is the rawest material they would start from, instead of what has
   already been digested for you? — the event rows, not the dashboard; the
   trials, not the coverage.
3. Which specific methods and tools would they use? — each tied to the step it
   serves.
4. What, other than the model or you, would show the result is right? — a
   check that can fail: a test, a reconciliation, a recorded baseline, a
   falsifiable prediction.

Then it rewrites your prompt to ask for exactly that, and a size test keeps it
honest: the rewrite may add steps, never deliverables. Trivial tasks get one
line and the missing piece instead of the full pass.

## Which pass?

- New to the territory and unsure what to ask → **blindspot pass**.
- You can state the task, and want it done the way the best practitioner would
  do it → **depth pass**.
- Both → blindspot pass first; its rewritten prompt is a good input to the
  depth pass.

## Layout

```text
skills/
  blindspot-pass/
    SKILL.md                 # the pass, loaded by /blindspot-pass
    references/
      after-the-pass.md      # optional: during / after-build moves
  depth-pass/
    SKILL.md                 # the pass, loaded by /depth-pass
evals/
  evals.json                 # depth-pass scenarios: depth vs. scope assertions
  README.md                  # what the evals measure and how to run them
```

## Installation

```bash
claude plugin install omniagents-unknowns@omniagents
```

## Usage

```text
/blindspot-pass adding a Slack notifications plugin — never touched this repo
/blindspot-pass migrating the auth module to OIDC; I know our auth code well but not OIDC
/blindspot-pass color-grading this video — I don't know what color grading is
/depth-pass speed up our /search endpoint, users say it's slow
/depth-pass write a short post for leadership on why churn rose last quarter
/depth-pass summarize the research on creatine and memory in healthy adults
```

## Credits

The four-quadrant unknowns framing and the map-vs-territory lens come from
[Thariq Shihipar (ThariqS)](https://github.com/ThariqS) of Anthropic's Claude
Code team — see his
[Know your unknowns examples](https://thariqs.github.io/html-effectiveness/unknowns/).
The reactable-report shape sharpens three moves from
[dzhng's explore-unknowns](https://github.com/dzhng/skills/blob/main/skills/engineering/explore-unknowns/SKILL.md):
artifacts you react to instead of describe, a report that assembles your next
message, and citing the files the survey actually read. This plugin packages
that workflow as a focused, single-pass Claude Code skill.

The depth pass's four questions are Felix Rieseberg's, from
[How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/),
where depth is one of four kinds of ambition alongside speed, altitude, and
range. The skill adds the guards: the size test, the named practitioner, the
digestion ladder, step-bound methods, and the catalogue of outside checks.
