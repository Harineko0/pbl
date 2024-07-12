import {Dislike} from "../entity/dislike";

export class DislikeRepository {
    private readonly sheetName = 'SHIFT_REQUEST_FORM';
    private readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.sheetName);

    findMany(): Dislike[] {
        if (this.sheet === null) return [];

        const values = this.sheet.getRange("B8:D").getValues();

        return values.map(val => ({
            worker_id: val[0],
            target_id: val[1]
        }));
    }
}
