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
   * This method creates a new link between two entities. 
   * Starting from their ids, extract the two entities from the configuration, 
   * add the link to the configuration and update the JSON.
   * @param first_entity first entity id.
   * @param second_entity second entity id.
   */
  saveLink(first_entity: number, second_entity: number) {

    const firstElementIndex = this.configuration.entities.findIndex(entity => entity.entity_id === first_entity);
    const secondElementIndex = this.configuration.entities.findIndex(entity => entity.entity_id === second_entity);

    const firstEntity = this.configuration.entities.at(firstElementIndex)
    const secondEntity = this.configuration.entities.at(secondElementIndex)

    if (firstEntity != undefined && secondEntity != undefined) {
      const link = new Link(firstEntity, secondEntity);

      this.configuration.links.push(link)
      this.saveConfiguration()
    }
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
  }

  /**
   * This method creates the entity part of the JSON.
   * @returns json of the entities.
   */
  createEntityJson() {
    const jsonEntities = this.configuration.entities.map(entity => ({
      name: entity.entity_name,
      entity_id: entity.entity_id,
      fields: this.createFields(entity)
    }));
    return jsonEntities
  }

  /**
   * This method creates the link part of the JSON.
   * @returns json of the links.
   */
  createLinkJson() {
    const jsonLink = this.configuration.links.map(link => ({
      first_entity: link.first_entity.entity_name,
      second_entity: link.second_entity.entity_name,
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
      table_id: table.table_id,
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
      const elementIndex = this.configuration.entities.findIndex(entity => entity.entity_id === id);
      this.configuration.entities.splice(elementIndex, 1)
      console.log(this.configuration.entities)
    } else if (class_name == 'Table') {
      const elementIndex = this.configuration.tables.findIndex(table => table.table_id === id);
      this.configuration.tables.splice(elementIndex, 1)
    }
    this.saveConfiguration()
  }


  /**
   * This method remove a link from configuration
   * and update JSON.
   * @param first_entity first entity id to remove.
   * @param second_entity second entity id to remove.
   */
  removeLink(first_entity: string, second_entity: string) {
    const elementIndex = this.configuration.links.findIndex(link =>
      link.first_entity.entity_id === parseInt(first_entity) && link.second_entity.entity_id === parseInt(second_entity));
      console.log(elementIndex)
    this.configuration.links.splice(elementIndex, 1)
    this.saveConfiguration();
  }

  /**
   * This method delete all configuration.
   */
  clear() {
    this.configuration.entities = []
    this.configuration.links = []
    this.configuration.tables = []
    this.saveConfiguration()
  }

  /**
   * This method allows you to export the configuration.
   */
  export() {
    this.jsonDownloadService.downloadJson()
  }
}
