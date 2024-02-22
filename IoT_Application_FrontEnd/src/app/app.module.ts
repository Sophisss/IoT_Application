import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HomepageComponent } from "./components/homepage/homepage.component";
import { HeaderComponent } from "./components/header/header.component";
import { WorkspaceComponent } from "./components/workspace/workspace.component";
import { DiagramComponent } from './components/diagram/diagram.component';
import { RulesComponent } from './components/rules/rules.component';
import { SidenavComponent } from './components/sidenav/sidenav.component';
import { ProvaComponent } from './components/prova/prova.component';

import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {
  DxBoxModule,
  DxButtonModule,
  DxCheckBoxModule,
  DxDataGridModule,
  DxDiagramModule,
  DxDrawerModule,
  DxFormModule,
  DxNumberBoxModule,
  DxPopupModule,
  DxRadioGroupModule,
  DxSelectBoxModule,
  DxTextBoxModule,
  DxToolbarModule,
  DxTooltipModule,
  DxListModule,
  DxTabPanelModule,
  DxValidatorModule,
  DxValidationSummaryModule,
  DxValidationGroupModule,
  DxToastModule,
  DxResizableModule
} from "devextreme-angular";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { DrawerContentComponent } from './components/drawer-content/drawer-content.component';
import { HttpClientModule } from '@angular/common/http';
import { JsonPipe, TitleCasePipe } from "@angular/common";
import { Clipboard } from "@angular/cdk/clipboard";

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    HeaderComponent,
    WorkspaceComponent,
    DiagramComponent,
    DrawerContentComponent,
    RulesComponent,
    SidenavComponent,
    ProvaComponent
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
    DxFormModule,
    DxRadioGroupModule,
    DxBoxModule,
    DxNumberBoxModule,
    DxSelectBoxModule,
    DxCheckBoxModule,
    HttpClientModule,
    DxDataGridModule,
    DxListModule,
    DxTabPanelModule,
    DxValidatorModule,
    DxValidationSummaryModule,
    DxValidationGroupModule,
    DxToastModule,
    DxResizableModule
  ],
  providers: [
    JsonPipe,
    TitleCasePipe,
    Clipboard
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
