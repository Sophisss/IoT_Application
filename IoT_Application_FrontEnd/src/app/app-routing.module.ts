import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomepageComponent} from "./components/homepage/homepage.component";
import {WorkspaceComponent} from "./components/workspace/workspace.component";
import { RulesComponent } from './components/rules/rules.component';
import { DiagramComponent } from './components/diagram/diagram.component';

const routes: Routes = [
  {path: '', title: "Homepage", component: HomepageComponent},
  {path: 'new', title: "Diagram", component: WorkspaceComponent,
    children: [
      {path: 'rules', component: RulesComponent}
      ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
