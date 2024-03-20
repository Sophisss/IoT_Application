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

  icon = "menu";

  buttonOptions: any = this.getButtonOptions();

  updateButtonOptions() {
    this.buttonOptions = this.getButtonOptions();
  }

  getButtonOptions() {
    return {
      icon: this.icon,
      onClick: () => {
        this.toggleSidebar();
        this.updateButtonOptions();
      }
    };
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
    this.icon = this.isSidebarOpen ? "menu" : "chevrondoubleleft";
    if (this.isSidebarOpen) {
      this.icon = "menu";
    } else {
      this.icon = "chevrondoubleleft";
    }
    this.toggleSidebarForMe.emit();
  }
}
