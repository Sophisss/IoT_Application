import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-dialog-entity',
  templateUrl: './dialog-entity.component.html',
  styleUrls: ['./dialog-entity.component.scss']
})
export class DialogEntityComponent {

  constructor(
    private dialogRef: MatDialogRef<DialogEntityComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {}) 
    { }

    onNoClick(): void {
    this.dialogRef.close();
  }

}
