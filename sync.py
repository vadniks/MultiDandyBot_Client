from typing import Callable, List, Tuple
import requests as rq
import json
from time import sleep
from threading import Thread


sid: int
pid: int
name: str
HOST = 'http://127.0.0.1:5000'
THRESHOLD = 0.1 # seconds


def newSession(_name: str, script: str) -> bool:
    global sid, pid, name
    name = _name

    try:
        rsp: rq.Response = rq.post(f'{HOST}/new',
                                   json={'name': name, 'script': script, 'level': 0})
    except Exception: return True

    if rsp.status_code != 200:
        return False
    else:
        sid = int(json.loads(rsp.text)['sid'])
        pid = int(json.loads(rsp.text)['pid'])
        print(sid, pid)
        return True


def _checkForPlayers() -> List[str] | None:
    try:
        rsp: rq.Response = rq.get(f'{HOST}/chk/{pid}')
    except Exception: return None

    if rsp.status_code != 200:
        return None
    else:
        a = json.loads(rsp.text)
        return a


def waitForPlayers(onFinish: Callable, onWait: Callable = None):
    def wait():
        while True:
            if (players := _checkForPlayers()) \
                    is not None and len(players) > 0:
                onFinish(players)
                break
            if onWait is not None:
                onWait()
            sleep(THRESHOLD)

    thread = Thread(target=wait)
    thread.daemon = True
    thread.start()


def quitt():
    try: rq.post(f'{HOST}/qt/{pid}')
    except Exception: pass


def tracePlayers(onUpdate: Callable):
    #                           id   lvl   x    y
    def request() -> List[Tuple[int, int, int, int]] | None:
        try:
            rsp: rq.Response = rq.post(f'{HOST}/trc/{pid}/{sid}')
        except Exception:
            return None

        return json.loads(rsp.text) if rsp.status_code == 200 else None

    def trace():
        while True:
            if (positions := request()) is not None:
                assert len(positions) > 0
                onUpdate(positions)
            sleep(THRESHOLD)

    thread = Thread(target=trace)
    thread.daemon = True
    thread.start()
