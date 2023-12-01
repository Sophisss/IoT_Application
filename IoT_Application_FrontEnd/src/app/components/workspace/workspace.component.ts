import {Component} from '@angular/core';
import {SideDrawerService} from "../../services/side-drawer.service";

@Component({
    selector: 'app-workspace',
    templateUrl: './workspace.component.html',
    styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent {
    constructor(private drawerService: SideDrawerService) {
    }

    getDrawerOpen(): boolean {
        return this.drawerService.isDrawerOpened();
    }
}
