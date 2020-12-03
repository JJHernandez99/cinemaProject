import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AgregarSalaComponent } from './componentes/agregar-sala/agregar-sala.component';
import { SalasListComponent } from './componentes/salas-list/salas-list.component';
import { SalasDetailComponent } from './componentes/salas-detail/salas-detail.component';

import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    AgregarSalaComponent,
    SalasListComponent,
    SalasDetailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
