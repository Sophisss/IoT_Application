import {Injectable} from '@angular/core';
import {SideDrawerService} from "./side-drawer.service";
import {ConfigurationService} from "./configuration.service";
import {JsonDownloadService} from "./json-download.service";

@Injectable({
  providedIn: 'root'
})
export class CustomCommandService {

  constructor(private drawerService: SideDrawerService, private configService: ConfigurationService,
              private jsonDownload: JsonDownloadService) {
  }

  customCommandHandler(e: any) {
    const commandName: string = e.name;

    if (commandName === 'export') {
      this.exportToJson();
    }
    if (commandName === 'viewJson') {
      this.drawerService.toggleDrawer();
    }
    if (commandName === 'generateCode') {
      console.log(this.configService.exportConfiguration());
    }
  }

  private exportToJson() {
    this.jsonDownload.downloadJson('diagram');
  }
}
