import { Component, OnInit } from '@angular/core';
import Drawflow from 'drawflow';
import { EntityComponent } from './entity/entity.component';


@Component({
  selector: 'app-drawflow',
  templateUrl: './drawflow.component.html',
  styleUrls: ['./drawflow.component.scss']
})
export class DrawflowComponent implements OnInit {

  editor!: Drawflow;

  mobile_item_selec = ''

  mobile_last_move: any

  constructor(private entityComponent: EntityComponent){

  }


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
      ev.dataTransfer.setData('node', ev.target.getAttribute('data-node'));
  }

  drop(ev: any) {
      ev.preventDefault();
      const data = ev.dataTransfer.getData("node");
      this.addNodeToDrawFlow(data, ev.clientX, ev.clientY);
  }

  addNodeToDrawFlow(name: string, pos_x: number, pos_y: number) {
    pos_x = pos_x * (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom)) - (this.editor.precanvas.getBoundingClientRect().x * (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom)));
    pos_y = pos_y * (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom)) - (this.editor.precanvas.getBoundingClientRect().y * (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom)));

    switch (name) {
      case 'entity':
        const entityHtml = this.entityComponent.getHtmlContent()
        this.editor.addNode(
          'entity',
          0,
          1,
          pos_x,
          pos_y,
          'entity',
          {},
          entityHtml,
          ""
        );
        break;
      case 'link':
        this.editor.addNode
        break;
      case 'table':
        this.editor.addNode
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
