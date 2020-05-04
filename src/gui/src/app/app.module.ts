import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { LoadVcfComponent } from './load-vcf/load-vcf.component';
import { HomeComponent } from './home/home.component';
import { HttpClientModule } from '@angular/common/http';
import { GeminiDbsComponent } from './gemini-dbs/gemini-dbs.component';
import { FormsModule } from '@angular/forms';
import { QueryComponent } from './query/query.component';
import { VcfsComponent } from './vcfs/vcfs.component';


@NgModule({
  declarations: [
    AppComponent,
    LoadVcfComponent,
    HomeComponent,
    GeminiDbsComponent,
    QueryComponent,
    VcfsComponent
  ],
  imports: [
    BrowserModule,
    NgbModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
