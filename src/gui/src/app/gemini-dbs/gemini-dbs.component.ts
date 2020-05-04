import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-gemini-dbs',
  templateUrl: './gemini-dbs.component.html',
  styleUrls: ['./gemini-dbs.component.scss']
})
export class GeminiDbsComponent implements OnInit {
  dbs = [];
  apiUrl: String;

  constructor(public apiService: ApiService) {
    this.apiUrl = this.apiService.API_URL;
  }

  ngOnInit() {
    this.getGeminiDbs();
  }

  getGeminiDbs(){
    this.apiService.getGeminiDbs().subscribe((data: any[] ) => {
      this.dbs = data;
    });
  }

}
