import requests as rq
import json


# noinspection PyBroadException
class Sync:

    @staticmethod
    def newSession(name: str, script: str):
        try:
            rsp: rq.Response = rq.post('http://127.0.0.1:5000',
                data=json.dumps({'name': name, 'script': script}))
        except Exception:
            return None

        if rsp.status_code != 200:
            return None
        else:
            return int(json.loads(rsp.text)['sid'])
