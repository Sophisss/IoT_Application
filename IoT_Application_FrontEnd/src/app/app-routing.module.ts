import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { BlankComponent } from './er-drawer/blank/blank.component';
import { ProvaComponent } from './er-drawer/prova/prova.component';

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'drawer', component: ProvaComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule {
}
