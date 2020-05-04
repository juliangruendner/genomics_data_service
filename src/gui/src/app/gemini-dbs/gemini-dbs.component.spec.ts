import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GeminiDbsComponent } from './gemini-dbs.component';

describe('GeminiDbsComponent', () => {
  let component: GeminiDbsComponent;
  let fixture: ComponentFixture<GeminiDbsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GeminiDbsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GeminiDbsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
