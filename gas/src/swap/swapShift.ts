export function shiftswap(id: string) {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const shiftSheet = spreadsheet.getSheetByName("shifts");
    const swapSheet = spreadsheet.getSheetByName("swaps");
    if (shiftSheet == null || swapSheet == null) {
        return;
    }
    const shiftLastRow = shiftSheet.getLastRow();
    const swapLastRow2 = swapSheet.getLastRow();
    let swap = null;
    for (let i = 1; i < swapLastRow2; i++) {
        const swapId = swapSheet.getRange(i + 1, 1).getValue()
        if (swapId == id) {
            swap = swapSheet.getRange(i + 1, 2, 1, 2).getValues();
            break;
        }
    }
    if (swap == null) {
        return;
    }
    let targetShift: GoogleAppsScript.Spreadsheet.Range | null = null;
    let srcShift: GoogleAppsScript.Spreadsheet.Range | null = null;

    for (let i = 0; i < shiftLastRow - 1; i++) {
        const shiftId = shiftSheet.getRange(i + 2, 1).getValue();
        if (shiftId == swap[0][0]) {
            targetShift = shiftSheet.getRange(i + 2, 4);
        } else if (shiftId == swap[0][1]) {
            srcShift = shiftSheet.getRange(i + 2, 4);
        }
    }
    if (targetShift == null || srcShift == null) {
        return;
    }
    let targetValues = targetShift.getValues();
    let srcValues = srcShift.getValues();
    targetShift.setValues(srcValues);
    srcShift.setValues(targetValues);
}
