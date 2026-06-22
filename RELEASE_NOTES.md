# Release notes v0.4

- Copertura pubblicata: `10569/16255` audio, pari al `65.02%`.
- Avanzamento cumulativo interno: `10594/16255`, pari al `65.17%`.
- Asset generati: `10569` WEM, `182.39 MiB` nel manifest mod.
- Pacchetto installabile: `007-first-light-italian-dub-v0.4.zip`, circa `207.99 MiB`.
- Aggiornata la pagina pubblica metodo/casting/video: https://teogsxr.github.io/007-first-light-italian-dub/
- Aggiunto video gameplay WIP del capitolo 1, con nota che alcuni fix sottotitoli/HUD sono successivi alla cattura.
- Capitolo 1 in test gameplay ravvicinato: fix mirati su sottotitoli non allineati, testo adattato, timing e frasi troncate.
- Installer aggiornato con supporto append-relocation per `6` WEM che superano lo slot originale.
- Esclusi dal pacchetto pubblico `25` asset preserve/originali: sono tracciati nel cumulativo locale ma non ridistribuiti.
- Aggiornati manifest, progressi per personaggio e audit di ricostruzione WEM.
- Installer agnostico rispetto allo store: procedura guidata Steam/non Steam, `-GamePath`, `game_path.txt`, variabili ambiente e rilevamento da cartelle parent.
- Metodo source-first confermato: voce target approvata, audio sorgente come autorita di recitazione, QA ASR/timing/semantic/runtime/subtitle.
- Non include file originali del gioco.

## Note qualita

La v0.4 non e una localizzazione finale rifinita a mano: e una release WIP giocabile della pipeline automatica. La priorita resta preservare pathos, sincronizzazione, sottotitoli coerenti e sicurezza runtime. Alcune righe possono avere recitazione meno precisa o accento residuo se correggerli avrebbe danneggiato timing/testo o rallentato troppo la copertura.
