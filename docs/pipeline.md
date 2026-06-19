# Pipeline source-first v0.2

1. Mappa WEM ufficiali, speaker e sottotitoli.
2. Approva una voce target stabile per ogni personaggio.
3. Analizza l'audio sorgente: emozione, intensita, pause, respiri, urla, tosse, distanza e timing.
4. Genera italiano source-first: source audio come performance authority, target voice come identity authority.
5. Adatta il testo italiano quando il timing originale lo richiede; se il parlato cambia, il sottotitolo va sincronizzato.
6. QA ASR: testo parlato, parole richieste, nessun tag letto.
7. QA performance: timing, pause, energia, emozione, pathos e nonverbali rispetto al source.
8. Filtro semantico/editoriale.
9. Mastering 48 kHz mono PCM16.
10. Wwise Vorbis encode, preferendo il tier che passa capacity senza degradare la resa.
11. Marker preservation.
12. Runtime safety/capacity gate.
13. Subtitle-link audit pre-apply e cumulativo.
14. Patch in-place solo dei WEM promossi.
15. Aggiorna cumulativo e blocca ogni hash gia applicato dai batch successivi, salvo retake qualita esplicito.

La v0.2 aggiunge una build release ricostruita dal cumulativo e un resolver conservativo dei WEM generati. I file originali del gioco non vengono inclusi nel repo o nel pacchetto.
