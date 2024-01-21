import {Injectable} from '@angular/core';
import {ToggleService} from "./toggle.service";
import {ConfigurationService} from "./configuration.service";
import {JsonDownloadService} from "./json-download.service";
import ArrayStore from "devextreme/data/array_store";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../../environments/environments";
import {ToastNotificationService} from "./toast-notification.service";
import {lastValueFrom} from "rxjs";
import {Clipboard} from "@angular/cdk/clipboard";

@Injectable({
  providedIn: 'root'
})
export class CustomCommandService {

  constructor(private toggleService: ToggleService, private configService: ConfigurationService,
              private jsonDownload: JsonDownloadService, private httpClient: HttpClient,
              private notificationService: ToastNotificationService, private clipboard: Clipboard) {
  }

  /**
   * Custom command handler:
   * - export: update the current configuration and export it to json;
   * - viewJson: toggle the json view;
   * - generateCode: generate the code from the current configuration;
   * @param e the current event
   * @param nodes the data source of the nodes
   * @param links the data source of the links
   */
  customCommandHandler(e: any, nodes: ArrayStore, links: ArrayStore) {
    const commandName: string = e.name;

    if (commandName === 'export') {
      console.log("export");
      this.configService.updateConfiguration(nodes, links);
      this.downloadJsonFile();
    }
    if (commandName === 'viewJson') {
      this.toggleService.toggleDrawer();
    }
    if (commandName === 'generateCode') {
      this.notificationService.displayToast("Generating code...", 230,
        "#toast-container", "info", 2000);

      const jsonFile = this.configService.exportConfiguration();
      this.generateCode(jsonFile).then(
        (data: any) => {
          console.log('Response:', data);
          const responseData = data.url;

          if (typeof responseData === 'string') {
            if (this.clipboard.copy(responseData)) {
              this.notificationService.displayToast("The code has been generated successfully and the" +
                " URL to download it has been copied into your clipboard!", 370,
                "#toast-container", "success", 4000);
            }
          } else {
            this.notificationService.displayToast("Unknown Error", 230,
              "#toast-container", "error", 3000);
          }

        },
        (error: any) => {
          this.notificationService.displayToast("Something went wrong, you might want " +
            "to check your configuration...", 300,
            "#toast-container", "warning", 4000);

          console.error('Error:', error);
        }
      );
    }
  }

  /**
   * Downloads the current configuration as a json file and sets the name of the file.
   */
  private downloadJsonFile() {
    this.jsonDownload.downloadJson();
  }

  private async generateCode(jsonFile: any): Promise<any> {
    const apiURL = `${environment.baseUrl}/download`;

    const headers = new HttpHeaders({
      'Content-Type': 'application/json' // Set the content type based on your API requirements
    });

    return await lastValueFrom(this.httpClient.post(apiURL, jsonFile, {headers}));
  }
}
