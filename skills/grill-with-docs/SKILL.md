---
name: grill-with-docs
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases. Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* a context file for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Treat domain-model files as durable project documentation. For new work, follow `project-layout`: put context files under `docs/domain/`, ADRs under `docs/adr/`, and keep root files only for tool-required controls such as `AGENTS.md` or ecosystem configuration.

Most repos have a single context:

```
/
├── docs/
│   ├── domain/
│   │   └── CONTEXT.md
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `docs/domain/CONTEXT-MAP.md` exists, the repo has multiple contexts. The map points to where each one lives:

```
/
├── docs/
│   ├── domain/
│   │   ├── CONTEXT-MAP.md
│   │   ├── ordering/
│   │   │   └── CONTEXT.md
│   │   └── billing/
│   │       └── CONTEXT.md
│   └── adr/
│       ├── 0001-system-wide-decision.md
│       ├── ordering/
│       │   └── 0001-ordering-decision.md
│       └── billing/
│           └── 0001-billing-decision.md
├── src/
│   ├── ordering/
│   └── billing/
```

Create files lazily — only when you have something to write. If no context file exists, create `docs/domain/CONTEXT.md` when the first term is resolved. If no ADR directory exists, create the relevant `docs/adr/` directory when the first ADR is needed.

On an existing repo, recognize legacy root files such as `CONTEXT.md` and `CONTEXT-MAP.md`, or legacy context-local ADR directories, and keep using the established tree rather than creating a parallel canonical one. Migrate only when the user asks or the task includes reorganization.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in the relevant context file, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update context files inline

When a term is resolved, update the relevant `docs/domain/.../CONTEXT.md` file right there. Don't batch these up — capture them as they happen. Use the format:

# Context file format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

## Single vs multi-context repos

**Single context (most repos):** One `docs/domain/CONTEXT.md`.

**Multiple contexts:** A `docs/domain/CONTEXT-MAP.md` lists the contexts, where they live, and how they relate to each other:

```md
# Context Map

## Contexts

- [Ordering](./ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

The skill infers which structure applies:

- If `docs/domain/CONTEXT-MAP.md` exists, read it to find contexts
- If `docs/domain/CONTEXT.md` exists, use the single context
- If legacy root `CONTEXT-MAP.md` or `CONTEXT.md` exists, keep using that established structure
- If neither exists, create `docs/domain/CONTEXT.md` lazily when the first term is resolved

When multiple contexts exist, infer which one the current topic relates to. If unclear, ask.

Context files should be totally devoid of implementation details. Do not treat them as specs, scratch pads, or repositories for implementation decisions. They are glossaries and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format:

# ADR Format

ADRs live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Use `docs/adr/` for system-wide decisions and `docs/adr/<context-slug>/` for context-specific decisions.

Create the relevant `docs/adr/` directory lazily — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

## Numbering

Scan the target ADR directory for the highest existing number and increment by one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it — otherwise someone will suggest GraphQL again in six months.
