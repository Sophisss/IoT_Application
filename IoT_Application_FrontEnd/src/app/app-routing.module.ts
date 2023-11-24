import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomeComponent} from './old_stuff/pages/home/home.component';
import {BlankComponent} from './old_stuff/er-drawer/blank/blank.component';

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'drawer', component: BlankComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule {
}
