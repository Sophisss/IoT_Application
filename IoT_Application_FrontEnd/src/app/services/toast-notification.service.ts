import {Injectable} from '@angular/core';
import notify from "devextreme/ui/notify";

@Injectable({
  providedIn: 'root'
})
export class ToastNotificationService {


  displayToast(message: string, width: number, container: string, type: 'error' | 'info' | 'success' | 'warning',
               time: number) {
    notify(
      {
        message,
        width: width,
        position: {
          at: "bottom",
          my: "bottom",
          offset: "0 -10",
          of: container
        }
      },
      type,
      time
    );
  }
}
