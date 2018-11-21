# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from __future__ import print_function

import os
import pymqi
import sys

# python3 compatability
try:
    zrange = xrange
except NameError:
    zrange = range

host = os.environ.get('HOST', 'localhost')
port = os.environ.get('PORT', '11414')
user = os.environ.get('USERNAME', 'admin')
password = os.environ.get('PASSWORD', 'passw0rd')

channel = os.environ.get('CHANNEL', 'DEV.ADMIN.SVRCONN')

queue_manager = os.environ.get('QUEUE_MANAGER', 'datadog')
queue_name = os.environ.get('QUEUE', 'DEV.QUEUE.1')

conn_info = '%s(%s)' % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

queue = pymqi.Queue(qmgr, queue_name)

range = int(os.environ.get('RANGE', '10'))

for i in zrange(range):
    try:
        message = 'Hello from Python! Message {}'.format(i)
        print("sending message: {}".format(message))
        queue.put(message.encode())
    except Exception as e:
        print(e)
        queue.close()
        qmgr.disconnect()
        sys.exit()

queue.close()
qmgr.disconnect()
sys.exit()
