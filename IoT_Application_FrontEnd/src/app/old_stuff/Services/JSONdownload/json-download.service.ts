import {Injectable} from '@angular/core';
import {saveAs} from 'file-saver';

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of JSON export.
 */
export class JsonDownloadService {
  jsonData: any;

  /**
   * Set the data that will be downloaded next.
   * @param data data to download.
   */
  setData(data: any) {
    this.jsonData = data;
  }

  /**
   * Get the data set previously.
   * @returns set data.
   */
  getData(): any {
    return this.jsonData;
  }

  /**
   * Download data as JSON file.
   * @param fileName file name to save.
   */
  downloadJson(fileName: string) {
    const jsonData = this.getData();

    if (jsonData) {
      const jsonStr = JSON.stringify(jsonData, null, 2);
      const blob = new Blob([jsonStr], {type: 'application/json'});
      saveAs(blob, `${fileName}.json`);

    } else {
      alert('No JSON data available.');
    }
  }
}
