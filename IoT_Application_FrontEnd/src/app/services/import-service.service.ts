import {Injectable} from '@angular/core';
import {ConfigurationService} from "./configuration.service";
import {Item} from "../models/item.model";

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of JSON import.
 */
export class ImportServiceService {

  constructor(private configService: ConfigurationService) {
  }

  /**
   * Takes all the elements from the imported .json file and pushes them into the list.
   * @param jsonContent the content of the .json file
   */
  pushToConfiguration(jsonContent: any) {
    //read entities
    for (const entity of jsonContent.entities) {
      let nodeEntity: Item = {
        ID: this.configService.assignID(),
        name: entity.name,
        type: "entity",
        //fields: entity.fields,
        table: entity.table,
        partition_key: null,
        sort_key: null,
        first_item: null,
        second_item: null,
      }
      this.configService.getItems().push(nodeEntity);
    }

    //read tables
    for (const table of jsonContent.awsConfig.dynamo.tables) {
      let nodeTable: Item = {
        ID: this.configService.assignID(),
        name: table.tableName,
        type: "table",
        //fields: entity.fields,
        table: null,
        partition_key: null,
        sort_key: null,
        first_item: null,
        second_item: null,
      }
      this.configService.getItems().push(nodeTable);
    }

    //read links
    for (const link of jsonContent.links) {
      let edge: Item =
        {
          ID: this.configService.assignID(),
          name: link.first_entity + " - " + link.second_entity,
          type: 'link',
          table: null,
          partition_key: null,
          sort_key: null,
          first_item: link.first_entity,
          second_item: link.second_entity,
          //fields: link.fields,
        }
      this.configService.getItems().push(edge);
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
