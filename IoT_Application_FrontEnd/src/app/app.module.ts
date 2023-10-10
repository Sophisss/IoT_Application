import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MaterialModule} from './material.module';
import {ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {NgxGraphModule} from '@swimlane/ngx-graph';
import {StructureComponent} from './Structure/structure.component';
import {FooterComponent} from './componentsHome/footer/footer.component';
import {HeaderHomeComponent} from './componentsHome/header-home/header-home.component';

@NgModule({
  declarations: [
    AppComponent,
    StructureComponent,
    FooterComponent,
    HeaderHomeComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    ReactiveFormsModule,
    HttpClientModule,
    NgxGraphModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
