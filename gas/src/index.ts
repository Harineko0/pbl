import {doGet} from "./http/doGet";
import {onEdit} from "./attend_button/onEdit";

global.main = () => {
    console.log('Hello World!');

    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    ScriptApp.newTrigger('onEdit').forSpreadsheet(spreadsheet).onEdit();
}

global.doGet = doGet;
global.onEdit = onEdit;
