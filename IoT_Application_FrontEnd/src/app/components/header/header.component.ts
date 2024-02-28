import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ConfigurationService } from "../../services/configuration.service";
import { Router } from '@angular/router';
import { IoT } from 'src/app/models/iot.model';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  @Input() isSidebarOpen: boolean = false;
  @Output() toggleSidebarForMe: EventEmitter<any> = new EventEmitter();

  isModifiable: boolean = false;

  buttonOptions: any = {
    icon: "menu",
    onClick: () => {
      this.toggleSidebar();
    }
  }

  exitButtonOptions: any = {
    icon: 'export',
    text: 'Exit',
    onClick: () => {
      this.initDiagram();
      this.initIoTRules();
      this.router.navigate(['']);
    }
  }


  initDiagram() {
    this.configurationService.items = [];
  }

  initIoTRules() {
    const iot = new IoT();
    this.configurationService.updateIoTConfiguration(iot);
  }

  constructor(protected configurationService: ConfigurationService, private router: Router) { }

  /**
   * Handles the switch to the text mode of the title of the project.
   */
  switchToText() {
    this.isModifiable = false;
    this.configurationService.updateContent();
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
    this.toggleSidebarForMe.emit();
  }
}
