import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ConfigurationService } from "../../services/configuration.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  @Input() isSidebarOpen: boolean = false;
  @Output() toggleSidebarForMe: EventEmitter<any> = new EventEmitter();
  @Output() exitClicked: EventEmitter<void> = new EventEmitter<void>();

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
      this.exitClicked.emit();
    }
  }

  constructor(protected configurationService: ConfigurationService) { }

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
