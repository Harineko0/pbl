import {WorkerRepository} from "../db/repository/workerRepository";

const sheetName = "CALENDER";
const workerRepository = new WorkerRepository();

const ownerEmail = "harinekouniv@gmail.com";
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);

export function sendAttendanceEmailHandler(e: GoogleAppsScript.Events.SheetsOnEdit) {
    if (e.source.getSheetName() !== 'CALENDER') return;
    if (e.range.getColumn() !== 1) return;

    if (e.oldValue === "TRUE" || e.value === "FALSE") {
        Logger.log("Checkbox is unchecked or already checked.");
        return;
    }

    const row = e.range.getRow();
    if (sheet === null) {
        console.error(`Sheet ${sheetName} not found`);
        return;
    }

    const id = sheet.getRange(row, 2).getValue();

    if (typeof id !== "string") {
        console.error(`id is not string: ${id}`);
        return;
    }

    const worker = workerRepository.get(id);

    if (worker == null) {
        console.error(`Worker not found: ${id}`);
        return;
    }

    console.log(`Send email to ${worker.email}`);
    GmailApp.sendEmail(ownerEmail, "出勤確認", `出勤ボタンが押されました。(${worker.email})`);
}

export function resetCheckbox() {
    if (sheet === null) {
        console.error(`Sheet ${sheetName} not found`);
        return;
    }

    for (let i = 2; i <= sheet.getLastRow(); i++) {
        sheet.getRange(i, 1).setValue("FALSE");
    }
}
