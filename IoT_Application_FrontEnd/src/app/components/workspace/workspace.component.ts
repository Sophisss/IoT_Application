import {Component} from '@angular/core';
import {MatSidenav} from "@angular/material/sidenav";

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent {
  sidebarToggle: boolean = false;
  //TODO: correggere
  sidenav: MatSidenav;

  constructor() {
  }

  toggleSidebar() {
    this.sidebarToggle = !this.sidebarToggle;
    this.sidenav.toggle();
  }

  getToggleSidebar() {
    return this.sidebarToggle;
  }
}
