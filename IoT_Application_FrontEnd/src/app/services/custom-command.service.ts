import {Injectable} from '@angular/core';
import {ToggleService} from "./toggle.service";
import {ConfigurationService} from "./configuration.service";
import {JsonDownloadService} from "./json-download.service";
import ArrayStore from "devextreme/data/array_store";

@Injectable({
  providedIn: 'root'
})
export class CustomCommandService {

  constructor(private toggleService: ToggleService, private configService: ConfigurationService,
              private jsonDownload: JsonDownloadService) {
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
      console.log("export")
      this.configService.updateConfiguration(nodes, links);
      this.downloadJsonFile();
    }
    if (commandName === 'viewJson') {
      this.toggleService.toggleDrawer();
    }
    if (commandName === 'generateCode') {
      console.log(this.configService.exportConfiguration());
    }
  }

  /**
   * Downloads the current configuration as a json file and sets the name of the file.
   */
  private downloadJsonFile() {
    this.jsonDownload.downloadJson();
  }
}
