import { Component } from '@angular/core';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent {
  toggleSidebar: boolean = true;


  setToggleSidebar() {
    this.toggleSidebar = !this.toggleSidebar;
  }

  getToggleSidebar() {
    return this.toggleSidebar;
  }

}
