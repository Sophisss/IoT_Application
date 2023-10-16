import Drawflow from "drawflow";

export class Drawflowoverride extends Drawflow {

    override addConnection(event: any) {
        console.log("sono dentro")
        // Disegna la connessione
        const connection = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.classList.add('main-path');
        path.setAttributeNS(null, 'd', '');
        connection.classList.add('connection');
        connection.appendChild(path);
        this.precanvas.appendChild(connection);
    }
}
