import {onCheckboxChecked} from "./attend";

export function onEdit(e: GoogleAppsScript.Events.SheetsOnEdit) {
    if (e.source.getSheetName() !== 'CALENDER') return;
    const range = e.range;
    const col = range.getColumn();

    if (col !== 1) return;

    if (e.oldValue === "TRUE" || e.value === "FALSE") {
        console.log("Checkbox is unchecked or already checked.");
        return;
    }
    onCheckboxChecked(range.getRow());
}
