import {doGet} from "./http/doGet";
import {onEdit} from "./attend_button/onEdit";
import {resetCheckbox} from "./attend_button/attend";

global.main = () => {
    console.log('Hello World!');
}

global.doGet = doGet;
global.onEdit = onEdit;
global.resetCheckbox = resetCheckbox;
