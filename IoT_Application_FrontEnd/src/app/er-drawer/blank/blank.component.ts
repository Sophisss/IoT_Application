import { Component } from '@angular/core';
import Drawflow from 'drawflow';
import { GeneratorService } from 'src/app/Services/Generator/generator.service';

@Component({
  selector: 'app-blank',
  templateUrl: './blank.component.html',
  styleUrls: ['./blank.component.scss']
})
/**
 * This class represents my canvas.
 */
export class BlankComponent {

  /**
   * Variable representing an instance of the Drawflow editor.
   */
  editor!: Drawflow;

  /**
   * Variable that tracks the selected node in the Drawflow editor.
   */
  selectedNode: any = {};

  sideBarOpen = true;

  /**
   * Constructor for this Component.
   * @param generatorService service to generate JSON configuration.
   */
  constructor(
    private generatorService: GeneratorService
  ) { }

  ngOnInit(): void {
    this.initializeDrawflow();
  }

  /**
   * This method initializes the Drawflow editor.
   */
  initializeDrawflow() {
    const id = document.getElementById("drawflow") as HTMLElement;
    this.editor = new Drawflow(id);
    this.editor.reroute = true
    this.editor.editor_mode = 'edit'
    this.editor.start();
    this.addEditorEvents();
    this.dragstart()
  }

  /**
   * This method handles the dragstart event on elements with class .drag-drawflow.
   * It is used to attach an event handler to draggable elements.
   */
  dragstart() {
    const dragElements = document.querySelectorAll('.drag-drawflow');
    dragElements.forEach((element) => {
      element.addEventListener('dragstart', (ev) => this.drag(ev));
    });
  }

  /**
   * Log Drawflow editor events to handle user interactions
   * inside the editor.
   */
  addEditorEvents() {
    this.editor.on('nodeCreated', (id: any) => {
      console.log('Node created ' + id)
      this.addObjectRelativeClassNode(id)
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

    this.editor.on('click', (e: any) => {
      console.log('Click :', e);
    });
  }

  /**
   * Removes a node from the Drawflow editor 
   * and calls the generator service to remove the associated object.
   * @param id node id to remove.
   */
  removeNode(id: number) {
    this.generatorService.removeObject(id, this.selectedNode.class)
  }

  /**
   * Adds a connection between two nodes in the Drawflow editor and saves this connection.
   * @param connection object representing the connection between nodes.
   */
  addLink(connection: any) {
    const first = this.editor.getNodeFromId(connection.output_id)
    const second = this.editor.getNodeFromId(connection.input_id)
    this.generatorService.saveLink(first.id, second.id)
  }

  /**
   * Removes a connection between two entities from the Drawflow editor 
   * and removes the associated link.
   * @param first_entity first entity id to remove.
   * @param second_entity second entity id to remove.
   */
  removeLink(first_entity: string, second_entity: string) {
    this.generatorService.removeLink(first_entity, second_entity)
  }


  /**
   * This method adds an object associated with a Drawflow editor node,
   * based on the node class, and saves this object.
   * @param id node id from which to obtain the associated node.
   */
  addObjectRelativeClassNode(id: number | string) {
    const node = this.editor.getNodeFromId(id)
    if (node.class == 'Entity') {
      this.generatorService.saveEntity(node.id, node.name)
    }
    else if (node.class == 'Table') {
      this.generatorService.saveTable(node.id, node.name)
    }
  }

  /**
   * This method allows the release of an object
   * dragged to a specific area.
   * @param ev the "drag-and-drop" event to handle.
   */
  allowDrop(ev: any) {
    ev.preventDefault();
  }

  /**
   * This method handles the start of the "drag" operation when an element is dragged.
   * @param ev drag event to handle.
   */
  drag(ev: any) {
    ev.dataTransfer.setData('node', ev.target.getAttribute('data-node'));
  }

  /**
   * This method handles the drop event when an object is dropped in a specific area.
   * @param ev drop event to handle.
   */
  drop(ev: any) {
    ev.preventDefault();
    const data = ev.dataTransfer.getData("node");
    this.addNodeToDrawFlow(data, ev.clientX, ev.clientY);
  }

  /**
   * This method adds a new node to the Drawflow editor 
   * based on specific parameters such as position.
   * @param name name that identifies which object to add.
   * @param pos_x the x coordinate of the node position.
   * @param pos_y the y coordinate of the node position.
   */
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
        this.editor.addNode(name, 1, 1, pos_x, pos_y, 'Entity', {}, entityHtml, false);
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
        this.editor.addNode('IoT', 0, 0, pos_x, pos_y, 'Table', {}, tableHtml, false);
        break;
      default:
    }
  }

  /**
   * This method import a configuration.
   */
  import() {
    console.log("import")
  }

  /**
   * This method exports the project.
   */
  export() {
    this.generatorService.export()
    console.log("Export")
  }

  /**
   * This method clears all contents from the Drawflow editor.
   */
  clearModuleSelected() {
    this.generatorService.clear();
    this.editor.clear();
  }

}
