import {Component, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";
import {Router} from "@angular/router";
import {WorkspaceComponent} from "../workspace/workspace.component";
import {CustomCommandsService} from "../../services/custom-commands.service";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent {

  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;

  constructor(private router: Router, private workspace: WorkspaceComponent, private customCommandsService: CustomCommandsService) {
  }

  log() {
    console.log('log')
  }

  onCustomCommand(e: any) {
    this.customCommandsService.executeCommand(e.name);
  }

  requestEditOperationHandler(e: any) {
    if (e.operation === "changeConnection")
      if (e.args.connector && e.args.connector.fromId === e.args.connector.toId)
        e.allowed = false;
  }

  openFieldsEditor() {
    this.router.navigate(['new/card/content']);
    this.workspace.setToggleSidebar()
    console.log(this.workspace.getToggleSidebar())
  }
}
