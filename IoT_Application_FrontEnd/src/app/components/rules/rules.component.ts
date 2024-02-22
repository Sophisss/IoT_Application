import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { IoT } from 'src/app/models/iot.model';
import { ConfigurationService } from 'src/app/services/configuration.service';

@Component({
  selector: 'app-rules',
  templateUrl: './rules.component.html',
  styleUrl: './rules.component.scss'
})
export class RulesComponent implements OnInit {

  form !: FormGroup;

  modify_rule: boolean = false;

  choice_list = [
    'Sending and storing data when the device status (shadow) changes',
    'Sending and storing data when receives an MQTT message with changes to a device shadow']

  configure_topic: boolean = false;

  firstBoxZIndex = 1000

  secondBoxZIndex = 0

  thirdBoxZIndex = 0

  storage_choice: string = '';

  isToastVisible: boolean;

  isCheckboxValid: boolean = false;

  checkValidity = true;

  type = 'success';

  message = '';

  iot: IoT = this.configService.getIoTConfiguration();

  keepAspectRatio = true;

  handles: string[] = ['left', 'top', 'right', 'bottom'];

  resizableClasses = '';

  resizePage = false;

  constructor(private formBuilder: FormBuilder,
    public configService: ConfigurationService) { }


  ngOnInit(): void {
    this.initForm();
  }

  ngAfterViewInit() {
    this.initConfigurTopicForm();
  }


  //This is the method for init the FormGroup.
  initForm() {
    this.form = this.formBuilder.group({
      database_name: [this.iot.database_name, Validators.required],
      table_name: [this.iot.table_name, Validators.required],
      topic: [this.iot.topic, Validators.required]
    });
  }

  initConfigurTopicForm() {
    this.configure_topic = this.iot.storage_method === this.choice_list[1];
  }


  //This is the method for reset the FormGroup value.
  resetForm() {
    this.form.reset();
  }

  modify_iot_rules_configuration() {
    if (this.modify_rule) this.firstBoxZIndex = 1000;
  }


  firstBoxVisibility_backButton() {
    this.firstBoxZIndex = 1000;
    this.secondBoxZIndex = 0;
  }

  secondBoxVisibility_nextButton() {
    this.modify_rule = false;
    this.iot.database_name = this.form.value.database_name;
    this.iot.table_name = this.form.value.table_name;

    if (this.iot.database_name != '' && this.iot.table_name != '') {
      this.firstBoxZIndex = 0;
      this.secondBoxZIndex = 1000;
      this.checkValidity = true;
    }
  }

  secondBoxVisibility_backButton() {
    this.secondBoxZIndex = 1000;
    this.thirdBoxZIndex = 0;
  }

  onStorageMethodChanged(event: any) {
    this.storage_choice = event.value;
    this.isCheckboxValid = true;
  }

  thirdBoxVisibility_nextButton() {
    this.iot.storage_method = this.storage_choice;

    if (this.iot.storage_method !== '') {
      this.configure_topic = this.iot.storage_method === this.choice_list[1];
      this.secondBoxZIndex = 0;
      this.thirdBoxZIndex = 1000;
    }
  }

  save() {
    this.modify_rule = true;

    if (!this.configure_topic || this.form.value.topic !== '') {
      this.iot.topic = this.configure_topic ? this.form.value.topic : '';
      this.showToast('The IoT rule has been successfully configured!');
      this.configService.updateIoTConfiguration(this.iot);
    }
  }

  private showToast(message: string) {
    this.message = message;
    this.isToastVisible = true;
    this.thirdBoxZIndex = 0;
  }

  showResizePage() {
    this.resizePage = !this.resizePage;
  }
}
