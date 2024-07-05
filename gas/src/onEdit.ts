import {sendAttendanceEmailHandler} from "./edit_handlers/attend";

const handlers = [sendAttendanceEmailHandler];

export function onEdit(e: GoogleAppsScript.Events.SheetsOnEdit) {
    for (const handler of handlers) {
        handler(e);
    }
}
