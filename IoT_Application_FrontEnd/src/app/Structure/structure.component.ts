import {Component, ElementRef} from '@angular/core';
import {Entity} from '../Models/Entity';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Configuration} from '../Models/Configuration';
import {Field} from '../Models/Field';
import {JsonDownloadService} from "../Services/JSONdownload/json-download.service";
import { Link } from '../Models/Link';
import Drawflow, * as drawflow from 'drawflow';



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

  editor : any

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
    const drawFlowHtmlElement = <HTMLElement>document.getElementById('drawflow-container');

    const testEditor = new Drawflow(drawFlowHtmlElement);

    this.editor = new Drawflow(drawFlowHtmlElement);

    this.editor.reroute = true;
    this.editor.curvature = 0.5;
    this.editor.reroute_fix_curvature = true;
    this.editor.reroute_curvature = 0.5;
    this.editor.force_first_input = false;
    this.editor.line_path = 1;
    this.editor.editor_mode = 'edit';

    this.editor.start();
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
    const nome = this.form.value.nome;
    this.entity = new Entity(nome);
    this.showForm = true
  }

  saveAttributes() {
    const nomeAttributo = this.form.value.nomeAttributo
    const type = this.form.value.type
    const isrequired = this.form.value.isrequired
    const newField = new Field(nomeAttributo, type, isrequired)
    this.entity.fields.push(newField)
    this.resetForm()
  }

  saveConfiguration() {
    this.showForm = false;
    this.configuration.entities.push(this.entity);
    const jsonEntities = this.createEntityJson()
    const jsonLinks = this.createLinkJson()
  
    const jsonObject = {
      entities: jsonEntities,
      links : jsonLinks
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


  createLinkJson(){
    const jsonLink = this.configuration.links.map(link => ({
      first_entity: link.first_entity,
      second_entity: link.second_entity,
      fields : this.createFields(link)
    }));
    return jsonLink
  }

  createFields(object: Entity | Link){
    const fields = object.fields.map(field => ({
      name: field.name,
      type: field.type,
      required: field.required
    }))
    return fields
  }

  export() {
    this.jsonDownloadService.downloadJson()
  }

}