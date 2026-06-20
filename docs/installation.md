# Installazione agnostica

La mod non richiede Steam. Funziona con qualunque installazione di 007 First Light se indichi la cartella principale del gioco.

La cartella corretta e quella che contiene:

```text
Runtime\chunk0.rpkg
Runtime\chunk1.rpkg
```

## Installazione guidata

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

Se l'installer non trova il gioco automaticamente, fa una domanda semplice:

- se usi Steam, prova i percorsi Steam comuni e poi ti chiede la libreria Steam o la cartella del gioco;
- se non usi Steam, ti chiede direttamente la cartella principale del gioco del tuo store/launcher.

## Installazione con path esplicito

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1 -GamePath "D:\Games\007 First Light" -SaveGamePath
```

Sostituisci `D:\Games\007 First Light` con il percorso reale della tua installazione.
Se passi per errore direttamente la cartella `Runtime`, lo script prova a risalire automaticamente alla cartella principale del gioco.

## Installazione con game_path.txt

Crea un file `game_path.txt` accanto a `install.ps1` e scrivi al suo interno la cartella principale del gioco. Poi esegui:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

## Rilevamento automatico

`install.ps1` prova anche a leggere:

- `game_path.txt`;
- variabili ambiente `IOI_007_FIRST_LIGHT_PATH`, `FIRST_LIGHT_GAME_PATH`, `007_FIRST_LIGHT_PATH`;
- la cartella corrente e alcune cartelle parent;
- alcuni percorsi comuni Steam come fallback.
- se non trova nulla, avvia la procedura guidata Steam/non Steam.

Se vuoi evitare ogni domanda interattiva, usa `-NoPrompt` insieme a `-GamePath` o `game_path.txt`.

## Dry run

Per verificare path e manifest senza modificare i chunk runtime:

```powershell
.\install.ps1 -GamePath "D:\Games\007 First Light" -DryRun
```

Il dry-run scrive solo un report in `dryrun_reports/`; non crea un backup di
ripristino e non viene usato da `uninstall.ps1`.

## Disinstallazione

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\uninstall.ps1
```

Il ripristino usa il backup creato durante l'installazione, quindi resta indipendente dallo store usato per installare il gioco.
