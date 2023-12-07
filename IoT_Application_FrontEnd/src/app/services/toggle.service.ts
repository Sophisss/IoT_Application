import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ToggleService {
  isDrawerOpen: boolean = false;

  isPopupOpen: boolean = false;
  selectedItem: any;

  toggleDrawer(): void {
    this.isDrawerOpen = !this.isDrawerOpen;
  }

  isDrawerOpened(): boolean {
    return this.isDrawerOpen;
  }

  openPopup(event: any): void {
    this.isPopupOpen = true;
    this.selectedItem = event.item;
    console.log(event)
  }

  closePopup(): void {
    this.isPopupOpen = false;
  }

  isPopupOpened(): boolean {
    return this.isPopupOpen;
  }
}
