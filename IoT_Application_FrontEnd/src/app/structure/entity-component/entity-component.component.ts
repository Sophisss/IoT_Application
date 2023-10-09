import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Configuration } from 'src/app/Models/Configuration';
import { Entity } from 'src/app/Models/Entity';
import { environment } from 'src/environments/environments';

@Component({
  selector: 'app-entity-component',
  templateUrl: './entity-component.component.html',
  styleUrls: ['./entity-component.component.scss']
})
export class EntityComponentComponent {
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
