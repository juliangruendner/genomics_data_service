import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LoadVcfComponent } from './load-vcf.component';

describe('LoadVcfComponent', () => {
  let component: LoadVcfComponent;
  let fixture: ComponentFixture<LoadVcfComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoadVcfComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoadVcfComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
