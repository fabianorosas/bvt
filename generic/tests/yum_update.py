import logging
import os

from generic.tests import yum_install
from generic.tests import utils

YUM_UPDATE_COMMAND = "yum update --assumeyes --debuglevel 1"


def run(test, params, env):
    """
    Update packages using yum.

    Args:
        test (avocado.core.plugins.vt.VirtTest): QEMU test object
        params ({
            'yum_install_timeout': int,
            'yum_install_config_file_path': str,
            'packages_to_install': str,
            'yum_update_timeout': int,
            'yum_update_config_file_path': str,
        }): Dictionary with test parameters
        env ({?}): Dictionary with test environment
    """

    session = utils.get_session(params, env)

    yum_install_timeout = int(test.params.get("yum_install_timeout"))
    yum_install_config_file_path = test.params.get(
        "yum_install_config_file_path")
    packages_to_install = test.params.get("packages_to_install")
    yum_update_timeout = int(test.params.get("yum_update_timeout"))
    yum_update_config_file_path = test.params.get(
        "yum_update_config_file_path")

    yum_install_command = yum_install.YUM_INSTALL_COMMAND + packages_to_install

    yum_install.execute_yum_command(
        session, yum_install_command, timeout=yum_install_timeout,
        config_file_path=yum_install_config_file_path)

    yum_install.execute_yum_command(
        session, YUM_UPDATE_COMMAND, timeout=yum_update_timeout,
        config_file_path=yum_update_config_file_path)

    session.close()
