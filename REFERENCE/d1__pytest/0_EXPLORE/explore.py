import pytest

def test_1__wrong_fixname(config):
    """
    WRONG NAME

    test setup failed
    file C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\REFERENCE\d1__pytest\m0_cmd_0__explore.py, line 12
      def test__1(config):
    E       fixture 'config' not found
    >       available fixtures: _class_scoped_runner, _function_scoped_runner, _module_scoped_runner, _package_scoped_runner, _session_scoped_runner, anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, cov, dash_br, dash_duo, dash_duo_mp, dash_multi_process_server, dash_process_server, dash_thread_server, dashjl, dashjl_server, dashr, dashr_server, diskcache_manager, doctest_namespace, event_loop_policy, extra, extras, include_metadata_in_junit_xml, metadata, monkeypatch, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, subtests, testrun_uid, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, unused_tcp_port, unused_tcp_port_factory, unused_udp_port, unused_udp_port_factory, worker_id
    >       use 'pytest --fixtures [testpath]' for help on them.

    C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\REFERENCE\d1__pytest\m0_cmd_0__explore.py:12
    """
    assert config.getoption("--opt1")


def test_2__good_pytestconfig(pytestconfig):
    assert pytestconfig.getoption("--opt1")

def test_3__good_request(request):
    assert request.config.getoption("--opt1")


