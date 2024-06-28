import {Shift} from "../entity/shift";

export class ShiftRepository {
    readonly sheetName = 'shifts';
    readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.sheetName);

    create(shift: Shift) {
        if (this.sheet === null) return;

        const last = this.sheet.getLastRow();

        this.sheet.getRange(last + 1, 1).setValue(shift.id);
        this.sheet.getRange(last + 1, 2).setValue(shift.date);
        this.sheet.getRange(last + 1, 3).setValue(shift.shift_type);
        this.sheet.getRange(last + 1, 4).setValue(shift.worker_id);
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
}
