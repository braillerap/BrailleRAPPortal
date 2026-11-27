import os
import shutil
import subprocess

class NMCliProxyError (Exception):
    """
        NMCliProxy exception
    """

class NMCliProxy:

    def runcmd (self, *args, Timeout=120, check=False) -> str:
        """
        The method run the system network manager nmcli in a subprocess
        """
        NMCLICMD = "nmcli"
        try:
            res = subprocess.run (
                [NMCLICMD, *args],
                capture_output = True,
                text = True,
                timeout = Timeout
            )
            print ("subprocess:", res.stdout, res.stderr)

        except subprocess.TimeoutExpired as ex:
            print (ex)
            raise NMCliProxyError("No answer from nmcli")
        except Exception as ex:
            print (ex)
            raise NMCliProxyError("Error calling nmcli", ex)

        if check and res.returncode != 0:
            print (res.stderr)
            raise NMCliProxyError('nmcli error')

        return res

    def list_connexions (self) -> []:
        print ("list_connexions")
        clist = []
        try:
            res = self.runcmd("-t", "connection", "show")
            clist = self.parse_result(res.stdout)
            print ("result clist", clist)
        except Exception as ex:
            print (ex)
            return clist
        return clist
    def get_ip4_from_id (self, id):
        ip = []
        try:
            res = self.runcmd("-t", "-g", "IP4.ADDRESS", "connection", "show", "id", id)
            clist = self.parse_result(res.stdout)
            print ("result ip", clist)
        except Exception as ex:
            print (ex)
            return ip

    def parse_result (self, nmcli_output:str)->[]:
        result = []
        res = nmcli_output.splitlines()
        for line in res:
            elms = line.split(':')
            result.append (elms)
        return result

if __name__ == '__main__':
    nmcli = NMCliProxy()

    cnxs = nmcli.list_connexions()

    #search for wlan0
    for cn in cnxs:
        if cn[-1] == "wlan0":
            print (nmcli.get_ip4_from_id(cn[0]))
