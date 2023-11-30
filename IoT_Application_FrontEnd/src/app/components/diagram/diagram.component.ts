import {Component, OnInit, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";
import {ActivatedRoute} from "@angular/router";
import {JsonDownloadService} from "../../services/json-download.service";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent implements OnInit {
  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;

  popupVisible = false;
  sidebarToggle: boolean = false;
  private receivedData: any;

  constructor(private route: ActivatedRoute, private jsonDownload : JsonDownloadService) {
  }

  async ngOnInit(): Promise<void> {
    this.route.queryParams.subscribe(params => {
      this.receivedData = params['file'];
    });
    await (1);
    this.diagram.instance.import(this.receivedData, false)
  }

  onCustomCommand(e: any) {
    const commandName: string = e.name;

    if (commandName === 'export') {
      this.exportToJson();
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
    this.diagram.instance.focus();
  }

  private exportToJson() {
    this.jsonDownload.setData(this.diagram.instance.export());
    this.jsonDownload.downloadJson('diagram');
  }
}
