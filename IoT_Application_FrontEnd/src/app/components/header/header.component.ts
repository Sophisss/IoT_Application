import {Component, EventEmitter, Output} from '@angular/core';
import {ConfigurationService} from "../../services/configuration.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  @Output() toggleSidebarForMe: EventEmitter<any> = new EventEmitter();

  isModifiable: boolean = false;

  buttonOptions: any = {
    icon: "menu",
    onClick: () => {
      this.toggleSidebar();
    }
  }

  constructor(protected configurationService: ConfigurationService) {
  }

  /**
   * Handles the switch to the text mode of the title of the project.
   */
  switchToText() {
    this.isModifiable = false;
    this.configurationService.updateContent();
  }

  toggleSidebar() {
    this.toggleSidebarForMe.emit();
  }
}
