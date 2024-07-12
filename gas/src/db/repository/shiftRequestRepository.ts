import {ShiftRequest} from "../entity/shiftRequest";

export class ShiftRequestRepository {
    private readonly sheetName = 'SHIFT_REQUEST_FORM';
    private readonly sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(this.sheetName);

    findMany(): ShiftRequest[] {
        if (this.sheet === null) return [];

        const values = this.sheet.getRange("F8:G").getValues();

        return values.map(val => ({
            worker_id: val[0],
            day: val[1],
            shift_type: val[2]
        }));
    }
}
