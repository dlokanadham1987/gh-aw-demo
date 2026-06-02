# Presentation assets

Screenshots used by `presentation/index.html`.

## Required files

The slides reference these images:

- `1-pr-raised.png`
- `2-workflow-triggered.png`
- `3-workflow-executing.png`
- `4-workflow-completed.png`
- `5-claude-comment.png`

## How to populate

Copy them from your existing companion-docs folder:

```powershell
# from C:\Practice\AI\GithubAgenticWorkflow\gh-aw-demo
copy ..\docs\images\*.png presentation\assets\
```

Or in bash / PowerShell with forward slashes:

```bash
cp ../docs/images/*.png presentation/assets/
```

After Thursday's demo, you can replace these with fresh screenshots
captured from the new `gh-aw-demo` repo's first PR run.
