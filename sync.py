from typing import Callable, List, Tuple
import requests as rq
import json
from time import sleep
from threading import Thread


sid = -1
pid = 0
name: str
level = 0
_HOST = 'http://127.0.0.1:5000'
_THRESHOLD = 0.5 # seconds
_waiterThread: Thread
_canWaitForServer = True
solo = False


def connect(_name: str, script: str) -> bool:
    global sid, pid, name
    name = _name

    try:
        rsp: rq.Response = rq.post(f'{_HOST}/new',
            json={'name': name, 'script': script, 'level': level})
    except Exception: return False

    if rsp.status_code == 200:
        if (sid := int(json.loads(rsp.text)['sid'])) == -1:
            return False

        pid = int(json.loads(rsp.text)['pid'])
        print(sid, pid)
        return True


def checkForPlayers() -> List[Tuple[int, str]] | None:
    try:
        rsp: rq.Response = rq.get(f'{_HOST}/chk/{pid}')
    except Exception: return None

    if rsp.status_code != 200:
        return None
    else:
        a = json.loads(rsp.text)
        return a


def waitForPlayers(onFinish: Callable, onWait: Callable = None):
    global _waiterThread, _canWaitForServer

    def wait():
        while _canWaitForServer:
            if (players := checkForPlayers()) \
                    is not None and len(players) > 0:
                onFinish(players)
                break
            if onWait is not None:
                onWait()
            sleep(_THRESHOLD)

    _waiterThread = Thread(target=wait)
    _waiterThread.daemon = True
    _waiterThread.start()


def endWaiter():
    global _canWaitForServer
    _canWaitForServer = False
    _waiterThread.join()


def quitt():
    print('quit')
    try: rq.post(f'{_HOST}/qt/{pid}')
    except Exception: pass


#                                id  name level  x    y   gold
def tracePlayers() -> List[Tuple[int, str, int, int, int, int]] | None:
    if solo: return None
    try: rsp: rq.Response = rq.get(f'{_HOST}/trc/{sid}/{pid}')
    except Exception: return None

    if rsp.status_code != 200: return None

    jsn = json.loads(rsp.text)
    _list = []
    for i in jsn:
        _list.append((int(i[0]), i[1], int(i[2]), int(i[3]),
                      int(i[4]), int(i[5])))
    return _list


def updatePlayer(lvl: int, x: int, y: int, goldAmount: int):
    if solo: return
    try:
        rq.post(f'{_HOST}/upd/{pid}',
                json={'level': lvl, 'x': x, 'y': y, 'gold': goldAmount})
    except Exception: pass


#                                     x    y
def updateBoard(goldTakenFrom: Tuple[int, int]):
    if solo: return
    try: rq.post(f'{_HOST}/brd/{sid}/{level}',
                 json={'pid': pid, 'gtf_x': goldTakenFrom[0], 'gtf_y': goldTakenFrom[1]})
    except Exception: pass


#                              pid   x    y
def traceBoard() -> List[Tuple[int, int, int]] | None:
    if solo: return None
    try: rsp: rq.Response = rq.get(f'{_HOST}/trc_b/{sid}/{pid}/{level}')
    except Exception: return None

    if rsp.status_code != 200: return None

    jsn = json.loads(rsp.text)
    _list = []
    for i in jsn:
        _list.append((int(i[0]), int(i[1]), int(i[2])))
    return _list


def getCurrentGoldAmountOnBoard() -> int | None:
    if solo: return None
    try: rsp: rq.Response = rq.get(f'{_HOST}/gld/{sid}/{level}')
    except Exception: return None

    if rsp.status_code != 200: return None
    return int(rsp.text)


#                             name score date
def getSavedPlayers() -> List[Tuple[str, int, int]] | None:
    try: rsp: rq.Response = rq.get(f'{_HOST}/db',
            json={'mode': 'select', 'pid': pid})
    except Exception: return None

    if rsp.status_code != 200: return None

    jsn = json.loads(rsp.text)
    _list = []
    [_list.append((i[0], int(i[1]), int(i[2]))) for i in jsn]
    return _list


def saveCurrentPlayerResult():
    if solo: return
    print('save')
    try: rq.Response = rq.post(f'{_HOST}/db',
            json={'mode': 'insert', 'pid': pid})
    except Exception: pass
