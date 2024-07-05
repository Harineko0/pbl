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

export const getSwapShiftUrl = (swapId: string) => {
    const authority = "https://script.google.com/macros/library/d/1u3X2dxkUIvtSnEO45lXblg5Ej_dDKF_txqD6r10sTydek73xqq9mfp1r/18";
    return `${authority}/swap?swap-id=${swapId}`;
}
