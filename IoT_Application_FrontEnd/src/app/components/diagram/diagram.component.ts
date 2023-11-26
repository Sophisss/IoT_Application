import {Component, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";
import {Router} from "@angular/router";
import {WorkspaceComponent} from "../workspace/workspace.component";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent {

  constructor(private router: Router, private workspace: WorkspaceComponent) {
  }

  log() {
    console.log('log')
  }

  @ViewChild(DxDiagramComponent, { static: false }) diagram: DxDiagramComponent;
  requestEditOperationHandler(e: any) {
    if (e.operation === "changeConnection")
      if (e.args.connector && e.args.connector.fromId === e.args.connector.toId)
        e.allowed = false;
  }

  protected readonly navigator = navigator;

  openFieldsEditor() {
    this.router.navigate(['new/card/content']);
    this.workspace.setToggleSidebar()
    console.log(this.workspace.getToggleSidebar())
  }
}
