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
   * This method is called when the user performs any action in the diagram and updates the lists of nodes and links.
   * @param diagram the diagram where the action is taking place
   * @param e the event that triggered the action
   */
  updateLists(diagram: DxDiagramComponent, e: any) {
    let items = diagram.instance.getItems();
    this.clearLists();
    for (const itemKey in items){
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