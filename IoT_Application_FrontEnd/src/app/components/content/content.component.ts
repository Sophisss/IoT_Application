import {Component, OnDestroy, OnInit} from '@angular/core';
import {ToggleService} from "../../services/toggle.service";
import {DiagramNode} from "../../models/node.module";
import {Link} from "../../models/link.model";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss']
})
export class ContentComponent implements OnInit, OnDestroy {
  currentEmployee: string;
  selectedItem: DiagramNode | Link;
  itemType: string = 'table';

  private selectedItemSubscription: Subscription;

  constructor(private toggleService: ToggleService) {
  }

  ngOnInit(): void {
    this.selectedItemSubscription = this.toggleService.getSelectedItemObservable().subscribe((selectedItem) => {
      this.selectedItem = selectedItem;
      if (this.selectedItem) {
        if (this.selectedItem.type !== undefined) {
          console.log(this.selectedItem.type)
        } else {
          console.log('link')
        }
      }

      console.log("sel", this.selectedItem);
    });
  }

  closePopup(): void {
    this.toggleService.closePopup();
  }

  ngOnDestroy(): void {
    if (this.selectedItemSubscription) {
      this.selectedItemSubscription.unsubscribe();
    }
  }
}
