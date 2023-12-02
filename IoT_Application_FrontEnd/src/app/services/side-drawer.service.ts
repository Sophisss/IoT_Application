import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SideDrawerService {
  isDrawerOpen = false;

  toggleDrawer(): void {
    this.isDrawerOpen = !this.isDrawerOpen;
  }

  isDrawerOpened(): boolean {
    return this.isDrawerOpen;
  }
}
