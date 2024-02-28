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

  iot: IoT = this.configService.getIoTConfiguration();

  choice_list = [
    { text: "Sending and storing data when the device status changes", value: false },
    { text: "Sending and storing data when receives an MQTT message with changes to a device shadow", value: false }
  ];

  selectFieldPattern: RegExp = /^topic\(\d+\) as [A-Za-z]+$/;

  // Variabile to change box visibility

  firstBoxZIndex = 1000

  secondBoxZIndex = 0

  thirdBoxZIndex = 0

  // Variable to show toast message

  isToastVisible: boolean;

  type = 'success';

  message = '';

  // Other variables

  configure_topic: boolean = false;

  showTopics: boolean = false;

  changeConfiguration = false;

  isSecondBoxValid = true;

  constructor(private formBuilder: FormBuilder,
    public configService: ConfigurationService) { }


  ngOnInit(): void {
    this.initForm();
    this.initCheckBox();
  }

  /**
   * This method is used to initialize the form.
   */
  initForm() {
    this.form = this.formBuilder.group({
      database_name: [this.iot.database_name, Validators.required],
      table_name: [this.iot.table_name, Validators.required],
      topic: [this.iot.topic, Validators.required]
    });
  }

  /**
 * This method is used to initialize the checkbox.
 */
  initCheckBox() {
    this.choice_list.forEach((choice, index) => {
      choice.value = index === 0 ? this.iot.shadow_notify : index === 1 && (this.configure_topic = !!this.iot.topic_notify);
    });

    this.showTopics = this.choice_list.every(choice => choice.value);
  }

  /**
 * This method is used to show the second box and hide the first box.
 */
  firstBox_nextButton() {
    this.iot.database_name = this.form.value.database_name;
    this.iot.table_name = this.form.value.table_name;

    if (this.iot.database_name != '' && this.iot.table_name != '') {
      this.firstBoxZIndex = 0;
      this.secondBoxZIndex = 1000;
    }
  }

  /**
   * This method is used to show the first box and hide the second box.
   */
  secondBox_backButton() {
    this.firstBoxZIndex = 1000;
    this.secondBoxZIndex = 0;
  }

  /**
   * This method is used to show the third box and hide the second box.
   */
  secondBox_nextButton() {
    this.checkSecondBoxValidity();

    if (this.isSecondBoxValid) {
      this.isShowedTopics();
      this.secondBoxZIndex = 0;
      this.thirdBoxZIndex = 1000;
    }
  }

  /**
   * This method is used to check the validity of the second box.
   */
  checkSecondBoxValidity() {
    this.isSecondBoxValid = this.choice_list.find(item => item.value) != null;
  }

  isShowedTopics() {
    this.configure_topic = this.iot.topic_notify;
    this.showTopics = this.iot.shadow_notify && this.iot.topic_notify;
  }

  /**
   * This method is used to show the second box and hide the third box.
   */
  thirdBox_backButton() {
    this.secondBoxZIndex = 1000;
    this.thirdBoxZIndex = 0;
  }

  /**
 * This method saves the IoT rule configuration.
 */
  save_button() {
    if (!this.configure_topic) {
      this.resetData();
      this.ifSuccess();
    } else {
      this.iot.topic = this.form.value.topic;
      this.iot.select_fields = this.configService.selectedItems;

      if (this.iot.topic !== '' && this.iot.select_fields.length > 0) this.ifSuccess();
    }
  }

  /**
   * This method is used to reset the data.
   */
  private resetData() {
    this.form.value.topic = '';
    this.iot.select_fields = [];
    this.configService.selectedItems = [];
  }

  /**
   * This method is used when the configuration is successful.
   */
  private ifSuccess() {
    this.showToast('The IoT rule has been successfully configured!');
    this.changeConfiguration = true;
  }

  /**
   * This method is used to show the toast message.s
   * @param message The message to show.
   */
  private showToast(message: string) {
    this.message = message;
    this.isToastVisible = true;
    this.thirdBoxZIndex = 0;
  }

  /**
   * This method is used to change the configuration.
   */
  modify_iot_rules_configuration() {
    if (this.changeConfiguration) this.firstBoxZIndex = 1000;
  }

  /**
   * This method is used when a checkbox is changed.
  */
  onStorageMethodChanged() {
    this.checkSecondBoxValidity();

    this.iot.shadow_notify = this.choice_list[0].value;
    this.iot.topic_notify = this.choice_list[1].value;
  }

  /**
   * This method save the selected items.
   * @param event The event that contains the selected items.
   */
  onValueChanged(event: any) {
    this.configService.selectedItems = event.value;
  }
}
