import { Component, OnInit, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ApiService } from '../api.service';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-query',
  templateUrl: './query.component.html',
  styleUrls: ['./query.component.scss']
})
export class QueryComponent implements OnInit {

  @ViewChild('f')
  f: NgForm;

  data: any[] = [];
  max_index: number;
  keys: any;
  dbs = [];
  exec_query: any;
  skip: number = 50;
  limit: number = this.skip;
  index: number = 0;
  error: string = null;

  exampleQueries = [
    {desc: "Show entire variants table", query: "select *, gts, gt_types, gt_phases, gt_depths, gt_ref_depths, gt_alt_depths, gt_alt_freqs, gt_quals from variants"},
    {desc: "Apply filters on variants table", query: "select *, gts, gt_types, gt_phases, gt_depths, gt_ref_depths, gt_alt_depths, gt_alt_freqs, gt_quals from variants where filter is null and (impact_severity = 'HIGH' or impact_severity = 'MED' or (impact_severity = 'LOW' and impact not in ('stop_retained_variant', 'synonymous_variant', '5_prime_UTR_variant', '3_prime_UTR_variant', 'intron_variant', 'upstream_gene_variant', 'downstream_gene_variant', 'intergenic_variant', 'start_retained_variant', 'conserved_intron_variant', 'nc_transcript_variant', 'non_coding_exon_variant'))) and aaf_1kg_all <= 0.02"},
    {desc: "Extract the nucleotide diversity for each variant", query: "select chrom, start, end, pi from variants"},
    {desc: "Extract all loss-of-function variants with an alternate allele frequency < 1%", query: "select * from variants where is_lof = 1 and aaf >= 0.01"},
    {desc: "Extract all transitions with a call rate > 95%", query: "select * from variants where sub_type = 'ts' and call_rate >= 0.95"},
    {desc: "Report the genotype for all samples", query: "select chrom, start, end, ref, alt, gene, (gts).(*) from variants"},
    {desc: "Samples with an observed alignment depth of at least 20 reads", query: `"select chrom, start, end, ref, alt, gene, gt_depths from variants" --gt-filter "(gt_depths).(*).(>=20).(all)"`}
  ];

  closeResult: string;

  constructor(public apiService: ApiService, public modalService: NgbModal, public cd: ChangeDetectorRef) { }

  ngOnInit() {
    this.init_stuff();
    this.getGeminiDbs();
  }

  init_stuff() {
    this.data = [];
    this.max_index = 0;
    this.keys = null;
    this.exec_query = null;
    this.index = 0;
    this.error = null;
  }

  query() {
    this.apiService.query(this.f.value.db, this.f.value.query, this.index*this.skip, this.limit).subscribe((data: any) => {
      this.max_index = Math.ceil(data.count / this.limit);
      this.data = data.data;
      this.keys = Object.getOwnPropertyNames(this.data[0]);
      this.exec_query = this.query;
    }, error => {
      this.error = error.error.message.split(/\r?\n/)[0];
    });
  }

  query_variants() {
    this.apiService.query_variants(this.f.value.db, this.index*this.skip, this.limit).subscribe((data: any) => {
      this.max_index = Math.ceil(data.count / this.limit);
      this.data = data.data;
      this.keys = Object.getOwnPropertyNames(this.data[0]);
      this.exec_query = this.query_variants;
    }, error => {
      this.error = error.error.message.split(/\r?\n/)[0];
    });
  }

  getGeminiDbs() {
    this.apiService.getGeminiDbs().subscribe((data: any[] ) => {
      this.dbs = data;
    });
  }

  next_chunk() {
    if(this.exec_query) {
      this.index++;
      this.exec_query();
    }
  }

  prev_chunk() {
    if(this.index > 0 && this.exec_query) {
      this.index--;
      this.exec_query();
    } 
  }

  selectSampleQuery(q) {
    this.f.controls['query'].setValue(q.query);
    this.query();
  }

  open(content) {
    this.modalService.open(content, {windowClass: "queryExamplesModal", ariaLabelledBy: 'modal-basic-title'});
  }
}