import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppComponent} from './app.component';
import {HomepageComponent} from "./components/homepage/homepage.component";
import {HeaderComponent} from "./components/header/header.component";
import {WorkspaceComponent} from "./components/workspace/workspace.component";
import {DiagramComponent} from './components/diagram/diagram.component';

import {AppRoutingModule} from './app-routing.module';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {
  DxButtonModule,
  DxDiagramModule,
  DxDrawerModule,
  DxFormModule,
  DxPopupModule,
  DxTextBoxModule,
  DxToolbarModule,
  DxTooltipModule
} from "devextreme-angular";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {DrawerContentComponent} from './components/drawer-content/drawer-content.component';

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    HeaderComponent,
    WorkspaceComponent,
    DiagramComponent,
    DrawerContentComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    DxButtonModule,
    DxTooltipModule,
    DxToolbarModule,
    DxDrawerModule,
    DxDiagramModule,
    DxPopupModule,
    DxTextBoxModule,
    FormsModule,
    ReactiveFormsModule,
    DxFormModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
