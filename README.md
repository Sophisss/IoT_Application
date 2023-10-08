# IoT_DevQ_Application
Lo scopo di questa applicazione è la creazione di un applicativo di configurazione e
un’applicazione mobile di esempio.
L’applicativo di configurazione verrà utilizzato in scenari in cui del personale tecnico
specializzato dovrà configurare il funzionamento del sistema IoT finale in base alle esigenze
del cliente. Ad esempio, permetterà di aggiungere entità, personalizzarne le proprietà e creare
relazioni tra di loro, ma anche di configurare impostazioni relative alla sicurezza come, ad
esempio, il comportamento del sistema per quanto riguarda l’autenticazione degli utenti.
In questo contesto, visto che la prima versione del sistema sarà
basata su AWS, il configuratore potrà decidere se creare o meno uno User Pool su Amazon
Cognito (servizio di AWS dedicato alla user-management), definirne i parametri e le regole di
funzionamento.
Alla fine del proprio lavoro l’utente configuratore avrà costruito una configurazione per il
sistema che potrà essere utilizzata per la generazione del codice ed, inoltre, verrà archiviata in
modo tale da rendere possibili future evoluzioni o revisioni del funzionamento.
Questa configurazione di sistema è costituita da un file in formato JSON che rappresenta la
struttura vera e propria e contiene tutte le informazioni, i parametri e le necessità del cliente
riguardo alle entità e alle relazioni fra queste ultime. Questo file può in qualunque momento
essere utilizzato per generare le altre risorse, ma può anche essere completato parzialmente e
poi modificato in seguito. Utilizzando questa configurazione possiamo generare diversi
artefatti:
• Una cartella compressa in formato ZIP contenente i file necessari al funzionamento del
sistema personalizzato, fra cui:
- Un template che descrive tutta l’infrastruttura cloud. Nell'ambito di AWS questo
template è un file in formato YAML che elenca tutte le risorse da generare e tutte le relative
impostazioni. Utilizzando CloudFormation, un servizio AWS in grado di creare risorse a
partire da questi file YAML, saremo in grado di costruire in modo replicabile la nostra
infrastruttura cloud. I vantaggi di usare questi servizi, che permettono di adottare un
approccio Infrastructure as Code (IaC), sono molteplici, tra cui: la possibilità di fare
provisioning di risorse in modo automatico, il versioning dell’infrastruttura in modo tale da
avere uno storico di come essa sia evoluta nel tempo, la possibilità duplicare l’intera
infrastruttura in diverse region per permettere di abbattere i tempi di latenza o ancora la
possibilità di duplicarla in diversi ambienti come development, staging, production, ...
- Il codice delle API, necessario per poter manipolare i dati correttamente e interagire
con il Database tramite le operazioni CRUD (create, read, update, delete), che sarà oggetto di
analisi approfondita con lo scopo di capire se sia possibile utilizzare servizi come ORM o
GraphQL (un linguaggio e runtime di query per API) o se invece si debba optare per l’utilizzo
di normali API REST.
Una parte di codice è generata automaticamente in base alle informazioni inserite dall’utente
durante la procedura di setup, il resto è molto flessibile per potersi così adattare alle possibili
configurazioni del sistema.
• Una cartella compressa in formato ZIP contenente una parte di codice delle App mobili
native per Android/IOS, preferite rispetto a delle piattaforme multipiattaforma (es. Flutter,
React native, etc.) che non garantiscono gli standard di personalizzazione e customizzazione
richieste tipicamente dai clienti. Questo codice costituirà una base da cui partire per la
realizzazione delle applicazioni mobili destinate al cliente e agli utenti.
Nel contesto del group project si tratterà di un’app mobile di esempio per valutare il corretto
funzionamento delle risorse generate dall’applicativo di configurazione nella loro interezza:
codice generato, risorse cloud e codice delle app.
• Un file in formato Markdown utilizzabile dal cliente e contenente una guida passo passo per
portare a termine il deploy del codice e delle risorse generate.
Grazie a questo processo si potrà configurare un sistema ampiamente personalizzato sulla
base delle singole necessità del cliente in tempi molto più brevi rispetto all’intera procedura
di creazione.

Requisiti principali del sistema/prodotto finale da realizzare
Le funzionalità del sistema includono:
● La possibilità per gli utenti di creare una configurazione personalizzata da zero o da
una parzialmente completa
● La generazione del codice e la possibilità per gli utenti di esportarlo tramite un file ZIP
che contiene tutti i componenti
● La fornitura di una guida dettagliata per assistere gli utenti nel processo di deploy
dell'applicazione sul cloud
Dopo aver arricchito l'applicazione mobile con il codice generato dal sistema, inclusi i
componenti di autenticazione e le API, l'applicazione è in grado di:

● Permettere all’utente di registrarsi ed autenticarsi
● Creare nuove entità
● Modificare le configurazioni delle entità esistenti
● Eliminare entità
