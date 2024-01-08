import {Component} from '@angular/core';
import {ImportServiceService} from "../../services/import-service.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent {
  descriptionText: string = "Trascina e personalizza le tue entità o tabelle, monitorando in tempo reale" +
    " il file JSON prodotto.\nQuando sei soddisfatto del risultato," +
    " puoi salvare il file sul tuo dispositivo per ricominciare quando" +
    " vuoi oppure generare direttamente un URL da cui scaricare il codice generato" +
    " per il tuo sistema IoT con le relative app.";

  constructor(private importService: ImportServiceService, private router: Router) {
  }

  /**
   * This method handles the import of a JSON file via the specified event and redirects to the diagram component.
   * @param event file input event that contains the selected file.
   */
  import(event: Event) {
    this.importService.onFileSelected(event)
      .then((jsonContent) => {
        this.importService.pushToConfiguration(jsonContent);
      })
      .then(() => {
        this.router.navigate(['/new']);
      })
      .catch((error) => {
        alert(error);
      });
  }
}
