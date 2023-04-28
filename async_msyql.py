# -*- coding: UTF-8 -*- 
import threading
import traceback
from dongjsPy.MyLogger import logger
from django.conf import settings

class SelfThread(threading.Thread):
    def __init__(self,sql,ds,service,sha1):
        threading.Thread.__init__(self)
        try:
            self.inception_check_params = "--enable-check=1;--enable-ignore-warnings;";
            self.inception_split_params = "--enable-split;--enable-execute;";
            self.inception_execute_params = "--enable-execute;--enable-ignore-warnings;--disable-remote-backup;";

            self.inception_host = getattr(settings, 'INCEPTION_HOST')
            self.inception_port = int(getattr(settings, 'INCEPTION_PORT'))

            self.inception_remote_backup_host = getattr(settings, 'INCEPTION_REMOTE_BACKUP_HOST')
            self.inception_remote_backup_port = int(getattr(settings, 'INCEPTION_REMOTE_BACKUP_PORT'))
            self.inception_remote_backup_user = getattr(settings, 'INCEPTION_REMOTE_BACKUP_USER')
            self.inception_remote_backup_password = getattr(settings, 'INCEPTION_REMOTE_BACKUP_PASSWORD')

            self.sql = sql
            self.ds = ds
            self.service = service
            self.sha1=sha1
        except BaseException as e:
            trace_message = traceback.format_exc()
            logger.error("SelfThread.__init__ failed:\n" + trace_message)

    # 缁ф壙Thread绫婚渶瑕佹樉绀簉un鏂规硶锛岀嚎绋嬪湪寮�鍚悗杩愯
    def run(self):
        logger.info('start SelfThread.run')
        self.service._sql_async_execute(self.sql,self.ds,self.sha1)


