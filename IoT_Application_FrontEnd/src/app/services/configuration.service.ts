import {Injectable} from '@angular/core';
import {Link} from "../models/link.model";
import {DiagramNode} from "../models/node.module";

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
}