import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StructureComponent } from './structure/structure.component';
import { EntityComponentComponent } from './structure/entity-component/entity-component.component';

const routes: Routes = [
{ path: '', component: StructureComponent },
{ path: 'add_entity', component: EntityComponentComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
