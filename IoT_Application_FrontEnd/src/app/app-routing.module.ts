import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomepageComponent} from "./components/homepage/homepage.component";
import {WorkspaceComponent} from "./components/workspace/workspace.component";
import {ContentComponent} from "./components/content/content.component";

const routes: Routes = [
  {path: '', title: "Homepage", component: HomepageComponent},
  {path: 'new', title: "New Project", component: WorkspaceComponent, children: [
      {path: 'content', component: ContentComponent},
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule {
}
