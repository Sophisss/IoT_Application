import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrl: './sidenav.component.scss'
})
export class SidenavComponent {
  @Output() toggleSidebarForMe: EventEmitter<any> = new EventEmitter();

  navigation: any[] = [
    { id: 1, text: "Diagram", icon: "mediumiconslayout", path: "new/diagram" },
    { id: 2, text: "IoT Rules", icon: "edit", path: "new/rules" }
  ];

  constructor(private _router: Router) { }

  itemClick(e: any) {
    const destination = e.itemData.path;
    this._router.navigateByUrl(destination);
  }

  click() {
    this.toggleSidebarForMe.emit();
  }
}
