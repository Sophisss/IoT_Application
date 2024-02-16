import {Component} from '@angular/core';
import {ToggleService} from "../../services/toggle.service";

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent {

  isDrawerOpened: boolean = false;

  constructor(private toggleService: ToggleService) {
  }


  sideBarToggler() {
    this.isDrawerOpened = !this.isDrawerOpened;
  }

  getDrawerOpen(): boolean {
    return this.toggleService.isDrawerOpened();
  }
}
