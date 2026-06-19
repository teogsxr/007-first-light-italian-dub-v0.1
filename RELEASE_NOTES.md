# Release notes v0.2

- Copertura pubblicata: `5925/16255` audio, pari al `36.45%`.
- Asset generati: `5925` WEM, `95.14 MiB` nel manifest mod.
- Pacchetto installabile: `007-first-light-italian-dub-v0.2.zip`, circa `97.59 MiB`.
- Aggiornata la pagina pubblica metodo/casting: https://teogsxr.github.io/007-first-light-italian-dub-v0.1/
- Aggiornati manifest, progressi per personaggio e audit di ricostruzione WEM.
- Aggiunta pipeline di release da cumulativo con risoluzione conservativa dei soli WEM generati.
- Consolidato il flusso guarded/prededuped: niente rerender/ripatch accidentale di hash gia applicati.
- Metodo source-first: voce target approvata, audio sorgente come autorita di recitazione, QA ASR/timing/semantic/runtime/subtitle.
- Non include file originali del gioco.

## Note qualita

La v0.2 non e una localizzazione finale rifinita a mano: e una prima passata automatica pensata per scalare velocemente. La pipeline privilegia pathos, timing e coerenza source-first rispetto a un polish di accento che, nei test, tendeva a rovinare la recitazione.
