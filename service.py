# -*- coding: utf-8 -*-
#
# Copyright 2014 - StackStorm, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# from aiohttp import MultiDict
# from urlhandler import Url_handler

import asyncio
from aiohttp import web
# import os
import json
import loghandler
import pcaphandler
import config

__author__ = 'techbk'


class UrlHandler(object):
    def __init__(self, _loop):
        """

        :param _loop: object
        """
        self._loop = _loop
        self._pcapfilehandler = pcaphandler.PcapFileHandler()
        self._loghandler = loghandler.LogHandler()

    @asyncio.coroutine
    def pcap(self, request):
        # print(request.headers)
        """

        :param request:
        :return:
        """
        print(request.GET)
        # print(request.content_type)
        # json_data = yield from request.json()
        # print(json_data)
        data = yield from request.post()
        print(data)

        input_file = data['file'].file
        content = input_file.read()
        asyncio.async(self._pcapfilehandler.handle_file_pcap(data['ID_Client'], data['file'].filename, content))

        return web.Response(body=b"ok")

    @asyncio.coroutine
    def test(self, request):
        """

        :param request:
        :return: web.Response
        """
        print(request.path_qs)

        print(request.GET['project'])
        # text = yield from request.text()
        # print(text)
        # text = "{'test':'ok'}"
        text = json.dumps({'test': 'ok'})
        print(text)
        return web.Response(body=text.encode('utf-8'))

    @asyncio.coroutine
    def instancelog(self, request):
        instance = request.GET['instance']

        jsonlog = self._loghandler.instancelog(instance)
        jsonlog = jsonlog.encode('utf-8')

        return web.Response(body=jsonlog)

    @asyncio.coroutine
    def projectlog(self, request):
        project = request.GET['project']

        jsonlog = self._loghandler.projectlog(project)
        print(jsonlog)
        jsonlog = jsonlog.encode('utf-8')

        return web.Response(body=jsonlog)


@asyncio.coroutine
def index(request):
    print(request.path)
    return web.Response(body=b"Welcome")


@asyncio.coroutine
def init(_loop):
    """
    tao task pasrsing file pcap
    asyncio.async()
    :param _loop:
    :return:
    """
    url_handler = UrlHandler(_loop)

    app = web.Application(loop=_loop)

    # app.router.add_route('GET', '/', index)
    app.router.add_route('POST', '/pcap', url_handler.pcap)
    app.router.add_route('GET', '/test', url_handler.test)
    app.router.add_route('GET', '/projectlog', url_handler.projectlog)
    app.router.add_route('GET', '/instancelog', url_handler.instancelog)

    # app.router.add_route('GET', '/doblastn', url_handler.doblastn)
    # app.router.add_route('GET', '/dostart_app1', url_handler.do_start_app1)
    # app.router.add_route('GET', '/checkresult/{id}', url_handler.check_result)

    handler = app.make_handler()
    srv = yield from _loop.create_server(handler, config.SERVICE_IP, config.SERVICE_PORT)
    print("Server started at http://0.0.0.0:8080")
    return srv, handler


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    srv, handler = loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
