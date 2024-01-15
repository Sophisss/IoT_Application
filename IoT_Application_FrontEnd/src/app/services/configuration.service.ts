import {Injectable} from '@angular/core';
import {Item} from "../models/item.model";
import ArrayStore from "devextreme/data/array_store";
import {BehaviorSubject} from "rxjs";
import {TitleCasePipe} from "@angular/common";
import {Field} from "../models/field.model";

const items: Item[] = [];

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {

  projectTitle: string = "IoT Application";
  readonly defaultTitle: string = "IoT Application";

  //Since the ID is generated automatically, we need to keep track of the first and last ID.
  readonly firstID: number = 100;
  generatedID: number = 100;
  specialIDs: number[] = [];

  private updateSignalSubject = new BehaviorSubject<void>(null);
  updateSignal$ = this.updateSignalSubject.asObservable();

  constructor(private titleCase: TitleCasePipe) {
  }

  /**
   * Signals to the drawer the necessity to update its content.
   */
  updateContent() {
    this.updateSignalSubject.next();
  }

  getPrimaryKeyField(item: Item) {
    return item.fields.find(field => field.isPrimaryKey);
  }

  /**
   * This method increments the ID by 1 and returns it to assign it to a new item.
   */
  assignID() {
    //console.log("generatedID", this.generatedID)
    return this.generatedID++;
  }

  getItems(): Item[] {
    return items;
  }

  getTitle(): string {
    return this.projectTitle;
  }

  /**
   * This method creates a new configuration with a basic structure.
   */
  exportConfiguration() {
    const jsonEntities = this.createEntityJson();
    const jsonTable = this.createTableJson()
    const jsonLinks = this.createLinkJson()

    return {
      projectName: this.projectTitle.trim().replace(/\s/g, '_'),
      entities: jsonEntities,
      links: jsonLinks,
      awsConfig: {
        dynamo: {
          tables: jsonTable,
        },
        authentication: {
          cognito: {
            UserPool: {
              resource_name: "IoTApplicationUserPool",
              UserPoolName: "IoTApplicationUserPoolName",
              policy: {
                "PasswordPolicy": {
                  "MinimumLength": 8,
                  "RequireUppercase": true,
                  "RequireLowercase": true,
                  "RequireNumbers": true,
                  "RequireSymbols": false,
                  "TemporaryPasswordValidityDays": 14
                }
              }
            },
            IdentityPool: {
              "resource_name": "IoTApplicationIdentityPool",
              "IdentityPoolName": "IdentityPool"
            }
          }
        }
      }
    };
  }

  /**
   * Reset the list of items and updates the configuration with the new entities,tables and links by
   * iterating over the nodes and links data sources.
   * @param nodes the list of the nodes coming from the diagram
   * @param links the list of the links coming from the diagram
   */
  updateConfiguration(nodes: ArrayStore, links: ArrayStore) {
    this.clearList();
    for (let i = this.getFirstID(); i <= this.getCurrentID(); i++) {
      //console.log("nodes", i)
      nodes.byKey(i).then((data) => {

        items.push(data);
        //console.log(data)
      });
    }

    for (let i = this.getFirstID(); i <= this.getCurrentID(); i++) {
      //console.log("links", i)
      links.byKey(i).then((data) => {

        items.push(data);
        //console.log(data)
      });
    }
  }

  getCurrentID() {
    return this.generatedID;
  }

  getFirstID() {
    return this.firstID;
  }

  /**
   * Calculates the special ID for the table-entity link.
   * @param tableID the ID of the table
   * @param entityID the ID of the entity
   */
  getSpecialID(tableID: number, entityID: number) {
    let temp = tableID.toString() + entityID.toString();
    return parseInt(temp);
  }

  /**
   * Returns all the special IDs reserved for a table.
   * @param tableID the ID of the table
   */
  getAllSpecialIDsForTable(tableID: number): number[] {
    const prefixString = tableID.toString();
    return this.specialIDs.filter(number => number.toString().startsWith(prefixString));
  }

  getAllLinksFromEntity(i: Item): Item[] {
    return this.getItems().filter((item) => item.type === 'link' && item.first_item_ID === i.ID)
  }

  getAllLinksToEntity(i: Item): Item[] {
    return this.getItems().filter((item) => item.type === 'link' && item.second_item_ID === i.ID)
  }

  /**
   * Reserves a special ID for the table-entity link.
   * @param sID
   */
  assignSpecialID(sID: number) {
    this.specialIDs.push(sID);
  }

  /**
   * Checks if the table is already linked to an entity.
   * @param sID the ID of the link between the table and the entity
   */
  tableAlreadyLinked(sID: number) {
    return this.specialIDs.includes(sID);
  }

  reset() {
    this.projectTitle = this.defaultTitle;
    this.clearList();
    this.generatedID = this.firstID;
    this.specialIDs = [];
  }

  /**
   * Clears the list of items.
   */
  private clearList() {
    items.splice(0, items.length);
  }

  /**
   * Iterates over the list of items and creates a list of entities ready to be exported.
   */
  private createEntityJson() {
    return this.getItems().filter(entity => entity.type === 'entity').map(entity => ({
      name: entity.name,
      table: entity.table,
      fields: this.createFieldJson(entity.fields),
      primary_key: entity.primary_key,
      API: [
        {
          name: "create" + this.titleCase.transform(entity.name),
          type: "PUT"
        },
        {
          name: "delete" + this.titleCase.transform(entity.name),
          type: "DELETE"
        },
        {
          name: "update" + this.titleCase.transform(entity.name),
          type: "POST",
          parameters: this.getAPIParameters(entity.fields)
        },
        {
          name: "get" + this.titleCase.transform(entity.name) + "ById",
          type: "GET"
        },
        {
          name: "get" + this.titleCase.transform(entity.name) + "s",
          type: "GET_ALL"
        }
      ]
    }));
  }

  /**
   * Iterates over the list of items and creates a list of links ready to be exported.
   */
  private createLinkJson() {
    return this.getItems().filter(entity => entity.type === 'link').map(link => ({
      first_entity: this.getEntityNameByID(link.first_item_ID),
      second_entity: this.getEntityNameByID(link.second_item_ID),
      numerosity: link.numerosity,
      table: link.table,
      fields: this.createFieldJson(link.fields),
      primary_key: link.primary_key,
      API: [
        {
          name: "createLink" + this.getEntityNameByID(link.first_item_ID) + this.getEntityNameByID(link.second_item_ID),
          type: "PUT"
        },
        {
          name: "deleteLink" + this.getEntityNameByID(link.first_item_ID) + this.getEntityNameByID(link.second_item_ID),
          type: "DELETE"
        },
        {
          name: "getLink" + this.getEntityNameByID(link.first_item_ID) + this.getEntityNameByID(link.second_item_ID),
          type: "GET"
        }
      ]
    }));
  }

  /**
   * Iterates over the list of items and creates a list of tables ready to be exported.
   */
  private createTableJson() {
    return this.getItems().filter(entity => entity.type === 'table').map(table => ({
      tableName: table.name,
      partition_key: {
        name: table.partition_key_name,
        type: table.partition_key_type
      },
      sort_key: {
        name: table.sort_key_name,
        type: table.sort_key_type
      },
      GSI: {
        index_name: table.sort_key_name + "-" + table.partition_key_name,
        partition_key: table.sort_key_name,
        sort_key: table.partition_key_name
      },
      parameters: {
        single_entity_storage_keyword: table.keyword,
        id_separator: table.separator
      }
    }))
  }

  private createFieldJson(fields: Field[]) {
    const fieldList: Field[] = [];

    for (let field of fields) {
      fieldList.push({
        name: field.name,
        type: field.type,
        required: field.required,
        minLength: field.minLength,
        maxLength: field.maxLength,
        minimum: field.minimum,
        maximum: field.maximum,
      })
    }
    return fieldList;
  }

  private getEntityNameByID(id: number) {
    return this.getItems().find(entity => entity.ID === id)?.name;
  }

  private getAPIParameters(fields: Field[]): string[] {
    return fields.filter(field => field.isPrimaryKey === false).map(field => (field.name));
  }
}
