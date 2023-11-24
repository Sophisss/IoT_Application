import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MaterialModule} from './material.module';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {StructureComponent} from './pages/Structure/structure.component';
import {FooterComponent} from './componentsHome/footer/footer.component';
import {HeaderHomeComponent} from './componentsHome/header-home/header-home.component';
import {HomeComponent} from './pages/home/home.component';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {BlankComponent} from './er-drawer/blank/blank.component';
import {SidenavComponent} from './er-drawer/sidenav/sidenav.component';
import {EntityComponent} from './er-drawer/components/entity/entity.component';
import {TableComponent} from './er-drawer/components/table/table.component';
import {DialogContentComponent} from './er-drawer/mat_dialog/dialog-content/dialog-content.component';
import {DialogEntityComponent} from './er-drawer/mat_dialog/dialog-entity/dialog-entity.component';
import {DialogTableComponent} from './er-drawer/mat_dialog/dialog-table/dialog-table.component';
import {DialogLinkComponent} from './er-drawer/mat_dialog/dialog-link/dialog-link.component';
import {DialogExportComponent} from './er-drawer/mat_dialog/dialog-export/dialog-export.component';

@NgModule({
  declarations: [
    AppComponent,
    StructureComponent,
    FooterComponent,
    HeaderHomeComponent,
    HomeComponent,
    BlankComponent,
    SidenavComponent,
    EntityComponent,
    TableComponent,
    DialogContentComponent,
    DialogEntityComponent,
    DialogTableComponent,
    DialogLinkComponent,
    DialogExportComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    DragDropModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
