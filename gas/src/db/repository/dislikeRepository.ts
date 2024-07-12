import {Dislike} from "../entity/dislike";

export class DislikeRepository {
    private readonly sheetName = 'dislikes';
    private readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.sheetName);

    findMany(): Dislike[] {
        if (this.sheet === null) return [];

        const values = this.sheet.getDataRange().getValues().slice(1);

        return values.map(val => ({
            worker_id: val[0],
            target_id: val[1]
        }));
    }
}
