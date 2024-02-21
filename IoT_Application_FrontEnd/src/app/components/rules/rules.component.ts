import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { IoT } from 'src/app/models/iot.model';
import { ToastNotificationService } from 'src/app/services/toast-notification.service';

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

  isToastVisible: boolean = false;

  type = 'success';

  message = '';

  iot: IoT = new IoT();

  constructor(private formBuilder: FormBuilder, private notificationService: ToastNotificationService) { }


  ngOnInit(): void {
    this.initForm();
  }


  //This is the method for init the FormGroup.
  initForm() {
    this.form = this.formBuilder.group({
      database_name: ['', Validators.required],
      table_name: ['', Validators.required],
      topic: ['', Validators.required]
    });
  }

  //This is the method for reset the FormGroup value.
  resetForm() {
    this.form.reset();
  }

  modify_iot_rules_configuration() {
    if (this.modify_rule == true) {
      this.firstBoxZIndex = 1000;
    }
  }

  firstBoxVisibility_backButton() {
    this.firstBoxZIndex = 1000;
    this.secondBoxZIndex = 0;
  }

  secondBoxVisibility_nextButton() {
    this.modify_rule = false;

    if (this.iot.database_name != '' && this.iot.table_name != '') {
      this.firstBoxZIndex = 0;
      this.secondBoxZIndex = 1000;
    }
  }

  secondBoxVisibility_backButton() {
    this.secondBoxZIndex = 1000;
    this.thirdBoxZIndex = 0;
  }

  thirdBoxVisibility_nextButton() {
    if (this.storage_choice != '') {

      if (this.storage_choice == this.choice_list[1]) {
        this.configure_topic = true;
      }
      else {
        this.configure_topic = false;
      }

      this.secondBoxZIndex = 0;
      this.thirdBoxZIndex = 1000;
    }
  }

  onStorageMethodChanged(event: any) {
    this.storage_choice = event.value;
  }

  save() {
    this.modify_rule = true;

    if (this.iot.topic != '' || this.configure_topic == false) {
      this.message = 'The IoT rule has been successfully configured!';
      this.isToastVisible = true;
      this.thirdBoxZIndex = 0;
    }
  }

}
