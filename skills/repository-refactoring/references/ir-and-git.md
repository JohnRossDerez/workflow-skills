# Choosing an IR alongside Git

An intermediate representation is useful when it enables a decision or query that source history alone makes difficult. It is not proof of correctness.

Git's commit DAG records revision ancestry. Trees and diffs show source snapshots and changes; branches, merge bases, and worktrees support integration and isolation. Use these as the audit's revision identity and preserve existing design/operational records as evidence.

The three-layer audit describes semantic relationships: outcome to behavioral flow to concrete implementation, compared across baseline and target. A commit can move files without showing that every deployed mode still reaches a consumer. An import graph can be intact while a runtime configuration choice, external resource, or artifact handoff is missing.

| Situation | Appropriate starting point |
| --- | --- |
| Local behavior is easily traced | Diff, relevant callers, and focused checks |
| Bounded package extraction | Compact capability table with flow notes |
| Multiple capabilities, modes, owners, or repositories | Three-layer baseline-to-target comparison |
| Repeated impact queries or substantial resumable/delegated work | Structured mappings/graph with stable capability IDs |

A task DAG layered on Git can host the semantic mappings if its nodes and edges represent the relevant capabilities and contracts. Do not maintain a parallel graph simply because the skill calls it an IR.

## Useful consumers of the mapping

- Planning a vertical migration slice without dropping its consumers or operational modes.
- Giving a worker the relevant capability contract and dependencies without the whole repository.
- Finding outcomes without target owners or flows without a connected execution path.
- Selecting behavioral checks and locating affected capabilities after a source change.

Declared links can be missing or wrong. Confirm important mappings against source, callers, operational contracts, and execution. A file hash proves identity; it does not prove semantic coverage. Refresh affected findings when their evidence changes, without introducing universal bookkeeping for unrelated files.

Keep a field only when it changes a decision, supports a useful query, or helps catch a material failure. If an IR merely paraphrases a small diff, use the diff.
