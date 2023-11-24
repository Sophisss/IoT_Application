import {Component} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {Router} from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  openDialog = false

  constructor(private router: Router,
              public dialog: MatDialog) {
  }


  open() {
    this.openDialog = true
  }

  changeRoute(route: string) {
    if (route === '/drawer') {
      this.router.navigate(['/drawer']);
    }
  }

  onNoClick(): void {
    this.openDialog = false
  }
}
