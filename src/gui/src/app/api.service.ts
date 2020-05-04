import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from  '@angular/common/http';
import { NgForm } from '@angular/forms';
import {environment} from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  API_URL = environment.apiUrl;
  constructor(private  httpClient:  HttpClient) {}

  getGeminiDbs(){
    return this.httpClient.get(`${this.API_URL}/gemini/dbs`);
  }

  getVcfFiles(){
    return this.httpClient.get(`${this.API_URL}/gemini/vcfs`);
  }

  loadVcfFile(f: NgForm) {
    return this.httpClient.post(`${this.API_URL}/gemini/import_vcf?db_name=` + f.value.db_name + `&vcf_file=` + f.value.vcf, {});
  }

  uploadVcfFiles(vcfFiles: File[]) {
    let header: HttpHeaders = new HttpHeaders();
    header.append('Content-Type', 'application/x-www-form-urlencoded');
    let options = { headers: header };
    let data: FormData = new FormData();
    for(let f of vcfFiles) {
      data.append('files', f);
    }
    return this.httpClient.post(`${this.API_URL}/gemini/upload_vcf`, data, options);
  }

  query(db_name: string, query: string, skip: number, limit: number) {
    return this.httpClient.post(`${this.API_URL}/gemini/query`, {"db_name": db_name, "query": query, "skip": skip, "limit": limit});
  }

  query_variants(db_name: string, skip: number, limit: number) {
    return this.httpClient.post(`${this.API_URL}/gemini/query/variants`, {"db_name": db_name, "skip": skip, "limit": limit});
  }
  
  merge(tool: string, filter_option: string, file_names: string[], output_file_name: string) {
    return this.httpClient.post(`${this.API_URL}/gemini/vcfs/merge`, {"tool": tool, "filter_option": filter_option, "file_names": file_names, "output_file_name": output_file_name});
  }
}
