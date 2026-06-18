# Publishing

The local repo is ready to publish.

Current local state:

- Local repo: `C:\00 - Doppiaggio\12_releases\007-first-light-italian-dub-v0.1\repo`
- Latest commit: `06f3677 Add README hero artwork`
- Generated README image: `docs/assets/source-first-dubbing-hero.png`
- Release ZIP: `C:\00 - Doppiaggio\12_releases\007-first-light-italian-dub-v0.1\007-first-light-italian-dub-v0.1.zip`
- GitHub target: `teogsxr/007-first-light-italian-dub-v0.1`

GitHub CLI is installed here:

```powershell
C:\Users\matte\AppData\Local\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\gh.exe
```

The repo has not yet been published because `gh` is not authenticated. Run the helper below and complete the browser login with the `teogsxr` account:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
& "C:\00 - Doppiaggio\12_releases\007-first-light-italian-dub-v0.1\publish_to_github.ps1"
```

The helper will:

1. authenticate GitHub CLI if needed;
2. create the public repo `teogsxr/007-first-light-italian-dub-v0.1` if missing;
3. push local `main`;
4. open the repo in the browser.

After the repo exists and `main` is pushed, create the release:

```powershell
$gh = "C:\Users\matte\AppData\Local\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\gh.exe"
cd "C:\00 - Doppiaggio\12_releases\007-first-light-italian-dub-v0.1\repo"
& $gh release create v0.1 "..\007-first-light-italian-dub-v0.1.zip" --title "v0.1 - Source-first Italian dubbing pass" --notes-file RELEASE_NOTES.md
```

Do not add original game chunks, original WEMs, or the local comparison page with original source audio to the public repo.
