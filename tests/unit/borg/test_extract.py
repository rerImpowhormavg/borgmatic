import logging

from flexmock import flexmock

from borgmatic.borg import extract as module

from ..test_verbosity import insert_logging_mock


def insert_execute_command_mock(command):
    flexmock(module).should_receive('execute_command').with_args(command).once()


def insert_execute_command_output_mock(command, result):
    flexmock(module).should_receive('execute_command').with_args(
        command, output_log_level=None
    ).and_return(result).once()


def test_extract_last_archive_dry_run_calls_borg_with_last_archive():
    insert_execute_command_output_mock(
        ('borg', 'list', '--short', 'repo'), result='archive1\narchive2\n'
    )
    insert_execute_command_mock(('borg', 'extract', '--dry-run', 'repo::archive2'))

    module.extract_last_archive_dry_run(repository='repo', lock_wait=None)


def test_extract_last_archive_dry_run_without_any_archives_should_not_raise():
    insert_execute_command_output_mock(('borg', 'list', '--short', 'repo'), result='\n')

    module.extract_last_archive_dry_run(repository='repo', lock_wait=None)


def test_extract_last_archive_dry_run_with_log_info_calls_borg_with_info_parameter():
    insert_execute_command_output_mock(
        ('borg', 'list', '--short', '--info', 'repo'), result='archive1\narchive2\n'
    )
    insert_execute_command_mock(('borg', 'extract', '--dry-run', '--info', 'repo::archive2'))
    insert_logging_mock(logging.INFO)

    module.extract_last_archive_dry_run(repository='repo', lock_wait=None)


def test_extract_last_archive_dry_run_with_log_debug_calls_borg_with_debug_parameter():
    insert_execute_command_output_mock(
        ('borg', 'list', '--short', '--debug', '--show-rc', 'repo'), result='archive1\narchive2\n'
    )
    insert_execute_command_mock(
        ('borg', 'extract', '--dry-run', '--debug', '--show-rc', '--list', 'repo::archive2')
    )
    insert_logging_mock(logging.DEBUG)

    module.extract_last_archive_dry_run(repository='repo', lock_wait=None)


def test_extract_last_archive_dry_run_calls_borg_via_local_path():
    insert_execute_command_output_mock(
        ('borg1', 'list', '--short', 'repo'), result='archive1\narchive2\n'
    )
    insert_execute_command_mock(('borg1', 'extract', '--dry-run', 'repo::archive2'))

    module.extract_last_archive_dry_run(repository='repo', lock_wait=None, local_path='borg1')


def test_extract_last_archive_dry_run_calls_borg_with_remote_path_parameters():
    insert_execute_command_output_mock(
        ('borg', 'list', '--short', '--remote-path', 'borg1', 'repo'), result='archive1\narchive2\n'
    )
    insert_execute_command_mock(
        ('borg', 'extract', '--dry-run', '--remote-path', 'borg1', 'repo::archive2')
    )

    module.extract_last_archive_dry_run(repository='repo', lock_wait=None, remote_path='borg1')


def test_extract_last_archive_dry_run_calls_borg_with_lock_wait_parameters():
    insert_execute_command_output_mock(
        ('borg', 'list', '--short', '--lock-wait', '5', 'repo'), result='archive1\narchive2\n'
    )
    insert_execute_command_mock(
        ('borg', 'extract', '--dry-run', '--lock-wait', '5', 'repo::archive2')
    )

    module.extract_last_archive_dry_run(repository='repo', lock_wait=5)


def test_extract_archive_calls_borg_with_restore_path_parameters():
    insert_execute_command_mock(('borg', 'extract', 'repo::archive', 'path1', 'path2'))

    module.extract_archive(
        dry_run=False,
        repository='repo',
        archive='archive',
        restore_paths=['path1', 'path2'],
        location_config={},
        storage_config={},
    )


def test_extract_archive_calls_borg_with_remote_path_parameters():
    insert_execute_command_mock(('borg', 'extract', '--remote-path', 'borg1', 'repo::archive'))

    module.extract_archive(
        dry_run=False,
        repository='repo',
        archive='archive',
        restore_paths=None,
        location_config={},
        storage_config={},
        remote_path='borg1',
    )


def test_extract_archive_calls_borg_with_numeric_owner_parameter():
    insert_execute_command_mock(('borg', 'extract', '--numeric-owner', 'repo::archive'))

    module.extract_archive(
        dry_run=False,
        repository='repo',
        archive='archive',
        restore_paths=None,
        location_config={'numeric_owner': True},
        storage_config={},
    )


def test_extract_archive_calls_borg_with_umask_parameters():
    insert_execute_command_mock(('borg', 'extract', '--umask', '0770', 'repo::archive'))

    module.extract_archive(
        dry_run=False,
        repository='repo',
        archive='archive',
        restore_paths=None,
        location_config={},
        storage_config={'umask': '0770'},
    )


def test_extract_archive_calls_borg_with_lock_wait_parameters():
    insert_execute_command_mock(('borg', 'extract', '--lock-wait', '5', 'repo::archive'))

    module.extract_archive(
        dry_run=False,
        repository='repo',
        archive='archive',
        restore_paths=None,
        location_config={},
        storage_config={'lock_wait': '5'},
    )


def test_extract_archive_with_log_info_calls_borg_with_info_parameter():
    insert_execute_command_mock(('borg', 'extract', '--info', 'repo::archive'))
    insert_logging_mock(logging.INFO)

    module.extract_archive(
        dry_run=False,
        repository='repo',
        archive='archive',
        restore_paths=None,
        location_config={},
        storage_config={},
    )


def test_extract_archive_with_log_debug_calls_borg_with_debug_parameters():
    insert_execute_command_mock(
        ('borg', 'extract', '--debug', '--list', '--show-rc', 'repo::archive')
    )
    insert_logging_mock(logging.DEBUG)

    module.extract_archive(
        dry_run=False,
        repository='repo',
        archive='archive',
        restore_paths=None,
        location_config={},
        storage_config={},
    )


def test_extract_archive_calls_borg_with_dry_run_parameter():
    insert_execute_command_mock(('borg', 'extract', '--dry-run', 'repo::archive'))

    module.extract_archive(
        dry_run=True,
        repository='repo',
        archive='archive',
        restore_paths=None,
        location_config={},
        storage_config={},
    )


def test_extract_archive_calls_borg_with_progress_parameter():
    flexmock(module).should_receive('execute_command_without_capture').with_args(
        ('borg', 'extract', '--progress', 'repo::archive')
    ).once()

    module.extract_archive(
        dry_run=False,
        repository='repo',
        archive='archive',
        restore_paths=None,
        location_config={},
        storage_config={},
        progress=True,
    )
