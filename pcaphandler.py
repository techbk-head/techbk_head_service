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


import os
import json
import asyncio

__author__ = 'techbk'


def handle_file_info(directory, filename):
    # print(directory)
    # print(os.path.isfile(directory+'info'))
    """

    :param directory:
    :param filename:
    """
    if not os.path.isfile(directory + 'info'):
        with open(directory + 'info', 'w') as outfile:
            json.dump({filename: 0}, outfile)
            outfile.close()
    else:
        with open(directory + 'info', 'w+') as outfile:
            info = json.load(outfile)
            info[filename] = 0
            outfile.seek(0)
            outfile.write(json.dumps(info))
            outfile.truncate()
            outfile.close()

    with open(directory + 'info', 'r') as outfile:
        # print(json.load(outfile))
        outfile.close()


class PcapFileHandler:
    def __init__(self):
        pass

    @asyncio.coroutine
    def handle_file_pcap(self, appname, filename, content):
        """

        :param appname:
        :param filename:
        :param content:
        :return:
        """
        print('File name upload:', filename)
        directory = 'pcap/' + appname + '/'

        if not os.path.exists(directory):
            os.makedirs(directory)

        # dest_filename = directory + filename
        with open(directory + filename, 'wb+') as destination:
            destination.write(content)
            destination.close()

        handle_file_info(directory, filename)

        print('Saving file is DONE')
        return True
