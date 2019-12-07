import pytest
from flexmock import flexmock

from borgmatic.config import validate as module


def test_validation_error_str_contains_error_messages_and_config_filename():
    error = module.Validation_error('config.yaml', ('oops', 'uh oh'))

    result = str(error)

    assert 'config.yaml' in result
    assert 'oops' in result
    assert 'uh oh' in result


def test_apply_logical_validation_raises_if_archive_name_format_present_without_prefix():
    with pytest.raises(module.Validation_error):
        module.apply_logical_validation(
            'config.yaml',
            {
                'storage': {'archive_name_format': '{hostname}-{now}'},
                'retention': {'keep_daily': 7},
            },
        )


def test_apply_logical_validation_raises_if_archive_name_format_present_without_retention_prefix():
    with pytest.raises(module.Validation_error):
        module.apply_logical_validation(
            'config.yaml',
            {
                'storage': {'archive_name_format': '{hostname}-{now}'},
                'retention': {'keep_daily': 7},
                'consistency': {'prefix': '{hostname}-'},
            },
        )


def test_apply_locical_validation_raises_if_unknown_repository_in_check_repositories():
    with pytest.raises(module.Validation_error):
        module.apply_logical_validation(
            'config.yaml',
            {
                'location': {'repositories': ['repo.borg', 'other.borg']},
                'retention': {'keep_secondly': 1000},
                'consistency': {'check_repositories': ['repo.borg', 'unknown.borg']},
            },
        )


def test_apply_locical_validation_does_not_raise_if_known_repository_in_check_repositories():
    module.apply_logical_validation(
        'config.yaml',
        {
            'location': {'repositories': ['repo.borg', 'other.borg']},
            'retention': {'keep_secondly': 1000},
            'consistency': {'check_repositories': ['repo.borg']},
        },
    )


def test_apply_logical_validation_does_not_raise_if_archive_name_format_and_prefix_present():
    module.apply_logical_validation(
        'config.yaml',
        {
            'storage': {'archive_name_format': '{hostname}-{now}'},
            'retention': {'prefix': '{hostname}-'},
            'consistency': {'prefix': '{hostname}-'},
        },
    )


def test_apply_logical_validation_does_not_raise_otherwise():
    module.apply_logical_validation('config.yaml', {'retention': {'keep_secondly': 1000}})


def test_remove_examples_strips_examples_from_map():
    schema = {
        'map': {
            'foo': {'desc': 'thing1', 'example': 'bar'},
            'baz': {'desc': 'thing2', 'example': 'quux'},
        }
    }

    module.remove_examples(schema)

    assert schema == {'map': {'foo': {'desc': 'thing1'}, 'baz': {'desc': 'thing2'}}}


def test_remove_examples_strips_examples_from_sequence_of_maps():
    schema = {'seq': [{'map': {'foo': {'desc': 'thing', 'example': 'bar'}}, 'example': 'stuff'}]}

    module.remove_examples(schema)

    assert schema == {'seq': [{'map': {'foo': {'desc': 'thing'}}}]}


def test_normalize_repository_path_passes_through_remote_repository():
    repository = 'example.org:test.borg'

    module.normalize_repository_path(repository) == repository


def test_normalize_repository_path_passes_through_absolute_repository():
    repository = '/foo/bar/test.borg'
    flexmock(module.os.path).should_receive('abspath').and_return(repository)

    module.normalize_repository_path(repository) == repository


def test_normalize_repository_path_resolves_relative_repository():
    repository = 'test.borg'
    absolute = '/foo/bar/test.borg'
    flexmock(module.os.path).should_receive('abspath').and_return(absolute)

    module.normalize_repository_path(repository) == absolute


def test_repositories_match_does_not_raise():
    flexmock(module).should_receive('normalize_repository_path')

    module.repositories_match('foo', 'bar')


def test_guard_configuration_contains_repository_does_not_raise_when_repository_in_config():
    flexmock(module).should_receive('repositories_match').replace_with(
        lambda first, second: first == second
    )

    module.guard_configuration_contains_repository(
        repository='repo', configurations={'config.yaml': {'location': {'repositories': ['repo']}}}
    )


def test_guard_configuration_contains_repository_does_not_raise_when_repository_not_given():
    module.guard_configuration_contains_repository(
        repository=None, configurations={'config.yaml': {'location': {'repositories': ['repo']}}}
    )


def test_guard_configuration_contains_repository_errors_when_repository_assumed_to_match_config_twice():
    with pytest.raises(ValueError):
        module.guard_configuration_contains_repository(
            repository=None,
            configurations={'config.yaml': {'location': {'repositories': ['repo', 'repo2']}}},
        )


def test_guard_configuration_contains_repository_errors_when_repository_missing_from_config():
    flexmock(module).should_receive('repositories_match').replace_with(
        lambda first, second: first == second
    )

    with pytest.raises(ValueError):
        module.guard_configuration_contains_repository(
            repository='nope',
            configurations={'config.yaml': {'location': {'repositories': ['repo', 'repo2']}}},
        )


def test_guard_configuration_contains_repository_errors_when_repository_matches_config_twice():
    flexmock(module).should_receive('repositories_match').replace_with(
        lambda first, second: first == second
    )

    with pytest.raises(ValueError):
        module.guard_configuration_contains_repository(
            repository='repo',
            configurations={
                'config.yaml': {'location': {'repositories': ['repo', 'repo2']}},
                'other.yaml': {'location': {'repositories': ['repo']}},
            },
        )
