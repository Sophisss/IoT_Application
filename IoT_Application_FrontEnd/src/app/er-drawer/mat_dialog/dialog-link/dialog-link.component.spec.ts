import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogLinkComponent } from './dialog-link.component';

describe('DialogLinkComponent', () => {
  let component: DialogLinkComponent;
  let fixture: ComponentFixture<DialogLinkComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DialogLinkComponent]
    });
    fixture = TestBed.createComponent(DialogLinkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
