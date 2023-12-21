import {Component, OnDestroy, OnInit} from '@angular/core';
import {ConfigurationService} from "../../services/configuration.service";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-drawer-content',
  templateUrl: './drawer-content.component.html',
  styleUrls: ['./drawer-content.component.scss']
})
export class DrawerContentComponent implements OnInit, OnDestroy {
  drawerContent: any;
  private updateContentSubscription: Subscription;

  constructor(private configService: ConfigurationService) {
  }

  ngOnInit() {
    this.updateContentSubscription = this.configService.updateSignal$.subscribe(() => {
      this.updateContent();
    });
  }

  updateContent() {
    let configuration = JSON.stringify(this.configService.exportConfiguration());
    this.drawerContent = JSON.parse(configuration);
    //console.log(this.drawerContent);
  }

  ngOnDestroy() {
    this.updateContentSubscription.unsubscribe();
  }
}