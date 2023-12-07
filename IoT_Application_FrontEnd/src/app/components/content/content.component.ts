import {Component} from '@angular/core';
import {ToggleService} from "../../services/toggle.service";

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss']
})
export class ContentComponent {
  currentEmployee: string;

  constructor(private toggleService: ToggleService) {
  }

  closePopup(): void {
    this.toggleService.closePopup();
    console.log(this.currentEmployee)
  }
}
