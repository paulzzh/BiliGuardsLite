import sys
import time

class Loggger():
    debug_level = 0
    info_level = 1
    warning_level = 2
    error_level =3
    def __init__(self,filename):
        self.filename = filename

    def debug(self,data):
        data = f"{self.timestamp()} [Line:{sys._getframe().f_lineno}] - DEBUG: {data}"
        print("\033[34;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")

    def info(self,data):
        data = f"{self.timestamp()} [Line:{sys._getframe().f_lineno}] - INFO: {data}"
        print("\033[32;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")

    def warning(self,data):
        data = f"{self.timestamp()} [Line:{sys._getframe().f_lineno}] - WARNING: {data}"
        print("\033[33;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")

    def error(self,data):
        data = f"{self.timestamp()} [Line:{sys._getframe().f_lineno}] - ERROR: {data}"
        print("\033[31;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")

    def critical(self,data):
        data = f"{self.timestamp()} [Line:{sys._getframe().f_lineno}] - CRITICAL: {data}"
        print("\033[35;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")
    
    def timestamp(self):
        str_time = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
        return str_time

Log = Loggger(".\Src\BiliBiliHelper.log")
