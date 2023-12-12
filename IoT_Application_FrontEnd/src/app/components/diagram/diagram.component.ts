import {Component, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";
import ArrayStore from "devextreme/data/array_store";
import {ConfigurationService} from "../../services/configuration.service";
import {CustomCommandService} from "../../services/custom-command.service";
import {Item} from "../../models/item.model";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent {
  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;

  items: Item[];
  currentItem: Item = new Item();

  dataSource: ArrayStore;
  linksDataSource: ArrayStore;

  popupVisible = false;
  generatedID = 100;

  constructor(private customCommandService: CustomCommandService, private configService: ConfigurationService) {
    const that = this;
    this.items = this.configService.getItems();
    this.dataSource = new ArrayStore({
      key: 'ID',
      data: this.configService.getItems().filter((item) => this.isTable(item) || this.isEntity(item)),
      onInserting(values) {
        values.ID = values.ID || that.generatedID++;
        values.name = values.name || "Entity's Name";
      },
    });
    this.linksDataSource = new ArrayStore({
      key: 'ID',
      data: this.configService.getItems().filter((item) => item.type === 'link'),
      onInserting(values) {
        console.log("values", values)
        values.ID = values.ID || that.generatedID++;
        values.name = values.name || that.getLinkName(values);
        values.type = 'link';
      },
    });
  }

  // @ts-ignore
  itemCustomDataExpr(obj, value) {
    if (value === undefined) {
      return {
        name: obj.name,
        table: obj.table,
        partition_key: obj.partition_key,
        sort_key: obj.sort_key,
      };
    }
    obj.name = value.name;
  }

  editItem(item: Item) {
    this.currentItem = {...item};
    this.popupVisible = true;
  }

  deleteItem(item: Item) {
    this.dataSource.push([{type: 'remove', key: item.ID}]);
    this.cancelEditItem();
    console.log(this.dataSource);
  }

  updateItem() {
    console.log(this.currentItem.type)
    if (this.currentItem.type === 'link') {
      this.linksDataSource.push([{
        type: 'update',
        key: this.currentItem.ID,
        data: {
          name: this.currentItem.name,
        },
      }]);
    } else {
      this.dataSource.push([{
        type: 'update',
        key: this.currentItem.ID,
        data: {
          name: this.currentItem.name,
          table: this.currentItem.table,
          partition_key: this.currentItem.partition_key,
          sort_key: this.currentItem.sort_key,
        },
      }]);
    }
    this.popupVisible = false;

    //TODO aggiungi aggiorna json
  }

  cancelEditItem() {
    if (this.currentItem.type === 'entity' || this.currentItem.type === 'table') {
      console.log(this.currentItem.type, this.dataSource);
    } else {
      console.log(this.currentItem.type, this.linksDataSource);
    }

    this.currentItem = new Item();
    this.popupVisible = false;


    /*let len = 0;
    this.dataSource.totalCount({}).then((count) => {
      len = count;
    });*/

    const items: Item[] = [];
    for (let i = 1; i <= this.generatedID; i++) {
      console.log(i)
      this.linksDataSource.byKey(i).then((data) => {
        if (data.type === 'link') {
          items.push(data);
          console.log(data)
        }
      });
    }
    console.log(items)
  }

  onDisposing() {
    this.configService.clearList();
    this.dataSource.clear();
    this.linksDataSource.clear();
    this.diagram.instance.dispose();
  }

  //The deleteShape operation is possible only by opening the popup window
  requestEditOperationHandler(event: any) {
    if (event.operation === "deleteShape") {
      event.allowed = false;
    }
    if (event.operation === "changeConnection")
      //Connecting a shape to itself is not allowed
      if (event.args.connector && event.args.connector.fromId === event.args.connector.toId)
        event.allowed = false;

    //TODO aggiungi aggiorna json
  }

  requestLayoutUpdateHandler(e: any) {
    for (let i = 0; i < e.changes.length; i++) {
      if (e.changes[i].type === 'remove') {
        e.allowed = true;
      }
    }
  }

  selectionChangedHandler(e: any) {
    console.log(e.items)
  }

  onCustomCommand(e: any) {
    this.customCommandService.customCommandHandler(e);
  }

  /**
   * Builds the string for the name of the link.
   * @param values the link's values
   */
  getLinkName(values: any): string {
    let linkName: string, firstItem: string, secondItem: string;
    //usare questo se si vuole usare l'ID come key
    /*this.dataSource.byKey(values.first_item).then((data) => {
      firstItem = data.name;
    });
    this.dataSource.byKey(values.second_item).then((data) => {
      secondItem = data.name;
    });
    linkName = firstItem + ' - ' + secondItem;*/

    linkName = values.first_item + ' - ' + values.second_item;
    console.log(linkName)
    return linkName;
  }

  isTable(item: any): boolean {
    return item.type === 'table' && item.table === null
  }

  isEntity(item: any): boolean {
    return item.type === 'entity' && item.partition_key === null && item.sort_key === null
  }
}
