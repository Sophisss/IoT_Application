import {Injectable} from '@angular/core';
import {Entity} from "../models/entity.model";
import {Link} from "../models/link.model";
import {Table} from "../models/table.model";

const entities: Entity[] = [];

const tables: Table[] = [];

const links: Link[] = [];

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {
  getEntities(): Entity[] {
    return entities;
  }

  getTables(): Table[] {
    return tables;
  }

  getLinks(): Link[] {
    return links;
  }

  clearLists() {
    links.splice(0, links.length);
    tables.splice(0, tables.length);
    entities.splice(0, entities.length);
  }
}