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

import pandas as pd
import glob
import config

__author__ = 'techbk,thang,nhat'


class LogHandler(object):
    def __init__(self, path=None):
        if not path:
            self._path = config.LOG_PATH
        else:
            self._path = path

    def _log_path(self, name_service):
        path = {}
        # print(self._path)
        # print(glob.glob(self._path))
        if name_service == 'nova':
            path['nova'] = []
            for file in glob.glob(self._path + '*.log'):
                print(file)
                path['nova'].append(file)

        return path

    def _read_log(self, log_name):
        path = self._log_path(log_name)
        # print(path)
        cols = ['dates', 'pid', 'level', 'prog', 'infor']  # Set columns for DataFrame
        log = pd.DataFrame()
        for log_file in path[log_name]:
            # print(log_file)
            rl = pd.read_csv(log_file, sep=',', names=cols)  # Read file log and display to dataframe's format
            # print(rl)
            log = log.append(rl, ignore_index=True)
        # print(log)
        sort = log.sort_values(['dates'], ascending=False)  # sort time
        sort = sort.reset_index(drop=True)
        # print(sort)
        # print(sort.to_json(orient='index'))
        return sort.to_json(orient='index')

    def projectlog(self, project):
        """

        :param project:
        :return:
        """
        return self._read_log(project)

    def instancelog(self, instance):
        pass


if __name__ == "__main__":
    handler = LogHandler()
    handler.projectlog('nova')
