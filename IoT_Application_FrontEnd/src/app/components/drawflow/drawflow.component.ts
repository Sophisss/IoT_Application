import { Component, Input, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import Drawflow from 'drawflow';


@Component({
  selector: 'app-drawflow',
  templateUrl: './drawflow.component.html',
  styleUrls: ['./drawflow.component.scss']
})
export class DrawflowComponent implements OnInit {
  @Input()
  nodes!: any[];

  editor!: Drawflow;

  selectedNode: any = {};

  editDivHtml!: HTMLElement;

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
    this.addEditorEvents();

    // Gestisci l'evento "dragstart" sugli elementi trascinabili
    const dragElements = document.querySelectorAll('.drag-drawflow');
    dragElements.forEach((element) => {
      element.addEventListener('dragstart', (ev) => this.drag(ev));
    });

  }

  private addEditorEvents() {
    // Events!
    this.editor.on('nodeCreated', (id: any) => {
      console.log('Editor Event :>> Node created ' + id, this.editor.getNodeFromId(id));
    });

    this.editor.on('nodeMoved', (id: any) => {
      console.log('Editor Event :>> Node moved ' + id);
    });

    this.editor.on('nodeRemoved', (id: any) => {
      console.log('Editor Event :>> Node removed ' + id);
    });

    this.editor.on('nodeSelected', (id: any) => {
      console.log('Editor Event :>> Node selected ' + id, this.editor.getNodeFromId(id));
      this.selectedNode = this.editor.drawflow.drawflow.Home.data[`${id}`];
      console.log('Editor Event :>> Node selected :>> this.selectedNode :>> ', this.selectedNode);
      console.log('Editor Event :>> Node selected :>> this.selectedNode :>> ', this.selectedNode.data);
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
    const pos_x = ev.clientX;
    const pos_y = ev.clientY;
    console.log("data:" + data)
    this.addNodeToDrawFlow(data, pos_x, pos_y);
  }


  addNodeToDrawFlow(name: string, pos_x: number, pos_y: number) {
    console.log("sono dentro")
    console.log("posx: " + pos_x + "posy: " + pos_y)
    pos_x =
      pos_x * (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom)) -
      this.editor.precanvas.getBoundingClientRect().x *
      (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom));

    pos_y =
      pos_y * (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom)) -
      this.editor.precanvas.getBoundingClientRect().y *
      (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom));

    switch (name) {
      case 'entity':
        console.log("Switch case entity")
        const entityHtml = `
        <div>
          <div class="title-box"><i class="fab fa-entity "></i>Entity</div>
          <div class="box">
            <p>Enter entity name</p>
          <input type="text" df-name>
          </div>
        </div>
        `;
        console.log(entityHtml)
        this.editor.addNode(
          'entity',
          1,
          1,
          pos_x,
          pos_y,
          'entity',
          {},
          entityHtml,
          false
        );
        break;
      case 'table':
        const tableHtml = `
        <div>
          <div class="title-box"><i class="fab fa-table "></i>Table</div>
          <div class="box">
            <p>Enter table name</p>
          <input type="text" df-name>
          </div>
          <div class="box">
            <p>Enter partition key</p>
          <input type="text" df-pk>
          </div>
          <div class="box">
            <p>Enter sort key</p>
          <input type="text" df-sk>
          </div>
        </div>
        `;
        this.editor.addNode(
          'table',
          0,
          0,
          pos_x,
          pos_y,
          'table',
          {},
          tableHtml,
          false
        )
        break;
      default:
    }
  }


  export() {
    return this.editor.export();
  }

  clearModuleSelected() {
    this.editor.clear();
    console.log("Clear")
  }


}
