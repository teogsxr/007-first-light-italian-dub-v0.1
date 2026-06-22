# 007 First Light - Doppiaggio Italiano AI Source-First v0.4

![Source-first dubbing pipeline](docs/assets/source-first-dubbing-hero.png)

Versione `0.4` del doppiaggio italiano source-first per 007 First Light.

[Pagina metodo, casting voci e video WIP](https://teogsxr.github.io/007-first-light-italian-dub/): ascolto pubblico con soli audio generati, confronto voce target senza patos vs source-first con patos, e anteprima gameplay del capitolo 1.

## Stato v0.4

- Audio generati installabili: `10569/16255` = `65.02%`.
- Audio ufficiali ancora mancanti: `5686`.
- Avanzamento cumulativo interno: `10594/16255` = `65.17%`.
- Righe preserve/originali tracciate internamente ma non ridistribuite: `25`.
- Bond: `538/715` = `75.24%`.
- Greenway: `243/328` = `74.09%`.
- Moneypenny: `231/335` = `68.96%`.
- Asset generati inclusi: `10569` WEM, `182.39 MiB`.
- Pacchetto zip v0.4: circa `207.99 MiB`.
- Installer aggiornato con supporto append-relocation per `6` WEM fuori capacita originale.

La tabella completa per personaggio e in [`docs/progress_by_character.md`](docs/progress_by_character.md). Le istruzioni di installazione agnostica sono in [`docs/installation.md`](docs/installation.md).

## Video gameplay WIP v0.4

Il video mostra un controllo reale del primo capitolo sulla build locale v0.4. La scena non e ancora una localizzazione finale rifinita a mano, ma fa vedere dove sta arrivando la pipeline source-first: voce target stabile, patos recuperato dal source, adattamento italiano e sottotitoli in revisione.

> Nota: dopo questa cattura sono stati applicati ulteriori fix mirati ai sottotitoli/HUD nella scena di apertura.

![Gameplay WIP v0.4](docs/assets/video/ch1-opening-wip-v0.4-preview.gif)

## Cosa cambia in v0.4

- Copertura pubblicata aumentata da `8182` a `10569` audio generati installabili.
- Capitolo 1 portato in una fase di test gameplay piu vicina alla produzione, con fix mirati su sottotitoli, HUD escaped, frasi troncate e timing.
- Confermata la metodologia source-first: l'audio sorgente resta la regia della performance, mentre la voce italiana usa un'identita target approvata.
- Aggiunto supporto installer per append-relocation nei rari casi in cui il WEM italiano e piu grande dello slot originale.
- Esclusi dal pacchetto pubblico `25` asset preserve/originali: restano nel tracking interno, ma non vengono ridistribuiti.
- Aggiornati manifest, progressi per personaggio, pacchetto installabile e pagina GitHub Pages.
- Mantenuta la doppia qualita di produzione: `gold strict` quando la take passa tutti i gate source-first/pathos, `playable provisional` quando e sicura e giocabile ma da rifinire.
- Consolidati i controlli di QA: ASR, parole richieste, timing, conformance, pathos source-first, marker preservation, subtitle audit, capacity/runtime gate.

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

Il testo italiano viene adattato quando serve per stare nel tempo disponibile, e quando l'adattamento cambia davvero la frase anche il sottotitolo deve seguire l'audio. Ogni take promosso passa attraverso QA ASR, controllo parole richieste, controllo timing/performance, filtro semantico, mastering 48 kHz, Wwise Vorbis, preservazione marker, runtime safety e audit sottotitoli.

Perche a volte resta un lieve accento inglese: nei test, il polish dell'accento rovinava recitazione o timing. In v0.4 preferiamo preservare pathos, sincronizzazione e comprensibilita rispetto a forzare una dizione perfetta ma piatta.

Questa e una prima passata automatica pensata anche come pipeline riusabile per altri giochi: priorita a velocita, sicurezza e coerenza, poi raffinamento. Le righe `playable provisional` sono installabili e controllate, ma non vanno lette come doppiaggio finale rifinito a mano.

## Stato qualitativo

- Le battute pubblicate sono state promosse dalla pipeline automatica e applicate al runtime locale.
- Il primo capitolo e in test gameplay ravvicinato: audio e sottotitoli sono stati corretti con feedback video, ma restano possibili micro-retake.
- Parte della copertura v0.4 e `playable provisional`: testo, timing, sottotitoli e runtime sono controllati, ma pathos/conformance possono richiedere un secondo passaggio.
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
