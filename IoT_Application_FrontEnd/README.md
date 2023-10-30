# Deploy CloudFormation resources on AWS S3

**IMPORTANT: The resources have already been deployed so these steps are to be performed only if the stack 
and bucket have been deleted.**

To deploy the resources the steps are:
1) Execute on CLI the command `sam build`
2) Execute on CLI the command `sam deploy --stack-name devq-iot-platform --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoT_Application --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND`
3) Go on 'AWS Console > S3 > devq-iot-platform > Autorizzazioni > Proprietà dell'oggetto' and enable ACL
4) Execute on CLI the command `npm run aws-publicaaccessblock`
5) Execute on CLI the command `sam build --template full.yml`
6) Execute on CLI the command `sam deploy --stack-name devq-iot-platform --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoT_Application --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND`

# Deploy Angular resources on AWS S3

**IMPORTANT: Perform this every time there is a change in the code.**

1) Execute on CLI the command `npm run aws-deploy`
2) (Optional) To show the URL of the hosted website, execute on CLI the command `aws cloudformation describe-stacks --stack-name devq-iot-platform --query 'Stacks[0].Outputs[0].OutputValue' --output text`

# IoTApplicationFrontEnd

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 16.2.5.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
