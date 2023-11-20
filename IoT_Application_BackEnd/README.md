# COMMANDS FOR DEPLOYMENT

### Angular application deployment

- sam build --template-file ...
- sam deploy --stack-name devq-iot-platform-frontend --template-file .aws-sam/build/template.yaml  --parameter-overrides Project=IoT_Platform --s3-bucket devq.iot.iot-platform  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND


### Cognito template deployment

- sam build --template-file cognito.yaml
- sam deploy --stack-name devq-iot-platform-cognito --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoT_Platform  --s3-bucket devq.iot.iot-platform  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND

### GraphQL template deployment

- sam build --template-file api.yaml 
- sam deploy --stack-name devq-iot-platform-graphql --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoT_Platform  --s3-bucket devq.iot.iot-platform  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND

### Template with aws resources deployment

- sam build --template-file template.yaml
- sam deploy --stack-name devq-iot-platform --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoT_Platform  --s3-bucket devq.iot.iot-platform  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
