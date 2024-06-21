import {swapShiftHandler} from "./swapShiftHandler";

const handlers = new Map([
    ['/swap', swapShiftHandler]
])

/**
 * GET リクエストを受け取る
 * https://script.google.com/macros/s/<app_id>/exec
 * @param e
 */
export function doGet(e: GoogleAppsScript.Events.DoGet) {
    const path = e.pathInfo;
    const handler = handlers.get(path);

    if (handler === undefined) {
        return ContentService.createTextOutput('Not Found');
    }

    const res = handler({parameter: e.parameter});
    return res.content;
}

