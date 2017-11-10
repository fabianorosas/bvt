import logging
import os

from generic.tests import utils

YUM_INSTALL_COMMAND = "yum install --assumeyes --debuglevel 1 "


def execute_yum_command(
        session, yum_command, timeout=None, config_file_path=None):
    """
    Execute yum command on open session.

    Args:
        session (aexpect.client.ShellSession): session ready to receive
            commands
        yum_command (str): yum command to execute
        timeout (int): timeout for the command execution
        config_file_path (str): configuration file to pass to yum
            command
    """

    extra_args = ""
    if (config_file_path):
        config_file_target_path = os.path.join(
            "/tmp", os.path.basename(config_file_path))
        utils.copy_file_to_guest(
            session, config_file_path, config_file_target_path)
        extra_args = " --config " + config_file_target_path
    yum_command += extra_args
    install_command_output = session.cmd(yum_command, timeout=timeout)
    logging.info("Command output:\n{}".format(install_command_output))


def run(test, params, env):
    """
    Install packages using yum.

    Args:
        test (avocado.core.plugins.vt.VirtTest): QEMU test object
        params ({
            'yum_install_timeout': int,
            'yum_config_file_path': str,
            'packages_to_install': str,
        }): Dictionary with test parameters
        env ({?}): Dictionary with test environment
    """

    session = utils.get_session(params, env)

    yum_install_timeout = int(test.params.get("yum_install_timeout"))
    yum_config_file_path = test.params.get("yum_config_file_path")
    packages_to_install = test.params.get("packages_to_install")

    yum_install_command = YUM_INSTALL_COMMAND + packages_to_install

    execute_yum_command(
        session, yum_install_command, timeout=yum_install_timeout,
        config_file_path=yum_config_file_path)

    session.close()
