"""
 * Authors - Yonatan Ratner & Shaked Levi
 * Date - 7.1.2022
"""
import os


def server_stop():
    command_stop_server = "\x03"  # this is the escape sequence for 'CTRL-C'.
    os.system(command_stop_server)


class RunServerScript:

    def __init__(self):
        self.parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.server_jar_path = self.parent_path + "/Ex4_Server_v0.0.jar"  # this is exact!
        self.server_name = "Ex4_Server_v0.0.jar"

    def server_activate(self, case: int):
        command_run_server = 'java -jar ' + self.server_name + ' ' + str(case)
        CWD = os.getcwd()
        os.chdir(self.parent_path)
        os.system(command_run_server)
        exit(0)
