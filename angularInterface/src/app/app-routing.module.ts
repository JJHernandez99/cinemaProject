import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {AgregarSalaComponent} from './componentes/agregar-sala/agregar-sala.component';
import {SalasDetailComponent} from './componentes/salas-detail/salas-detail.component';
import {SalasListComponent} from './componentes/salas-list/salas-list.component';


const routes: Routes = [
  {path: '', redirectTo: '/api/salas', pathMatch: 'full'},
  {path: '/api/salas', component: SalasListComponent},
  {path: '/api/salas/:id', component: SalasDetailComponent},
  {path: 'add', component: AgregarSalaComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
