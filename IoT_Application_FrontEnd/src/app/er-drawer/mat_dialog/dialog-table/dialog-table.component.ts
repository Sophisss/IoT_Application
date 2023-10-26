import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-dialog-table',
  templateUrl: './dialog-table.component.html',
  styleUrls: ['./dialog-table.component.scss']
})
export class DialogTableComponent {

  constructor(
    private dialogRef: MatDialogRef<DialogTableComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {}) 
    { }

    onNoClick(): void {
    this.dialogRef.close();
  }

}
