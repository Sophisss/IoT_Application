import { Component, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-entity',
  templateUrl: './entity.component.html',
  styleUrls: ['./entity.component.scss']
})
export class EntityComponent {
  @ViewChild('entity')
  entityElement!: ElementRef;

  getHtmlContent(): string {
    // Accedi all'elemento HTML utilizzando this.entityElement.nativeElement
    return this.entityElement.nativeElement.innerHTML;
  }


}
