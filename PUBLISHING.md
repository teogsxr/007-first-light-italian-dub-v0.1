# Publishing

This local repo is ready to publish, but this machine currently has no `gh`
command in `PATH` and no `GITHUB_TOKEN`/`GH_TOKEN` environment variable.

Once GitHub CLI is installed and authenticated, publish with:

```powershell
cd "C:\00 - Doppiaggio\12_releases\007-first-light-italian-dub-v0.1\repo"
gh auth login
gh repo create 007-first-light-italian-dub-v0.1 --public --source . --remote origin --push
gh release create v0.1 "..\007-first-light-italian-dub-v0.1.zip" --title "v0.1 - Source-first Italian dubbing pass" --notes-file RELEASE_NOTES.md
```

Do not add original game chunks, original WEMs, or the local comparison page
with original source audio to the public repo.
