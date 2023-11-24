import {Component} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {GeneratorService} from 'src/app/old_stuff//Services/Generator/generator.service';
import {DialogContentComponent} from '../mat_dialog/dialog-content/dialog-content.component';
import {ImportServiceService} from 'src/app/old_stuff//Services/Import_Json/import-service.service';
import {DialogEntityComponent} from '../mat_dialog/dialog-entity/dialog-entity.component';
import {DialogTableComponent} from '../mat_dialog/dialog-table/dialog-table.component';
import {DialogExportComponent} from '../mat_dialog/dialog-export/dialog-export.component';
import Drawflow, {ConnectionEvent, ConnectionStartEvent, DrawflowNode} from 'drawflow';

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
  selectedNode!: DrawflowNode;

  /**
   * This variable represents the current HTML element associated
   * with the input in the Drawflow editor.
   */
  currentInputElement: HTMLElement | null = null;

  /**
   * Variable represents the file name.
   */
  fileName!: string;

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
  ) {
  }

  ngOnInit(): void {
    this.initDrawingBoard();
  }

  /**
   * This method initializes the drawing board, which includes creating a Drawflow editor
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
    this.drawflowElement = document.getElementById('drawflow') as HTMLElement;
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
   * This method log Drawflow editor events to handle user interactions
   * inside the editor.
   */
  addEditorEvents() {
    this.editor.on('nodeCreated', (id: number) => {
      this.addObjectRelativeClassNode(id)
    });

    this.editor.on('nodeRemoved', (id: number) => {
      this.handleNodeRemoved(id)
    });

    this.editor.on('nodeSelected', (id: number) => {
      this.handleNodeSelected(id)
    });

    this.editor.on('nodeMoved', () => {
      this.setEditorProperties({viewOutputHover: 'visible'})
    });

    this.editor.on('connectionStart', (event) => {
      console.log("connectionStart: ", event);
      this.handleConnectionStart(event);
    });

    this.editor.on('connectionCreated', (connection) => {
      console.log('Connection created: ', connection);
      this.handleConnectionCreated(connection);
    });

    this.editor.on('connectionRemoved', (connection) => {
      this.handleConnectionRemoved(connection)
    });

    this.editor.on('connectionCancel', () => {
      this.handleConnectionCancel()
    });

    this.editor.on('contextmenu', () => {
      this.setEditorProperties({viewOutputHover: 'visible'})
    });

    this.editor.on('click', () => {
      this.setEditorProperties({viewOutputHover: 'visible'})
    });
  }

  /**
   * This method gets the input element associated with a given HTML element.
   * @param element HTML element to search for the input element.
   * @returns the found input element or null if not found.
   */
  getNodeInput(element: HTMLElement | null) {
    const inputElement = element?.querySelector(".inputs .input.input_1") as HTMLElement;
    this.currentInputElement = inputElement;
    return this.currentInputElement;
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
   * This method Checks the connections of a node when a connection is started.
   * @param event event object representing the connection start.
   */
  checkNodeConnection(event: ConnectionStartEvent) {
    const node = this.editor.getNodeFromId(event.output_id);
    this.checkOutputsConnections(node);
    //this.checkInputsConnections(node);
  }

  /**
   * This method checks the connections of the outputs of a given node
   * and updates the visibility of a related element.
   * @param node node for which connections are checked.
   */
  checkOutputsConnections(node: DrawflowNode) {
    const entityConnectedToTable = Object.values(node.outputs)
      .some(output =>
        output.connections.some(connection =>
          this.editor.getNodeFromId(connection.node).class === 'Table'));
    this.drawflowElement.style.setProperty('--viewInputTable', entityConnectedToTable ? 'hidden' : 'visible');
  }

  /**
   * This method adds a connection between two nodes in the Drawflow editor and saves this connection.
   * @param connection object representing the connection between nodes.
   */
  addLink(connection: ConnectionEvent) {
    const result = this.getNode(connection);
    this.generatorService.saveLink(result.first.id, result.second.id, result.second.class)
  }

  /**
   * This method removes a connection between two entities from the Drawflow editor
   * and removes the associated link.
   * @param connection object representing the connection to remove.
   */
  removeLink(connection: ConnectionEvent) {
    const result = this.getNode(connection);
    this.generatorService.removeLinkConfiguration(result.first.id, result.second.id, result.second.class)
  }

  /**
   * This method retrieves two nodes based on output and input IDs from the Drawflow editor.
   * @param event An object containing output_id and input_id for the nodes.
   * @returns An object with the first and second nodes.
   */
  getNode(event: ConnectionEvent) {
    return {first: this.editor.getNodeFromId(event.output_id), second: this.editor.getNodeFromId(event.input_id)};
  }

  /**
   * This method adds an object associated with a Drawflow editor node,
   * based on the node class, and saves this object.
   * @param id node id from which to obtain the associated node.
   */
  addObjectRelativeClassNode(id: number | string) {
    const node = this.editor.getNodeFromId(id)
    switch (node.class) {
      case 'Entity':
        this.generatorService.saveEntity(node.id, node.name);
        break;
      case 'Table':
        this.generatorService.saveTable(node.id, node.name);
        break;
    }
  }

  /**
   * This method allows the release of an object
   * dragged to a specific area.
   * @param ev the "drag-and-drop" event to handle.
   */
  allowDrop(ev: Event) {
    ev.preventDefault();
  }

  /**
   * This method handles the start of the "drag" operation when an element is dragged.
   * @param ev drag event to handle.
   */
  drag(ev: any) {
    ev.dataTransfer.setData('node', ev.target.getAttribute('data-node'));
  }

  // checkInputsConnections(node: DrawflowNode) {
  //   const inputs = Object.values(node.inputs);
  //   inputs.forEach(input => {
  //     input.connections.forEach(connection => {
  //       const connectedNode = document.getElementById(`node-${connection.node}`);
  //       this.getNodeInput(connectedNode).style.visibility = 'hidden';
  //     });
  //   });
  // }

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

    switch (name) {
      case 'entity':
        this.addNode('Entity', position.pos_x, position.pos_y, 'Entity');
        break;
      case 'table':
        this.addNode('IoT', position.pos_x, position.pos_y, 'Table');
        break;
      default:
    }
  }

  /**
   * This method adds a node to the Drawflow editor with the specified parameters.
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
   * This method attaches a double-click event listener to a specific node based on its type.
   * @param node_id id of the node to which the double-click event listener is attached.
   * @param nodeType type of the node.
   */
  dblClickNode(node_id: string | number, nodeType: string) {
    document.querySelector(`#node-${node_id}.drawflow-node.${nodeType}`)?.addEventListener('dblclick', () => {
      switch (nodeType) {
        case 'Entity':
          this.dialog.open(DialogEntityComponent, {
            data: {
              name: "device",
              type: "string"
            }
          });
          break;
        case 'Table':
          this.dialog.open(DialogTableComponent, {
            data: {}
          });
          break;
      }
    });
  }

  /**
   * This method calculate the coordinates relative to the Drawflow editor canvas.
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

    return {pos_x, pos_y}
  }

  /**
   * This method removes a node from the Drawflow editor
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
  convertToDrawflowFormat(inputData: any) {
    this.addEntityToDrawflow(inputData);
    this.addTableToDrawflow(inputData);
    this.addLinksBetweenEntityToDrawflow(inputData);
    this.addLinkTableEntityToDrawflow(inputData);
  }

  /**
   * This method adds entities to the Drawflow diagram based on the provided data.
   * @param data data containing entity information.
   */
  addEntityToDrawflow(data: { entities: any[]; }) {
    data.entities.forEach((entity) => {
      this.addNode(entity.name, 100 * entity.entity_id, 100 * entity.entity_id, 'Entity');
    });
  }

  /**
   * This method adds tables to the Drawflow diagram based on the provided data.
   * @param data data containing table information.
   */
  addTableToDrawflow(data: { awsConfig: { dynamo: { tables: any[]; }; }; }) {
    data.awsConfig.dynamo.tables.forEach((table) => {
      this.addNode(table.tableName, 100 * table.table_id, 100 * table.table_id, 'Table');
    });
  }

  /**
   * This method adds connections between nodes in Drawflow based on the provided link data.
   * @param data data containing links information.
   */
  addLinksBetweenEntityToDrawflow(data: { links: any[]; entities: any[]; }) {
    data.links.forEach((link) => {
      const first_entity_id = data.entities.find((entity) => entity.name === link.first_entity)?.entity_id;
      const second_entity_id = data.entities.find((entity) => entity.name === link.second_entity)?.entity_id;

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
  addLinkTableEntityToDrawflow(data: { entities: any[]; awsConfig: { dynamo: { tables: any[]; }; }; }) {
    data.entities.forEach((entity) => {
      if (entity.table) {
        const table_id = data.awsConfig.dynamo.tables.find((table) => table.tableName === entity.table)?.table_id;
        this.editor.addConnection(entity.entity_id, table_id, 'output_1', 'input_1');
      }
    });
  }

  /**
   * This method exports the project
   * and generate a configuration.
   */
  export() {
    const dialogRef = this.dialog.open(DialogExportComponent, {
      data: {file: this.fileName},
    });

    dialogRef.afterClosed().subscribe(result => {
      this.fileName = result;
      if (this.fileName) {
        this.generatorService.export(this.fileName);
      }
    });
  }

  /**
   * This method opens a dialog to view the configured JSON.
   */
  viewJson() {
    const json = this.generatorService.saveConfiguration();
    const jsonString = JSON.stringify(json, null, 2);
    this.dialog.open(DialogContentComponent, {
      data: {json: jsonString}
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

  addLabelText(bgPath: any, labelText: string) {
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

  /**
   * This method handles the removal of a node.
   * @param id unique identifier of the removed node.
   */
  private handleNodeRemoved(id: number) {
    this.setEditorProperties({viewOutputHover: 'visible'});
    this.removeNode(id);
  }

  /**
   * This method handles the selection of a node.
   * @param id unique identifier of the selected node.
   */
  private handleNodeSelected(id: number) {
    this.setEditorProperties({viewOutputHover: 'hidden'});
    this.selectedNode = this.editor.drawflow.drawflow.Home.data[`${id}`];
  }

  /**
   * This method handles the start of a connection event.
   * @param event connection start event to be handled.
   */
  private handleConnectionStart(event: ConnectionStartEvent) {
    const element = document.getElementById(`node-${event.output_id}`);
    this.getNodeInput(element).style.visibility = 'hidden';
    this.setEditorProperties({viewOutputHover: 'hidden', viewInputEntity: 'visible'});
    this.checkNodeConnection(event);
  }

  /**
   * This method handles the event when a connection is created.
   * @param connection connection event to be handled.
   */
  private handleConnectionCreated(connection: ConnectionEvent) {
    if (this.currentInputElement) {
      this.currentInputElement.style.removeProperty('visibility');
    }
    this.setEditorProperties({viewOutputHover: 'visible', viewInputTable: 'hidden', viewInputEntity: 'hidden'});
    this.addLabelText(document.querySelector(".connection"), "Prova");
    this.addLink(connection);
  }

  /**
   * This method handles the event when a connection is cancelled.
   */
  private handleConnectionCancel() {
    if (this.currentInputElement) {
      this.currentInputElement.style.removeProperty('visibility');
    }
    this.setEditorProperties({viewOutputHover: 'visible', viewInputTable: 'hidden', viewInputEntity: 'hidden'});
  }

  /**
   * This method handles the event when a connection is removed.
   * @param connection connection event to be handled.
   */
  private handleConnectionRemoved(connection: ConnectionEvent) {
    this.setEditorProperties({viewOutputHover: 'visible', viewInputEntity: 'hidden'});
    this.removeLink(connection);
  }
}
