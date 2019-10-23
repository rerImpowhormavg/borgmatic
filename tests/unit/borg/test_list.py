import logging

import pytest
from flexmock import flexmock

from borgmatic.borg import list as module

from ..test_verbosity import insert_logging_mock


def test_list_archives_calls_borg_with_parameters():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', 'repo'), output_log_level=logging.WARNING
    )

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=False, successful=False),
    )


def test_list_archives_with_log_info_calls_borg_with_info_parameter():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--info', 'repo'), output_log_level=logging.WARNING
    )
    insert_logging_mock(logging.INFO)

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=False, successful=False),
    )


def test_list_archives_with_log_info_and_json_suppresses_most_borg_output():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--json', 'repo'), output_log_level=None
    )
    insert_logging_mock(logging.INFO)

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=True, successful=False),
    )


def test_list_archives_with_log_debug_calls_borg_with_debug_parameter():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--debug', '--show-rc', 'repo'), output_log_level=logging.WARNING
    )
    insert_logging_mock(logging.DEBUG)

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=False, successful=False),
    )


def test_list_archives_with_log_debug_and_json_suppresses_most_borg_output():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--json', 'repo'), output_log_level=None
    )
    insert_logging_mock(logging.DEBUG)

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=True, successful=False),
    )


def test_list_archives_with_lock_wait_calls_borg_with_lock_wait_parameters():
    storage_config = {'lock_wait': 5}
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--lock-wait', '5', 'repo'), output_log_level=logging.WARNING
    )

    module.list_archives(
        repository='repo',
        storage_config=storage_config,
        list_arguments=flexmock(archive=None, json=False, successful=False),
    )


def test_list_archives_with_archive_calls_borg_with_archive_parameter():
    storage_config = {}
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', 'repo::archive'), output_log_level=logging.WARNING
    )

    module.list_archives(
        repository='repo',
        storage_config=storage_config,
        list_arguments=flexmock(archive='archive', json=False, successful=False),
    )


def test_list_archives_with_local_path_calls_borg_via_local_path():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg1', 'list', 'repo'), output_log_level=logging.WARNING
    )

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=False, successful=False),
        local_path='borg1',
    )


def test_list_archives_with_remote_path_calls_borg_with_remote_path_parameters():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--remote-path', 'borg1', 'repo'), output_log_level=logging.WARNING
    )

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=False, successful=False),
        remote_path='borg1',
    )


def test_list_archives_with_short_calls_borg_with_short_parameter():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--short', 'repo'), output_log_level=logging.WARNING
    ).and_return('[]')

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=False, successful=False, short=True),
    )


@pytest.mark.parametrize(
    'argument_name',
    (
        'prefix',
        'glob_archives',
        'sort_by',
        'first',
        'last',
        'exclude',
        'exclude_from',
        'pattern',
        'patterns_from',
    ),
)
def test_list_archives_passes_through_arguments_to_borg(argument_name):
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--' + argument_name.replace('_', '-'), 'value', 'repo'),
        output_log_level=logging.WARNING,
    ).and_return('[]')

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(
            archive=None, json=False, successful=False, **{argument_name: 'value'}
        ),
    )


def test_list_archives_with_successful_calls_borg_to_exclude_checkpoints():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--glob-archives', module.BORG_EXCLUDE_CHECKPOINTS_GLOB, 'repo'),
        output_log_level=logging.WARNING,
    ).and_return('[]')

    module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=False, successful=True),
    )


def test_list_archives_with_json_calls_borg_with_json_parameter():
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', '--json', 'repo'), output_log_level=None
    ).and_return('[]')

    json_output = module.list_archives(
        repository='repo',
        storage_config={},
        list_arguments=flexmock(archive=None, json=True, successful=False),
    )

    assert json_output == '[]'
