import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalasDetailComponent } from './salas-detail.component';

describe('SalasDetailComponent', () => {
  let component: SalasDetailComponent;
  let fixture: ComponentFixture<SalasDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SalasDetailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SalasDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
