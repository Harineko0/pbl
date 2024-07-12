import {ShiftRequest} from "../entity/shiftRequest";
import {Dislike} from "../entity/dislike";
import {Shift} from "../entity/shift";
import {ShiftRequestRepository} from "./shiftRequestRepository";
import {DislikeRepository} from "./dislikeRepository";
import {ForCreate} from "../entity/_utils";

interface ShiftResponse {
    [k: string]: {
        [d in string]: string
    }
}

const shiftRequestRepository = new ShiftRequestRepository();
const dislikeRepository = new DislikeRepository();

export class ShiftCreateApi {
    private readonly uri = "https://pbl-vlf0.onrender.com/";

    async createShift(year: number, month: number): Promise<ForCreate<Shift>[]> {
        const requests = shiftRequestRepository.findMany();
        const dislikes = dislikeRepository.findMany();
        const body = JSON.stringify(this.convertToBody(year, month, requests, dislikes));

        Logger.log(body);

        try {
            const res = await UrlFetchApp.fetch(this.uri, {
                headers: {
                    'Content-Type': 'application/json',
                },
                method: 'post',
                payload: body
            });
            Logger.log(res);
            const json: ShiftResponse = JSON.parse(res.getContentText());

            const workerIds = Object.keys(json);

            return workerIds.map(worker => {
                const dates = Object.keys(worker);

                return dates.map(date => ({
                    date: new Date(date),
                    shift_type: json[worker][date],
                    worker_id: worker,
                }));
            }).reduce((acc, val) => acc.concat(val), []);

        } catch (e) {
            console.error(e);
            return Promise.reject(e);
        }
    }

    private convertToBody(year: number, month: number, requests: ShiftRequest[], dislikes: Dislike[]) {
        const workerIds = Array.from(new Set(requests.map(request => request.worker_id)));

        return {
            year,
            month,
            people: workerIds.map(worker => ({
                name: worker,
                requests: requests
                    .filter(req => req.worker_id === worker)
                    .map(req => ({
                        day: req.day,
                        type: req.shift_type,
                    })),
                bad: dislikes
                    .filter(dis => dis.worker_id === worker)
                    .map(dis => dis.target_id)
            }))
        };
    }
}
