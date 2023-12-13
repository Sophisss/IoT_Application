import {Component} from '@angular/core';
import {ToggleService} from "../../services/toggle.service";

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent {
  constructor(private toggleService: ToggleService) {
  }

  /**
   * Returns the drawer state to the template to handle the drawer open/close.
   */
  getDrawerOpen(): boolean {
    return this.toggleService.isDrawerOpened();
  }
}
