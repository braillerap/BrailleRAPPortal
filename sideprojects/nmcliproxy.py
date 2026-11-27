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
            clist = self.parse_result_array(res.stdout)
            print ("result clist", clist)
        except Exception as ex:
            print (ex)
            return clist
        return clist

    def if_down(self, id) -> bool:
        """
        Disable the connection identied by id (ifdown)
        """
        try:
            result = self.runcmd("connection", "down", "id", id)

            return result.returncode == 0
        except Exception as ex:
            print (ex)
        return False

    def if_up(self, id) -> bool:
        """
        Disable the connection identied by id (ifdown)
        """
        try:
            result = self.runcmd("connection", "up", "id", id)

            return result.returncode == 0
        except Exception as ex:
            print (ex)
        return False

    def is_exist(self, id:str) -> bool:
        """
        Return True if the connection identified by id exist in
        system configuration
        """
        result = self.runcmd("connection", "show", "id", id,
                         check=False)

        return result.returncode == 0

    def get_ip4_from_id (self, id) -> []:
        """
        Return a string containing the IP V4 address assotiated with the
        connexion identified by id
        """
        ip = []
        try:
            res = self.runcmd("-t", "-g", "IP4.ADDRESS", "connection", "show", "id", id)
            clist = self.parse_result_array(res.stdout)
            for ipadr in clist:
                ip.append (ipadr)
        except Exception as ex:
            print (ex)

        return ip

    def is_up(self, id:str) -> bool:
        """
        Return true if the connection identified by id is connected (active)

        """
        try:
            result = self.runcmd("-t", "-f", "GENERAL.STATE",
                           "connection", "show", "id", id)

            return result.stdout.strip().endswith(":activated")
        except Exception as ex:
            print (ex)
            return False
        return False

    def parse_result_array (self, nmcli_output:str)->[]:
        """
        The method parse the returning string of nmcli to build an array of
        outputed line. Each line is splited by the ":"
        separator (nmcli option -t)
        """
        result = []
        res = nmcli_output.splitlines()
        for line in res:
            elms = line.split(':')
            result.append (elms)
        return result

if __name__ == '__main__':
    nmcli = NMCliProxy()

    cnxs = nmcli.list_connexions()
    wifi = ""
    #search for wlan0
    for cn in cnxs:
        if cn[2] == "802-11-wireless":
            wifi = cn[0] # save wifi connection
            print (cn[0], nmcli.get_ip4_from_id(cn[0]))
    for cn in cnxs:
        print (cn[0], ":UP" if nmcli.is_up(cn[0]) else ":Down")

    for cn in cnxs:
        print (cn[0], ":Exist" if nmcli.is_exist(cn[0]) else ":Unknown")

    print ("bidon", ":Exist" if nmcli.is_exist("bidon") else ":Unknown")
