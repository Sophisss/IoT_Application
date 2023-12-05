import {Component, OnDestroy, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";
import {JsonDownloadService} from "../../services/json-download.service";
import {SideDrawerService} from "../../services/side-drawer.service";
import ArrayStore from "devextreme/data/array_store";
import {ConfigurationService} from "../../services/configuration.service";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent implements OnDestroy {
  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;

  popupVisible = false;
  selectedItems: any[];
  flowLinksDataSource: ArrayStore;
  flowNodesDataSource: ArrayStore;

  constructor(private jsonDownload: JsonDownloadService, private drawerService: SideDrawerService,
              private nodesEdgesService: ConfigurationService) {

    this.flowNodesDataSource = new ArrayStore({
      key: 'id',
      data: this.nodesEdgesService.getNodes(),
    });

    this.flowLinksDataSource = new ArrayStore({
      key: 'id',
      data: this.nodesEdgesService.getLinks(),
    });
  }

  onCustomCommand(e: any) {
    const commandName: string = e.name;

    if (commandName === 'export') {
      this.exportToJson();
    }
    if (commandName === 'viewJson') {
      this.drawerService.toggleDrawer();
    }
  }

  selectionChangedHandler(e: any) {
    this.selectedItems = e.items.filter((item: any) => item.itemType === 'shape');
    console.log(this.selectedItems);
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

  ngOnDestroy(): void {
    this.nodesEdgesService.clearLists();
    this.diagram.instance.dispose();
  }

  private exportToJson() {
    this.jsonDownload.setData(this.diagram.instance.export());
    this.jsonDownload.downloadJson('diagram');
  }
}
