import logging
import subprocess
import time

from flexmock import flexmock

import borgmatic.hooks.command
from borgmatic.commands import borgmatic as module


def test_run_configuration_runs_actions_for_each_repository():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    expected_results = [flexmock(), flexmock()]
    flexmock(module).should_receive('run_actions').and_return(expected_results[:1]).and_return(
        expected_results[1:]
    )
    config = {'location': {'repositories': ['foo', 'bar']}}
    arguments = {'global': flexmock(monitoring_verbosity=1)}

    results = list(module.run_configuration('test.yaml', config, arguments))

    assert results == expected_results


def test_run_configuration_with_invalid_borg_version_errors():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_raise(ValueError)
    flexmock(module.command).should_receive('execute_hook').never()
    flexmock(module.dispatch).should_receive('call_hooks').never()
    flexmock(module).should_receive('run_actions').never()
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'prune': flexmock()}

    list(module.run_configuration('test.yaml', config, arguments))


def test_run_configuration_calls_hooks_for_prune_action():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').twice()
    flexmock(module.dispatch).should_receive('call_hooks').at_least().twice()
    flexmock(module).should_receive('run_actions').and_return([])
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'prune': flexmock()}

    list(module.run_configuration('test.yaml', config, arguments))


def test_run_configuration_calls_hooks_for_compact_action():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').twice()
    flexmock(module).should_receive('run_actions').and_return([])
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'compact': flexmock()}

    list(module.run_configuration('test.yaml', config, arguments))


def test_run_configuration_executes_and_calls_hooks_for_create_action():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').twice()
    flexmock(module.dispatch).should_receive('call_hooks').at_least().twice()
    flexmock(module).should_receive('run_actions').and_return([])
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}

    list(module.run_configuration('test.yaml', config, arguments))


def test_run_configuration_calls_hooks_for_check_action():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').twice()
    flexmock(module.dispatch).should_receive('call_hooks').at_least().twice()
    flexmock(module).should_receive('run_actions').and_return([])
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'check': flexmock()}

    list(module.run_configuration('test.yaml', config, arguments))


def test_run_configuration_calls_hooks_for_extract_action():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').twice()
    flexmock(module.dispatch).should_receive('call_hooks').never()
    flexmock(module).should_receive('run_actions').and_return([])
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'extract': flexmock()}

    list(module.run_configuration('test.yaml', config, arguments))


def test_run_configuration_does_not_trigger_hooks_for_list_action():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').never()
    flexmock(module.dispatch).should_receive('call_hooks').never()
    flexmock(module).should_receive('run_actions').and_return([])
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'list': flexmock()}

    list(module.run_configuration('test.yaml', config, arguments))


def test_run_configuration_logs_actions_error():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook')
    flexmock(module.dispatch).should_receive('call_hooks')
    expected_results = [flexmock()]
    flexmock(module).should_receive('make_error_log_records').and_return(expected_results)
    flexmock(module).should_receive('run_actions').and_raise(OSError)
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False)}

    results = list(module.run_configuration('test.yaml', config, arguments))

    assert results == expected_results


def test_run_configuration_logs_pre_hook_error():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').and_raise(OSError).and_return(None)
    expected_results = [flexmock()]
    flexmock(module).should_receive('make_error_log_records').and_return(expected_results)
    flexmock(module).should_receive('run_actions').never()
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}

    results = list(module.run_configuration('test.yaml', config, arguments))

    assert results == expected_results


def test_run_configuration_bails_for_pre_hook_soft_failure():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    error = subprocess.CalledProcessError(borgmatic.hooks.command.SOFT_FAIL_EXIT_CODE, 'try again')
    flexmock(module.command).should_receive('execute_hook').and_raise(error).and_return(None)
    flexmock(module).should_receive('make_error_log_records').never()
    flexmock(module).should_receive('run_actions').never()
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}

    results = list(module.run_configuration('test.yaml', config, arguments))

    assert results == []


def test_run_configuration_logs_post_hook_error():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').and_return(None).and_raise(
        OSError
    ).and_return(None)
    flexmock(module.dispatch).should_receive('call_hooks')
    expected_results = [flexmock()]
    flexmock(module).should_receive('make_error_log_records').and_return(expected_results)
    flexmock(module).should_receive('run_actions').and_return([])
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}

    results = list(module.run_configuration('test.yaml', config, arguments))

    assert results == expected_results


def test_run_configuration_bails_for_post_hook_soft_failure():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    error = subprocess.CalledProcessError(borgmatic.hooks.command.SOFT_FAIL_EXIT_CODE, 'try again')
    flexmock(module.command).should_receive('execute_hook').and_return(None).and_raise(
        error
    ).and_return(None)
    flexmock(module.dispatch).should_receive('call_hooks')
    flexmock(module).should_receive('make_error_log_records').never()
    flexmock(module).should_receive('run_actions').and_return([])
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}

    results = list(module.run_configuration('test.yaml', config, arguments))

    assert results == []


def test_run_configuration_logs_on_error_hook_error():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook').and_raise(OSError)
    expected_results = [flexmock(), flexmock()]
    flexmock(module).should_receive('make_error_log_records').and_return(
        expected_results[:1]
    ).and_return(expected_results[1:])
    flexmock(module).should_receive('run_actions').and_raise(OSError)
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}

    results = list(module.run_configuration('test.yaml', config, arguments))

    assert results == expected_results


def test_run_configuration_bails_for_on_error_hook_soft_failure():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    error = subprocess.CalledProcessError(borgmatic.hooks.command.SOFT_FAIL_EXIT_CODE, 'try again')
    flexmock(module.command).should_receive('execute_hook').and_return(None).and_raise(error)
    expected_results = [flexmock()]
    flexmock(module).should_receive('make_error_log_records').and_return(expected_results)
    flexmock(module).should_receive('run_actions').and_raise(OSError)
    config = {'location': {'repositories': ['foo']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}

    results = list(module.run_configuration('test.yaml', config, arguments))

    assert results == expected_results


def test_run_configuration_retries_soft_error():
    # Run action first fails, second passes
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook')
    flexmock(module).should_receive('run_actions').and_raise(OSError).and_return([])
    expected_results = [flexmock()]
    flexmock(module).should_receive('make_error_log_records').and_return(expected_results).once()
    config = {'location': {'repositories': ['foo']}, 'storage': {'retries': 1}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}
    results = list(module.run_configuration('test.yaml', config, arguments))
    assert results == expected_results


def test_run_configuration_retries_hard_error():
    # Run action fails twice
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook')
    flexmock(module).should_receive('run_actions').and_raise(OSError).times(2)
    expected_results = [flexmock(), flexmock()]
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[:1]).with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(
        expected_results[1:]
    ).twice()
    config = {'location': {'repositories': ['foo']}, 'storage': {'retries': 1}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}
    results = list(module.run_configuration('test.yaml', config, arguments))
    assert results == expected_results


def test_run_repos_ordered():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook')
    flexmock(module).should_receive('run_actions').and_raise(OSError).times(2)
    expected_results = [flexmock(), flexmock()]
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[:1]).ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'bar: Error running actions for repository', OSError
    ).and_return(expected_results[1:]).ordered()
    config = {'location': {'repositories': ['foo', 'bar']}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}
    results = list(module.run_configuration('test.yaml', config, arguments))
    assert results == expected_results


def test_run_configuration_retries_round_robbin():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook')
    flexmock(module).should_receive('run_actions').and_raise(OSError).times(4)
    expected_results = [flexmock(), flexmock(), flexmock(), flexmock()]
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[0:1]).ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'bar: Error running actions for repository', OSError
    ).and_return(expected_results[1:2]).ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[2:3]).ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'bar: Error running actions for repository', OSError
    ).and_return(expected_results[3:4]).ordered()
    config = {'location': {'repositories': ['foo', 'bar']}, 'storage': {'retries': 1}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}
    results = list(module.run_configuration('test.yaml', config, arguments))
    assert results == expected_results


def test_run_configuration_retries_one_passes():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook')
    flexmock(module).should_receive('run_actions').and_raise(OSError).and_raise(OSError).and_return(
        []
    ).and_raise(OSError).times(4)
    expected_results = [flexmock(), flexmock(), flexmock()]
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[0:1]).ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'bar: Error running actions for repository', OSError
    ).and_return(expected_results[1:2]).ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'bar: Error running actions for repository', OSError
    ).and_return(expected_results[2:3]).ordered()
    config = {'location': {'repositories': ['foo', 'bar']}, 'storage': {'retries': 1}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}
    results = list(module.run_configuration('test.yaml', config, arguments))
    assert results == expected_results


def test_run_configuration_retry_wait():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook')
    flexmock(module).should_receive('run_actions').and_raise(OSError).times(4)
    expected_results = [flexmock(), flexmock(), flexmock(), flexmock()]
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[0:1]).ordered()

    flexmock(time).should_receive('sleep').with_args(10).and_return().ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[1:2]).ordered()

    flexmock(time).should_receive('sleep').with_args(20).and_return().ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[2:3]).ordered()

    flexmock(time).should_receive('sleep').with_args(30).and_return().ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[3:4]).ordered()
    config = {'location': {'repositories': ['foo']}, 'storage': {'retries': 3, 'retry_wait': 10}}
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}
    results = list(module.run_configuration('test.yaml', config, arguments))
    assert results == expected_results


def test_run_configuration_retries_timeout_multiple_repos():
    flexmock(module.borg_environment).should_receive('initialize')
    flexmock(module.borg_version).should_receive('local_borg_version').and_return(flexmock())
    flexmock(module.command).should_receive('execute_hook')
    flexmock(module).should_receive('run_actions').and_raise(OSError).and_raise(OSError).and_return(
        []
    ).and_raise(OSError).times(4)
    expected_results = [flexmock(), flexmock(), flexmock()]
    flexmock(module).should_receive('make_error_log_records').with_args(
        'foo: Error running actions for repository', OSError
    ).and_return(expected_results[0:1]).ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'bar: Error running actions for repository', OSError
    ).and_return(expected_results[1:2]).ordered()

    # Sleep before retrying foo (and passing)
    flexmock(time).should_receive('sleep').with_args(10).and_return().ordered()

    # Sleep before retrying bar (and failing)
    flexmock(time).should_receive('sleep').with_args(10).and_return().ordered()
    flexmock(module).should_receive('make_error_log_records').with_args(
        'bar: Error running actions for repository', OSError
    ).and_return(expected_results[2:3]).ordered()
    config = {
        'location': {'repositories': ['foo', 'bar']},
        'storage': {'retries': 1, 'retry_wait': 10},
    }
    arguments = {'global': flexmock(monitoring_verbosity=1, dry_run=False), 'create': flexmock()}
    results = list(module.run_configuration('test.yaml', config, arguments))
    assert results == expected_results


def test_load_configurations_collects_parsed_configurations():
    configuration = flexmock()
    other_configuration = flexmock()
    flexmock(module.validate).should_receive('parse_configuration').and_return(
        configuration
    ).and_return(other_configuration)

    configs, logs = tuple(module.load_configurations(('test.yaml', 'other.yaml')))

    assert configs == {'test.yaml': configuration, 'other.yaml': other_configuration}
    assert logs == []


def test_load_configurations_logs_critical_for_parse_error():
    flexmock(module.validate).should_receive('parse_configuration').and_raise(ValueError)

    configs, logs = tuple(module.load_configurations(('test.yaml',)))

    assert configs == {}
    assert {log.levelno for log in logs} == {logging.CRITICAL}


def test_log_record_does_not_raise():
    module.log_record(levelno=1, foo='bar', baz='quux')


def test_log_record_with_suppress_does_not_raise():
    module.log_record(levelno=1, foo='bar', baz='quux', suppress_log=True)


def test_make_error_log_records_generates_output_logs_for_message_only():
    flexmock(module).should_receive('log_record').replace_with(dict)

    logs = tuple(module.make_error_log_records('Error'))

    assert {log['levelno'] for log in logs} == {logging.CRITICAL}


def test_make_error_log_records_generates_output_logs_for_called_process_error():
    flexmock(module).should_receive('log_record').replace_with(dict)
    flexmock(module.logger).should_receive('getEffectiveLevel').and_return(logging.WARNING)

    logs = tuple(
        module.make_error_log_records(
            'Error', subprocess.CalledProcessError(1, 'ls', 'error output')
        )
    )

    assert {log['levelno'] for log in logs} == {logging.CRITICAL}
    assert any(log for log in logs if 'error output' in str(log))


def test_make_error_log_records_generates_logs_for_value_error():
    flexmock(module).should_receive('log_record').replace_with(dict)

    logs = tuple(module.make_error_log_records('Error', ValueError()))

    assert {log['levelno'] for log in logs} == {logging.CRITICAL}


def test_make_error_log_records_generates_logs_for_os_error():
    flexmock(module).should_receive('log_record').replace_with(dict)

    logs = tuple(module.make_error_log_records('Error', OSError()))

    assert {log['levelno'] for log in logs} == {logging.CRITICAL}


def test_make_error_log_records_generates_nothing_for_other_error():
    flexmock(module).should_receive('log_record').replace_with(dict)

    logs = tuple(module.make_error_log_records('Error', KeyError()))

    assert logs == ()


def test_get_local_path_uses_configuration_value():
    assert module.get_local_path({'test.yaml': {'location': {'local_path': 'borg1'}}}) == 'borg1'


def test_get_local_path_without_location_defaults_to_borg():
    assert module.get_local_path({'test.yaml': {}}) == 'borg'


def test_get_local_path_without_local_path_defaults_to_borg():
    assert module.get_local_path({'test.yaml': {'location': {}}}) == 'borg'


def test_collect_configuration_run_summary_logs_info_for_success():
    flexmock(module.command).should_receive('execute_hook').never()
    flexmock(module).should_receive('run_configuration').and_return([])
    arguments = {}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert {log.levelno for log in logs} == {logging.INFO}


def test_collect_configuration_run_summary_executes_hooks_for_create():
    flexmock(module).should_receive('run_configuration').and_return([])
    arguments = {'create': flexmock(), 'global': flexmock(monitoring_verbosity=1, dry_run=False)}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert {log.levelno for log in logs} == {logging.INFO}


def test_collect_configuration_run_summary_logs_info_for_success_with_extract():
    flexmock(module.validate).should_receive('guard_configuration_contains_repository')
    flexmock(module).should_receive('run_configuration').and_return([])
    arguments = {'extract': flexmock(repository='repo')}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert {log.levelno for log in logs} == {logging.INFO}


def test_collect_configuration_run_summary_logs_extract_with_repository_error():
    flexmock(module.validate).should_receive('guard_configuration_contains_repository').and_raise(
        ValueError
    )
    expected_logs = (flexmock(),)
    flexmock(module).should_receive('make_error_log_records').and_return(expected_logs)
    arguments = {'extract': flexmock(repository='repo')}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert logs == expected_logs


def test_collect_configuration_run_summary_logs_info_for_success_with_mount():
    flexmock(module.validate).should_receive('guard_configuration_contains_repository')
    flexmock(module).should_receive('run_configuration').and_return([])
    arguments = {'mount': flexmock(repository='repo')}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert {log.levelno for log in logs} == {logging.INFO}


def test_collect_configuration_run_summary_logs_mount_with_repository_error():
    flexmock(module.validate).should_receive('guard_configuration_contains_repository').and_raise(
        ValueError
    )
    expected_logs = (flexmock(),)
    flexmock(module).should_receive('make_error_log_records').and_return(expected_logs)
    arguments = {'mount': flexmock(repository='repo')}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert logs == expected_logs


def test_collect_configuration_run_summary_logs_missing_configs_error():
    arguments = {'global': flexmock(config_paths=[])}
    expected_logs = (flexmock(),)
    flexmock(module).should_receive('make_error_log_records').and_return(expected_logs)

    logs = tuple(module.collect_configuration_run_summary_logs({}, arguments=arguments))

    assert logs == expected_logs


def test_collect_configuration_run_summary_logs_pre_hook_error():
    flexmock(module.command).should_receive('execute_hook').and_raise(ValueError)
    expected_logs = (flexmock(),)
    flexmock(module).should_receive('make_error_log_records').and_return(expected_logs)
    arguments = {'create': flexmock(), 'global': flexmock(monitoring_verbosity=1, dry_run=False)}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert logs == expected_logs


def test_collect_configuration_run_summary_logs_post_hook_error():
    flexmock(module.command).should_receive('execute_hook').and_return(None).and_raise(ValueError)
    flexmock(module).should_receive('run_configuration').and_return([])
    expected_logs = (flexmock(),)
    flexmock(module).should_receive('make_error_log_records').and_return(expected_logs)
    arguments = {'create': flexmock(), 'global': flexmock(monitoring_verbosity=1, dry_run=False)}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert expected_logs[0] in logs


def test_collect_configuration_run_summary_logs_for_list_with_archive_and_repository_error():
    flexmock(module.validate).should_receive('guard_configuration_contains_repository').and_raise(
        ValueError
    )
    expected_logs = (flexmock(),)
    flexmock(module).should_receive('make_error_log_records').and_return(expected_logs)
    arguments = {'list': flexmock(repository='repo', archive='test')}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert logs == expected_logs


def test_collect_configuration_run_summary_logs_info_for_success_with_list():
    flexmock(module).should_receive('run_configuration').and_return([])
    arguments = {'list': flexmock(repository='repo', archive=None)}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert {log.levelno for log in logs} == {logging.INFO}


def test_collect_configuration_run_summary_logs_run_configuration_error():
    flexmock(module.validate).should_receive('guard_configuration_contains_repository')
    flexmock(module).should_receive('run_configuration').and_return(
        [logging.makeLogRecord(dict(levelno=logging.CRITICAL, levelname='CRITICAL', msg='Error'))]
    )
    flexmock(module).should_receive('make_error_log_records').and_return([])
    arguments = {}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert {log.levelno for log in logs} == {logging.CRITICAL}


def test_collect_configuration_run_summary_logs_run_umount_error():
    flexmock(module.validate).should_receive('guard_configuration_contains_repository')
    flexmock(module).should_receive('run_configuration').and_return([])
    flexmock(module.borg_umount).should_receive('unmount_archive').and_raise(OSError)
    flexmock(module).should_receive('make_error_log_records').and_return(
        [logging.makeLogRecord(dict(levelno=logging.CRITICAL, levelname='CRITICAL', msg='Error'))]
    )
    arguments = {'umount': flexmock(mount_point='/mnt')}

    logs = tuple(
        module.collect_configuration_run_summary_logs({'test.yaml': {}}, arguments=arguments)
    )

    assert {log.levelno for log in logs} == {logging.INFO, logging.CRITICAL}


def test_collect_configuration_run_summary_logs_outputs_merged_json_results():
    flexmock(module).should_receive('run_configuration').and_return(['foo', 'bar']).and_return(
        ['baz']
    )
    stdout = flexmock()
    stdout.should_receive('write').with_args('["foo", "bar", "baz"]').once()
    flexmock(module.sys).stdout = stdout
    arguments = {}

    tuple(
        module.collect_configuration_run_summary_logs(
            {'test.yaml': {}, 'test2.yaml': {}}, arguments=arguments
        )
    )
