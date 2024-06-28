import {ShiftType} from "../entity/shiftType";

export class ShiftTypeRepository {
    readonly name = 'shift_types';
    readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.name);

    create(shiftType: ShiftType) {
        if (this.sheet === null) return;

        const last = this.sheet.getLastRow();

        this.sheet.getRange(last + 1, 1).setValue(shiftType.id);
        this.sheet.getRange(last + 1, 2).setValue(shiftType.name);
    }

    get(id: string): ShiftType | null {
        if (this.sheet === null) return null;

        const values = this.sheet.getDataRange().getValues();
        const row = values.findIndex((row) => row[0] === id);

        if (row === -1) return null;

        return {
            id: values[row][0],
            name: values[row][1]
        };
    }
}
