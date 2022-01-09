"""
 * Authors - Yonatan Ratner & Shaked Levi
 * Date - 7.1.2022
"""
import os
from Ex4.client_python.Misc import Misc


def server_stop():
    command_stop_server = "\x03"  # this is the escape sequence for 'CTRL-C'.
    os.system(command_stop_server)


class RunServerScript:

    def __init__(self):
        self.server_name = "Ex4_Server_v0.0.jar"
        self.parent_path = Misc.resource_path(relative_path='data')

    def server_activate(self, case: int):
        command_run_server = 'java -jar ' + os.path.join(self.parent_path, self.server_name) + ' ' + str(case)
        os.chdir(self.parent_path)
        os.system(command_run_server)
        exit(0)
