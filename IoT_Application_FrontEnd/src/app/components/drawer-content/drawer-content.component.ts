import {Component} from '@angular/core';
import {ConfigurationService} from "../../services/configuration.service";

@Component({
  selector: 'app-drawer-content',
  templateUrl: './drawer-content.component.html',
  styleUrls: ['./drawer-content.component.scss']
})
export class DrawerContentComponent {
  drawerContent: string = "Drawer content";

  constructor(private configService: ConfigurationService) {
    let configuration = JSON.stringify(this.configService.exportConfiguration());

    console.log(configuration);
    this.drawerContent = JSON.parse(configuration);
  }
}