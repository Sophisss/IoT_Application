import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class JsonDownloadService {
  private jsonData: any = null;

  constructor() { }

  setData(data: any) {
    this.jsonData = data;
  }

  getData(): any {
    return this.jsonData;
  }

  downloadJson() {
    const jsonData = this.jsonData;

    if (jsonData) {
      const jsonStr = JSON.stringify(jsonData, null, 2);
      const blob = new Blob([jsonStr], {type: 'application/json'});
      const url = window.URL.createObjectURL(blob);

      // Create a temporary anchor element to trigger the download
      const a = document.createElement('a');
      a.href = url;
      a.download = 'structure.json'; // Specify the file name
      a.click();

      // Clean up resources
      window.URL.revokeObjectURL(url);
    } else {
      // Handle the case where data is not available
      console.error('No JSON data available.');
    }
  }
}
