import { Component } from '@angular/core';
import { environment } from 'src/environments/environments';
import { Entity } from '../Models/Entity';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Configuration } from '../Models/Configuration';
import { Field } from '../Models/Field';

@Component({
  selector: 'app-structure',
  templateUrl: './structure.component.html',
  styleUrls: ['./structure.component.scss']
})
export class StructureComponent {

  responseData: any;

  //This is the variable for the FormGroup.
  form!: FormGroup;

  entities: Entity[] = [];

  configuration: Configuration = new Configuration;


  showForm = false

  entity!: Entity;

  /**
   * Constructor for this Component. 
   * @param httpClient the HttpClient object.
   */
  constructor(
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
      nome: ['', Validators.required],
      nomeAttributo: ['', Validators.required],
      type: ['', Validators.required],
      isrequired: ['', Validators.required]
    });
  }

  openForm() {
    const nome = this.form.value.nome;
    this.entity = new Entity(nome);
    this.configuration.entities.push(this.entity)
    this.showForm = true
    console.log("Entità aggiunta")
  }

  save() {
    const nomeAttributo = this.form.value.nomeAttributo
    const type = this.form.value.type
    const isrequired = this.form.value.isrequired
    const newField = new Field(nomeAttributo, type, isrequired)
    this.entity.fields.push(newField)
    this.resetForm()
  }

  closeAttributesForm() {
    this.showForm = false;
  }

  export() {
    const jsonEntities = this.configuration.entities.map(entity => (this.exportFields(entity)));
    const jsonObject = {
      entities: jsonEntities
    };
    this.resetForm()
    console.log(jsonObject)
  }

  exportFields(entity: Entity) {
    const jsonField = entity.fields.map(fields => ({
      name: entity.entity_name,
      fields: [{
        name: fields.name,
        type: fields.type,
        required: fields
      }]
    }))
    return jsonField
  }



  click() {
    console.log("Stampa")
  }

}
