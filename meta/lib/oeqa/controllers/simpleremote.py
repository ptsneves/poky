from oeqa.utils.sshcontrol import SSHControl
from oeqa.controllers.sshtarget import OESSHTarget

class SimpleRemoteTarget(OESSHTarget):

    def __init__(self, td, logger, **kwargs):
        super(SimpleRemoteTarget, self).__init__(td, logger, **kwargs)
        addr = td['TEST_TARGET_IP'] or bb.fatal('Please set TEST_TARGET_IP with the IP address of the machine you want to run the tests on.')
        self.ip = addr.split(":")[0]
        try:
            self.port = addr.split(":")[1]
        except IndexError:
            self.port = None
        self.logger.info("Target IP: %s" % self.ip)
        self.server_ip = td['TEST_SERVER_IP']
        if not self.server_ip:
            try:
                self.server_ip = subprocess.check_output(['ip', 'route', 'get', self.ip ]).split("\n")[0].split()[-1]
            except Exception as e:
                bb.fatal("Failed to determine the host IP address (alternatively you can set TEST_SERVER_IP with the IP address of this machine): %s" % e)
        self.logger.info("Server IP: %s" % self.server_ip)

    def deploy(self):
        super(SimpleRemoteTarget, self).deploy()

    def start(self, params=None, ssh=True, extra_bootparams=None):
        if ssh:
            self.connection = SSHControl(self.ip, port=self.port)

    def stop(self):
        self.connection = None
        self.ip = None
        self.server_ip = None
