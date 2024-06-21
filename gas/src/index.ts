import {doGet} from "./http/doGet";

global.main = () => {
    console.log('Hello World!');
}

global.doGet = doGet;
