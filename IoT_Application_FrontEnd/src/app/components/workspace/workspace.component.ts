import { Component, OnInit } from '@angular/core';
import { ToggleService } from "../../services/toggle.service";
import { Router } from '@angular/router';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent {

  isDrawerOpened: boolean = false;

  constructor(private toggleService: ToggleService, private router: Router) {
  }

  // ngOnInit() {
  //   this.router.navigate(['/new/diagram']);
  // }


  sideBarToggler() {
    this.isDrawerOpened = !this.isDrawerOpened;
  }

  getDrawerOpen(): boolean {
    return this.toggleService.isDrawerOpened();
  }
}
