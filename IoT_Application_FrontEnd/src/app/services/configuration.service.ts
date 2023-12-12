import {Injectable} from '@angular/core';
import {Item} from "../models/item.model";
import ArrayStore from "devextreme/data/array_store";

const items: Item[] = [];

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {
  firstID: number = 100;
  generatedID: number = 100;

  assignID() {
    console.log("generatedID", this.generatedID)
    return this.generatedID++;
  }

  getItems(): Item[] {
    return items;
  }

  clearList() {
    items.splice(0, items.length);
    //this.testService.getItems().splice(0, this.testService.getItems().length);
  }

  /**
   * This method creates a new configuration with a basic structure, updating it from time to time
   * based on the needs requested by the customer regarding entities, links...
   */
  exportConfiguration() {
    const jsonEntities = this.createEntityJson();
    const jsonTable = this.createTableJson()
    const jsonLinks = this.createLinkJson()

    return {
      projectName: "Prova",
      entities: jsonEntities,
      links: jsonLinks,
      awsConfig: {
        dynamo: {
          tables: jsonTable
        }
      }
    };
  }

  /**
   * This method is called when the user performs any action in the diagram and updates the lists of nodes and links.
   * @param diagram the diagram where the action is taking place
   * @param e the event that triggered the action
   */
  updateLists(diagram: DxDiagramComponent, e: any) {
    let items = diagram.instance.getItems();
    this.clearList();
    for (const itemKey in items) {
      const item = items[itemKey];
      if (item.itemType === 'shape') {
        //nodes.push();
      }
      if (item.itemType === 'connector') {
        //links.push();
      }
    }
  }

  private createEntityJson() {
    return this.getItems().filter(entity => entity.type === 'entity').map(entity => ({
      name: entity.name,
      //fields: entity.fields,
      table: entity.table,
      primary_key: []
    }));
  }

  private createTableJson() {
    return this.getItems().filter(entity => entity.type === 'table').map(table => ({
      tableName: table.name,
      partition_key: table.partition_key,
      sort_key: table.sort_key
    }))
  }

  private createLinkJson() {
    return this.getItems().filter(entity => entity.type === 'link').map(link => ({
      first_entity: link.first_item,
      second_entity: link.second_item,
      //fields: link.fields
    }));
  }

  getCurrentID() {
    return this.generatedID;
  }
  getFirstID() {
    return this.firstID;
  }
}
