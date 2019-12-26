# !/usr/bin/python
# -*- coding: UTF-8 -*-

import requests

appKey = '12574478'

def get_params(api, v, data, t, sign=''):
    return {
        'type': 'originaljson',
        'jsv': '2.4.0',
        'appKey': appKey,
        't': t,
        'AntiCreep': 'true',
        'api': api,
        'v': v,
        'data': data,
        'sign': sign,

    }


def get_headers(cookie=''):
    return {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'accept': '*/*',
        'cookie': cookie,
        'authority': 'h5api.m.taobao.com',
    }


def get_url(api, v):
    return 'https://h5api.m.taobao.com/h5/{0}/{1}'.format(api, v)


def http_get_mtopAPI(api, v, data, t, sign, _m_h5_tk, _m_h5_tk_enc):
    url = get_url(api, v)
    params_with_sign = get_params(api, v, data, t, sign)
    cookie = '_m_h5_tk={0};_m_h5_tk_enc={1}'.format(_m_h5_tk, _m_h5_tk_enc)
    return requests.get(url, headers=get_headers(cookie), params=params_with_sign)


if __name__ == '__main__':
    t = 1577286443561
    api = 'mtop.mediaplatform.video.livedetail.itemlist'
    v = '1.0'
    data = '{"type":"0","liveId":"247413960423","creatorId":"63239528"}'
    sign = 'bb9003938280a631ad72eb26b9612560'
    _m_h5_tk = '4893f2d2097a8eb027ca501300a8d0d9_1577294004211'
    _m_h5_tk_enc = '7f686dbb9133153e36a68d6cf6aa7a00'
    response = http_get_mtopAPI(api, v, data, t, sign, _m_h5_tk, _m_h5_tk_enc)
    print(response.json())
