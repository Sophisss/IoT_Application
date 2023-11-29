import {Component, OnInit, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";
import {HttpClient} from "@angular/common/http";
import {ImportServiceService} from "../../services/import-service.service";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent implements OnInit {
  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;

  popupVisible = false;
  sidebarToggle: boolean = false;

  constructor(private http: HttpClient, private importService: ImportServiceService) {
  }

  ngOnInit(): void {
    const diagramFlow = this.importService.getSavedFileContent();
    console.log(diagramFlow);
    if (diagramFlow) {
      this.diagram.instance.import(JSON.stringify(diagramFlow));
    }
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
