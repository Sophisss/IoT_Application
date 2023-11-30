import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppComponent} from './app.component';
import {HomepageComponent} from "./components/homepage/homepage.component";
import {HeaderComponent} from "./components/header/header.component";
import {WorkspaceComponent} from "./components/workspace/workspace.component";
import {ContentComponent} from './components/content/content.component';
import {DiagramComponent} from './components/diagram/diagram.component';

import {MaterialModule} from "./material.module";
import {AppRoutingModule} from './app-routing.module';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatButtonModule} from "@angular/material/button";
import {MatTooltipModule} from "@angular/material/tooltip";
import {MatIconModule} from "@angular/material/icon";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatListModule} from "@angular/material/list";
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatTableModule} from "@angular/material/table";
import {
    DxButtonModule,
    DxDiagramModule,
    DxFileUploaderModule,
    DxPopupModule,
    DxToolbarModule
} from "devextreme-angular";
import {HttpClientModule} from "@angular/common/http";

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    HeaderComponent,
    WorkspaceComponent,
    ContentComponent,
    DiagramComponent
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        MatFormFieldModule,
        FormsModule,
        ReactiveFormsModule,
        MatInputModule,
        MatButtonModule,
        MatSidenavModule,
        MatListModule,
        MatToolbarModule,
        MatIconModule,
        MatTableModule,
        MatTooltipModule,
        MaterialModule,
        DxButtonModule,
        DxDiagramModule,
        DxFileUploaderModule,
        HttpClientModule,
        DxPopupModule,
        DxToolbarModule
    ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
