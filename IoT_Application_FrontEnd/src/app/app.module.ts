import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MaterialModule} from './material.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {StructureComponent} from './components/pages/Structure/structure.component';
import {FooterComponent} from './componentsHome/footer/footer.component';
import {HeaderHomeComponent} from './componentsHome/header-home/header-home.component';
import { HomeComponent } from './components/pages/home/home.component';
import { DrawflowComponent } from './components/drawflow/drawflow.component';
import { EntityComponent } from './components/drawflow/entity/entity.component';
import { TableComponent } from './components/drawflow/table/table.component';
import { DragDropModule} from '@angular/cdk/drag-drop'

@NgModule({
  declarations: [
    AppComponent,
    StructureComponent,
    FooterComponent,
    HeaderHomeComponent,
    HomeComponent,
    DrawflowComponent,
    EntityComponent,
    TableComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    HttpClientModule,
    DragDropModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
