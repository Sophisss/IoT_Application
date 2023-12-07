import {Injectable} from '@angular/core';
import {ConfigurationService} from "./configuration.service";
import {Link} from "../models/link.model";
import {DiagramNode} from "../models/node.module";

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of JSON import.
 */
export class ImportServiceService {

  constructor(private nodesEdgesService: ConfigurationService) {
  }

  /**
   * Takes all the elements from the imported .json file and pushes them into the correspondent list.
   * @param jsonContent the content of the .json file
   */
  pushToConfiguration(jsonContent: any) {
    //read entities
    for (const entity of jsonContent.entities) {
      let nodeEntity: DiagramNode = new DiagramNode(entity.id, entity.name, "entity", entity.fields, entity.table);
      /*{
         id: entity.id,
         name: entity.name,
         table: entity.table,
         fields: entity.fields,
         type: "entity"
       }*/
      this.nodesEdgesService.getNodes().push(nodeEntity);
    }

    //read tables
    for (const table of jsonContent.awsConfig.dynamo.tables) {
      let nodeTable: DiagramNode = new DiagramNode(table.id, table.tableName, "table", [], null, table.partition_key, table.sort_key);
      /*{
      id: table.id,
      name: table.tableName,
      type: "table",
      partition_key: "pk",
      sort_key: "sk",
      fields: []
    }*/
      this.nodesEdgesService.getNodes().push(nodeTable);
    }

    //read links
    for (const link of jsonContent.links) {
      let edge: Link = new Link(link.id, link.first_entity + " - " + link.second_entity, link.first_entity, link.second_entity, link.fields);
      /*{
      id: link.id,
      first_entity: link.first_entity,
      second_entity: link.second_entity,
      fields: link.fields,
      name: link.first_entity + " - " + link.second_entity,
    }*/
      this.nodesEdgesService.getLinks().push(edge);
    }
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
}
