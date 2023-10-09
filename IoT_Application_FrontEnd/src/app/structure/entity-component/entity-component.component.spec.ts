import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EntityComponentComponent } from './entity-component.component';

describe('EntityComponentComponent', () => {
  let component: EntityComponentComponent;
  let fixture: ComponentFixture<EntityComponentComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [EntityComponentComponent]
    });
    fixture = TestBed.createComponent(EntityComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
