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
  private selectedItemSubscription: Subscription;

  constructor(private toggleService: ToggleService) {
  }

  ngOnInit(): void {
    this.selectedItemSubscription = this.toggleService.getSelectedItemObservable().subscribe((selectedItem) => {
      this.selectedItem = selectedItem;
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
