import os
import shutil
import subprocess

class NMCliProxyError (Exception):
    """
        NMCliProxy exception
    """

class NMCliProxy:
    nmclicmd = "nmcli"
    def runcmd (*argument, Timeout=120 check=False) -> str:
        try:
            res = subprocess.run (
                [nmclicmd, *args],
                capture_output = True,
                text = True,
                timeout = Timeout
            )
        except subprocess.TimeoutExpired as ex:
            raise NMCliProxyError("No answer from nmcli")
        if check and res.returncode != 0:
            raise NMCliProxyError('nmcli error')

        return res

    def list_connexions () -> []:
        clist = []
        try:
            res = self.runcmd(["-t", "connection", "show"])
            print (res)
        except:
            return

if __name__ == '__main__':
    nmcli = NMCliProxy()

    nmcli.list_connexions()

    
