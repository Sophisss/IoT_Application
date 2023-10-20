import { Component } from '@angular/core';
import * as d3 from 'd3';
import { GeneratorService } from 'src/app/Services/Generator/generator.service';

@Component({
  selector: 'app-prova',
  templateUrl: './prova.component.html',
  styleUrls: ['./prova.component.scss']
})
export class ProvaComponent {

  sideBarOpen = true;

  /**
   * Constructor for this Component.
   * @param generatorService service to generate JSON configuration.
   */
  constructor(
    private generatorService: GeneratorService
  ) { }

  nodes = [
    { "id": "Device", "x": "0px", "y": "0px" },
    { "id": "Building", "x": "140px", "y": "0px" },
    { "id": "User", "x": "40px", "y": "100px" }
  ]

  initDrawingBoard() {

    d3.select("#container")
      .selectAll('.node')
      .data(this.nodes)
      .enter()
      .append("div")
      .on("click", this.connectorClicked)
      .classed("node", true)
      .attr("id", d => d.id)
      .style("left", d => d.x)
      .style("top", d => d.y)
      .text(d => d.id);


      const drag = d3.drag()
      .on("start", this.started)
      .on("drag", this.moved)
      .on("end", this.stopped)

      // @ts-ignore
      d3.selectAll(".node").call(drag);

      d3.selectAll('.node')
      .append("div")
      .on("mouseover", this.connectorMouseover)
      .on("mouseout", this.connectorMouseout)
      .on("click", this.connectorClicked)

      .classed("connector", true)
      .classed("left-connector", true)

    d3.selectAll('.node')
      .append("div")
      .on("mouseover", this.connectorMouseover)
      .on("mouseout", this.connectorMouseout)
      .on("click", this.connectorClicked)
      .classed("connector", true)
      .classed("right-connector", true)

  }

  ngOnInit(): void {
    this.initDrawingBoard();
  }

  started(event: DragEvent) {
    // @ts-ignore
    d3.select("#" + event.subject.id)
      .style("left", event.x)
      .style("top", `${event.y}px`)
      .classed("dragging-node", true)
  }

  moved(event: DragEvent) {
    d3.select("body")
      .style("cursor", "all-scroll")

    // @ts-ignore
    d3.select("#" + event.subject.id)
      .style("left", `${event.x}px`)
      .style("top", `${event.y}px`)
  }

  stopped(event: DragEvent) {
    d3.select("body")
      .style("cursor", "auto")

    // @ts-ignore
    d3.select("#" + event.subject.id)
      .style("left", `${event.x}px`)
      .style("top", `${event.y}px`)
      .classed("dragging-node", false)
  }


  connectorClicked(event: any) {
    console.log(event);
  }

  connectorMouseover(event: MouseEvent) {
    console.log(event);
    event.stopPropagation();
    event.stopImmediatePropagation();
    // d3.selectAll(".node").on('mousedown.drag', null);
  }

  connectorMouseout(event: MouseEvent) {
    console.log(event);
    event.stopPropagation();
    event.stopImmediatePropagation();
    // const drag = d3.drag()
    //   .on("start", this.started)
    //   .on("drag", this.moved)
    //   .on("end", this.stopped)

    // // @ts-ignore
    // d3.selectAll(".node").call(drag);
  }

  /**
   * This method exports the project.
   */
  export() {
    this.generatorService.export()
    console.log("Export")
  }

  clearModuleSelected() {
    this.generatorService.clear();
  }

}
