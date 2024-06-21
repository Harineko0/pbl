import {RequestHandler, Response} from "./requestHandler";

type Parameter = {
    'swap-id': string
}

const validateParameter = (param: {[p: string]: string}): Parameter | undefined => {
    if ('swap-id' in param) {
        return {'swap-id': param['swap-id']}
    }
    return undefined;
}

export const swapShiftHandler: RequestHandler = (req) => {
    const param = validateParameter(req.parameter);

    if (param === undefined) {
        return Response.text('Parameter is wrong. (?swap-id=XXX)');
    }

    const swapId = param['swap-id'];

    // TODO: シフト交換ロジックを呼ぶ
    // ...

    return Response.text('Shift swap complete.');
}
