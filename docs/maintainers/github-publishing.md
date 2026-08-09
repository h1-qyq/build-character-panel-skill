# GitHub publishing for maintainers

This document stays separate from the product README. Users need the local
installation path; release mechanics belong here.

Use `scripts/publish-to-github.ps1` when you intentionally want to publish a
clean local worktree.

Prerequisites:

- Run `gh auth login`, then check the session with `gh auth status`.
- The worktree is clean.
- PowerShell is available.

Publish with the default private visibility:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\publish-to-github.ps1
```

Publish publicly when that is an intentional release decision:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File `
  .\scripts\publish-to-github.ps1 `
  -Visibility public
```

The script refuses a dirty worktree, never embeds credentials, verifies an
existing `origin`, and supports PowerShell `-WhatIf`. Local use does not
require publishing.
