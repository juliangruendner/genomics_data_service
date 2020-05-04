import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoadVcfComponent } from './load-vcf/load-vcf.component';
import { HomeComponent } from './home/home.component';
import { GeminiDbsComponent } from './gemini-dbs/gemini-dbs.component';
import { QueryComponent } from './query/query.component';
import { VcfsComponent } from './vcfs/vcfs.component';

const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'gemini-dbs',
    component: GeminiDbsComponent
  },
  {
    path: 'query',
    component: QueryComponent
  },
  {
      path: 'load-vcf',
      component: LoadVcfComponent
  },
  {
    path: 'vcfs',
    component: VcfsComponent
},
  {
      path: '',
      redirectTo: '/home',
      pathMatch: 'full'
  },
  {
      path: '**',
      redirectTo: '/home',
      pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
