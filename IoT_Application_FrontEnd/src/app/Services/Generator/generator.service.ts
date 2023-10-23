import { Injectable } from '@angular/core';
import { Configuration } from 'src/app/Models/Configuration';
import { Entity } from 'src/app/Models/Entity';
import { Link } from 'src/app/Models/Link';
import { JsonDownloadService } from '../JSONdownload/json-download.service';
import { Table } from 'src/app/Models/Table';

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of all JSON generation.
 */
export class GeneratorService {

  /**
   * Variable that represent a new configuration.
   */
  configuration: Configuration = new Configuration;

  /**
   * Constructor for this Component. 
   * @param jsonDownloadService service to export JSON.
   */
  constructor(private jsonDownloadService: JsonDownloadService) { }

  /**
   * This method creates a new entity, 
   * adds it to the configuration, and updates the final JSON.
   * @param entity_id entity id.
   * @param entityName entity name.
   */
  saveEntity(entity_id: number, entityName: string) {
    const entity = new Entity(entity_id, entityName);
    this.configuration.entities.push(entity)
    this.saveConfiguration()
  }

  /**
   * This method creates a new link between two entities or 
   * between entity and table. 
   * Starting from their ids, extract the two object from the configuration, 
   * add the link to the configuration and update the JSON.
   * @param first_id first object id.
   * @param second_id second object id.
   * @param first_class first object class.
   * @param second_class second object class.
   */
  saveLink(first_id: number, second_id: number, second_class: string) {
    let firstEntity = undefined;
    let secondEntity = undefined;

    if (second_class === 'Entity') {
      firstEntity = this.configuration.entities.find(entity => entity.id === first_id);
      secondEntity = this.configuration.entities.find(entity => entity.id === second_id);

      if (firstEntity && secondEntity) {
        const link = new Link(firstEntity, secondEntity);
        this.configuration.links.push(link);
      }
    } else if (second_class === 'Table') {
      firstEntity = this.configuration.entities.find(entity => entity.id === first_id);
      secondEntity = this.configuration.tables.find(table => table.id === second_id);

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
    this.configuration.tables.push(table)
    this.saveConfiguration()
  }

  /**
   * saveAttributes() {
    const nomeAttributo = this.form.value.nomeAttributo
    const type = this.form.value.type
    const isrequired = this.form.value.isrequired
    const newField = new Field(nomeAttributo, type, isrequired)
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
    const jsonEntities = this.configuration.entities.map(entity => ({
      name: entity.name,
      table: entity.table,
      entity_id: entity.id,
      fields: this.createFields(entity),
      primary_key: []
    }));
    return jsonEntities
  }

  /**
   * This method creates the link part of the JSON.
   * @returns json of the links.
   */
  createLinkJson() {
    const jsonLink = this.configuration.links.map(link => ({
      first_entity: link.first_entity.name,
      second_entity: link.second_entity.name,
      fields: this.createFields(link)
    }));
    return jsonLink
  }

  /**
   * This method creates the table part of the JSON.
   * @returns json of the tables.
   */
  createTableJson() {
    const jsonTable = this.configuration.tables.map(table => ({
      tableName: table.name,
      table_id: table.id,
      partitionKey: table.partition_key,
      sortKey: table.sort_Key
    }))
    return jsonTable
  }

  /**
   * This method creates the fields part of the JSON.
   * @param object representing an entity or link from which to get the list of fields.
   * @returns json of the fields.
   */
  createFields(object: Entity | Link) {
    const fields = object.fields.map(field => ({
      name: field.name,
      type: field.type,
      required: field.required
    }))
    return fields
  }

  /**
   * This method remove an object (entity or table) from configuration 
   * and update JSON.
   * @param id object id to remove.
   * @param class_name indicates whether to remove an entity or a table.
   */
  removeObject(id: number, class_name: string) {
    if (class_name == 'Entity') {
      const elementIndex = this.configuration.entities.findIndex(entity => entity.id === id);
      this.configuration.entities.splice(elementIndex, 1)
    } else if (class_name == 'Table') {
      const elementIndex = this.configuration.tables.findIndex(table => table.id === id);
      this.configuration.tables.splice(elementIndex, 1)
    }
    this.saveConfiguration()
  }


  /**
   * This method remove a link from configuration
   * and update JSON.
   * @param first_entity first entity id to remove.
   * @param second_entity second entity id to remove.
   * @param node_class second entity class.
   */
  removeLinkConfiguration(first_entity: number, second_entity: number, node_class: string) {
    if (node_class === 'Table') {
      const entity = this.configuration.entities.find(entity => entity.id === first_entity);

      if(entity){
        entity.resetTable();
      }
    } else {
      const elementIndex = this.configuration.links.findIndex(link =>
        link.first_entity.id === first_entity && link.second_entity.id === second_entity);
      this.configuration.links.splice(elementIndex, 1)
    }
    this.saveConfiguration();
  }

  /**
   * This method delete all configuration.
   *   
   */
  clear() {
    this.configuration.entities = []
    this.configuration.links = []
    this.configuration.tables = []
    this.saveConfiguration();
  }

  /**
   * This method allows you to export the configuration.
   */
  export() {
    this.jsonDownloadService.downloadJson()
  }
}
