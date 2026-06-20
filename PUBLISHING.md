# Publishing

Public repository:

- `https://github.com/teogsxr/007-first-light-italian-dub`

Public Pages:

- `https://teogsxr.github.io/007-first-light-italian-dub/`

Current public release:

- `https://github.com/teogsxr/007-first-light-italian-dub/releases/tag/v0.3`

The repo contains generated mod assets, manifests, documentation and installer scripts.
It must not contain original game chunks, original WEMs, original source audio, or local
QA pages that embed original source audio.

To rebuild the v0.3 package from local production state:

```powershell
$env:DUBBING_007_PROJECT_ROOT = "<local 007_first_light project path>"
python .\tools\build_release_from_cumulative.py
```

To publish after checking the diff:

```powershell
git status -sb
git add -A
git commit -m "Release v0.3 playable milestone"
git push
git tag v0.3
git push origin v0.3
gh release create v0.3 ..\007-first-light-italian-dub-v0.3.zip --title "007 First Light Italian Dub v0.3" --notes-file RELEASE_NOTES.md
```

If the release already exists:

```powershell
gh release upload v0.3 ..\007-first-light-italian-dub-v0.3.zip --clobber
gh release edit v0.3 --title "007 First Light Italian Dub v0.3" --notes-file RELEASE_NOTES.md
```

Before every push, scan for local-only or original-audio paths:

```powershell
Get-ChildItem -Recurse -File |
  Select-String -Pattern '127\.0\.0\.1|local comparison|original source audio|source_vs_italian'
```
