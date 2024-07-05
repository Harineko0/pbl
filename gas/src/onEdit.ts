import {sendAttendanceEmailHandler} from "./edit_handlers/sendAttendanceEmailHandler";

const handlers = [sendAttendanceEmailHandler];

export function onEdit(e: GoogleAppsScript.Events.SheetsOnEdit) {
    for (const handler of handlers) {
        handler(e);
    }
}
