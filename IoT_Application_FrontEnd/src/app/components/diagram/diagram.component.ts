import {Component, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";
import ArrayStore from "devextreme/data/array_store";
import {ConfigurationService} from "../../services/configuration.service";
import {CustomCommandService} from "../../services/custom-command.service";
import {ToggleService} from "../../services/toggle.service";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent {
  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;

  popupVisible = false;
  selectedItems: any[];
  flowLinksDataSource: ArrayStore;
  flowNodesDataSource: ArrayStore;

  constructor(private nodesEdgesService: ConfigurationService, private customCommandService: CustomCommandService,
              private toggleService: ToggleService) {

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
    this.customCommandService.customCommandHandler(e);
  }

  selectionChangedHandler(e: any) {
    this.selectedItems = e.items.filter((item: any) => item.itemType === 'shape' || item.itemType === 'connector');
    this.diagram.instance.focus();
    console.log(this.selectedItems);
  }

  requestEditOperationHandler(e: any) {
    this.diagram.instance.focus();
    //TODO riattivare sotto per aggiornare le liste di nodi e link
    //this.nodesEdgesService.updateLists(this.diagram, e);
    //console.log(e);
    if (e.operation === "changeConnection")
      //Connecting a shape to itself is not allowed
      if (e.args.connector && e.args.connector.fromId === e.args.connector.toId)
        e.allowed = false;

    //Connecting a shape to another shape already connected to it is not allowed
    //if (e.args.connector && e.args.connector.fromId === e.args.connector.toId)

  }

  getPopupState(): boolean {
    return this.toggleService.isPopupOpened();
  }

  openPopup(e: any) {
    this.toggleService.openPopup(e);
  }

  onDisposing() {
    this.nodesEdgesService.clearLists();
    this.diagram.instance.dispose();
    this.flowLinksDataSource.clear();
    this.flowNodesDataSource.clear();
  }
}
