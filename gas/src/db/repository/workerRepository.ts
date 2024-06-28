import { Worker } from '../entity/worker';

export class WorkerRepository {
    readonly name = 'workers';
    readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.name);

    create(worker: Worker) {
        if (this.sheet === null) return;

        const last = this.sheet.getLastRow();

        this.sheet.getRange(last + 1, 1).setValue(worker.id);
        this.sheet.getRange(last + 1, 2).setValue(worker.email);
    }

    get(id: string): Worker | null {
        if (this.sheet === null) return null;

        const values = this.sheet.getDataRange().getValues();
        const row = values.findIndex((row) => row[0] === id);

        if (row === -1) return null;

        return {
            id: values[row][0],
            email: values[row][1]
        };
    }
}
