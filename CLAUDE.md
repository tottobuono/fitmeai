# CLAUDE.md

## 1. Panoramica progetto
Fitme.ai è una startup AI-native per **virtual try-on** e **fit intelligence**: aiuta gli utenti a capire come un capo visto su un e‑commerce (es. Zara, Nike) potrebbe stare sul proprio corpo, prima di acquistare.

Modalità supportate:
- **Foto + misure**: l’utente carica 1–2 foto del corpo e inserisce misure (altezza, peso, torace, vita, fianchi, ecc.). Il sistema genera immagini fotorealistiche con il capo indossato e fornisce insight sulla vestibilità/taglia.
- **Solo misure**: l’utente non fornisce foto, solo misure. Il sistema usa un avatar/modello rappresentativo con proporzioni simili per mostrare il capo, e comunque restituisce suggerimenti di fit/taglia.

Obiettivi chiave:
- MVP credibile in **2–3 mesi**.
- Usare **API esterne di virtual try‑on**, non modelli locali, in questa fase.
- Tenere il layer di rendering **provider‑agnostic** (facile cambiare modello/fornitore).
- Separare **rendering immagine** da **logica di fit/sizing**.
- Progettare da subito pensando a **GDPR** e **AI Act** (privacy, trasparenza, diritti utente).

## 2. Stack consigliato
- **Frontend**: Next.js + TypeScript.
- **Backend**: FastAPI (Python) con tipizzazione forte.
- **Database**: PostgreSQL.
- **Storage**: bucket S3‑compatibile in regione EU (es. eu-central-1).
- **Async jobs**: coda + worker (es. Redis + worker Python).
- **Virtual try‑on**: adapter interno verso provider esterni (es. TryOn‑API/Fal/FASHN), nessuna chiamata diretta dal frontend.

Questi dettagli sono linee guida; se il progetto usa uno stack diverso, mantieni comunque gli stessi principi architetturali.

## 3. Regole architetturali
1. **Provider di try‑on dietro un’unica astrazione**  
   - Nessun componente UI o business deve chiamare direttamente provider esterni.  
   - Esporre un’interfaccia interna del tipo `VirtualTryOnProvider.generate(TryOnRequest) -> TryOnResult`.

2. **Separazione delle responsabilità**  
   - Moduli distinti per: profilo corpo, ingestion del capo, orchestrazione try‑on, fit/sizing, compliance.  
   - La logica di raccomandazione taglia/fit non vive dentro gli adapter dei provider.

3. **Provider‑agnostic**  
   - Tutto il codice fuori dagli adapter deve conoscere solo il contratto interno, non i dettagli del singolo fornitore.  
   - Cambiare provider o modello deve richiedere modifiche minime.

4. **Semplicità prima**  
   - Preferire soluzioni semplici, esplicite, facilmente manutenibili.  
   - Evitare over‑engineering, microservizi inutili, astrazioni premature.

5. **Privacy by design**  
   - Trattare foto e misure come dati personali sensibili.  
   - Minimizzare ciò che salvi e ciò che logghi.  
   - Prevedere da subito retention, cancellazione, consenso e audit.

## 4. Requisiti di compliance (GDPR / AI Act)
- **Dati**: foto corpo, misure, immagini generate e metadati sono tutti potenzialmente dati personali.  
- **Log**: non loggare mai contenuti di immagini, misure in chiaro o identificativi inutili.  
- **Storage**: preferire regioni EU, URL firmati a breve scadenza, cifratura at‑rest e in‑transit.  
- **Diritti utente**: prevedere API/flow per cancellazione, esportazione e rettifica dei dati.  
- **Trasparenza AI**: marcare in UI che le immagini di try‑on sono generate da AI, non foto reali.  
- **Fornitori esterni**: considerarli come processor/sub‑processor, con DPA e SCC ove necessario.

## 5. Stile di ingegneria
- Scrivere codice **pronto per la produzione**, non solo pseudo‑codice.  
- Usare modelli tipizzati (es. Pydantic/TypeScript types) per request, response, entità di dominio.  
- Documentare brevemente trade‑off quando si fanno scelte architetturali rilevanti.  
- Favorire piccoli cambi incrementali e facilmente revisionabili.  
- Aggiornare documentazione e schema quando si introducono nuovi servizi, env vars o flussi.

## 6. Organizzazione repo (guideline)
Struttura raccomandata (adattabile alle esigenze reali):

- `apps/web` – frontend Next.js.  
- `apps/api` – backend FastAPI.  
- `workers/tryon` – worker/consumer per job di generazione.  
- `packages/shared` – code shared (tipi, client, modelli dominio).  
- `docs/` – documentazione high‑level.  
- `.claude/agents/` – prompt degli agenti specializzati.

Non è obbligatorio seguirla alla lettera, ma evita strutture caotiche.

## 7. Workflow con gli agenti
Agenti disponibili in `.claude/agents/` (nomi indicativi):
- `00-fitme-shared-context.md` – contesto base da leggere per tutti.  
- `01-fitme-orchestrator.md` – product/system orchestrator.  
- `02-fitme-ai-tryon-agent.md` – AI & virtual try‑on.  
- `03-fitme-backend-agent.md` – backend & API.  
- `04-fitme-frontend-agent.md` – frontend.  
- `05-fitme-body-fit-agent.md` – corpo, fit & sizing.  
- `06-fitme-compliance-agent.md` – privacy & compliance.  
- `07-fitme-product-ingestion_agent.md` – ingestion prodotti/capi.  
- `08-fitme-devops-agent.md` – DevOps & piattaforma.

### Ordine di lavoro consigliato
1. **Orchestrator** – definisce scope, milestone, servizi e confini.  
2. **Backend** – entità DB, API pubbliche, orchestrazione job async.  
3. **AI try‑on** – implementa l’astrazione dei provider e la chiamata alle API esterne.  
4. **Frontend** – integra i flussi di onboarding, input capi, generazione e visualizzazione.  
5. **Body fit** – aggiunge logica di sizing, avatar e fit insights.  
6. **Compliance** – rivede flussi, retention, consenso, logging e fornitori.  
7. **DevOps** – prepara ambienti, deploy, osservabilità e controlli di costo.

Per ogni task, scegli l’agente più pertinente, carica il suo `.md` nella sessione e lavora in modo focalizzato.

## 8. Cosa evitare
- Iniziare dal training di modelli custom senza bisogno.  
- Accoppiare strettamente il codice a un singolo provider di try‑on.  
- Mischiare logica di fit/sizing dentro gli adapter dei provider.  
- Introdurre feature che rendono poco chiaro all’utente che l’immagine è generata.  
- Aggiungere complessità infrastrutturale non giustificata dall’MVP.

## 9. Output attesi
Quando si lavora con Claude in questo progetto, puntare sempre a produrre:
- strutture di file chiare
- definizioni di endpoint/API
- modelli tipizzati
- migrazioni DB
- interfacce di servizio
- test significativi
- README o note di architettura sintetiche per chi arriva dopo

Mantieni la coerenza con questo documento e con gli agenti specifici di dominio.
