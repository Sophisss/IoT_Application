import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MaterialModule} from './material.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {StructureComponent} from './pages/Structure/structure.component';
import {FooterComponent} from './componentsHome/footer/footer.component';
import {HeaderHomeComponent} from './componentsHome/header-home/header-home.component';
import { HomeComponent } from './pages/home/home.component';
import { DragDropModule} from '@angular/cdk/drag-drop';
import { BlankComponent } from './er-drawer/blank/blank.component';
import { SidenavComponent } from './er-drawer/sidenav/sidenav.component'

@NgModule({
  declarations: [
    AppComponent,
    StructureComponent,
    FooterComponent,
    HeaderHomeComponent,
    HomeComponent,
    BlankComponent,
    SidenavComponent,
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
