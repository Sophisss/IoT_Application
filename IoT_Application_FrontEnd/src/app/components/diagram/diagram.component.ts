import {Component, ViewChild} from '@angular/core';
import {DxDiagramComponent} from "devextreme-angular";
import ArrayStore from "devextreme/data/array_store";
import {ConfigurationService} from "../../services/configuration.service";
import {CustomCommandService} from "../../services/custom-command.service";
import {Item} from "../../models/item.model";
import {Field} from "../../models/field.model";

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

  /**
   * Constructor of the diagram component. It initializes the data sources of the diagram taking the items from the
   * configuration service which contains the items of an eventual uploaded json file.
   * @param customCommandService the service that handles the custom commands of the diagram
   * @param configService the service that handles the configuration aspects of the diagram
   */
  constructor(private customCommandService: CustomCommandService, private configService: ConfigurationService) {
    const that = this;
    this.items = this.configService.getItems();
    this.dataSource = new ArrayStore({
      key: 'ID',
      data: this.configService.getItems().filter((item) => this.isTable(item) || this.isEntity(item)),
      onInserting(values) {
        values.ID = values.ID || that.configService.assignID();
        values.name = values.name || "Entity's Name";
        values.fields = values.fields || [];
      },
      onModified() {
        that.drawerUpdateMethods();
      }
    });
    this.linksDataSource = new ArrayStore({
      key: 'ID',
      data: this.configService.getItems().filter((item) => item.type === 'link'),
      onInserting(values) {
        values.ID = values.ID || that.configService.assignID();
        values.type = 'link';
      },
      onModified() {
        that.drawerUpdateMethods();
      }
    });
  }

  newField() {
    this.currentItem.fields.push(new Field());
  }

  /**
   * Calls for the update of the content of the drawer.
   */
  drawerUpdateMethods() {
    this.configService.updateConfiguration(this.dataSource, this.linksDataSource);
    this.configService.updateContent();
  }

  /**
   * ???
   * @param obj
   * @param value
   */
  // @ts-ignore
  itemCustomDataExpr(obj, value) {
    if (value === undefined) {
      return {
        name: obj.name,
        table: obj.table,
        fields: obj.fields,
        partition_key: obj.partition_key,
        sort_key: obj.sort_key,
      };
    }
    obj.name = value.name;
  }

  /**
   * The methods that opens the popup window to edit an item, setting the currentItem to the item to edit.
   * @param item the item to edit
   */
  editItem(item: Item) {
    this.currentItem = {...item};
    this.popupVisible = true;
  }

  /**
   * The method called from the 'delete' button that deletes the current item from
   * the diagram, removes it from the data source and closes the popup window.
   * @param item the item to delete
   */
  deleteItem(item: Item) {
    this.dataSource.push([{type: 'remove', key: item.ID}]);
    this.cancelEditItem();
    //TODO rimuovi link corrispondenti se entity
  }

  /**
   * The method called from the 'update' button that updates the current item, applies the changes to the
   * data source based on the type of the item and closes the popup window.
   */
  updateItem() {
    if (this.currentItem.type === 'link') {
      this.linksDataSource.push([{
        type: 'update',
        key: this.currentItem.ID,
        data: {},
      }]);
    } else {
      this.dataSource.push([{
        type: 'update',
        key: this.currentItem.ID,
        data: {
          name: this.currentItem.name,
          table: this.currentItem.table,
          fields: this.currentItem.fields,
          partition_key: this.currentItem.partition_key,
          sort_key: this.currentItem.sort_key,
        },
      }]);
    }
    this.popupVisible = false;

    this.drawerUpdateMethods();
  }

  /**
   * The method called from the 'cancel' button that simply closes the popup window without applying any
   * changes to the current item.
   */
  cancelEditItem() {
    this.currentItem = new Item();
    this.popupVisible = false;
  }

  /**
   *  Handles the resources disposal of the diagram component.
   */
  onDisposing() {
    this.configService.clearList();
    this.dataSource.clear();
    this.linksDataSource.clear();
    this.diagram.instance.dispose();
  }

  /**
   * Handles the various edit requests of the diagram in a custom way.
   * - deleteShape: the delete operation is possible only by opening the popup window;
   * - changeConnection: the connection between a shape and itself is not allowed.
   * @param event
   */
  requestEditOperationHandler(event: any) {
    if (event.operation === "deleteShape") {
      event.allowed = false;
    }
    if (event.operation === "changeConnection") {
      //Connecting a shape to itself is not allowed
      if (event.args.connector && event.args.connector.fromId === event.args.connector.toId)
        event.allowed = false;
      //Connecting two shapes more than once is not allowed
      if (event.args.connector && this.linkAlreadyExists(event.args.connector.fromKey, event.args.connector.toKey)) {
        event.allowed = false;
      }
      //Connecting an entity to a table is not allowed
      if (event.args.connector && event.args.newShape && event.args.newShape.dataItem.type === 'table') {
        event.allowed = false;
      }
    }
  }

  /**
   * Checks if a link between two shapes already exists.
   * @param fromKey the name of the first shape (the one from which the link starts)
   * @param toKey the name of the second shape (the one to which the link arrives)
   */
  linkAlreadyExists(fromKey: string, toKey: string): boolean {
    const items = this.configService.getItems();

    let links = items.filter((item) => item.type === 'link' &&
      (item.first_item === fromKey && item.second_item === toKey || item.first_item === toKey && item.second_item === fromKey))

    return links.length > 0;
  }

  /**
   * Handles the various layout update requests of the diagram in a custom way.
   * @param event
   */
  requestLayoutUpdateHandler(event: any) {
    this.drawerUpdateMethods();
    for (let i = 0; i < event.changes.length; i++) {
      if (event.changes[i].type === 'remove') {
        event.allowed = true;
      }
    }
  }

  selectionChangedHandler(event: any) {
    //console.log(event.items)
  }

  /**
   * Calls the custom command service to handle the custom commands of the diagram.
   * @param event
   */
  onCustomCommand(event: any) {
    this.customCommandService.customCommandHandler(event, this.dataSource, this.linksDataSource);
  }

  /**
   * Checks if the item is a table.
   * @param item the item to check
   */
  isTable(item: any): boolean {
    return item.type === 'table' && item.table === null
  }

  /**
   * Checks if the item is an entity.
   * @param item the item to check
   */
  isEntity(item: any): boolean {
    return item.type === 'entity' && item.partition_key === null && item.sort_key === null
  }
}
