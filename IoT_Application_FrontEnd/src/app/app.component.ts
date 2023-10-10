import {Component, OnInit} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'IoT_Application_FrontEnd';

  showStructurForm = true

  /**
   * Constructor for AppComponent.
   * @param router the Router module.
   */
  constructor(
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        if (event.url === '')
          this.showStructurForm = true;
      } else {
        this.showStructurForm = false;
      }
    })
  }
}
