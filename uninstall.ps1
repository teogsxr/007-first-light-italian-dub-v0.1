param(
  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackupRoot = Join-Path $Root "backups"

if (!(Test-Path $BackupRoot)) {
  throw "No backups folder found. Restore manually from your own game backup."
}

$Backup = Get-ChildItem $BackupRoot -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($null -eq $Backup) {
  throw "No backup found under backups\. Restore manually from your own game backup."
}

& $Python (Join-Path $Root "tools\restore_backup.py") --backup $Backup.FullName
