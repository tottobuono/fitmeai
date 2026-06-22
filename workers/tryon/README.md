# workers/tryon — Worker async di try-on

Consumer che esegue i job di generazione in modo asincrono, fuori dal ciclo richiesta/risposta
dell'API.

## Responsabilità
- Consumare i `TryOnJob` dalla coda (Redis).
- Invocare il provider tramite l'astrazione `VirtualTryOnProvider.generate(TryOnRequest)`.
- Salvare l'immagine risultante su storage EU e aggiornare lo stato del job (`done`/`failed`).
- Gestione base di errori e retry.

## Confini
- **Non** espone API pubbliche.
- Conosce solo il **contratto interno** del provider, non i dettagli del singolo fornitore.
- **Non** contiene logica di fit/sizing.

## Stato
🚧 Placeholder. Il consumer arriva con il Task 6.
