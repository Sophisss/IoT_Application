import {Component} from '@angular/core';
import {ConfigurationService} from "../../services/configuration.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  isModifiable: boolean = false;

  constructor(protected configurationService: ConfigurationService) {
  }
}
