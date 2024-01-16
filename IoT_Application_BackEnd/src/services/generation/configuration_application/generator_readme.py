def generate_readme(project_name: str) -> str:
    """
    This method generates the README.md file.
    :param project_name: The name of the project.
    :return: The README.md file.
    """
    return f"""# {project_name.upper()} PROJECT

## Introduzione

Utilizzando la configurazione definita dall'utente sulla base delle esigenze specifiche del cliente,
sono stati generati diversi artefatti.

## Template

- api.yaml: contiene la definizione delle risorse AWS che verranno create.
In questo caso sono state definite funzioni Lambda associate ad ogni entità e link,
il ruolo che verrà assunto da queste funzioni Lambda e la rispettiva policy associata
ed infine le API GraphQL che verranno esposte.

- cognito.yaml: contiene la definizione delle risorse AWS relative all'autenticazione.
In questo caso sono state definite le risorse per la creazione di un pool di utenti cognito e
le risorse per la creazione di un client relativo al pool di utenti.

## Risorse

- dal: contiene il DAL (Data Access Layer) che facilita l'interazione con il database.
- model: contiene i modelli per la definizione dei dati.
- graphql: contiene il resolver e lo schema graphql.
- event: contiene la gestione dell'evento che attiva la funzione Lambda.
- funzioni lambda progettate per gestire le operazioni CRUD.


## Per iniziare

Per le istruzioni di deploy, vedere la [Deployment Guide](./template/guide/deployment_guide.md).


    """