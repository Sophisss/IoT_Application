import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrl: './sidenav.component.scss'
})
export class SidenavComponent {
  @Output() toggleSidebarForMe: EventEmitter<any> = new EventEmitter();

  navigation: any[] = [
    { id: 1, text: "Diagram", icon: "mediumiconslayout", path: "new" },
    { id: 2, text: "IoT Rules", icon: "edit", path: "new/rules" }
];

toggleSidebar() {
  this.toggleSidebarForMe.emit();
}

}
