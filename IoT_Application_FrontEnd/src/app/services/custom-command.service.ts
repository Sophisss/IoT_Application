import {Injectable} from '@angular/core';
import {ToggleService} from "./toggle.service";
import {ConfigurationService} from "./configuration.service";
import {JsonDownloadService} from "./json-download.service";

@Injectable({
  providedIn: 'root'
})
export class CustomCommandService {

  constructor(private toggleService: ToggleService, private configService: ConfigurationService,
              private jsonDownload: JsonDownloadService) {
  }

  customCommandHandler(e: any) {
    const commandName: string = e.name;

    if (commandName === 'export') {
      this.exportToJson();
    }
    if (commandName === 'viewJson') {
      this.toggleService.toggleDrawer();
      console.log(this.toggleService.isDrawerOpened());
    }
    if (commandName === 'generateCode') {
      console.log(this.configService.exportConfiguration());
    }
  }

  private exportToJson() {
    this.jsonDownload.downloadJson('diagram');
  }
}
