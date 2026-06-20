# 007 First Light - Doppiaggio Italiano AI Source-First v0.3

![Source-first dubbing pipeline](docs/assets/source-first-dubbing-hero.png)

Versione `0.3` del doppiaggio italiano source-first per 007 First Light.

[Pagina metodo e casting voci](https://teogsxr.github.io/007-first-light-italian-dub/): ascolto pubblico con soli audio generati, confronto voce target senza patos vs source-first con patos.

## Stato v0.3

- Audio patchati: `8182/16255` = `50.34%`.
- Mancanti: `8073`.
- Bond: `439/715`.
- Asset generati inclusi: `8182` WEM, `133.30 MiB`.
- Pacchetto zip v0.3: circa `136.16 MiB`.

La tabella completa per personaggio e in [`docs/progress_by_character.md`](docs/progress_by_character.md). Le istruzioni di installazione agnostica sono in [`docs/installation.md`](docs/installation.md).

## Cosa cambia in v0.3

- Aumentata la copertura pubblicata da `5925` a `8182` audio runtime-approved.
- Introdotta la doppia qualita di produzione: `gold strict` per le righe che passano anche source-first conformance/pathos, e `playable provisional` per aumentare rapidamente la copertura mantenendo timing, ASR, semantica, sottotitoli, capacity e runtime gate.
- Aggiornati manifest, progressi per personaggio, pacchetto installabile e pagina Pages.
- Integrata la pipeline guarded/prededuped: nessun hash gia applicato viene rigenerato o ripatchato per errore.
- Aggiunta ricostruzione release da cumulativo con audit dei WEM risolti dalle cache generate, senza includere audio originale del gioco.
- Consolidati i controlli di QA: ASR, parole richieste, timing, conformance, pathos source-first, marker preservation, subtitle audit e capacity/runtime gate.

## Installazione

1. Chiudi il gioco.
2. Apri PowerShell nella cartella del mod.
3. Lancia l'installer:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

Se non trova il gioco da solo, ti chiede se usi Steam. Se rispondi si, prova i percorsi Steam comuni e poi ti lascia inserire la libreria Steam o la cartella del gioco. Se rispondi no, inserisci la cartella principale del gioco del tuo store/launcher.

Puoi anche passare subito il percorso esplicito:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1 -GamePath "D:\Games\007 First Light" -SaveGamePath
```

La cartella principale del gioco e quella che contiene `Runtime\chunk0.rpkg` e `Runtime\chunk1.rpkg`. Steam, GOG, Epic, installazioni portabili e librerie custom funzionano allo stesso modo: conta solo il path corretto.

Puoi anche creare un file `game_path.txt` accanto a `install.ps1` con dentro il path del gioco, poi lanciare:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

Lo script prova anche a rilevare il gioco se il mod e stato estratto dentro o vicino alla cartella del gioco. In ogni caso crea un backup locale in `backups/` prima di modificare `Runtime\chunk0.rpkg` e `Runtime\chunk1.rpkg`.

Per controllare il percorso senza applicare la mod:

```powershell
.\install.ps1 -GamePath "D:\Games\007 First Light" -DryRun
```

Il dry-run scrive solo un report in `dryrun_reports/`, non un backup usato dalla disinstallazione.

## Disinstallazione

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\uninstall.ps1
```

Ripristina l'ultimo backup creato dall'installer.

## Metodo reale

Questa mod non usa one-shot clone diretto di ogni battuta originale. La pipeline usa una voce target approvata per il personaggio e l'audio sorgente come autorita di recitazione: emozione, pause, respiro, tosse, urla, distanza, urgenza e timing.

Il testo italiano viene adattato quando serve per stare nel tempo disponibile. Ogni take promosso passa attraverso QA ASR, controllo parole richieste, controllo timing/performance, filtro semantico, mastering 48 kHz, Wwise Vorbis, preservazione marker, runtime safety e audit sottotitoli.

Perche a volte resta un lieve accento inglese: nei test, il polish dell'accento rovinava recitazione o timing. In v0.3 preferiamo preservare pathos, sincronizzazione e comprensibilita rispetto a forzare una dizione perfetta ma piatta.

Questa e una prima passata automatica pensata anche come pipeline riusabile per altri giochi: priorita a velocita, sicurezza e coerenza, poi raffinamento. Le righe `playable provisional` sono installabili e controllate, ma non vanno lette come doppiaggio finale rifinito a mano.

## Stato qualitativo

- Le battute pubblicate sono state promosse dalla pipeline automatica e applicate al runtime locale.
- Parte della copertura v0.3 e `playable provisional`: testo, timing, sottotitoli e runtime sono controllati, ma pathos/conformance possono richiedere un secondo passaggio.
- Non tutte le voci/personaggi sono completi: il progetto e ancora in avanzamento.
- Le righe non patchate restano in backlog per retake, Profile B/C repair o approvazione voce.
- Alcuni take possono mantenere lieve accento o enfasi non perfetta se correggerli danneggia pathos/timing.
- Non include file originali del gioco.

## Supporto al progetto

Il progetto resta gratuito e andra avanti anche senza donazioni. Le eventuali donazioni vengono usate per acquistare crediti AI, rigenerare audio e migliorare piu velocemente le prossime versioni.

<p align="center">
  <a href="https://www.paypal.com/donate/?business=matteo.sai%40hotmail.it&currency_code=EUR" target="_blank" rel="noopener noreferrer">
    <img src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" alt="Dona con PayPal">
  </a>
</p>
