import { Component, OnInit, ElementRef } from '@angular/core';
import {NgForm} from '@angular/forms';
import { ApiService } from  '../api.service';
import { Subscription } from 'rxjs';
import { ViewChild } from '@angular/core';

@Component({
  selector: 'app-load-vcf',
  templateUrl: './load-vcf.component.html',
  styleUrls: ['./load-vcf.component.scss']
})
export class LoadVcfComponent implements OnInit {
  vcf_file: File;
  sub: Subscription;
  inProgress: boolean = false;
  error: boolean = false;
  success: boolean = false;
  @ViewChild('f')
  f: NgForm;
  vcfs = [];

  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.initStuff();
    this.getVcfs();
  }

  initStuff(){
    this.sub = null;
    this.inProgress = false;
    this.error = false;
    this.success = false;
    this.f.resetForm();
  }

  onLoadIntoGemini(){
    this.error = false;
    this.success = false;
    this.inProgress = true;
    this.sub = this.apiService.loadVcfFile(this.f).subscribe((data: any) => {
      this.initStuff();
      this.success = true;
    }, error => {
      this.initStuff();
      this.error = true;
    });
  }

  cancel(){
    if(this.sub != null) {
      this.sub.unsubscribe();
      this.initStuff();
    }
  }

  getVcfs(){
    this.apiService.getVcfFiles().subscribe((data: any[] ) => {
      this.vcfs = data;
    });
  }
}
