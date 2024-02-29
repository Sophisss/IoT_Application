import { Component } from '@angular/core';
import { ToggleService } from "../../services/toggle.service";
import { ConfigurationService } from 'src/app/services/configuration.service';
import { IoT } from 'src/app/models/iot.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent {

  isDrawerOpened: boolean = false;

  popupVisible: boolean = false;

  constructor(private toggleService: ToggleService,
    private configService: ConfigurationService,
    private router: Router) { }


  /**
   * Toggle the side bar to open or close it.
   */
  sideBarToggler() {
    this.isDrawerOpened = !this.isDrawerOpened;
  }

  /**
   * Get the status of the drawer.
   * @returns true if the drawer is opened, false otherwise.
   */
  getDrawerOpen(): boolean {
    return this.toggleService.isDrawerOpened();
  }

  /**
   * Show the popup to confirm the exit of the workspace.
   */
  showPopup() {
    this.popupVisible = !this.popupVisible;
  }

  /***
   * Initialize the diagram by removing all the items from the configuration service.
   */
  initDiagram() {
    this.configService.items = [];
  }

  /**
   * Initialize the IoT rules by updating the configuration service with the default IoT rules.
   */
  initIoTRules() {
    const iot = new IoT();
    this.configService.updateIoTConfiguration(iot);
  }

  /**
   * Exit the workspace and navigate to the home page.
   */
  exit() {
    this.initDiagram();
    this.initIoTRules();
    this.router.navigate(['']);
  }
}
