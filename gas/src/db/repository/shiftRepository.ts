import {Shift} from "../entity/shift";
import {ForCreate} from "../entity/_utils";

export class ShiftRepository {
    readonly sheetName = 'shifts';
    readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.sheetName);

    createMany(shifts: ForCreate<Shift>[]) {
        if (this.sheet === null) return;

        const last = this.sheet.getLastRow();
        const id = last;
        const values = shifts.map(shift => [
            id, shift.date, shift.shift_type, shift.worker_id
        ])

        this.sheet.getRange(last + 1, 1, shifts.length, 4).setValues(values);

        Logger.log(`Shift created.`);
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
