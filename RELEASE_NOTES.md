# Release notes v0.3

- Copertura pubblicata: `8182/16255` audio, pari al `50.34%`.
- Asset generati: `8182` WEM, `133.30 MiB` nel manifest mod.
- Pacchetto installabile: `007-first-light-italian-dub-v0.3.zip`, circa `136.16 MiB`.
- Aggiornata la pagina pubblica metodo/casting: https://teogsxr.github.io/007-first-light-italian-dub/
- Aggiornati manifest, progressi per personaggio e audit di ricostruzione WEM.
- Installer agnostico rispetto allo store: procedura guidata Steam/non Steam, `-GamePath`, `game_path.txt`, variabili ambiente e rilevamento da cartelle parent; Steam e solo un percorso possibile.
- Aggiunta pipeline di release da cumulativo con risoluzione conservativa dei soli WEM generati.
- Consolidato il flusso guarded/prededuped: niente rerender/ripatch accidentale di hash gia applicati.
- Metodo source-first: voce target approvata, audio sorgente come autorita di recitazione, QA ASR/timing/semantic/runtime/subtitle.
- Nuova lane `playable provisional`: aumenta velocemente la copertura giocabile mantenendo gate duri su testo, timing, sottotitoli, capacity e runtime, ma segnando pathos/conformance come debito di rifinitura.
- Non include file originali del gioco.

## Note qualita

La v0.3 non e una localizzazione finale rifinita a mano: e una prima passata automatica pensata per scalare velocemente. La pipeline privilegia copertura giocabile, sicurezza runtime, sottotitoli coerenti e possibilita di rifinire dopo. Alcune righe possono avere recitazione meno precisa o accento residuo se correggerli avrebbe rallentato troppo la copertura o danneggiato timing/testo.
