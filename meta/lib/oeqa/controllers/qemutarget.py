# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

import os
import sys
import signal
import time

from oeqa.controllers.sshtarget import OESSHTarget
from oeqa.utils.qemurunner import QemuRunner


class OEQemuTarget(OESSHTarget):
    supported_fstypes = ['ext3', 'ext4', 'cpio.gz', 'wic']
    def __init__(self, td, logger, timeout=300, user='root',
            port=None, machine='', rootfs='', kernel='', kvm=False,
            dump_dir='', dump_host_cmds='', display='', bootlog='',
            tmpdir='', dir_image='', boottime=60, **kwargs):

        super(OEQemuTarget, self).__init__(td, logger, timeout, user, port)

        self.ip = td['TEST_TARGET_IP']
        self.server_ip = td['TEST_SERVER_IP']
        self.machine = machine


        image_name = ("%s/%s" % (td['DEPLOY_DIR_IMAGE'], td['IMAGE_LINK_NAME']))

        # Get rootfs
        if not rootfs:
            fstypes = [fs for fs in td['IMAGE_FSTYPES'].split(' ')
                          if fs in self.supported_fstypes]
            if not fstypes:
                bb.fatal('Unsupported image type built. Add a comptible image to '
                         'IMAGE_FSTYPES. Supported types: %s' %
                         ', '.join(self.supported_fstypes))
            rootfs = '%s.%s' % (image_name, fstypes[0])
        self.rootfs = rootfs

        self.kernel = kernel
        self.kvm = kvm

        self.runner = QemuRunner(machine=machine, rootfs=rootfs, tmpdir=tmpdir,
                                 deploy_dir_image=dir_image, display=display,
                                 logfile=bootlog, boottime=boottime,
                                 use_kvm=kvm, dump_dir=dump_dir,
                                 dump_host_cmds=dump_host_cmds, logger=logger)

    def start(self, params=None, extra_bootparams=None):
        if self.runner.start(params, extra_bootparams=extra_bootparams):
            self.ip = self.runner.ip
            self.server_ip = self.runner.server_ip
        else:
            self.stop()
            raise RuntimeError("FAILED to start qemu - check the task log and the boot log")

    def deploy(self):
        pass

    def stop(self):
        self.runner.stop()
