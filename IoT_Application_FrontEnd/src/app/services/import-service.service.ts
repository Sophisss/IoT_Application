import { Injectable } from '@angular/core';
import { ConfigurationService } from "./configuration.service";
import { Item } from "../models/item.model";
import { Field } from "../models/field.model";
import { IoT } from '../models/iot.model';

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of JSON import.
 */
export class ImportServiceService {

  constructor(private configService: ConfigurationService) { }

  /**
   * Takes all the elements from the imported .json file and pushes them into the list.
   * @param jsonContent the content of the .json file
   */
  pushToConfiguration(jsonContent: any) {
    this.configService.setTitle(jsonContent.projectName);

    //read entities
    for (const entity of jsonContent.entities) {
      for (const field of entity.fields) {
        field.isPrimaryKey = false;
      }
      entity.fields.find((field: Field) => entity.primary_key[0] === field.name).isPrimaryKey = true;

      let nodeEntity: Item = {
        ID: this.configService.assignID(),
        name: entity.name,
        type: "entity",
        fields: entity.fields,
        table: entity.table,
        primary_key: entity.primary_key,
        partition_key_name: null,
        partition_key_type: null,
        sort_key_name: null,
        sort_key_type: null,
        first_item_ID: null,
        second_item_ID: null,
        numerosity: null,
        keyword: null,
        separator: null
      }
      this.configService.getItems().push(nodeEntity);
    }

    //read tables
    for (const table of jsonContent.awsConfig.dynamo.tables) {
      let nodeTable: Item = {
        ID: this.configService.assignID(),
        name: table.tableName,
        type: "table",
        table: null,
        partition_key_name: table.partition_key.name,
        partition_key_type: table.partition_key.type,
        sort_key_name: table.sort_key.name,
        sort_key_type: table.sort_key.type,
        first_item_ID: null,
        second_item_ID: null,
        fields: null,
        numerosity: null,
        primary_key: null,
        keyword: table.parameters.single_entity_storage_keyword,
        separator: table.parameters.id_separator
      }
      this.configService.getItems().push(nodeTable);
    }

    //read links
    for (const link of jsonContent.links) {
      let edge: Item =
      {
        ID: this.configService.assignID(),
        name: null,
        type: 'link',
        table: link.table,
        partition_key_name: null,
        partition_key_type: null,
        sort_key_name: null,
        sort_key_type: null,
        first_item_ID: this.getIDFromName(link.first_entity),
        second_item_ID: this.getIDFromName(link.second_entity),
        numerosity: link.numerosity,
        fields: link.fields,
        primary_key: link.primary_key,
        keyword: null,
        separator: null
      }
      this.configService.getItems().push(edge);
    }

    const rule = jsonContent.awsConfig.iot.iot_rule.rule;

    let iot: IoT = {
      database_name: jsonContent.awsConfig.iot.timestream.database.name,
      table_name: jsonContent.awsConfig.iot.timestream.table.name,
      shadow_notify: jsonContent.awsConfig.iot.iot_rule.shadow_notify,
      topic_notify: rule ? true : false,
      sql_statement: rule ? rule.sql_statement : null
    }

    this.configService.updateIoTConfiguration(iot);
  }

  /**
   * This method handles the selection of a file and asynchronously processes it.
   * @param event event triggered when a file is selected.
   * @returns a Promise that resolves with the content of the selected JSON file.
   */
  onFileSelected(event: Event) {
    return new Promise((resolve, reject) => {
      const fileInput = event.target as HTMLInputElement;
      const selectedFile = fileInput?.files?.[0];

      try {
        if (selectedFile) this.readFileContent(selectedFile)
          .then(resolve)
          .catch(reject);
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * This method reads the content of a selected file and resolves with its JSON data.
   * @param selectedFile file to read as a Blob.
   * @returns a Promise that resolves with the JSON data from the file.
   */
  readFileContent(selectedFile: Blob) {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();

      fileReader.onload = (e) => {
        if (e.target) {
          const jsonContent = JSON.parse(e.target.result as string);
          resolve(jsonContent);
        } else {
          reject('Errore nell\'evento di caricamento del file.');
        }
      };
      fileReader.readAsText(selectedFile);
    });
  }

  /**
   * This method returns the ID of an item given its name.
   * @param name the name of the item
   * @private
   */
  private getIDFromName(name: string): number {
    return this.configService.getItems().find(item => item.name === name).ID;
  }
}
