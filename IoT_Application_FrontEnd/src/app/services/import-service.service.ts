import {Injectable} from '@angular/core';
import {FlowEdge, FlowNode, NodesEdgesService} from "./nodes-edges.service";

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of JSON import.
 */
export class ImportServiceService {

  constructor(private nodesEdgesService: NodesEdgesService) {
  }

  parseToRightFormat(jsonContent: any) {
    // Parse the JSON content and add the nodes and edges to the array in the service
    // Call a function to convert the JSON content into a list with the right format

    // Push the list into the node/edge service

    for (const entity of jsonContent.entities) {
      let node: FlowNode = {
        id: entity.id,
        text: entity.text,
        type: entity.type
      }
      this.nodesEdgesService.getFlowNodes().push(node);
    }

    for (const link of jsonContent.links) {
      let edge: FlowEdge = {
        id: link.id,
        fromId: link.fromId,
        toId: link.toId,
        text: link.text
      }
      this.nodesEdgesService.getFlowEdges().push(edge);
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
