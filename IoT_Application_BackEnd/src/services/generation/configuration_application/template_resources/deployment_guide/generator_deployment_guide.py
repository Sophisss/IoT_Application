def generate_deployment_guide() -> str:
    """
    This method generates the deployment guide of the application.
    :return: the deployment guide of the application
    """
    return """# GUIDA AL DEPLOYMENT DELL'APPLICAZIONE 

Questa guida descrive i passaggi necessari per il deployment dell'applicazione.
Il deployment è il processo di distribuzione di un'applicazione in un ambiente di esecuzione,
in questo caso AWS, in modo che sia disponibile agli utenti finali.

## Build dell'applicazione

Prima di effettuare il deployment è necessario effettuare la build dell'applicazione.
La build è il processo di compilazione del codice sorgente in un formato eseguibile.
Per effettuare la build dell'applicazione è necessario eseguire il seguente comando:

```bash
sam build --template-file nome-del-file
```

Andiamo a specificare il template YAML in cui sono definite le risorse da creare
per l'applicazione.

## Deployment dell'applicazione

Una volta effettuata la build dell'applicazione è possibile effettuare il deployment.
Per effettuare il deployment è necessario eseguire il seguente comando:

```bash
sam deploy --stack-name nome-dello-stack --template-file .aws-sam/build/template.yaml 
--parameter-overrides Project=nome-del-progetto  --s3-bucket nome-del-bucket  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
```

Andiamo a specificare il nome dello stack che vogliamo creare, 
il percorso del template YAML generato dalla build, i parametri da passare al template,
il nome del bucket S3 in cui caricare il codice sorgente e le policy da aggiungere alle risorse create.

## Deployment dei template


### Api template deployment

Spostarsi nella cartella in cui si trova il template e lanciare il comando:

```bash
sam build -t api.yaml 
```

```bash
sam deploy --stack-name devq-iot-platform-graphql --template-file .aws-sam/build/template.yaml 
--parameter-overrides Project=IoT_Platform  --s3-bucket devq.iot.iot-platform  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
```


### Cognito template deployment

Spostarsi nella cartella in cui si trova il template e lanciare il comando:

```bash
sam build -t cognito.yaml
```

```bash
sam deploy --stack-name devq-iot-platform-cognito --template-file .aws-sam/build/template.yaml
--parameter-overrides Project=IoT_Platform  --s3-bucket devq.iot.iot-platform  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
```

  """
