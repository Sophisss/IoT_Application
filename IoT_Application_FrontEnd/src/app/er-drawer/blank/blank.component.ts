import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { GeneratorService } from 'src/app/Services/Generator/generator.service';
import { DialogContentComponent } from '../mat_dialog/dialog-content/dialog-content.component';
import { ImportServiceService } from 'src/app/Services/Import_Json/import-service.service';
import Drawflow from 'drawflow';
import { DialogEntityComponent } from '../mat_dialog/dialog-entity/dialog-entity.component';
import { DialogTableComponent } from '../mat_dialog/dialog-table/dialog-table.component';

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
   * HTML element representing the Drawflow area.
   */
  drawflowElement!: HTMLElement;

  /**
   * Variable that tracks the selected node in the Drawflow editor.
   */
  selectedNode: any = {};

  //Utility variables 

  sideBarOpen = true;

  /**
   * Constructor for this Component.
   * @param generatorService service to generate JSON configuration.
   * @param importService service to import JSON.
   * @param dialog the dialog service for handling user interactions.
   */
  constructor(
    private generatorService: GeneratorService,
    private importService: ImportServiceService,
    private dialog: MatDialog
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
    this.configureEditor();
    this.editor.start();
  }

  /**
   * This method configures the main options of the Drawflow editor.
   */
  configureEditor() {
    this.editor.reroute = true;
    this.editor.draggable_inputs = true;
    this.editor.line_path = 1;
    this.editor.editor_mode = 'edit';
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
      this.addObjectRelativeClassNode(id);
    });

    this.editor.on('nodeRemoved', (id: number) => {
      console.log('Node removed ' + id);
      this.setEditorProperties({ viewOutputHover: 'visible' });
      this.removeNode(id);
    });

    this.editor.on('connectionCreated', (connection) => {
      console.log('Connection created: ' + connection);
      this.setEditorProperties({ viewOutputHover: 'visible', viewInputTable: 'hidden', viewInputEntity: 'hidden' });
      //this.addLabelText(document.querySelector(".connection"), "Prova");
      this.addLink(connection)
    })

    this.editor.on('connectionRemoved', (connection: any) => {
      console.log('Connection removed ', connection);
      this.setEditorProperties({ viewOutputHover: 'visible', viewInputEntity: 'hidden' });
      this.removeLink(connection)
    });

    this.editor.on('connectionCancel', (connection: any) => {
      console.log('Connection cancel ', connection);
      this.setEditorProperties({ viewOutputHover: 'visible', viewInputTable: 'hidden', viewInputEntity: 'hidden' });
    });

    this.editor.on('nodeSelected', (id: any) => {
      this.setEditorProperties({ viewOutputHover: 'hidden' });
      this.selectedNode = this.editor.drawflow.drawflow.Home.data[`${id}`];
    });

    this.editor.on('contextmenu', (event: any) => {
      this.setEditorProperties({ viewOutputHover: 'visible' });
    });

    this.editor.on('click', (event: any) => {
      this.setEditorProperties({ viewOutputHover: 'visible' });
    });

    this.editor.on('nodeMoved', (event: any) => {
      this.setEditorProperties({ viewOutputHover: 'visible' });
    });

    this.editor.on('connectionStart', (event: any) => {
      console.log("connectionStart: ", event)
      this.setEditorProperties({ viewOutputHover: 'hidden', viewInputEntity: 'visible' });
      this.checkNodeConnection(event);
    });
  }

  /**
   * This method sets the editor's custom CSS properties.
   * @param properties object containing custom CSS properties.
   */
  setEditorProperties(properties: any) {
    Object.keys(properties).forEach(property => {
      this.drawflowElement.style.setProperty(`--${property}`, properties[property]);
    });
  }

  /**
   * Checks whether an entity is connected to a table and if so, 
   * prohibits the entity from connecting to another table.
   * @param event event associated with the node connection.
   */
  checkNodeConnection(event: any) {
    const node = this.editor.getNodeFromId(event.output_id);
    const entityConnectedToTable = Object.values(node.outputs)
      .some(output =>
        output.connections.some(connection =>
          this.editor.getNodeFromId(connection.node).class === 'Table'
        ));
    this.drawflowElement.style.setProperty('--viewInputTable', entityConnectedToTable ? 'hidden' : 'visible');
  }

  /**
   * Adds a connection between two nodes in the Drawflow editor and saves this connection.
   * @param connection object representing the connection between nodes.
   */
  addLink(connection: any) {
    const result = this.getNode(connection);
    this.generatorService.saveLink(result.first.id, result.second.id, result.second.class)
  }

  /**
   * Removes a connection between two entities from the Drawflow editor 
   * and removes the associated link.
   * @param connection object representing the connection to remove.
   */
  removeLink(connection: any) {
    const result = this.getNode(connection);
    this.generatorService.removeLinkConfiguration(result.first.id, result.second.id, result.second.class)
  }

  /**
   * Retrieves two nodes based on output and input IDs from the Drawflow editor.
   * @param event An object containing output_id and input_id for the nodes.
   * @returns An object with the first and second nodes.
  */
  getNode(event: any) {
    const first = this.editor.getNodeFromId(event.output_id);
    const second = this.editor.getNodeFromId(event.input_id);
    return { first, second };
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
    const position = this.getCoordinates(pos_x, pos_y);
    pos_x = position.pos_x;
    pos_y = position.pos_y;

    switch (name) {
      case 'entity':
        this.addNode('Entity', pos_x, pos_y, 'Entity');
        break;
      case 'table':
        this.addNode('IoT', pos_x, pos_y, 'Table');
        break;
      default:
    }
  }

  /**
 * Adds a node to the Drawflow editor with the specified parameters.
 * @param nodeName Name of the node.
 * @param posX X-coordinate position.
 * @param posY Y-coordinate position.
 * @param nodeType Type of the node.
 */
  addNode(nodeName: string, posX: number, posY: number, nodeType: string) {
    const output = nodeType === 'Table' ? 0 : 1
    const node_id = this.editor.addNode(nodeName, 1, output, posX, posY, nodeType, {},
      `
      <div>
        <div class="title-box"><i class="fab fa-${nodeType}"></i>${nodeName}</div>
      </div>
    `, false);
    this.dblClickNode(node_id, nodeType);
  }

  /**
   * Attaches a double-click event listener to a specific node based on its type.
   * @param node_id id of the node to which the double-click event listener is attached.
   * @param nodeType type of the node.
   */
  dblClickNode(node_id: any, nodeType: string) {
    if (nodeType === 'Entity') {
      document.querySelector(`#node-${node_id}.drawflow-node.${nodeType}`)?.addEventListener('dblclick', () => {
        console.log('Doppio click sul nodo entity');
        this.dialog.open(DialogEntityComponent, {
          data: {}
        });
      });
    } else if (nodeType === 'Table') {
      document.querySelector(`#node-${node_id}.drawflow-node.${nodeType}`)?.addEventListener('dblclick', () => {
        console.log('Doppio click sul nodo table');
        this.dialog.open(DialogTableComponent, {
          data: {}
        });
      });
    }
  }

  /**
   * Calculate the coordinates relative to the Drawflow editor canvas.
   * @param pos_x x coordinate to convert.
   * @param pos_y y coordinate to convert.
   * @returns object containing the calculated coordinates.
   */
  getCoordinates(pos_x: number, pos_y: number) {
    pos_x = pos_x * (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom)) -
      this.editor.precanvas.getBoundingClientRect().x *
      (this.editor.precanvas.clientWidth / (this.editor.precanvas.clientWidth * this.editor.zoom));

    pos_y = pos_y * (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom)) -
      this.editor.precanvas.getBoundingClientRect().y *
      (this.editor.precanvas.clientHeight / (this.editor.precanvas.clientHeight * this.editor.zoom));

    return { pos_x, pos_y }
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
   * This method handles the import of a JSON file via the specified event.
   * @param event file input event that contains the selected file.
   */
  import(event: Event) {
    this.importService.onFileSelected(event)
      .then((jsonContent) => {
        this.convertToDrawflowFormat(jsonContent);
      })
      .catch((error) => {
        alert(error);
      });
  }

  /**
   * This method adds entities, tables and links to the Drawflow diagram.
   * @param inputData json data to convert.
   */
  convertToDrawflowFormat(inputData: any): any {
    this.addEntityToDrawflow(inputData);
    this.addTableToDrawflow(inputData);
    this.addLinksBetweenEntityToDrawflow(inputData);
    this.addLinkTableEntityToDrawflow(inputData);
  }

  /**
   * Adds entities to the Drawflow diagram based on the provided data.
   * @param data data containing entity information.
   */
  addEntityToDrawflow(data: any) {
    data.entities.forEach((entity: any) => {
      const nodeId = entity.entity_id;
      const nodeName = entity.name;
      this.addNode(nodeName, 100 * nodeId, 100 * nodeId, 'Entity');
    });
  }

  /**
   * Adds tables to the Drawflow diagram based on the provided data.
   * @param data data containing table information.
   */
  addTableToDrawflow(data: any) {
    data.awsConfig.dynamo.tables.forEach((table: any) => {
      const nodeId = table.table_id;
      const nodeName = table.tableName;
      this.addNode(nodeName, 100 * nodeId, 100 * nodeId, 'Table');
    });
  }

  /**
 * This method adds connections between nodes in Drawflow based on the provided link data.
 * @param data data containing links information.
 */
  addLinksBetweenEntityToDrawflow(data: any) {
    data.links.forEach((link: any) => {
      const first_entity_id = data.entities.find((entity: any) => entity.name === link.first_entity)?.entity_id;
      const second_entity_id = data.entities.find((entity: any) => entity.name === link.second_entity)?.entity_id;

      if (first_entity_id && second_entity_id) {
        //Sostituire 1 e 2 
        this.editor.addConnection(1, 2, 'output_1', 'input_1');
      }
    });
  }

  /**
   * This method adds links between entities and tables based on the 'table' field of the entities.
   * @param data data containing information.
   */
  addLinkTableEntityToDrawflow(data: any) {
    data.entities.forEach((entity: any) => {
      const table_name = entity.table;
      if (table_name) {
        const table_id = data.awsConfig.dynamo.tables.find((table: any) => table.tableName === table_name)?.table_id;
        if (table_id) {
          this.editor.addConnection(entity.entity_id, table_id, 'output_1', 'input_1');
        }
      }
    });
  }

  /**
   * This method exports the project
   * and generate a configuration.
   */
  export() {
    this.generatorService.export()
  }

  /**
   * This method opens a dialog to view the configured JSON.
   */
  viewJson() {
    const json = this.generatorService.saveConfiguration();
    const jsonString = JSON.stringify(json, null, 2);
    this.dialog.open(DialogContentComponent, {
      data: { json: jsonString }
    });
  }

  /**
   * This method clears all contents from the Drawflow editor.
   */
  clearModuleSelected() {
    //TODO rivedi
    this.editor.clear();
    this.generatorService.clear();
  }

  // addLabelText(bgPath: any, labelText: any) {
  //   const newid = [bgPath.classList].join().replace(/\s/g, '');
  //   bgPath.childNodes[0].id = newid;
  //   let textElem = document.createElementNS(bgPath.namespaceURI, "text");
  //   let textElemPath = document.createElementNS(bgPath.namespaceURI, "textPath");
  //   textElemPath.setAttribute("href", `#${newid}`);
  //   textElemPath.setAttribute("text-anchor", "left");
  //   textElemPath.classList.add("label-text");
  //   textElemPath.textContent = labelText;
  //   textElem.appendChild(textElemPath);
  //   bgPath.appendChild(textElem);
  // }
}