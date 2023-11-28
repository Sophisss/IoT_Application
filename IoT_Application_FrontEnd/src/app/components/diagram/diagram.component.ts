import {Component, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent {

  popupVisible = false;
  sidebarToggle: boolean = false;

  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;

  constructor() {
  }

  log() {
    console.log('log')
  }

  onCustomCommand(e: any) {
    const commandName: string = e.name;

    if (commandName === 'export') {
      console.log('export')
    }
    if (commandName === 'viewJson') {
      this.showJson();
    }
  }

  requestEditOperationHandler(e: any) {
    if (e.operation === "changeConnection")
      if (e.args.connector && e.args.connector.fromId === e.args.connector.toId)
        e.allowed = false;
  }

  showPopup(event: any) {
    this.popupVisible = true;
    console.log(event);
  }

  private showJson() {
    this.sidebarToggle = !this.sidebarToggle;
    //this.diagram.instance.beginUpdate();
  }
}
