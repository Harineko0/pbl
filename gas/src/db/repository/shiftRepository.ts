import {Shift} from "../entity/shift";
import {ForCreate} from "../entity/_utils";

export class ShiftRepository {
    readonly sheetName = 'shifts';
    readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.sheetName);

    create(shift: ForCreate<Shift>) {
        if (this.sheet === null) return;

        const last = this.sheet.getLastRow();
        const id = last;
        const row = last + 1;

        this.sheet.getRange(row, 1).setValue(id);
        this.sheet.getRange(row, 2).setValue(shift.date);
        this.sheet.getRange(row, 3).setValue(shift.shift_type);
        this.sheet.getRange(row, 4).setValue(shift.worker_id);

        Logger.log(`Shift created. ${id}: ${shift}`);
    }

    get(id: string): Shift | null {
        if (this.sheet === null) return null;

        const values = this.sheet.getDataRange().getValues();
        const row = values.findIndex((row) => row[0] === id);

        if (row === -1) return null;

        return {
            id: values[row][0],
            date: values[row][1],
            shift_type: values[row][2],
            worker_id: values[row][3]
        };
    }

    getByDateAndWorker(date: Date, workerId: string) {
        if (this.sheet === null) return null;

        const values = this.sheet.getDataRange().getValues();
        const value = values.find((row) =>
            row[1] instanceof Date
            && (row[1] as Date).getTime() - date.getTime() < 1000
            && row[3] === workerId);

        if (value === undefined) return null;

        return {
            id: value[0],
            date: value[1],
            shift_type: value[2],
            worker_id: value[3]
        };
    }
}
