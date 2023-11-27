import {Component} from '@angular/core';
import {Router} from "@angular/router";
import {ImportServiceService} from "../../old_stuff/Services/Import_Json/import-service.service";

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

  constructor(private router: Router, private importService: ImportServiceService,) {

  }

  import(event: Event) {
    this.importService.onFileSelected(event)
      .then((jsonContent) => {
        this.convertToDiagram(jsonContent);
      })
      .catch((error) => {
        alert(error);
      });
  }

  private convertToDiagram(jsonContent: unknown) {

  }
}
