import requests
import json


def get_token(student_id, password):
    url = 'http://172.17.173.97:8080/api/user/login'
    dl = {
        "student_id": student_id,
        "password": password
    }
    r = requests.post(url, dl)
    res = json.loads(r.text)
    if res['status'] == 200:
        return res['data']['token']
    else:
        return False


def create_game(private, token):
    url = 'http://172.17.173.97:9000/api/game'
    dl = {
        "private": private
    }
    headers = {
        "Authorization": token
    }
    r = requests.post(url, dl, headers=headers)
    res = json.loads(r.text)
    if res['code'] == 200:
        return res['data']['uuid']
    else:
        return False


def join_game(token, uuid):
    url = 'http://172.17.173.97:9000/api/game/{}'.format(uuid)
    headers = {
        "Authorization": token
    }
    r = requests.post(url, headers=headers)
    res = json.loads(r.text)
    if res['code'] == 200:
        return res['msg']
    else:
        return False


def operation(token, uuid, type, card=None):
    url = 'http://172.17.173.97:9000/api/game/{}'.format(uuid)
    headers = {
        "Authorization": token
    }
    if card is None:
        dl = {
            "type": type,
        }
    else:
        dl = {
            "type": type,
            "card": card
        }
    r = requests.put(url, dl, headers=headers)
    res = json.loads(r.text)
    return res['data']['last_code']


def get_operation(token, uuid):
    url = 'http://172.17.173.97:9000/api/game/{}/last'.format(uuid)
    headers = {
        "Authorization": token
    }
    r = requests.get(url, headers=headers)
    res = json.loads(r.text)
    if res['code'] == 200:
        return res['data']
    else:
        return False


if __name__ == '__main__':
    '''url = 'http://172.17.173.97:8080/api/user/login'
    url2 = 'http://172.17.173.97:9000/api/game'
    dl = {
        "student_id": "031902621",
        "password": "123456789q"
    }
    dl2 = {
        "private": True
    }
    headers = {
        'Authorization': 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYzNDgzMTkwNiwiZXhwIjoxNjM1Njk1OTA2fQ.eyJpZCI6OTl9.AQhcy6M56cyfvg7NIB34h8oXCwrEyamr6VmXIXFCQ8eFPwIur8PjlMgmhDpbKz1EoSGREj6i-rYvuvyVtAjyUg'
    }
    # r = requests.post(url, dl)
    # r = requests.post(url2, dl2, headers=headers)
    #print(r.text)
    #text = json.loads(r.text)

    # print(r.text)print(text['code'])
    # print(r.content)'''
    token = get_token("031902621", "123456789q")
    uuid = create_game(True, token)
    # print(create_game(True, token))
    print(join_game(token, uuid))
    # print(operation(token, uuid, 0))
    print(get_operation(token, uuid))
    # print(operation(token, uuid, 0))
    print(get_operation(token, uuid))
    # print(operation(token, uuid, 0))
    print(get_operation(token, uuid))





