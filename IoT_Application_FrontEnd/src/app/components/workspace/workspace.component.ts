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

  getDrawerOpen(): boolean {
    return this.toggleService.isDrawerOpened();
  }
}
