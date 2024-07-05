import {WorkerRepository} from "./db/repository/workerRepository";
import {SwapRepository} from "./db/repository/swapRepository";
import {ShiftRepository} from "./db/repository/shiftRepository";
import {getSwapShiftUrl} from "./http/swapShiftHandler";

const workerRepository = new WorkerRepository();
const swapRepository = new SwapRepository();
const shiftRepository = new ShiftRepository();

const sheetName = 'SWAP_FORM';
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);

export function swapButton() {
    if (sheet === null) return;

    const swapDay: Date = sheet.getRange(3, 2).getValue();
    const targetWorkerId: string = sheet.getRange(3, 3).getValue();
    const targetWorker = workerRepository.get(targetWorkerId);

    if (targetWorker == null) {
        SpreadsheetApp.getUi().alert(`Worker not found. ${targetWorkerId}`);
        return;
    }

    const currentUserEmail = Session.getEffectiveUser().getEmail();
    const currentWorker = workerRepository.getByEmail(currentUserEmail);

    if (currentWorker == null) {
        SpreadsheetApp.getUi().alert("You are not registered as a worker.");
        return;
    }

    const targetShift = shiftRepository.getByDateAndWorker(swapDay, targetWorkerId);
    const myShift = shiftRepository.getByDateAndWorker(swapDay, currentWorker.id);

    if (targetShift == null || myShift == null) {
        SpreadsheetApp.getUi().alert("Shift not found.");
        return;
    }

    const swap = swapRepository.create({
        new_shift_id: targetShift.id, old_shift_id: myShift.id
    });

    GmailApp.sendEmail(targetWorker.email, "Swap Request",
        `Swap request has been sent to you. Please check the swap sheet. ${getSwapShiftUrl(swap.id)}`);
}
