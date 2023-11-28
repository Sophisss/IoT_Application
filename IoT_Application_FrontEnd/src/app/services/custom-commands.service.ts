import {Injectable} from '@angular/core';
import {DiagramComponent} from "../components/diagram/diagram.component";
import {WorkspaceComponent} from "../components/workspace/workspace.component";
import {MatSidenav} from "@angular/material/sidenav";

@Injectable({
  providedIn: 'root'
})
export class CustomCommandsService {


  workspace: WorkspaceComponent = new WorkspaceComponent();

  constructor() {
  }

  executeCommand(commandName: string) {
    if (commandName === 'export') {
      console.log('export')
    }
    //TODO: correggere
    if (commandName === 'viewJson') {
      this.workspace.toggleSidebar()
      console.log(this.workspace.getToggleSidebar());
    }
  }
}
