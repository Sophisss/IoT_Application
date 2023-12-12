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

  updateConfiguration(nodes: ArrayStore, links: ArrayStore) {
    this.clearList();
    console.log("updateConfiguration")
    for (let i = this.getFirstID(); i <= this.getCurrentID(); i++) {
      console.log("nodes", i)
      nodes.byKey(i).then((data) => {

        items.push(data);
        console.log(data)
      });
    }

    for (let i = this.getFirstID(); i <= this.getCurrentID(); i++) {
      console.log("links", i)
      links.byKey(i).then((data) => {

        items.push(data);
        console.log(data)
      });
    }

    console.log(items)
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
