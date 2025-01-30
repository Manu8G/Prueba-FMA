import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CrearTareaComponent } from './crear-tarea.component';

describe('CrearTareaComponent', () => {
  let component: CrearTareaComponent;
  let fixture: ComponentFixture<CrearTareaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CrearTareaComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CrearTareaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
