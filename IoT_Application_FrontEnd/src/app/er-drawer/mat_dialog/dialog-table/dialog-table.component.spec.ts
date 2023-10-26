import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogTableComponent } from './dialog-table.component';

describe('DialogTableComponent', () => {
  let component: DialogTableComponent;
  let fixture: ComponentFixture<DialogTableComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DialogTableComponent]
    });
    fixture = TestBed.createComponent(DialogTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
