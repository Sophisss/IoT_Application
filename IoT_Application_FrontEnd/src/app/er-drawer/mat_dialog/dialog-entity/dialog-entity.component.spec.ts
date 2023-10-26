import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogEntityComponent } from './dialog-entity.component';

describe('DialogEntityComponent', () => {
  let component: DialogEntityComponent;
  let fixture: ComponentFixture<DialogEntityComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DialogEntityComponent]
    });
    fixture = TestBed.createComponent(DialogEntityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
