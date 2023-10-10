import {Component} from '@angular/core';
import {Entity} from '../Models/Entity';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Configuration} from '../Models/Configuration';
import {Field} from '../Models/Field';
import {JsonDownloadService} from "../Services/JSONdownload/json-download.service";

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
    this.configuration.entities.push(this.entity)
    const jsonEntities = [];
    for (const entity of this.configuration.entities) {
      const jsonFields = [];

      for (const field of entity.fields) {
        jsonFields.push({
          name: field.name,
          type: field.type,
          required: field.required
        });

      }

      jsonEntities.push({
        name: entity.entity_name,
        fields: jsonFields
      });
    }

    const jsonObject = {
      entities: jsonEntities
    };


    this.resetForm()
    console.log(jsonObject)

    this.jsonDownloadService.setData(jsonObject);
  }

  closeAttributesForm() {
    this.showForm = false;
  }

  export() {
    this.jsonDownloadService.downloadJson()
  }

  click() {
  }
}
