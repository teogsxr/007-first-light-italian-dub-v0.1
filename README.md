# 007 First Light - Doppiaggio Italiano AI Source-First v0.2

![Source-first dubbing pipeline](docs/assets/source-first-dubbing-hero.png)

Versione `0.2` del doppiaggio italiano source-first per 007 First Light.

[Pagina metodo e casting voci](https://teogsxr.github.io/007-first-light-italian-dub-v0.1/): ascolto pubblico con soli audio generati, confronto voce target senza patos vs source-first con patos.

## Stato v0.2

- Audio patchati: `5925/16255` = `36.45%`.
- Mancanti: `10330`.
- Bond: `418/715`.
- Asset generati inclusi: `5925` WEM, `95.14 MiB`.
- Pacchetto zip v0.2: circa `97.59 MiB`.

La tabella completa per personaggio e in [`docs/progress_by_character.md`](docs/progress_by_character.md).

## Cosa cambia in v0.2

- Aumentata la copertura pubblicata da `4859` a `5925` audio runtime-approved.
- Aggiornati manifest, progressi per personaggio, pacchetto installabile e pagina Pages.
- Integrata la pipeline guarded/prededuped: nessun hash gia applicato viene rigenerato o ripatchato per errore.
- Aggiunta ricostruzione release da cumulativo con audit dei WEM risolti dalle cache generate, senza includere audio originale del gioco.
- Consolidati i controlli di QA: ASR, parole richieste, timing, conformance, pathos source-first, marker preservation, subtitle audit e capacity/runtime gate.

## Installazione

1. Chiudi il gioco.
2. Apri PowerShell nella cartella del mod.
3. Esegui:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1 -GamePath "C:\Program Files (x86)\Steam\steamapps\common\007 First Light"
```

Lo script crea un backup locale in `backups/` prima di modificare `Runtime\chunk0.rpkg` e `Runtime\chunk1.rpkg`.

## Disinstallazione

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\uninstall.ps1
```

Ripristina l'ultimo backup creato dall'installer.

## Metodo reale

Questa mod non usa one-shot clone diretto di ogni battuta originale. La pipeline usa una voce target approvata per il personaggio e l'audio sorgente come autorita di recitazione: emozione, pause, respiro, tosse, urla, distanza, urgenza e timing.

Il testo italiano viene adattato quando serve per stare nel tempo disponibile. Ogni take promosso passa attraverso QA ASR, controllo parole richieste, controllo timing/performance, filtro semantico, mastering 48 kHz, Wwise Vorbis, preservazione marker, runtime safety e audit sottotitoli.

Perche a volte resta un lieve accento inglese: nei test, il polish dell'accento rovinava recitazione o timing. In v0.2 preferiamo preservare pathos e ritmo del source rispetto a forzare una dizione perfetta ma piatta.

Questa e una prima passata automatica pensata anche come pipeline riusabile per altri giochi: priorita a velocita, sicurezza e coerenza, poi raffinamento.

## Stato qualitativo

- Le battute pubblicate sono state promosse dalla pipeline automatica e applicate al runtime locale.
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
