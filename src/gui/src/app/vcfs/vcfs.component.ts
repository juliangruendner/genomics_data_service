import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ApiService } from '../api.service';
import { NgForm } from '@angular/forms';
import { VcfFile } from '../../models/vcf_file';

@Component({
  selector: 'app-vcfs',
  templateUrl: './vcfs.component.html',
  styleUrls: ['./vcfs.component.scss']
})
export class VcfsComponent implements OnInit {
  vcfs: VcfFile[] = [];
  apiUrl: string;
  @ViewChild('vcfFile')
  vcfFileInput: ElementRef;
  vcfFiles: File[] = [];
  uploadInProgress: boolean = false;
  mergeInProgress: boolean = false;
  tools: string[] = ["bcf", "vcf"];
  filters: string[] = ["+", "x"];
  @ViewChild('f')
  f: NgForm;
  error: string = null;
  allChecked: boolean = false;

  constructor(public apiService: ApiService) { 
    this.apiUrl = this.apiService.API_URL;
  }

  public initStuff() {
    this.vcfFiles = [];
    this.vcfFileInput.nativeElement.value = "";
    this.uploadInProgress = false;
    this.mergeInProgress = false;
    this.error = null;
    this.f.resetForm();
    this.allChecked = false;
  }

  ngOnInit() {
    this.getVcfs();
  }
  
  getVcfs(){
    this.vcfs = [];
    this.apiService.getVcfFiles().subscribe((data: any[] ) => {
      for(var i: number = 0; i < data.length; i++) {
        this.vcfs.push(new VcfFile(data[i], false));
      }
    });
  }

  onChange(event: { srcElement: { files: File[]; }; }) {
    this.vcfFiles = [];
    for(let f of event.srcElement.files) {
      this.vcfFiles.push(f);
    }
  }

  onUpload(){
    this.uploadInProgress = true;
    this.apiService.uploadVcfFiles(this.vcfFiles).subscribe((data: any) => {
      this.getVcfs();
      this.initStuff();
    }, error => {
      this.getVcfs();
      this.initStuff();
      this.error = error.error.message;
    });
  }

  public merge() {
    this.mergeInProgress = true;
    var fileNames: string[] = [];
    for(let i: number = 0; i < this.vcfs.length; i++) {
      let f: VcfFile = this.vcfs[i];
      if(f.checked) {
        fileNames.push(f.name);
      }
    }
    this.apiService.merge(this.f.value.tool, this.f.value.filter, fileNames, this.f.value.output_file_name).subscribe((data: any) => {
      this.getVcfs();
      this.initStuff();
    }, error => {
      this.getVcfs();
      this.initStuff();
      this.error = error.error.message;
    });
  }

  public getCountChecked(): number {
    var ret: number = 0;
    for(var i: number = 0; i < this.vcfs.length; i++) {
      if(this.vcfs[i].checked) {
        ret++;
      }
    }
    return ret;
  }

  public onAllChecked() {
    let notAllChecked: boolean = !this.allChecked;
    for(let i: number = 0; i < this.vcfs.length; i++) {
      this.vcfs[i].checked = notAllChecked;
    }
  }
}
