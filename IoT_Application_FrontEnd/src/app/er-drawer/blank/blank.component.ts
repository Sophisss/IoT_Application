import { Component } from '@angular/core';
import Drawflow from 'drawflow';
import { GeneratorService } from 'src/app/Services/Generator/generator.service';

@Component({
  selector: 'app-blank',
  templateUrl: './blank.component.html',
  styleUrls: ['./blank.component.scss']
})
export class BlankComponent {

  editor!: Drawflow;

  selectedNode: any = {};

  sideBarOpen = true;

  constructor(private generatorService: GeneratorService) { }

  ngOnInit(): void {
    this.initializeDrawflow();
  }

  initializeDrawflow() {
    const id = document.getElementById("drawflow") as HTMLElement;
    this.editor = new Drawflow(id);
    this.editor.reroute = true
    this.editor.editor_mode = 'edit'
    this.editor.start();
    this.addEditorEvents();

    //TODO rivedi
    const dragElements = document.querySelectorAll('.drag-drawflow');
    dragElements.forEach((element) => {
      element.addEventListener('dragstart', (ev) => this.drag(ev));
    });

  }

  addEditorEvents() {
    //TODO rivedi creazione
    this.editor.on('nodeCreated', (id: any) => {
      console.log('Editor Event :>> Node created ' + id, this.editor.getNodeFromId(id));
    });

    this.editor.on('nodeRemoved', (id: number) => {
      console.log('Node removed ' + id);
      this.removeNode(id);
    });

    this.editor.on('connectionCreated', (connection) => {
      console.log('Connection created');
      this.addLink(connection)
    })

    this.editor.on('connectionRemoved', (connection: any) => {
      console.log('Connection removed ', connection);
      this.removeLink(connection.output_id, connection.input_id)
    });

    this.editor.on('nodeSelected', (id: any) => {
      this.selectedNode = this.editor.drawflow.drawflow.Home.data[`${id}`];
    });
  }

  removeNode(id: number) {
    this.generatorService.removeObject(id, this.selectedNode.class)
  }

  addLink(connection: any) {
    const first = this.editor.getNodeFromId(connection.output_id)
    const second = this.editor.getNodeFromId(connection.input_id)
    this.generatorService.saveLink(first.id, second.id)
  }


  removeLink(first_entity: string, second_entity: string){
    this.generatorService.removeLink(first_entity, second_entity)
  }

  addObjectRelativeClassNode(id: number | string) {
    const node = this.editor.getNodeFromId(id)
    if(node.class == 'Entity'){
      this.generatorService.saveEntity(node.id, node.name)
    }
    else if (node.class == 'Table') {
      this.generatorService.saveTable(node.id, node.name)
    }
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
        const entity_id = this.editor.addNode(
          name,
          1,
          1,
          pos_x,
          pos_y,
          'Entity',
          {},
          entityHtml,
          false
        );
        this.addObjectRelativeClassNode(entity_id)
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
        const table_id = this.editor.addNode(
          'IoT',
          1,
          0,
          pos_x,
          pos_y,
          'Table',
          {},
          tableHtml,
          false
        )
        this.addObjectRelativeClassNode(table_id)
        break;
      default:
    }
  }

  import() {
    console.log("import")
  }


  export() {
    this.generatorService.export()
    console.log("Export")
  }

  clearModuleSelected() {
    this.generatorService.clear();
    this.editor.clear();
  }

}
