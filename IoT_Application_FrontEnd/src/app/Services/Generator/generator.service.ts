import { Injectable } from '@angular/core';
import { Configuration } from 'src/app/Models/Configuration';
import { Entity } from 'src/app/Models/Entity';
import { Link } from 'src/app/Models/Link';
import { JsonDownloadService } from '../JSONdownload/json-download.service';
import { Table } from 'src/app/Models/Table';

@Injectable({
  providedIn: 'root'
})
export class GeneratorService {

  //New configuration
  configuration: Configuration = new Configuration;

  constructor(private jsonDownloadService: JsonDownloadService) { }

  saveEntity(entity_id: number, entityName: string) {
    const entity = new Entity(entity_id, entityName);
    this.configuration.entities.push(entity)
    this.saveConfiguration()
  }

  saveLink(first_entity: number, second_entity: number) {

    const firstElementIndex = this.configuration.entities.findIndex(entity => entity.entity_id === first_entity);
    const secondElementIndex = this.configuration.entities.findIndex(entity => entity.entity_id === second_entity);

    const firstEntity = this.configuration.entities.at(firstElementIndex)
    const secondEntity = this.configuration.entities.at(secondElementIndex)

    console.log("Save link")
    console.log("1: " + firstEntity?.entity_id)
    console.log("2: " + secondEntity?.entity_id)

    if (firstEntity != undefined && secondEntity != undefined) {
      const link = new Link(firstEntity, secondEntity);

      this.configuration.links.push(link)
      this.saveConfiguration()
    }
  }

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
   * This method create a new configuration
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

  createEntityJson() {
    const jsonEntities = this.configuration.entities.map(entity => ({
      name: entity.entity_name,
      entity_id: entity.entity_id,
      fields: this.createFields(entity)
    }));
    return jsonEntities
  }

  createLinkJson() {
    const jsonLink = this.configuration.links.map(link => ({
      first_entity: link.first_entity.entity_name,
      second_entity: link.second_entity.entity_name,
      fields: this.createFields(link)
    }));
    return jsonLink
  }

  createTableJson() {
    const jsonTable = this.configuration.tables.map(table => ({
      tableName: table.name,
      table_id: table.table_id,
      partitionKey: table.partition_key,
      sortKey: table.sort_Key
    }))
    return jsonTable
  }

  createFields(object: Entity | Link) {
    const fields = object.fields.map(field => ({
      name: field.name,
      type: field.type,
      required: field.required
    }))
    return fields
  }

  export() {
    this.jsonDownloadService.downloadJson()
  }

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


  removeLink(first_entity: string, second_entity: string) {
    const elementIndex = this.configuration.links.findIndex(link =>
      link.first_entity.entity_id === parseInt(first_entity) && link.second_entity.entity_id === parseInt(second_entity));
      console.log(elementIndex)
    this.configuration.links.splice(elementIndex, 1)
    this.saveConfiguration();
  }

  clear() {
    this.configuration.entities = []
    this.configuration.links = []
    this.configuration.tables = []
    this.saveConfiguration()
  }
}
