import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ToggleService {
  isDrawerOpen: boolean = false;

  /**
   * Toggles the drawer.
   */
  toggleDrawer(): void {
    this.isDrawerOpen = !this.isDrawerOpen;
  }

  isDrawerOpened(): boolean {
    return this.isDrawerOpen;
  }
}
