import {doGet} from "./http/doGet";
import {onEdit} from "./onEdit";
import {resetCheckbox} from "./edit_handlers/attend";
import {swapButton} from "./swapButton";

global.main = () => {
    console.log('Hello World!');
}

global.doGet = doGet;
global.onEdit = onEdit;
global.resetCheckbox = resetCheckbox;
global.swapButton = swapButton;
