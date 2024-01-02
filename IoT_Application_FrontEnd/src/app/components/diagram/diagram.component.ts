import {Component, ViewChild} from '@angular/core';
import ArrayStore from "devextreme/data/array_store";
import {ConfigurationService} from "../../services/configuration.service";
import {CustomCommandService} from "../../services/custom-command.service";
import {Item} from "../../models/item.model";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {DxDataGridComponent, DxDiagramComponent} from "devextreme-angular";

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent {
  tables: Item[] = [];

  fieldTypes: string[] = ['string', 'integer', 'double', 'boolean', 'date'];

  items: Item[];
  currentItem: Item = new Item();

  dataSource: ArrayStore;
  linksDataSource: ArrayStore;
  fieldsDataSource: ArrayStore;

  popupVisible = false;

  entityForm: FormGroup;
  tableForm: FormGroup;
  linkForm: FormGroup;
  placeholderForm: FormGroup;
  numerosityOptions: string[] = ['one-to-one', 'one-to-many', 'many-to-many'];
  cancelButtonOptions: any;
  saveButtonOptions: any;
  deleteButtonOptions: any;

  selectedItemKeys: any[] = [];

  @ViewChild(DxDataGridComponent, {static: false}) dataGrid: DxDataGridComponent;
  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;

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
      data: this.items.filter((item) => item.type !== 'link'),
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
      data: this.items.filter((item) => item.type === 'link'),
      onInserting(values) {
        values.ID = values.ID || that.configService.assignID();
        values.type = 'link';
        values.numerosity = values.numerosity || 'many-to-many';
        values.fields = values.fields || [];
      },
      onModified() {
        that.drawerUpdateMethods();
      }
    });
    this.cancelButtonOptions = {
      icon: 'close',
      onClick: () => {
        this.cancelEditItem();
      },
    };
    this.saveButtonOptions = {
      icon: 'save',
      onClick: () => {
        this.updateItem();
      },
    };
    this.deleteButtonOptions = {
      icon: 'trash',
      onClick: () => {
        this.deleteItem();
      },
    };
  }

  onSelectionChanged(data: any) {
    this.selectedItemKeys = data.selectedRowKeys;
  }

  deleteRecords() {
    this.selectedItemKeys.forEach((key) => {
      this.fieldsDataSource.remove(key);
    });
    this.dataGrid.instance.refresh();
  }

  checkCell(event: any) {
    console.log(event);
    if (this.typeNotChosen(event) || this.isNumericValue(event) || this.isTextualValue(event)) {
      event.cancel = true;
    }
    if (this.isNumericValue(event)) {
      event.data.maxLength = undefined;
      event.data.minLength = undefined;
    } else if (this.isTextualValue(event)) {
      event.data.maximum = undefined;
      event.data.minimum = undefined;
    }
  }

  typeNotChosen(event: any): boolean {
    const field = event.column.dataField;
    return (field === 'minLength' || field === 'maxLength' || field === 'maximum' || field === 'minimum')
      && (!("type" in event.data) || event.data.type === '');
  }

  isNumericValue(event: any) {
    const field = event.column.dataField;
    return (field === 'minLength' || field === 'maxLength') && (event.data.type === 'integer' || event.data.type === 'double')
  }

  isTextualValue(event: any) {
    const field = event.column.dataField;
    return (field === 'minimum' || field === 'maximum') && event.data.type === 'string'
  }

  /**
   * Returns the form group of the popup window based on the type of the current item.
   */
  getFormGroup() {
    switch (this.currentItem.type) {
      case 'entity':
        return this.entityForm;
      case 'table':
        return this.tableForm;
      case 'link':
        return this.linkForm;
      default:
        return this.placeholderForm;
    }
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
  itemCustomDataExpr(obj: Item, value: Item) {
    if (value === undefined) {
      return {
        name: obj.table,
        table: obj.table,
        fields: obj.fields,
        partition_key: obj.partition_key,
        sort_key: obj.sort_key,
      };
    } else {
      return null
    }
  }

  /**
   * The methods that opens the popup window to edit an item, setting the currentItem to the item to edit.
   * It also initializes the form groups of the popup window.
   * @param item the item to edit
   */
  editItem(item: Item) {
    this.tables = [];
    this.currentItem = {...item};

    for (let i = this.configService.getFirstID(); i <= this.configService.getCurrentID(); i++) {
      this.dataSource.byKey(i).then((data) => {
        if (data.type === 'table') {
          this.tables.push(data);
        }
      });
    }

    this.fieldsDataSource = new ArrayStore(
      {
        key: 'name',
        data: this.currentItem.fields,
      }
    );

    this.popupVisible = true;

    this.entityForm = new FormGroup({
      name: new FormControl(this.currentItem.name, Validators.required),
      table: new FormControl(this.currentItem.table, Validators.required),
    });
    this.tableForm = new FormGroup({
      name: new FormControl(this.currentItem.name, Validators.required),
      partition_key: new FormControl(this.currentItem.partition_key, Validators.required),
      sort_key: new FormControl(this.currentItem.sort_key, Validators.required),
    });
    this.linkForm = new FormGroup({
      name: new FormControl(this.currentItem.name),
      numerosity: new FormControl(this.currentItem.numerosity, Validators.required),
    });
    this.placeholderForm = new FormGroup({
      name: new FormControl()
    });
  }

  /**
   * The method called from the 'delete' button that deletes the current item from
   * the diagram, removes it from the data source and closes the popup window.
   */
  deleteItem() {
    if (this.currentItem.type === 'link') {
      if (this.configService.specialIDs.includes(this.currentItem.ID)) {
        this.configService.specialIDs.splice(this.configService.specialIDs.indexOf(this.currentItem.ID), 1);
      }
      this.linksDataSource.push([{type: 'remove', key: this.currentItem.ID}]);
    } else if (this.currentItem.type === 'table') {
      this.dataSource.push([{type: 'remove', key: this.currentItem.ID}]);

      for (let sID of this.configService.getAllSpecialIDsForTable(this.currentItem.ID)) {
        this.configService.specialIDs.splice(this.configService.specialIDs.indexOf(sID), 1);
      }

    } else if (this.currentItem.type === 'entity') {
      const tableLinkID = this.configService.getSpecialID((this.tables.filter((table) => table.name === this.currentItem.table)[0].ID), this.currentItem.ID);
      this.configService.specialIDs.splice(this.configService.specialIDs.indexOf(tableLinkID), 1);

      this.dataSource.push([{type: 'remove', key: this.currentItem.ID}]);
    }
    this.cancelEditItem();
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
        data: {
          name: this.currentItem.name,
          numerosity: this.currentItem.numerosity,
          fields: this.currentItem.fields,
        },
      }]);
    } else if (this.currentItem.type === 'table') {
      this.dataSource.push([{
        type: 'update',
        key: this.currentItem.ID,
        data: {
          name: this.currentItem.name,
          partition_key: this.currentItem.partition_key,
          sort_key: this.currentItem.sort_key,
        },
      }]);

      const allLinkedEntities = this.configService.getAllLinkedEntities(this.currentItem.ID);
      for (let entityID of allLinkedEntities) {
        this.dataSource.push([{
          type: 'update',
          key: entityID,
          data: {
            table: this.currentItem.name,
          },
        }]);
      }

      const allLinksToEntities = this.configService.getAllSpecialIDsForTable(this.currentItem.ID);
      for (let sID of allLinksToEntities) {
        console.log(sID)
        this.linksDataSource.push([{
          type: 'update',
          key: sID,
          data: {
            second_item: this.currentItem.name,
          },
        }]);
      }

      //console.log("special",this.configService.getAllSpecialIDsForTable(this.currentItem.ID));
    } else if (this.currentItem.type === 'entity') {
      this.dataSource.push([{
        type: 'update',
        key: this.currentItem.ID,
        data: {
          name: this.currentItem.name,
          table: this.currentItem.table,
          fields: this.currentItem.fields,
        },
      }]);

      const linkWithTable = this.configService.getSpecialID((this.tables.filter((table) => table.name === this.currentItem.table)[0].ID), this.currentItem.ID);

      const newLink: Item = {
        ID: linkWithTable,
        name: this.currentItem.name + " - " + this.currentItem.table,
        type: "link",
        fields: null,
        table: null,
        partition_key: null,
        sort_key: null,
        first_item: this.currentItem.name,
        second_item: this.currentItem.table,
        numerosity: 'one-to-one'
      }

      if (this.configService.tableAlreadyLinked(linkWithTable)) {
        console.log("already linked")
        //update link
        this.linksDataSource.push([{
          type: 'update',
          key: linkWithTable,
          data: {
            name: this.currentItem.name,
            first_item: this.currentItem.name,
            second_item: this.currentItem.table,
          },
        }]);
      } else {
        console.log("new")
        //create link
        this.configService.assignSpecialID(linkWithTable);
        this.linksDataSource.push([{
          type: 'insert',
          data: newLink,
        }]);
      }
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
    this.configService.resetTitle();
  }

  /**
   * Handles the various edit requests of the diagram in a custom way.
   * - deleteShape: the delete operation is possible only by opening the popup window;
   * - changeConnection: the connection between a shape and itself is not allowed.
   * @param event
   */
  requestEditOperationHandler(event: any) {
    if (event.operation === "deleteShape" || event.operation === "deleteConnector") {
      event.allowed = false;
    }
    if (event.operation === "changeConnection") {
      //Drawing a connector without connecting it to another shape is not allowed
      if (event.args.connector && event.args.newShape === undefined && event.args.oldShape === undefined) {
        event.allowed = false;
      }
      //Connecting a shape to itself is not allowed
      if (event.args.connector && event.args.connector.fromId === event.args.connector.toId)
        event.allowed = false;
      //Connecting two shapes more than once is not allowed
      if (event.args.connector && this.linkAlreadyExists(event.args.connector.fromKey, event.args.connector.toKey)) {
        event.allowed = false;
      }
      //Connecting a table to an entity is not allowed, only an entity to a table
      if (event.args.connector && event.args.newShape && event.args.newShape.dataItem.type === 'entity' && event.args.connectorPosition === 'end') {
        event.allowed = false;
      }
    }
    if (event.operation === "addShape") {
      //Adding a new blank shape before updating the existing one is not allowed
      if ((event.args.shape.type === 'entity' &&
          this.configService.getItems().filter((item) => item.name === "Entity").length > 0) ||
        (event.args.shape.type === 'table' &&
          this.configService.getItems().filter((item) => item.name === "Table").length > 0)) {
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
}
