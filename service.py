__author__ = 'techbk'

import asyncio
from aiohttp import web
from aiohttp import MultiDict
#from urlhandler import Url_handler


class Url_handler(object):
    def __init__(self,loop):
        pass
    @asyncio.coroutine
    def pcap(self,request):
        data = yield from request.post()
        #print(data)
        # filename contains the name of the file in string format.
        filename = data['file'].filename
        #filename = 'openstack_dashboard/dashboards/techbk_head/firstpanel/pcap/'+ f.name
        print(filename)
        # input_file contains the actual file data which needs to be
        # stored somewhere.

        input_file = data['file'].file

        content = input_file.read()
        for line in content:
            print(line)
        #print(content)
        dest_filename = 'pcap/'+ filename
        #filename = 'pcap/'+ f.name
        destination = open(dest_filename, 'wb+')
        destination.write(content)


        return web.Response(body=content)
        #return web.Response(body=content, headers=MultiDict({'CONTENT-DISPOSITION': input_file}))

@asyncio.coroutine
def index(request):
    return web.Response(body = b"Welcome")


@asyncio.coroutine
def init(loop):
    url_handler = Url_handler(loop)

    app = web.Application(loop = loop)

    #app.router.add_route('GET', '/', index)
    app.router.add_route('POST', '/pcap', url_handler.pcap)


    #app.router.add_route('GET', '/doblastn', url_handler.doblastn)
    #app.router.add_route('GET', '/dostart_app1', url_handler.do_start_app1)
    #app.router.add_route('GET', '/checkresult/{id}', url_handler.check_result)

    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '0.0.0.0', 8080)
    print("Server started at http://0.0.0.0:8080")
    return srv, handler





if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    srv, handler = loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass