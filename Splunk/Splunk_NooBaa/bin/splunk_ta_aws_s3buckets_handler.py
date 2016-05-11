"""
Custom REST Endpoint for enumerating AWS S3 Bucket.
"""

import os
import sys

import splunk
import splunk.admin

from taaws.aws_accesskeys import APPNAME, KEY_NAMESPACE, KEY_OWNER


import logging
from taaws.log import setup_logger
from taaws.aws_accesskeys import AwsAccessKeyManager
from taaws.s3util import connect_s3
import threading

logger = setup_logger(APPNAME + '-RestEndpoints', level=logging.DEBUG)


def log_enter_exit(func):
    def wrapper(*args, **kwargs):
        logger.debug("{} entered.".format(func.__name__))
        result = func(*args, **kwargs)
        logger.debug("{} exited.".format(func.__name__))
        return result
    return wrapper


def timed(timeout, func,default=None, args=(), kwargs={}):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise TimeLimitExpired
    """
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default

        def run(self):
            self.result = func(*args, **kwargs)

    it = FuncThread()
    it.start()
    it.join(timeout)
    return it.result

def all_buckets(s3_conn):
    return s3_conn.get_all_buckets()

class ConfigHandler(splunk.admin.MConfigHandler):

    @log_enter_exit
    def setup(self):
        self.supportedArgs.addOptArg('aws_account')
        self.supportedArgs.addReqArg('host_name')

    @log_enter_exit
    def handleList(self, confInfo):

        km = AwsAccessKeyManager(KEY_NAMESPACE, KEY_OWNER, self.getSessionKey())

        aws_account = self.callerArgs['aws_account'][0] if self.callerArgs['aws_account'] is not None else ""
        host_name = self.callerArgs['host_name'][0] if self.callerArgs['host_name'] is not None else ""
        if not aws_account:
            confInfo['S3BucketsResult'].append('buckets', [])
            return

        acct = km.get_accesskey(name=aws_account)
        if not acct:
            raise Exception(aws_account + " selected is incorrect, Setup App first.")

        connection = connect_s3(acct.key_id, acct.secret_key,
                                self.getSessionKey(),
                                host_name)

        rs = timed(25,all_buckets,[],(connection,))
        
        rlist = []

        for r in rs:
            rlist.append(r.name)

        confInfo['S3BucketsResult'].append('buckets', rlist)


@log_enter_exit
def main():
    splunk.admin.init(ConfigHandler, splunk.admin.CONTEXT_NONE)


if __name__ == '__main__':

    main()
