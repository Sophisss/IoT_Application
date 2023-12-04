import {Injectable} from '@angular/core';
import {Entity} from 'src/app/models/entity.model';
import {Link} from 'src/app/models/link.model';
import {JsonDownloadService} from './json-download.service';
import {Table} from 'src/app/models/table.model';
import {ConfigurationService} from "./configuration.service";

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of all JSON generation.
 */
export class GeneratorService {

  /**
   * Constructor for this Component.
   * @param jsonDownloadService service to export JSON.
   * @param confService service to model the .json file.
   */
  constructor(private jsonDownloadService: JsonDownloadService, private confService: ConfigurationService) {
  }

  /**
   * This method creates a new entity,
   * adds it to the configuration, and updates the final JSON.
   * @param entity_id entity id.
   * @param entityName entity name.
   */
  saveEntity(entity_id: number, entityName: string) {
    const entity = new Entity(entity_id, entityName);
    this.confService.getEntities().push(entity)
    this.saveConfiguration()
  }

  /**
   * This method creates a new link between two entities or
   * between entity and table.
   * Starting from their ids, extract the two object from the configuration,
   * add the link to the configuration and update the JSON.
   * @param first_id first object id.
   * @param second_id second object id.
   * @param second_class second object class.
   */
  saveLink(first_id: number, second_id: number, second_class: string) {
    let firstEntity = undefined;
    let secondEntity = undefined;

    if (second_class === 'Entity') {
      firstEntity = this.confService.getEntities().find(entity => entity.id === first_id);
      secondEntity = this.confService.getEntities().find(entity => entity.id === second_id);

      if (firstEntity && secondEntity) {
        const link = new Link(firstEntity, secondEntity);
        this.confService.getLinks().push(link);
      }
    } else if (second_class === 'Table') {
      firstEntity = this.confService.getEntities().find(entity => entity.id === first_id);
      secondEntity = this.confService.getTables().find(table => table.id === second_id);

      if (firstEntity && secondEntity) {
        firstEntity.setTable(secondEntity.name);
      }
    }
    this.saveConfiguration();
  }

  /**
   * This method create a new table,
   * adds it to the configuration, and updates the final JSON.
   * @param table_id table id.
   * @param name table name.
   */
  saveTable(table_id: number, name: string) {
    const table = new Table(table_id, name)
    this.confService.getTables().push(table)
    this.saveConfiguration()
  }

  /**
   * saveAttributes() {
   const nomeAttributo = this.form.value.nomeAttributo
   const type = this.form.value.type
   const isRequired = this.form.value.isRequired
   const newField = new Field(nomeAttributo, type, isRequired)
   this.entity.fields.push(newField)
   this.resetForm()
   }
   */

  /**
   * This method creates a new configuration,
   * with a basic structure, filling it from time to time
   * based on the needs requested by the customer regarding entities, links...
   */
  saveConfiguration() {
    const jsonEntities = this.createEntityJson()
    const jsonLinks = this.createLinkJson()
    const jsonTable = this.createTableJson()

    const jsonObject = {
      projectName: "Prova",
      entities: jsonEntities,
      links: jsonLinks,
      awsConfig: {
        dynamo: {
          tables: jsonTable
        }
      }
    };

    this.jsonDownloadService.setData(jsonObject);

    return jsonObject;
  }

  /**
   * This method creates the entity part of the JSON.
   * @returns json of the entities.
   */
  createEntityJson() {
    return this.confService.getEntities().map(entity => ({
      name: entity.name,
      table: entity.table,
      entity_id: entity.id,
      fields: this.createFields(entity),
      primary_key: []
    }));
  }

  /**
   * This method creates the link part of the JSON.
   * @returns json of the links.
   */
  createLinkJson() {
    return this.confService.getLinks().map(link => ({
      first_entity: link.first_entity.name,
      second_entity: link.second_entity.name,
      fields: this.createFields(link)
    }));
  }

  /**
   * This method creates the table part of the JSON.
   * @returns json of the tables.
   */
  createTableJson() {
    return this.confService.getTables().map(table => ({
      tableName: table.name,
      table_id: table.id,
      partitionKey: table.partition_key,
      sortKey: table.sort_Key
    }))
  }

  /**
   * This method creates the fields part of the JSON.
   * @param object representing an entity or a link from which to get the list of fields.
   * @returns json of the fields.
   */
  createFields(object: Entity | Link) {
    return object.fields.map(field => ({
      name: field.name,
      type: field.type,
      required: field.required
    }))
  }

  /**
   * This method removes an object (entity or table) from configuration
   * and updates JSON.
   * @param id object id to remove.
   * @param class_name indicates whether to remove an entity or a table.
   */
  removeObject(id: number, class_name: string) {
    if (class_name == 'Entity') {
      const elementIndex = this.confService.getEntities().findIndex(entity => entity.id === id);
      this.confService.getEntities().splice(elementIndex, 1)
    } else if (class_name == 'Table') {
      const elementIndex = this.confService.getTables().findIndex(table => table.id === id);
      this.confService.getTables().splice(elementIndex, 1)
    }
    this.saveConfiguration()
  }


  /**
   * This method removes a link from configuration
   * and updates JSON.
   * @param first_entity first entity id to remove.
   * @param second_entity second entity id to remove.
   * @param node_class second entity class.
   */
  removeLinkConfiguration(first_entity: number, second_entity: number, node_class: string) {
    if (node_class === 'Table') {
      const entity = this.confService.getEntities().find(entity => entity.id === first_entity);
      if (entity) {
        entity.resetTable();
      }
    } else {
      const elementIndex = this.confService.getLinks().findIndex(link =>
        link.first_entity.id === first_entity && link.second_entity.id === second_entity);
      this.confService.getLinks().splice(elementIndex, 1)
    }
    this.saveConfiguration();
  }

  /**
   * This method allows you to export the configuration.
   * @param fileName file name to save.
   */
  export(fileName: string) {
    this.jsonDownloadService.downloadJson(fileName);
  }
}
