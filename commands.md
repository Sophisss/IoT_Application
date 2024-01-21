### Api template deployment

```bash
sam build -t .\template\api.yaml
```

```bash
sam deploy --stack-name devq-iot-platform-graphql --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoTPlatform --s3-bucket devq.iot.iot-platform --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
```

### Cognito template deployment

```bash
sam build -t .\template\cognito.yaml
```

```bash
sam deploy --stack-name devq-iot-platform-cognito --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoTPlatform --s3-bucket devq.iot.iot-platform --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
```