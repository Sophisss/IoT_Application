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

  customCommandHandler(e: any, nodes: ArrayStore, links: ArrayStore) {
    const commandName: string = e.name;

    if (commandName === 'export') {
      console.log("export")
      this.configService.updateConfiguration(nodes, links);
      this.exportToJson();
    }
    if (commandName === 'viewJson') {
      this.toggleService.toggleDrawer();
    }
    if (commandName === 'generateCode') {
      console.log(this.configService.exportConfiguration());
    }
  }

  private exportToJson() {
    this.jsonDownload.downloadJson('diagram');
  }
}
