import requests as rq


class Server:

    @staticmethod
    def newSession(name: str, script: str):
        try:
            rsp: rq.Response = rq.post('http://127.0.0.1:5000',
                data={'name': name, 'script': script})
        except Exception:
            return None

        if rsp.status_code != 200:
            return None
