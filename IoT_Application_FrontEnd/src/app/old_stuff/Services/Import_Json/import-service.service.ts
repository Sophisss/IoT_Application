import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of JSON import.
 */
export class ImportServiceService {

  /**
   * Variable that tracks a File object or is set to null if no file is selected.
   */
  file: File | null = null;

  constructor() {
  }

  /**
   * This method validates the selected file.
   * @param selectedFile the selected file from the input.
   */
  validateFile(selectedFile: File | undefined) {
    if (!selectedFile) {
      throw 'Nessun file selezionato.';
    }

    if (!selectedFile.name.endsWith('.json')) {
      throw 'Seleziona un file .json.';
    }
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
   * This method handles the selection of a file and asynchronously processes it.
   * @param event event triggered when a file is selected.
   * @returns a Promise that resolves with the content of the selected JSON file.
   */
  onFileSelected(event: Event) {
    return new Promise((resolve, reject) => {
      const fileInput = event.target as HTMLInputElement;
      const selectedFile = fileInput?.files?.[0];

      try {
        this.validateFile(selectedFile);
        if (selectedFile) this.readFileContent(selectedFile)
          .then(resolve)
          .catch(reject);
      } catch (error) {
        reject(error);
      }
    });
  }

}
