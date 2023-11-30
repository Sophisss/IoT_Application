import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of JSON import.
 */
export class ImportServiceService {

  private savedFileContent: string | null = null;

  async manageImportedFile(event: Event): Promise<void> {
    try {
      const fileContent = await this.onFileSelected(event);
      // Save the file content for later use
      this.savedFileContent = fileContent;
    } catch (error) {
      console.error('Error:', error);
    }
  }

  /**
   * This method handles the selection of a file and asynchronously processes it.
   * @param event event triggered when a file is selected.
   * @returns a Promise that resolves with the content of the selected JSON file.
   */
  onFileSelected(event: Event): Promise<string> {
    return new Promise((resolve, reject) => {
      const fileInput = event.target as HTMLInputElement;
      const file: File | null = fileInput.files?.[0] || null;

      if (!file) {
        console.log('No file selected');
        reject('No file selected');
        return;
      }

      const reader = new FileReader();

      reader.onload = (event) => {
        // 'result' contains the contents of the file as a data URL
        const content: string | ArrayBuffer | null = event.target?.result;

        if (typeof content === 'string') {
          resolve(content);
        } else {
          reject('Failed to read file content');
        }
      };

      // Read the file as text
      reader.readAsText(file);
    });
  }

  /**
   * Getter method to retrieve the saved file content
   */
  getSavedFileContent(): string | null {
    return this.savedFileContent;
  }
}
