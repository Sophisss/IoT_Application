import {Component} from '@angular/core';
import {SidenavService} from "../../services/sidenav.service";
import {WorkspaceComponent} from "../workspace/workspace.component";

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss']
})
export class ContentComponent {


  constructor(private workspace: WorkspaceComponent) {
  }

  helloWorld() {
    console.log("hello")
  }

  openClose() {
    this.workspace.setToggleSidebar()
    console.log(this.workspace.getToggleSidebar())
  }
}
