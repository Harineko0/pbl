import {RequestHandler, Response} from "./requestHandler";
import {shiftswap} from "../swap/swapShift";

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

    shiftswap(swapId);

    return Response.text('Shift swap complete.');
}

export const getSwapShiftUrl = (swapId: string) => {
    const authority = "https://script.google.com/macros/s/AKfycbzUt8PBNl6AtiJefQe59A3fhEI_GSiVcVxR8gu6cj_3kiBjoHNk1Jmi9DjHIAFJ4BSTSg/exec";
    return `${authority}/swap?swap-id=${swapId}`;
}
