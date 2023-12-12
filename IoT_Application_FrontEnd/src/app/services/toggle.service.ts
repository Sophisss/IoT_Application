import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ToggleService {
  isDrawerOpen: boolean = false;

  toggleDrawer(): void {
    this.isDrawerOpen = !this.isDrawerOpen;
  }

  isDrawerOpened(): boolean {
    return this.isDrawerOpen;
  }
}
