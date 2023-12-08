import {Injectable} from '@angular/core';
import {BehaviorSubject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ToggleService {
  isDrawerOpen: boolean = false;

  isPopupOpen: boolean = false;
  selectedItem = new BehaviorSubject<any>(null);

  toggleDrawer(): void {
    this.isDrawerOpen = !this.isDrawerOpen;
  }

  isDrawerOpened(): boolean {
    return this.isDrawerOpen;
  }

  openPopup(event: any): void {
    this.isPopupOpen = true;
    this.selectedItem.next(event.item);
  }

  closePopup(): void {
    this.isPopupOpen = false;
    this.selectedItem.next(null);
  }

  isPopupOpened(): boolean {
    return this.isPopupOpen;
  }

  getSelectedItemObservable() {
    return this.selectedItem.asObservable();
  }
}
