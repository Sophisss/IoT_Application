import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CustomCommandsService {

  constructor() {
  }

  executeCommand(commandName: string) {
    if (commandName === 'clear') {
      console.log('clear')
    }

    if (commandName === 'export') {
      console.log('export')
    }
  }
}
