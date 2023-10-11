import { Component, OnInit } from '@angular/core';
import Drawflow from 'drawflow';

@Component({
  selector: 'app-drawflow',
  templateUrl: './drawflow.component.html',
  styleUrls: ['./drawflow.component.scss']
})
export class DrawflowComponent implements OnInit {

  editor!: Drawflow;

  mobile_item_selec = ''

  mobile_last_move = null

  ngOnInit(): void {
    try {
      const id = document.getElementById("drawflow") as HTMLElement;
      const element = document.getElementsByClassName('drag-drawflow');
      for (var i = 0; i < element.length; i++) {
        element[i].addEventListener('touchend', this.drop, false);
        element[i].addEventListener('touchmove', this.positionMobile, false);
        element[i].addEventListener('touchstart', this.drag, false);
      }
      this.editor = new Drawflow(id);
      this.editor.reroute = true
      this.editor.editor_mode = 'edit'
      this.editor.start();
      console.log("Connesso")
    } catch (exception) {
      console.error('Unable to start Drawflow', exception);
    }
  }

  positionMobile(ev: any) {
    this.mobile_last_move = ev;
  }

  allowDrop(ev: any) {
    ev.preventDefault();
  }

  drag(ev: any) {
    if (ev.type === "touchstart") {
      this.mobile_item_selec = ev.target.closest(".drag-drawflow").getAttribute('data-node');
    } else {
      ev.dataTransfer.setData("node", ev.target.getAttribute('data-node'));
    }
  }

  drop(){

  }

  /**
   * drop(ev: any){
    if (ev.type === "touchend") {
      var parentdrawflow = document.elementFromPoint(this.mobile_last_move.touches[0].clientX, this.mobile_last_move.touches[0].clientY).closest("#drawflow");
      if (parentdrawflow != null) {
        this.addNodeToDrawFlow(this.mobile_item_selec, this.mobile_last_move.touches[0].clientX, mobile_last_move.touches[0].clientY);
      }
      this.mobile_item_selec = '';
    } else {
      ev.preventDefault();
      var data = ev.dataTransfer.getData("node");
      this.addNodeToDrawFlow(data, ev.clientX, ev.clientY);
    }

  }
   * 
   */


  addNodeToDrawFlow(name: any, pos_x: any, pos_y: any) {
    pos_x = pos_x * (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom)) - (this.editor.precanvas.getBoundingClientRect().x * (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom)));
    pos_y = pos_y * (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom)) - (this.editor.precanvas.getBoundingClientRect().y * (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom)));

    switch (name) {
      case 'entity':
        this.editor.addNode(
          'entity',
          0,
          1,
          pos_x,
          pos_y,
          'entity',
          {},
          "html",
          ""
        );
        break;
      case 'link':
        this.editor.addNode
        break;
      case 'table':
        this.editor.addNode
        break;
      default : 
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
