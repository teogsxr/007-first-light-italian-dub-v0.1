param(
  [string]$GamePath = "C:\Program Files (x86)\Steam\steamapps\common\007 First Light",
  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Runtime = Join-Path $GamePath "Runtime"

if (!(Test-Path (Join-Path $Runtime "chunk0.rpkg")) -or !(Test-Path (Join-Path $Runtime "chunk1.rpkg"))) {
  throw "Runtime chunks not found. Pass -GamePath to your 007 First Light install folder."
}

& $Python (Join-Path $Root "tools\apply_wem_manifest.py") `
  --game-path $GamePath `
  --manifest "mod_manifest/runtime_wem_manifest.csv" `
  --label "007_it_dub_v0_1" `
  --apply
