import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VcfsComponent } from './vcfs.component';

describe('VcfsComponent', () => {
  let component: VcfsComponent;
  let fixture: ComponentFixture<VcfsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VcfsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VcfsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
