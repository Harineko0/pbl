import {Swap} from "../entity/swap";

export class SwapRepository {
    readonly name = 'swaps';
    readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.name);

    create(swap: Swap) {
        if (this.sheet === null) return;

        const last = this.sheet.getLastRow();

        this.sheet.getRange(last + 1, 1).setValue(swap.id);
        this.sheet.getRange(last + 1, 2).setValue(swap.old_shift_id);
        this.sheet.getRange(last + 1, 3).setValue(swap.new_shift_id);
    }

    get(id: string): Swap | null {
        if (this.sheet === null) return null;

        const values = this.sheet.getDataRange().getValues();
        const row = values.findIndex((row) => row[0] === id);

        if (row === -1) return null;

        return {
            id: values[row][0],
            old_shift_id: values[row][1],
            new_shift_id: values[row][2]
        };
    }
}
