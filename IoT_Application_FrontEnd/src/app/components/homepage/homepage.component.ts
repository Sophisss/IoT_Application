import {Component} from '@angular/core';
import {ImportServiceService} from "../../services/import-service.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent {
  descriptionText: string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean volutpat convallis sapien, vitae semper enim\n" +
    "      volutpat facilisis. Maecenas et lacus arcu. Mauris cursus eu risus nec iaculis. Integer a diam ut nisl luctus\n" +
    "      convallis vitae non metus. Suspendisse potenti. In in ipsum sem. Curabitur et mauris eget augue lacinia malesuada.\n" +
    "      Vivamus euismod neque convallis, maximus lacus at, semper sapien.Lorem ipsum dolor sit amet, consectetur\n" +
    "      adipiscing elit. Aenean volutpat convallis sapien, vitae semper enim volutpat facilisis. Maecenas et lacus arcu.\n" +
    "      Mauris cursus eu risus nec iaculis. Integer a diam ut nisl luctus convallis vitae non metus. Suspendisse potenti.\n" +
    "      In in ipsum sem.";

  constructor(private importService: ImportServiceService, private router: Router) {
  }

  /**
   * This method handles the import of a JSON file via the specified event.
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
