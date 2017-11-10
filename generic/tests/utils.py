import logging
import os


def get_session(params, env):
    """
    Verifies if main VM is alive and gets a session from it

    Args:
        params ({
            'main_vm': virttest.libvirt_vm.VM,
            'login_timeout': float
        }): Dictionary with test parameters (only relevant parameters listed)
        env ({?}): Dictionary with test environment

    Returns:
        aexpect.client.ShellSession: session ready to receive commands
    """

    vm = env.get_vm(params["main_vm"])
    vm.verify_alive()
    timeout = float(params.get("login_timeout"))
    return vm.wait_for_login(timeout=timeout)


def copy_file_to_guest(session, source_file_path, target_file_path):
    """
    Copy file from local host to guest using an open session.

    Args:
        session (aexpect.client.ShellSession): session ready to receive
            commands
        source_file_path (str): source file path in the local host
        target_file_path (str): target file path in the guest
    """

    with open(source_file_path) as source_file:
        file_contents = source_file.read()
    # Need newline escaping to send the command, otherwise it hangs
    file_contents = file_contents.replace("\n", r"\n")
    write_file_cmd = "echo -e '{contents}' > {file_path}".format(
        contents=file_contents, file_path=target_file_path)
    session.cmd(write_file_cmd)
