import {Injectable} from '@angular/core';
import {saveAs} from 'file-saver';
import {ConfigurationService} from "./configuration.service";

@Injectable({
  providedIn: 'root'
})
/**
 * Class that acts as a service that takes care of JSON export.
 */
export class JsonDownloadService {
  constructor(private configService: ConfigurationService) {
  }

  /**
   * Download data as JSON file.
   */
  downloadJson() {
    const jsonData: any = this.configService.exportConfiguration();
    let fileName: string = this.configService.getTitle().trim();

    if (jsonData) {
      const blob = new Blob([JSON.stringify(jsonData)], {type: 'application/json'});

      saveAs(blob, `${fileName}.json`);
    } else {
      alert('No JSON data available.');
    }
  }
}
