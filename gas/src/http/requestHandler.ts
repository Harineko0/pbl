export type Request = {
    parameter: { [p: string]: string }
}

export class Response {
    private constructor(public readonly content: GoogleAppsScript.Content.TextOutput) {
    }

    static text(text: string) {
        return new Response(ContentService.createTextOutput(text).setMimeType(ContentService.MimeType.TEXT));
    }
}

export type RequestHandler = (req: Request) => Response
