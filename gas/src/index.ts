import {doGet} from "./http/doGet";
import {onEdit} from "./onEdit";
import {resetCheckbox} from "./edit_handlers/sendAttendanceEmailHandler";
import {swapButton} from "./swapButton";
import {createShiftButton} from "./createShiftButton";

global.main = () => {
    console.log('Hello World!');
}

global.doGet = doGet;
global.onEdit = onEdit;
global.resetCheckbox = resetCheckbox;
global.swapButton = swapButton;
global.createShiftButton = createShiftButton;
