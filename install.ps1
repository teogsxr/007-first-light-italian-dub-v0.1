param(
  [string]$GamePath = "",
  [string]$Python = "python",
  [switch]$SaveGamePath,
  [switch]$DryRun,
  [switch]$NoPrompt
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

function Test-GameRoot {
  param([string]$Path)
  if ([string]::IsNullOrWhiteSpace($Path)) {
    return $false
  }
  $Runtime = Join-TextPath $Path "Runtime"
  return (Test-Path -LiteralPath (Join-TextPath $Runtime "chunk0.rpkg")) -and
         (Test-Path -LiteralPath (Join-TextPath $Runtime "chunk1.rpkg"))
}

function Join-TextPath {
  param(
    [string]$Base,
    [string]$Child
  )
  if ([string]::IsNullOrWhiteSpace($Base)) {
    return $Child
  }
  $baseClean = $Base.Trim().Trim('"') -replace '[\\/]+$', ''
  $childClean = $Child.Trim() -replace '^[\\/]+', ''
  return "$baseClean\$childClean"
}

function Resolve-CandidateGameRoot {
  param([string]$Path)
  if ([string]::IsNullOrWhiteSpace($Path)) {
    return ""
  }
  if (Test-GameRoot $Path) {
    return (Resolve-Path -LiteralPath $Path).Path
  }
  if ((Test-Path -LiteralPath (Join-TextPath $Path "chunk0.rpkg")) -and
      (Test-Path -LiteralPath (Join-TextPath $Path "chunk1.rpkg"))) {
    $runtime = Resolve-Path -LiteralPath $Path
    if ((Split-Path -Leaf $runtime.Path) -ieq "Runtime") {
      return (Split-Path -Parent $runtime.Path)
    }
  }
  return ""
}

function Add-Candidate {
  param(
    [System.Collections.Generic.List[string]]$Candidates,
    [string]$Path
  )
  if ([string]::IsNullOrWhiteSpace($Path)) {
    return
  }
  $expanded = [Environment]::ExpandEnvironmentVariables($Path.Trim().Trim('"'))
  if (-not [string]::IsNullOrWhiteSpace($expanded) -and -not $Candidates.Contains($expanded)) {
    [void]$Candidates.Add($expanded)
  }
}

function Add-Upward-Candidates {
  param(
    [System.Collections.Generic.List[string]]$Candidates,
    [string]$StartPath
  )
  if ([string]::IsNullOrWhiteSpace($StartPath) -or -not (Test-Path -LiteralPath $StartPath)) {
    return
  }
  $item = Get-Item -LiteralPath $StartPath
  if (-not $item.PSIsContainer) {
    $item = $item.Directory
  }
  for ($i = 0; $i -lt 5 -and $null -ne $item; $i++) {
    Add-Candidate $Candidates $item.FullName
    $item = $item.Parent
  }
}

function Resolve-ManualGamePathInput {
  param([string]$Path)

  if ([string]::IsNullOrWhiteSpace($Path)) {
    return ""
  }

  $Candidates = [System.Collections.Generic.List[string]]::new()
  Add-Candidate $Candidates $Path
  Add-Candidate $Candidates (Join-TextPath $Path "steamapps\common\007 First Light")
  Add-Candidate $Candidates (Join-TextPath $Path "common\007 First Light")
  Add-Candidate $Candidates (Join-TextPath $Path "007 First Light")

  foreach ($candidate in $Candidates) {
    $resolved = Resolve-CandidateGameRoot $candidate
    if (-not [string]::IsNullOrWhiteSpace($resolved)) {
      return $resolved
    }
  }

  return ""
}

function Ask-GamePathFromUser {
  if ($NoPrompt) {
    return ""
  }

  Write-Host ""
  Write-Host "Cannot auto-detect the 007 First Light install folder."
  Write-Host "The correct folder contains Runtime\chunk0.rpkg and Runtime\chunk1.rpkg."

  $steamAnswer = (Read-Host "Are you using Steam for this install? [Y/N]").Trim()
  if ($steamAnswer -match "^(y|yes|s|si)$") {
    foreach ($path in @(
      "C:\Program Files (x86)\Steam\steamapps\common\007 First Light",
      "C:\Program Files\Steam\steamapps\common\007 First Light",
      "D:\SteamLibrary\steamapps\common\007 First Light",
      "E:\SteamLibrary\steamapps\common\007 First Light"
    )) {
      $resolved = Resolve-CandidateGameRoot $path
      if (-not [string]::IsNullOrWhiteSpace($resolved)) {
        Write-Host "Steam install found:" $resolved
        return $resolved
      }
    }
    Write-Host "Steam was selected, but the common Steam folders were not valid."
    Write-Host "Paste either the Steam library folder or the game folder."
    Write-Host "Examples:"
    Write-Host "  D:\SteamLibrary"
    Write-Host "  D:\SteamLibrary\steamapps\common\007 First Light"
    $steamPath = Read-Host "Steam library or game folder"
    return (Resolve-ManualGamePathInput $steamPath)
  }

  Write-Host "Paste the game folder from your store/launcher/custom install."
  Write-Host "Example: D:\Games\007 First Light"
  $customPath = Read-Host "Game folder path"
  return (Resolve-ManualGamePathInput $customPath)
}

function Resolve-GamePath {
  $Candidates = [System.Collections.Generic.List[string]]::new()

  if (-not [string]::IsNullOrWhiteSpace($GamePath)) {
    $resolvedArgument = Resolve-CandidateGameRoot $GamePath
    if (-not [string]::IsNullOrWhiteSpace($resolvedArgument)) {
      return $resolvedArgument
    }
    Write-Host "-GamePath is not a valid 007 First Light install folder:" $GamePath
    $promptResolved = Ask-GamePathFromUser
    if (-not [string]::IsNullOrWhiteSpace($promptResolved)) {
      return $promptResolved
    }
    throw @"
Invalid -GamePath.

The game root must contain:
  Runtime\chunk0.rpkg
  Runtime\chunk1.rpkg
"@
  }

  foreach ($name in @("IOI_007_FIRST_LIGHT_PATH", "FIRST_LIGHT_GAME_PATH", "007_FIRST_LIGHT_PATH")) {
    Add-Candidate $Candidates ([Environment]::GetEnvironmentVariable($name, "Process"))
    Add-Candidate $Candidates ([Environment]::GetEnvironmentVariable($name, "User"))
    Add-Candidate $Candidates ([Environment]::GetEnvironmentVariable($name, "Machine"))
  }

  $ConfigPath = Join-Path $Root "game_path.txt"
  if (Test-Path -LiteralPath $ConfigPath) {
    Add-Candidate $Candidates (Get-Content -LiteralPath $ConfigPath -Raw)
  }

  Add-Upward-Candidates $Candidates $Root
  Add-Upward-Candidates $Candidates (Get-Location).Path

  foreach ($path in @(
    "C:\Program Files (x86)\Steam\steamapps\common\007 First Light",
    "C:\Program Files\Steam\steamapps\common\007 First Light",
    "C:\Games\007 First Light",
    "D:\Games\007 First Light",
    "D:\SteamLibrary\steamapps\common\007 First Light",
    "E:\SteamLibrary\steamapps\common\007 First Light"
  )) {
    Add-Candidate $Candidates $path
  }

  foreach ($candidate in $Candidates) {
    $resolved = Resolve-CandidateGameRoot $candidate
    if (-not [string]::IsNullOrWhiteSpace($resolved)) {
      return $resolved
    }
  }

  $promptResolved = Ask-GamePathFromUser
  if (-not [string]::IsNullOrWhiteSpace($promptResolved)) {
    return $promptResolved
  }

  $message = @"
Cannot find a valid 007 First Light install folder.

Pass the game root explicitly:
  .\install.ps1 -GamePath "D:\Games\007 First Light"

Or run without -NoPrompt and answer the Steam/custom install questions.

Or create a file named game_path.txt next to install.ps1 containing the game root.
The game root is the folder that contains:
  Runtime\chunk0.rpkg
  Runtime\chunk1.rpkg

Steam, GOG, Epic, portable and custom-library installs all work as long as -GamePath
points to that root folder.
"@
  throw $message
}

$ResolvedGamePath = Resolve-GamePath
$Runtime = Join-Path $ResolvedGamePath "Runtime"

if ($SaveGamePath) {
  Set-Content -LiteralPath (Join-Path $Root "game_path.txt") -Value $ResolvedGamePath -Encoding UTF8
}

Write-Host "007 First Light install folder:" $ResolvedGamePath
Write-Host "Runtime folder:" $Runtime

$ApplyArgs = @(
  (Join-Path $Root "tools\apply_wem_manifest.py"),
  "--game-path", $ResolvedGamePath,
  "--manifest", "mod_manifest/runtime_wem_manifest.csv",
  "--label", "007_it_dub_v0_3"
)

if (-not $DryRun) {
  $ApplyArgs += "--apply"
} else {
  Write-Host "Dry run only: no runtime chunks will be modified."
}

& $Python @ApplyArgs
