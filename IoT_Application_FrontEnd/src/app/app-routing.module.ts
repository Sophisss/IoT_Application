import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {StructureComponent} from './components/pages/Structure/structure.component';
import { HomeComponent } from './components/pages/home/home.component';
import { DrawflowComponent } from './components/drawflow/drawflow.component';

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'structure', component: DrawflowComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule {
}
