import {Injectable} from '@angular/core';
import {Link} from "../models/link.model";
import {DiagramNode} from "../models/node.module";
import {DxDiagramComponent} from "devextreme-angular";

const nodes: DiagramNode[] = [];

const links: Link[] = [];

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {
  getLinks(): Link[] {
    return links;
  }

  getNodes(): DiagramNode[] {
    return nodes;
  }

  clearLists() {
    nodes.splice(0, nodes.length);
    links.splice(0, links.length);
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

  private createEntityJson() {
    return this.getNodes().filter(entity => entity.type === 'entity').map(entity => ({
      id: entity.id,
      name: entity.name,
      fields: entity.fields,
      table: entity.table,
      primary_key: []
    }));
  }

  private createTableJson() {
    return this.getNodes().filter(entity => entity.type === 'table').map(table => ({
      id: table.id,
      tableName: table.name,
      partition_key: table.partition_key,
      sort_key: table.sort_key
    }))
  }

  private createLinkJson() {
    return this.getLinks().map(link => ({
      first_entity: link.first_entity,
      second_entity: link.second_entity,
      fields: link.fields
    }));
  }

  /**
   * This method is called when the user performs any action in the diagram and updates the lists of nodes and links.
   * @param diagram the diagram where the action is taking place
   * @param e the event that triggered the action
   */
  updateLists(diagram: DxDiagramComponent, e: any) {
    let items = diagram.instance.getItems();
    this.clearLists();
    for (const itemKey in items) {
      const item = items[itemKey];
      if (item.itemType === 'shape') {
        nodes.push();
      }
      if (item.itemType === 'connector') {
        links.push();
      }
    }
  }
}