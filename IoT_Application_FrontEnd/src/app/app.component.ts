import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Entity } from './Models/Entity';
import { Configuration } from './Models/Configuration';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environments';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'IoT_Application_FrontEnd';

  responseData: any;

  //This is the variable for the FormGroup.
  form!: FormGroup;

  entities: Entity[] = [];

  configuration: Configuration = new Configuration;


  showForm = false

  /**
   * Constructor for this Component. 
   * @param httpClient the HttpClient object.
   */
  constructor(
    private httpClient: HttpClient,
    private formBuilder: FormBuilder
  ) { }

  ngOnInit(): void {
    this.initForm();
  }

  //This is the method for reset the FormGroup value.
  resetForm() {
    this.form.reset();
  }

  //This is the method for reset the Data from backend.
  resetData() {
    this.responseData = null;
  }

  //This is the method for init the FormGroup. 
  initForm() {
    this.form = this.formBuilder.group({
      nome: ['', Validators.required]
    });
  }

  add() {
    this.showForm = true
  }

  close() {
    this.showForm = false
  }

  click(){
    console.log("Stampa")
  }

  addEntity() {
    const nome = this.form.value.nome;
    const newEntity = new Entity(nome);
    this.configuration.entities.push(newEntity);
    console.log("Entità aggiunta")
    this.resetForm();
  }

  export() {
    const jsonEntities = this.configuration.entities.map(entity => ({ name: entity.entity_name }));
    const jsonObject = {
      entities: jsonEntities
    };
    console.log(jsonObject)
    this.httpClient.post(`${environment.baseUrl}/test`, jsonObject).subscribe(
      response => {
        this.responseData = response;
        if (this.responseData.statusCode == 200) {
          console.log("Dati inviati con successo");
          this.resetData()
        }
      }, err => {
        console.log("Errore" + err)
      }
    )
  }

}