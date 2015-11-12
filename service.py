__author__ = 'techbk'

import asyncio
from aiohttp import web


# from aiohttp import MultiDict
# from urlhandler import Url_handler


class PcapFileHandler:
    def __init__(self):

        pass

    @asyncio.coroutine
    def handler_file_pcap(self, filename, content):
        print( 'File name upload:', filename )

        dest_filename = 'pcap/' + filename

        destination = open( dest_filename, 'wb+' )
        destination.write( content )

        print( 'Saving file is DONE' )
        return True



class UrlHandler(object):
    def __init__(self, loop):
        self._pcapfilehandler = PcapFileHandler()
        pass



    @asyncio.coroutine
    def pcap(self, request):
        print(request.headers)
        json_data = yield from request.json()
        print(json_data)
        data = yield from request.post()
        print(data)
        input_file = data['file'].file
        content = input_file.read()
        asyncio.async( self._pcapfilehandler.handler_file_pcap( data['file'].filename, content ) )

        return web.Response( body=b"ok" )
        # return web.Response(body=content, headers=MultiDict({'CONTENT-DISPOSITION': input_file}))


@asyncio.coroutine
def index(request):
    return web.Response( body=b"Welcome" )


@asyncio.coroutine
def init(loop):
    #tao task pasrsing file pcap
    #asyncio.async()
    url_handler = UrlHandler( loop )

    app = web.Application( loop=loop )

    # app.router.add_route('GET', '/', index)
    app.router.add_route( 'POST', '/pcap', url_handler.pcap )

    # app.router.add_route('GET', '/doblastn', url_handler.doblastn)
    # app.router.add_route('GET', '/dostart_app1', url_handler.do_start_app1)
    # app.router.add_route('GET', '/checkresult/{id}', url_handler.check_result)

    handler = app.make_handler( )
    srv = yield from loop.create_server( handler, '0.0.0.0', 8080 )
    print( "Server started at http://0.0.0.0:8080" )
    return srv, handler


if __name__ == '__main__':
    loop = asyncio.get_event_loop( )
    srv, handler = loop.run_until_complete( init( loop ) )
    try:
        loop.run_forever( )
    except KeyboardInterrupt:
        pass
