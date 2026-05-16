# coding: utf-8
from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


def test_user(host, get_vars):
    """ """
    user = get_vars.get("zot_system_user", "zot")
    group = get_vars.get("zot_system_group", "zot")

    assert host.group(group).exists
    assert host.user(user).exists

    if user != "root":
        assert group in host.user(user).groups


def test_version(host):
    """ """
    _facts = local_facts(host=host, fact="zot")

    version = _facts.get("version")

    install_dir = f"/usr/local/opt/zot/{version}"
    install_bin = f"{install_dir}/zot"
    binary_link = "/usr/bin/zot"

    print(install_dir)

    directory = host.file(install_dir)
    assert directory.is_directory

    binary = host.file(install_bin)
    assert binary.is_file

    link = host.file(binary_link)
    assert link.is_symlink
    assert link.linked_to == install_bin


def test_storage_directory(host, get_vars):
    """ """
    storage = (
        get_vars.get("zot_config", {})
        .get("storage", {})
        .get("local", {})
        .get("rootdir", None)
    )
    user = get_vars.get("zot_system_user", "zot")
    group = get_vars.get("zot_system_group", "zot")

    print(storage)

    if storage:
        directory = host.file(storage)
        assert directory.is_directory

        assert directory.user == user
        assert directory.group == group
        assert directory.mode == 0o755


def test_service(host, get_vars):
    service = host.service("zot")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    zot_config = get_vars.get("zot_config", {})

    print(zot_config)

    listen_address = "127.0.0.1:5000"

    if isinstance(zot_config, dict):
        _listen = zot_config.get("http")

        if isinstance(_listen, dict):
            _address = _listen.get("address")
            _port = _listen.get("port")

            listen_address = f"{_address}:{_port}"

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
