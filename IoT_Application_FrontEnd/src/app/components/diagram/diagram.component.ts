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
  numerosityOptions: string[] = ['one-to-one', 'one-to-many', 'many-to-many', 'many-to-one'];
  cancelButtonOptions: any;
  saveButtonOptions: any;
  deleteButtonOptions: any;

  selectedItemKeys: any[] = [];
  @ViewChild(DxDataGridComponent, {static: false}) dataGrid: DxDataGridComponent;
  @ViewChild(DxDiagramComponent, {static: false}) diagram: DxDiagramComponent;
  private previousSpecialID: number = 0;

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
      },
      onPush() {
        that.drawerUpdateMethods();
      }
    });
    this.linksDataSource = new ArrayStore({
      key: 'ID',
      data: this.getStartingLinks(),
      onInserting(values) {
        values.ID = values.ID || that.configService.assignID();
        values.type = 'link';
        values.numerosity = values.numerosity || 'many-to-many';
        values.fields = values.fields || [];
      },
      onModified() {
        that.drawerUpdateMethods();
      },
      onPush() {
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
        if (this.getFormGroup().valid) {
          this.updateItem();
        } else {
          console.log("Invalid form");
        }
      },
    };
    this.deleteButtonOptions = {
      icon: 'trash',
      onClick: () => {
        this.deleteItem();
      },
    };
  }

  /**
   * Handles the selection for the data grid in a custom way.
   * @param data
   */
  datagridSelectionHandler(data: any) {
    this.selectedItemKeys = data.selectedRowKeys;
  }

  /**
   * Handles the editing of a cell of the data grid in a custom way.
   * @param event the event that triggered the editing
   */
  cellEditingHandler(event: any) {
    if (this.typeNotChosen(event) || this.isNumericValue(event) || this.isTextualValue(event)
      || this.isDateOrBooleanValue(event) || this.nameAlreadyExists(event)) {
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
        first_item: obj.first_item_ID,
        second_item: obj.second_item_ID,
        numerosity: obj.numerosity,
      };
    } else {
      obj.name = value.table;
      obj.table = value.table;
      obj.fields = value.fields;
      obj.partition_key = value.partition_key;
      obj.sort_key = value.sort_key;
      obj.first_item_ID = value.first_item_ID;
      obj.second_item_ID = value.second_item_ID;
      obj.numerosity = value.numerosity;
      return null
    }
  }

  /**
   * The methods that opens the popup window to edit an item, setting the currentItem to the item to edit.
   * It also initializes the form groups of the popup window.
   * @param item the item to edit
   */
  editItem(item: Item) {
    let isSpecialLink: boolean = true;
    if (item.first_item_ID && item.second_item_ID) {
      isSpecialLink = !(this.isTable(item.first_item_ID) || this.isTable(item.second_item_ID));
    }

    if (isSpecialLink) {
      this.currentItem = {...item};

      if (this.currentItem.type === 'entity' && this.currentItem.table) {
        let designatedTable = this.tables.filter((table) => table.name === this.currentItem.table)[0]
        if (designatedTable) {
          this.previousSpecialID = this.configService.getSpecialID(designatedTable.ID, this.currentItem.ID);
        }
      }

      this.tables = [];

      for (let i = this.configService.getFirstID(); i <= this.configService.getCurrentID(); i++) {
        this.dataSource.byKey(i).then((data) => {
          if (data.type === 'table') {
            this.tables.push(data);
          }
        });
      }

      this.fieldsDataSource = new ArrayStore({
          key: 'name',
          data: this.currentItem.fields,
          onInserting(values) {
            values.type = values.type || "string";
            values.required = values.required || false;
          }
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

        this.linksDataSource.push([{type: 'remove', key: sID}]);
      }

    } else if (this.currentItem.type === 'entity') {
      if (this.currentItem.table) {
        let designatedTable = this.tables.filter((table) => table.name === this.currentItem.table)[0]
        if (designatedTable) {
          const tableLinkID = this.configService.getSpecialID(designatedTable.ID, this.currentItem.ID);
          this.configService.specialIDs.splice(this.configService.specialIDs.indexOf(tableLinkID), 1);
          this.linksDataSource.push([{type: 'remove', key: tableLinkID}]);
        }
      }

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

      this.cascadeUpdateToEntities(this.currentItem, this.configService.getAllLinkedEntities(this.currentItem.ID));

    } else if (this.currentItem.type === 'entity') {

      if (this.configService.tableAlreadyLinked(this.previousSpecialID)) {
        console.log("already linked", this.previousSpecialID)
        this.deleteLinkWithTable(this.previousSpecialID);
      }

      this.dataSource.push([{
        type: 'update',
        key: this.currentItem.ID,
        data: {
          name: this.currentItem.name,
          table: this.currentItem.table,
          fields: this.currentItem.fields,
        },
      }]);

      const finalID = this.configService.getSpecialID(
        (this.tables.filter((table) => table.name === this.currentItem.table)[0].ID), this.currentItem.ID);

      console.log("new link", finalID)
      this.createLinkWithTable(this.currentItem, finalID);

    }
    this.popupVisible = false;

    this.drawerUpdateMethods();
  }

  /**
   *  Handles the resources disposal of the diagram component.
   */
  onDisposing() {
    this.dataSource.clear();
    this.linksDataSource.clear();
    this.configService.reset();
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
    if (event.operation === "changeConnection" && event.args.connector) {
      //Drawing a connector without connecting it to another shape is not allowed
      if (event.args.newShape === undefined && event.args.oldShape === undefined) {
        event.allowed = false;
      }
      //Connecting a shape to itself is not allowed
      if (event.args.connector.fromId === event.args.connector.toId) {
        event.allowed = false;
      }
      //Connecting two shapes more than once is not allowed
      if (this.linkAlreadyExists(event.args.connector.fromKey, event.args.connector.toKey)) {
        event.allowed = false;
      }
      //TODO modificare questo per permettere l'assegnazione del campo tabella quando traccio
      //Creating connections between entities and tables is allowed only through assigning inside the popup window
      if (event.args.connector.fromKey && event.args.connector.toKey && (this.isTable(parseInt(event.args.connector.fromKey)) || this.isTable(parseInt(event.args.connector.toKey)))) {
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

  //TODO delete
  diagramSelectionHandler(event: any) {
    console.log("selected", event.items)
  }

  /**
   * Calls the custom command service to handle the custom commands of the diagram.
   * @param event
   */
  onCustomCommand(event: any) {
    this.customCommandService.customCommandHandler(event, this.dataSource, this.linksDataSource);
  }

  private typeNotChosen(event: any): boolean {
    const field = event.column.dataField;
    return (field === 'minLength' || field === 'maxLength' || field === 'maximum' || field === 'minimum')
      && (!("type" in event.data) || event.data.type === '');
  }

  private isNumericValue(event: any) {
    const field = event.column.dataField;
    return (field === 'minLength' || field === 'maxLength') &&
      (event.data.type === 'integer' || event.data.type === 'double');
  }

  private isTextualValue(event: any) {
    const field = event.column.dataField;
    return (field === 'minimum' || field === 'maximum') && event.data.type === 'string';
  }

  private isDateOrBooleanValue(event: any) {
    const field = event.column.dataField;
    return (field === 'minimum' || field === 'maximum' || field === 'minLength' || field === 'maxLength') &&
      (event.data.type === 'boolean' || event.data.type === 'date');
  }

  private nameAlreadyExists(event: any) {
    return ("name" in event.data) && (event.data.name !== '') && (event.column.dataField === 'name');
  }

  /**
   * Calls for the update of the content of the drawer.
   */
  private drawerUpdateMethods() {
    this.configService.updateConfiguration(this.dataSource, this.linksDataSource);
    this.configService.updateContent();
  }

  /**
   * The method called from the 'cancel' button that simply closes the popup window without applying any
   * changes to the current item.
   */
  private cancelEditItem() {
    this.currentItem = new Item();
    this.popupVisible = false;
  }

  /**
   * Checks if a link between two shapes already exists.
   * @param fromKey the name of the first shape (the one from which the link starts)
   * @param toKey the name of the second shape (the one to which the link arrives)
   */
  private linkAlreadyExists(fromKey: string, toKey: string): boolean {
    const items = this.configService.getItems();

    let links = items.filter((item) => item.type === 'link' &&
      (item.first_item_ID === parseInt(fromKey) && item.second_item_ID === parseInt(toKey) ||
        item.first_item_ID === parseInt(toKey) && item.second_item_ID === parseInt(fromKey)))

    return links.length > 0;
  }

  private isTable(id: number): boolean {
    return this.configService.getItems().find(entity => entity.ID === id).type === 'table';
  }

  /**
   * Deletes a link between an entity and a table.
   * @param id the ID of the link
   * @private
   */
  private deleteLinkWithTable(id: number) {
    this.linksDataSource.push([{
      type: 'remove',
      key: id,
    }]);
  }

  /**
   * Creates a link between an entity and a table.
   * @param entity the entity to link
   * @param id the ID of the link
   * @private
   */
  private createLinkWithTable(entity: Item, id: number) {
    this.configService.assignSpecialID(id);
    this.linksDataSource.push([{
      type: 'insert',
      data: {
        ID: id,
        name: entity.name + " - " + this.currentItem.table,
        type: "link",
        first_item_ID: entity.ID,
        second_item_ID: this.tables.filter((table) => table.name === this.currentItem.table)[0].ID,
      },
    }]);
  }

  /**
   * Creates the array of the links at the initialization of the component handling the links
   * between entities and tables.
   * @private
   */
  private getStartingLinks() {
    const tables: Item[] = this.items.filter((item) => item.type === 'table');
    const entities: Item[] = this.items.filter((item) => item.type === 'entity');

    const startingLinks: Item[] = this.items.filter((item) => item.type === 'link');

    for (let entity of entities) {
      const entityTable = tables.find((table) => table.name === entity.table)
      if (entityTable) {
        const linkID = this.configService.getSpecialID(entityTable.ID, entity.ID);
        startingLinks.push({
          ID: linkID,
          fields: null,
          first_item_ID: entity.ID,
          name: entity.name + " - " + entityTable.name,
          numerosity: null,
          partition_key: null,
          second_item_ID: entityTable.ID,
          sort_key: null,
          table: null,
          type: 'link'
        })
      }
    }
    return startingLinks;
  }

  /**
   * Cascades the update of a table to all the entities linked to it.
   * @param table the updated table
   * @param entitiesIDs the IDs of the entities linked to the table
   * @private
   */
  private cascadeUpdateToEntities(table: Item, entitiesIDs: number[]) {
    for (let entityID of entitiesIDs) {
      this.dataSource.push([{
        type: 'update',
        key: entityID,
        data: {
          table: table.name,
        },
      }]);
    }
  }
}
