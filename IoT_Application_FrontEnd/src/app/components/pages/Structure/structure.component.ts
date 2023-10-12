import { Component } from '@angular/core';
import { Entity } from '../../../Models/Entity';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Configuration } from '../../../Models/Configuration';
import { Field } from '../../../Models/Field';
import { JsonDownloadService } from "../../../Services/JSONdownload/json-download.service";
import { Link } from '../../../Models/Link';
import Drawflow from 'drawflow';



@Component({
  selector: 'app-structure',
  templateUrl: './structure.component.html',
  styleUrls: ['./structure.component.scss']
})
export class StructureComponent {

  //This is a variable, to associate all Http response.
  responseData: any;

  //This is the variable for the FormGroup.
  form!: FormGroup;

  //New configuration
  configuration: Configuration = new Configuration;

  //Boolean variables to indicate if form is visible.
  showForm = false

  entity!: Entity;

  /**
   * Constructor for this Component.
   * @param formBuilder
   * @param jsonDownloadService
   */
  constructor(
    private formBuilder: FormBuilder,
    private jsonDownloadService: JsonDownloadService,
  ) {
  }

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

  /**
   * This method create a new entity and allow you to view the form
   */
  openForm() {
    this.showForm = true
    const nome = this.form.value.nome;
    this.entity = new Entity(nome);
  }

  saveEntity() {
    const nome = this.form.value.nome;
    this.entity = new Entity(nome);
    this.saveConfiguration()
  }

  saveAttributes() {
    const nomeAttributo = this.form.value.nomeAttributo
    const type = this.form.value.type
    const isrequired = this.form.value.isrequired
    const newField = new Field(nomeAttributo, type, isrequired)
    this.entity.fields.push(newField)
    this.resetForm()
  }

  /**
   * This method create a new configuration
   */
  saveConfiguration() {
    this.configuration.entities.push(this.entity);
    this.showForm = false;
    const jsonEntities = this.createEntityJson()
    const jsonLinks = this.createLinkJson()
    const jsonTable = this.createTableJson()

    const jsonObject = {
      projectName: "Prova",
      entities: jsonEntities,
      links: jsonLinks,
      awsConfig: {
        dynamo: {
          tables: jsonTable
        }
      }
    };

    this.resetForm();
    console.log(jsonObject);

    this.jsonDownloadService.setData(jsonObject);
  }

  createEntityJson() {
    const jsonEntities = this.configuration.entities.map(entity => ({
      name: entity.entity_name,
      fields: this.createFields(entity)
    }));
    return jsonEntities
  }


  createLinkJson() {
    const jsonLink = this.configuration.links.map(link => ({
      first_entity: link.first_entity,
      second_entity: link.second_entity,
      fields: this.createFields(link)
    }));
    return jsonLink
  }

  createFields(object: Entity | Link) {
    const fields = object.fields.map(field => ({
      name: field.name,
      type: field.type,
      required: field.required
    }))
    return fields
  }

  createTableJson() {
    const jsonTable = this.configuration.tables.map(table => ({
      tableName: table.name,
      partitionKey: table.partition_key,
      sortKey: table.sort_Key
    }))
    return jsonTable
  }

  export() {
    this.jsonDownloadService.downloadJson()
  }



  //------

  drag() {
    
  }

  drop() {

  }


  addNodeToDrawFlow() {

  }
}