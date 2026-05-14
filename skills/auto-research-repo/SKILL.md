---
name: auto-research-repo
description: Create, audit, maintain, ingest into, query, or draft from an auto-research repository organized around immutable raw sources, a freeform notebook or scratchpad, an LLM-maintained wiki, manifests, a temporary ingest tray, a source wishlist, and a portable HTML publication corpus with exploratory and treatise lanes. Use when Codex needs to author a new research repo, clean up repo instructions, process newly provided sources, capture rough project thoughts, consolidate research notes, turn evidence into wiki pages, create exploratory publications, or move mature wiki synthesis toward a treatise.
---

# Auto-Research Repo

Use this skill to work in repositories whose purpose is cumulative research, not one-off answers. Preserve source evidence, compile it into a durable wiki, and publish portable HTML outputs only when their evidence status is clear.

## Core Pattern

Follow a one-way pipeline:

`raw/` -> `wiki/` -> `corpus/`

- Keep `raw/` as immutable evidence: papers, datasets, scans, archives, source bundles, and provenance records.
- Keep `notebook/` as a mutable scratchpad for rough project thoughts, hunches, outlines, dead ends, meeting notes, copied snippets, prompts, and other useful junk that is not yet evidence or synthesis.
- Keep `wiki/` as the maintained synthesis layer: concepts, entities, source notes, evidence maps, questions, conjectures, contradictions, and paper seeds.
- Keep `corpus/` as the publication output lane, with `corpus/index.html` as the public table of contents.
- Use `corpus/exploratory/` for publishable working reports, labs, evidence browsers, and conjecture pressure tests.
- Use `corpus/treatise/` for mature paper-shaped publications promoted from wiki synthesis, not as the starting point.
- Keep `ingest/` as a temporary intake tray for user-provided files.
- Keep `WISHLIST.md` or an equivalent source queue for missing, blocked, paywalled, or strategically important sources.

Adapt names to the repository if it already uses different but equivalent folders. Treat `scratchpad/`, `thoughts/`, `notes/`, or an equivalent project notebook as the same layer as `notebook/`.

## Start By Reading The Repo

Before changing anything:

1. Inspect the folder structure with `rg --files`, `find`, or existing project docs.
2. Read local instructions such as `AGENTS.md`, `README.md`, `SKILL.md`, schema files, `raw/README.md`, `notebook/README.md`, `wiki/index.md`, `wiki/log.md`, and manifest examples.
3. Infer existing naming conventions, link syntax, manifest fields, and log style from current files.
4. Prefer existing patterns over the generic defaults in this skill.

If the repo is new or incomplete, create the smallest useful scaffold:

- `raw/`
- `raw/manifests/`
- `notebook/`
- `notebook/README.md`
- `wiki/`
- `wiki/index.md`
- `wiki/log.md`
- `ingest/`
- `corpus/`
- `corpus/index.html`
- `corpus/exploratory/`
- `corpus/treatise/`
- `WISHLIST.md`

## Notebook Workflow

Use the notebook as a deliberately low-friction workbench.

- Put messy, mutable, informal material in `notebook/`: stray observations, half-formed arguments, reading plans, temporary outlines, prompts, conversation notes, false starts, and things the user wants to remember without hardening into the wiki.
- Prefer lightweight dated or topic files when creating new notebook entries, but do not over-organize it. The folder is allowed to be rough.
- Do not treat notebook notes as evidence. If a notebook idea matters, connect it back to `raw/`, a manifest, a source page, or a wishlist entry before using it for a strong claim.
- Do not cite notebook notes in publications as if they were sources. Promote useful material into `wiki/` once it becomes durable synthesis, and cite the underlying evidence there.
- Preserve the user's voice and intent in personal notes. Clean up, split, or move notebook material only when asked or when promoting selected ideas into the wiki.
- Search `notebook/` for leads, open questions, and user hunches, but distinguish those from sourced wiki claims.
- Log only meaningful promotions from `notebook/` into `wiki/`, `WISHLIST.md`, or `corpus/`; routine scribbling does not need a wiki log entry.

## Raw Source Rules

Treat raw sources as evidence.

- Do not edit downloaded or user-provided source files in place.
- Rename archived files descriptively unless their original names are already clear.
- Prefer names like `YYYY-author-short-title.ext` for papers and stable descriptive names for datasets.
- Store datasets with enough surrounding metadata to make later analysis reproducible.
- Record provenance before relying on a source for claims.
- Use checksums, preferably SHA-256, for archived files.

For each source batch, update or create a manifest. Include, when available:

- final file path
- citation or source title
- source URL, DOI, archive location, or user-provided provenance
- retrieval or ingest date
- checksum
- page count, row count, file inventory, or other shape notes
- why the source matters
- suggested wiki targets

## Ingest Workflow

When files appear in `ingest/`:

1. Identify each file and its best bibliographic or dataset description.
2. Rename it according to repo conventions.
3. Move it into the appropriate immutable `raw/` lane.
4. Update the relevant manifest with provenance and checksum.
5. If it satisfies a wishlist entry, mark that entry found with date, final path, and manifest or checksum reference. Preserve the historical search trail.
6. Update enough wiki pages that the source is discoverable.
7. Append a dated entry to `wiki/log.md`.
8. Leave `ingest/` empty except for placeholders.

Ask the user to place manually sourced files into `ingest/` when a source is blocked, paywalled, unavailable, or needs human retrieval.

## Wiki Workflow

Use the wiki as cumulative working memory.

- Compile each important source, observation, dataset, concept, entity, hypothesis, and contradiction once.
- Add or update source pages for important raw files or datasets.
- Add or update concept/entity pages for reusable domain knowledge.
- Add or update synthesis pages for cross-source arguments, evidence maps, tensions, conjectures, and teardowns.
- Keep `wiki/index.md` current as the navigation hub.
- Keep `wiki/log.md` as a dated record of ingest, query, synthesis, artifact, exploratory-publication, and treatise work.
- Keep source-corpus or bibliography pages aligned with the raw corpus when the repo has them.
- Use the repo's link syntax. If none exists, use normal Markdown links or Obsidian-style `[[page|label]]` consistently.

Strong claims need citations to raw files, manifests, source pages, or datasets. If the evidence is missing, add a wishlist entry instead of presenting the claim as settled.

## Wishlist Workflow

Maintain the wishlist as a historical source-acquisition queue.

Open entries should include:

- priority
- citation, dataset name, archival target, or best-known description
- why it matters
- attempted locations or failure modes
- likely destination under `raw/`

Found entries should keep the original search trail and add:

- date found
- final raw path
- source route or user-provided provenance
- checksum or manifest reference when available

Do not delete fulfilled entries unless the repo explicitly uses a different archival convention.

## Query And Synthesis Workflow

When answering research questions inside an auto-research repo:

1. Search the wiki first.
2. Check source pages, manifests, and raw filenames behind the relevant wiki claims.
3. Distinguish evidence, inference, conjecture, and rhetoric.
4. Update the wiki when the answer produces durable synthesis.
5. Update open questions or wishlist entries when the answer exposes missing evidence.
6. Log meaningful additions in `wiki/log.md`.

Avoid duplicating pages or rediscovering arguments. Extend the existing synthesis unless a new page is justified by a distinct concept, source corpus, or paper-shaped claim.

## Publication Corpus Workflow

Use `corpus/` for canonical publication output. Publication projects should be portable HTML packages with self-contained publication files.

Exploratory publications may be created before a claim is paper-ready when they expose data, pressure-test a conjecture, or make a useful working artifact publishable. Create them under `corpus/exploratory/<project-slug>/`, and label them as exploratory.

Draft mature treatise publications only from worked wiki synthesis. Before creating a mature treatise publication:

- Verify the claim is already represented in the wiki.
- Verify supporting and contradicting sources are linked.
- Add or update a paper seed if the repo uses one.
- Record the decision in `wiki/log.md`.

Create one directory per publication project under `corpus/exploratory/` or `corpus/treatise/`. Output should be HTML-first so it can be archived, moved, and published online without a custom build environment. Prefer:

- `index.html` as the directory table of contents, linking to every publication in that project.
- One self-contained single-page HTML file per publication, with inline CSS and JavaScript.
- No external CDN, remote stylesheet, remote script, or web-font dependency in the canonical HTML artifact.
- Inline or locally generated figures, tables, data extracts, and interactive elements tied back to `raw/`, source pages, manifests, or reproducible scripts.
- `refs.bib`, `references.md`, or an embedded references section drawn from source pages and raw manifests.
- A README or metadata block describing the lane, claim or purpose, status, category when applicable, source wiki pages, and reproducibility notes.
- Optional print/PDF export scripts only as secondary outputs generated from the HTML publication.

Useful mature treatise categories:

- `prove`: constructive result, new bound, derivation, model, or positive finding.
- `disprove`: refutation of a specific claim with evidence.
- `expose`: evidence-backed critique of unsupported, misleading, fraudulent, p-hacked, unfalsifiable, or citation-laundered work.

## Research Standards

- Prefer primary sources and reproducible datasets.
- Preserve uncertainty and unresolved contradictions.
- State what would falsify a conjecture.
- Attack the strongest version of a claim that the literature actually supports.
- Separate domain facts from repo-local hypotheses.
- Do not let unsupported claims harden into wiki synthesis.
- Prefer updating existing pages over creating fragmented parallel notes.
- Keep the output concise enough that future agents can use it as operational memory.
