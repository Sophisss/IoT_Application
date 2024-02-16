import { Component, ViewChild } from '@angular/core';
import { DxFormComponent } from 'devextreme-angular';
import { ConfigurationService } from 'src/app/services/configuration.service';

@Component({
  selector: 'app-tab-panel',
  templateUrl: './tab-panel.component.html',
  styleUrl: './tab-panel.component.scss'
})
export class TabPanelComponent {

  @ViewChild(DxFormComponent, { static: false }) form: DxFormComponent;

  selectedTabIndex = 0;

  database_name: string;

  isDisable_firstTab = false;

  isDisable_secondTab = true;

  isDisable_thirdTab = true;

  isButtonDisabled = true;

  labelTemplates = [
    {name: 'database name', icon: 'dx-icon-info'},
    {name: 'table name', icon: 'dx-icon-info'}
]

choice = [ 'Shadow changes', 'Receive mqtt message']



  seconStep() {
    if (this.isDisable_secondTab == true) {
      this.isDisable_secondTab = !this.isDisable_secondTab;
      this.selectedTabIndex = 1;
  }
}


  thirdStep() {
      if (this.isDisable_thirdTab == true) {
        this.isDisable_thirdTab = !this.isDisable_thirdTab;
        this.selectedTabIndex = 2;
    }

}
}
