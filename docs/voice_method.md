# Metodo voci v0.3

Le voci target sono template o varianti approvate per personaggio. La resa finale non e un clone diretto del take inglese: la voce target resta l'identita, mentre l'audio sorgente guida performance, intenzione, pause, respiri, urla, tosse, distanza e intensita.

La variante senza patos, usata nei test locali, viene generata usando solo la voce target e il testo italiano. La variante source-first aggiunge il source audio come riferimento di performance. Questo permette di mostrare che il risultato non e one-shot clone: identita vocale e regia della recitazione sono due passaggi separati.

Quando il testo italiano non entra nel tempo disponibile, la frase viene adattata professionalmente. La v0.3 preferisce mantenere pathos e timing anche se resta un lieve accento, perche i test di accent polish troppo aggressivo hanno spesso reso la recitazione piatta o meno credibile.

La produzione ora distingue due tier: `gold strict`, per i take che passano anche conformance/pathos source-first, e `playable provisional`, per aumentare rapidamente la copertura mantenendo obbligatori ASR, timing, semantica, sottotitoli, capacity e runtime safety. Il tier provisional resta debito di rifinitura, non approvazione attoriale definitiva.
