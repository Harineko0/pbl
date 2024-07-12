import {ShiftCreateApi} from "./db/repository/shiftCreateApi";
import {ShiftRepository} from "./db/repository/shiftRepository";

const sheetName = 'SHIFT_REQUEST_FORM';
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);

const shiftCreateApi = new ShiftCreateApi();
const shiftRepository = new ShiftRepository();
const ui = SpreadsheetApp.getUi();

export async function createShiftButton() {
    if (sheet === null) return;

    const year: number = sheet.getRange(4, 2).getValue();
    const month: number = sheet.getRange(4, 3).getValue();

    try {
        const shifts = await shiftCreateApi.createShift(year, month);
        shiftRepository.createMany(shifts);

    } catch (e) {
        ui.alert(`Error happened while creating shifts. ${e}`);
    }
}
