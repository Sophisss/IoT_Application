import {Component} from '@angular/core';
import {ImportServiceService} from "../../services/import-service.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent {
  descriptionText: string = "Drag, drop and customize your entities or tables, monitoring in real time" +
    " the produced JSON file.\nWhen you are satisfied with the result, you can save the file to your device" +
    " to start over whenever you want or generate an URL from which to download the generated code for your" +
    " IoT system with the related apps.";

  constructor(private importService: ImportServiceService, private router: Router) {
  }

  /**
   * This method handles the import of a JSON file via the specified event and redirects to the diagram component.
   * @param event file input event that contains the selected file.
   */
  import(event: Event) {
    this.importService.onFileSelected(event)
      .then((jsonContent) => {
        this.importService.pushToConfiguration(jsonContent);
      })
      .then(() => {
        this.router.navigate(['/new']);
      })
      .catch((error) => {
        alert(error);
      });
  }
}
