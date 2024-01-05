import {Injectable} from '@angular/core';
import {Item} from "../models/item.model";
import ArrayStore from "devextreme/data/array_store";
import {BehaviorSubject} from "rxjs";

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

  /**
   * Signals to the drawer the necessity to update its content.
   */
  updateContent() {
    this.updateSignalSubject.next();
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
   * Clears the list of items.
   */
  clearList() {
    items.splice(0, items.length);
  }

  /**
   * This method creates a new configuration with a basic structure.
   */
  exportConfiguration() {
    const jsonEntities = this.createEntityJson();
    const jsonTable = this.createTableJson()
    const jsonLinks = this.createLinkJson()

    return {
      projectName: this.projectTitle,
      entities: jsonEntities,
      links: jsonLinks,
      awsConfig: {
        dynamo: {
          tables: jsonTable,
          authentication: {}
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

  getSpecialID(tableID: number, entityID: number) {
    let temp = tableID.toString() + entityID.toString();
    return parseInt(temp);
  }

  getAllSpecialIDsForTable(tableID: number): number[] {
    const prefixString = tableID.toString();
    return this.specialIDs.filter(number => number.toString().startsWith(prefixString));
  }

  getAllLinkedEntities(prefix: number): number[] {
    const prefixString = prefix.toString();
    return this.specialIDs
      .filter(number => number.toString().startsWith(prefixString))
      .map(number => parseInt(number.toString().substring(prefixString.length)));
  }

  assignSpecialID(sID: number) {
    this.specialIDs.push(sID);
  }

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
   * Iterates over the list of items and creates a list of entities ready to be exported.
   */
  private createEntityJson() {
    return this.getItems().filter(entity => entity.type === 'entity').map(entity => ({
      name: entity.name,
      fields: entity.fields,
      table: entity.table,
      primary_key: []
    }));
  }

  /**
   * Iterates over the list of items and creates a list of tables ready to be exported.
   */
  private createTableJson() {
    return this.getItems().filter(entity => entity.type === 'table').map(table => ({
      tableName: table.name,
      partition_key: table.partition_key,
      sort_key: table.sort_key
    }))
  }

  /**
   * Iterates over the list of items and creates a list of links ready to be exported.
   */
  private createLinkJson() {
    return this.getItems().filter(entity => entity.type === 'link').map(link => ({
      first_entity: this.getEntityNameByID(link.first_item_ID),
      second_entity: this.getEntityNameByID(link.second_item_ID),
      numerosity: link.numerosity,
      fields: link.fields
    }));
  }

  private getEntityNameByID(id: number) {
    return this.getItems().find(entity => entity.ID === id).name;
  }
}
