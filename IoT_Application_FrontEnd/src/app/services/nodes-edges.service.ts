import {Injectable} from '@angular/core';

export class FlowNode {
  id: number;

  text: string;

  type: string;
}

export class FlowEdge {
  id: number;

  fromId: number;

  toId: number;

  text: string;
}

const flowNodes: FlowNode[] = [];

const flowEdges: FlowEdge[] = [];

@Injectable({
  providedIn: 'root'
})
export class NodesEdgesService {
  getFlowNodes() {
    return flowNodes;
  }

  getFlowEdges() {
    return flowEdges;
  }
}