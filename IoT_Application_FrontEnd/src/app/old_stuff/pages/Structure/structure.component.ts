import {Component} from '@angular/core';
import {Entity} from '../../Models/Entity';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Configuration} from '../../Models/Configuration';
import {JsonDownloadService} from "../../../services/json-download.service";


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
    //this.entity = new Entity(nome);
  }


}
