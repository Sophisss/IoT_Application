import { Injectable } from '@angular/core';

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

  constructor() { }

  /**
   * This method handles opening and reading a JSON file.
   * @param event event associated with the input file.
   * @returns a Promise that resolves with the contents of the JSON file or is rejected in case of errors.
   */
  onFileSelected(event: Event): Promise<any> {
    return new Promise((resolve, reject) => {
      const fileInput = event.target as HTMLInputElement;
      const selectedFile = fileInput?.files?.[0];

      if (!selectedFile) {
        return reject('Nessun file selezionato.');
      }

      if (!selectedFile.name.endsWith('.json')) {
        return reject('Seleziona un file .json.');
      }

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
