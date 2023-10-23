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

  drawflowElement!: HTMLElement;

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
    this.initDrawingBoard();
  }

  /**
   * Initializes the drawing board, which includes creating a Drawflow editor
   * and setting up various configuration options.
   */
  initDrawingBoard() {
    this.initDrawFlow();
    this.addEditorEvents();
    this.dragstart();
  }

  /**
   * This method initializes the Drawflow editor and configures its settings.
   */
  initDrawFlow() {
    this.drawflowElement = <HTMLElement>document.getElementById('drawflow');
    this.editor = new Drawflow(this.drawflowElement);
    this.editor.reroute = true;
    this.editor.draggable_inputs = true;
    this.editor.line_path = 1;
    this.editor.editor_mode = 'edit';
    this.editor.start();
  }

  /**
   * This method handles the dragstart event on elements with class .drag-drawflow.
   * It is used to attach an event handler to draggable elements.
   */
  dragstart() {
    document.querySelectorAll('.dragging-node').forEach((element) => {
      element.addEventListener('dragstart', (ev) => this.drag(ev));
    });
  }

  /**
   * Log Drawflow editor events to handle user interactions
   * inside the editor.
   */
  addEditorEvents() {
    this.editor.on('nodeCreated', (id: any) => {
      console.log(this.editor.getNodeFromId(id))
      this.addObjectRelativeClassNode(id)
    });

    this.editor.on('nodeRemoved', (id: number) => {
      console.log('Node removed ' + id);
      this.drawflowElement.style.setProperty('--viewOutputHover', "visible");
      this.removeNode(id);
    });

    this.editor.on('connectionCreated', (connection) => {
      console.log('Connection created: ' + connection);
      this.drawflowElement.style.setProperty('--viewInputTable', "hidden");
      this.drawflowElement.style.setProperty('--viewInputEntity', "hidden");
      this.drawflowElement.style.setProperty('--viewOutputHover', "visible");
      this.addLabelText(document.querySelector(".connection"), "Prova");
      this.addLink(connection)
    })

    this.editor.on('connectionRemoved', (connection: any) => {
      console.log('Connection removed ', connection);
      this.drawflowElement.style.setProperty('--viewInputEntity', "hidden");
      this.drawflowElement.style.setProperty('--viewOutputHover', "visible");
      this.removeLink(connection)
    });

    this.editor.on('connectionCancel', (connection: any) => {
      console.log('Connection cancel ', connection);
      this.drawflowElement.style.setProperty('--viewInputTable', "hidden");
      this.drawflowElement.style.setProperty('--viewInputEntity', "hidden");
      this.drawflowElement.style.setProperty('--viewOutputHover', "visible");
    });

    this.editor.on('nodeSelected', (id: any) => {
      this.drawflowElement.style.setProperty('--viewOutputHover', "hidden");
      console.log("nodeSelected")
      this.selectedNode = this.editor.drawflow.drawflow.Home.data[`${id}`];
    });

    this.editor.on('contextmenu', (event: any) => {
      this.drawflowElement.style.setProperty('--viewOutputHover', "visible");
      console.log("contextmenu: " + event)
    });

    this.editor.on('click', (event: any) => {
      this.drawflowElement.style.setProperty('--viewOutputHover', "visible");
      console.log("click: " + event);
    });

    this.editor.on('nodeMoved', (event: any) => {
      console.log("nodeMoved: " + event);
      this.drawflowElement.style.setProperty('--viewOutputHover', "visible");
    });

    this.editor.on('connectionStart', (event: any) => {
      console.log("connectionStart: ", event)
      this.drawflowElement.style.setProperty('--viewInputEntity', "visible");
      this.drawflowElement.style.setProperty('--viewOutputHover', "hidden");
      this.checkNodeConnection(event);
    });
  }


  /**
   * Checks whether an entity is connected to a table and if so, 
   * prohibits the entity from connecting to another table.
   * @param event event associated with the node connection.
   */
  checkNodeConnection(event: any) {
    const node = this.editor.getNodeFromId(event.output_id);
    const outputs = node.outputs;
    let entityConnectedToTable = false;

    for (const outputKey in outputs) {
      if (outputs.hasOwnProperty(outputKey)) {
        outputs[outputKey].connections.forEach((connection) => {
          const nodeConnection = this.editor.getNodeFromId(connection.node);

          if (nodeConnection.class === 'Table') {
            entityConnectedToTable = true;
          }
        });
      }
    }
    if (entityConnectedToTable) {
      this.drawflowElement.style.setProperty('--viewInputTable', "hidden");
    } else {
      this.drawflowElement.style.setProperty('--viewInputTable', "visible");
    }
  }


  /**
   * Adds a connection between two nodes in the Drawflow editor and saves this connection.
   * @param connection object representing the connection between nodes.
   */
  addLink(connection: any) {
    const first = this.editor.getNodeFromId(connection.output_id);
    const second = this.editor.getNodeFromId(connection.input_id);
    this.generatorService.saveLink(first.id, second.id, second.class)
  }

  /**
   * Removes a connection between two entities from the Drawflow editor 
   * and removes the associated link.
   * @param connection object representing the connection to remove.
   */
  removeLink(connection: any) {
    const first = this.editor.getNodeFromId(connection.output_id);
    const second = this.editor.getNodeFromId(connection.input_id);
    this.generatorService.removeLinkConfiguration(first.id, second.id, second.class)
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
            <i class="fab fa-entity "></i>Entity
        </div>
      `;
        this.editor.addNode(name, 1, 1, pos_x, pos_y, 'Entity', {}, entityHtml, false);
        break;
      case 'table':
        const tableHtml = `
        <div>
           <i class="fab fa-table "></i>Table
        </div>
      `;
        this.editor.addNode('IoT', 1, 0, pos_x, pos_y, 'Table', {}, tableHtml, false);
        break;
      default:
    }
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
   * This method import a configuration.
   */
  import(event: Event) {
    console.log("import")
  }

  /**
   * This method exports the project
   * and generate a configuration.
   */
  export() {
    this.generatorService.export()
    console.log("Export")
  }

  viewJson() {
    console.log("View json")
  }

  /**
   * This method clears all contents from the Drawflow editor.
   */
  clearModuleSelected() {
    this.generatorService.clear();
    this.editor.clear();
  }

  addLabelText(bgPath: any, labelText: any) {
        const newid = [bgPath.classList].join().replace(/\s/g, '');
        bgPath.childNodes[0].id = newid; 
        let textElem = document.createElementNS(bgPath.namespaceURI, "text");
        let textElemPath = document.createElementNS(bgPath.namespaceURI, "textPath");
        textElemPath.setAttribute("href", `#${newid}`);
        textElemPath.setAttribute("text-anchor", "left");
        textElemPath.classList.add("label-text");
        textElemPath.textContent = labelText;
        textElem.appendChild(textElemPath); 
        bgPath.appendChild(textElem);
    }
}


