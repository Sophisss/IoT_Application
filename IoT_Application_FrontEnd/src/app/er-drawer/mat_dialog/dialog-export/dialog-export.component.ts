import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-dialog-export',
  templateUrl: './dialog-export.component.html',
  styleUrls: ['./dialog-export.component.scss']
})
export class DialogExportComponent {

  constructor(
    private dialogRef: MatDialogRef<DialogExportComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {file: string}) { }

  onNoClick(): void {
    this.dialogRef.close();
  }

}
