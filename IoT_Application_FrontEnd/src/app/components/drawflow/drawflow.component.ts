import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import Drawflow from 'drawflow';
import { EntityComponent } from './entity/entity.component';


@Component({
  selector: 'app-drawflow',
  templateUrl: './drawflow.component.html',
  styleUrls: ['./drawflow.component.scss']
})
export class DrawflowComponent implements OnInit {

  editor!: Drawflow;

  entityComponent!: EntityComponent;


  ngOnInit(): void {
    try {
      this.initializeDrawflow();
      console.log("Connesso")
    } catch (exception) {
      console.error('Unable to start Drawflow', exception);
    }
  }

  initializeDrawflow() {
    const id = document.getElementById("drawflow") as HTMLElement;
    this.editor = new Drawflow(id);
    this.editor.reroute = true
    this.editor.editor_mode = 'edit'
    this.editor.start();

    // Gestisci l'evento "dragstart" sugli elementi trascinabili
    const dragElements = document.querySelectorAll('.drag-drawflow');
    dragElements.forEach((element) => {
      element.addEventListener('dragstart', (ev) => this.drag(ev));
    });

  }

  allowDrop(ev: any) {
    ev.preventDefault();
  }

  drag(ev: any) {
    console.log("drag")
      ev.dataTransfer.setData('node', ev.target.getAttribute('data-node'));
  }

  drop(ev: any) {
    console.log("drop")
      ev.preventDefault();
      const data = ev.dataTransfer.getData("node");
      console.log("data:" + data)
      this.addNodeToDrawFlow(data, ev.clientX, ev.clientY);
  }

  addNodeToDrawFlow(name: string, pos_x: number, pos_y: number) {
    console.log("sono dentro")
    console.log("name: " + name)
    pos_x = pos_x * (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom)) - (this.editor.precanvas.getBoundingClientRect().x * (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom)));
    pos_y = pos_y * (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom)) - (this.editor.precanvas.getBoundingClientRect().y * (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom)));

    switch (name) {
      case 'entity':
        console.log("Switch")
        const entityHtml = this.entityComponent.getHtmlContent();
        console.log(entityHtml)
        this.editor.addNode(
          'entity',
          0,
          1,
          pos_x,
          pos_y,
          'entity',
          {},
          entityHtml,
          false
        );
        break;
      case 'link':
        this.editor.addNode(
          'link',
          0,
          1,
          pos_x,
          pos_y,
          'link',
          {},
          "entityHtml",
          false
        )
        break;
      case 'table':
        this.editor.addNode(
          'table',
          0,
          1,
          pos_x,
          pos_y,
          'table',
          {},
          "entityHtml",
          false
        )
        break;
      default:
    }
  }
  
  
  export() {
    console.log("Export")
  }

  clearModuleSelected() {
    this.editor.clear();
    console.log("Clear")
  }


}
