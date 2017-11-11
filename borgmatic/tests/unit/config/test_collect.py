from flexmock import flexmock

from borgmatic.config import collect as module


def test_collect_config_filenames_collects_given_files():
    config_paths = ('config.yaml', 'other.yaml')
    flexmock(module.os.path).should_receive('isdir').and_return(False)

    config_filenames = tuple(module.collect_config_filenames(config_paths))

    assert config_filenames == config_paths


def test_collect_config_filenames_collects_files_from_given_directories_and_ignores_sub_directories():
    config_paths = ('config.yaml', '/etc/borgmatic.d')
    mock_path = flexmock(module.os.path)
    mock_path.should_receive('exists').and_return(True)
    mock_path.should_receive('isdir').with_args('config.yaml').and_return(False)
    mock_path.should_receive('isdir').with_args('/etc/borgmatic.d').and_return(True)
    mock_path.should_receive('isdir').with_args('/etc/borgmatic.d/foo.yaml').and_return(False)
    mock_path.should_receive('isdir').with_args('/etc/borgmatic.d/bar').and_return(True)
    mock_path.should_receive('isdir').with_args('/etc/borgmatic.d/baz.yaml').and_return(False)
    flexmock(module.os).should_receive('listdir').and_return(['foo.yaml', 'bar', 'baz.yaml'])

    config_filenames = tuple(module.collect_config_filenames(config_paths))

    assert config_filenames == (
        'config.yaml',
        '/etc/borgmatic.d/foo.yaml',
        '/etc/borgmatic.d/baz.yaml',
    )


def test_collect_config_filenames_skips_etc_borgmatic_config_dot_yaml_if_it_does_not_exist():
    config_paths = ('config.yaml', '/etc/borgmatic/config.yaml')
    mock_path = flexmock(module.os.path)
    mock_path.should_receive('exists').with_args('config.yaml').and_return(True)
    mock_path.should_receive('exists').with_args('/etc/borgmatic/config.yaml').and_return(False)
    mock_path.should_receive('isdir').with_args('config.yaml').and_return(False)
    mock_path.should_receive('isdir').with_args('/etc/borgmatic/config.yaml').and_return(True)

    config_filenames = tuple(module.collect_config_filenames(config_paths))

    assert config_filenames == ('config.yaml',)


def test_collect_config_filenames_skips_etc_borgmatic_dot_d_if_it_does_not_exist():
    config_paths = ('config.yaml', '/etc/borgmatic.d')
    mock_path = flexmock(module.os.path)
    mock_path.should_receive('exists').with_args('config.yaml').and_return(True)
    mock_path.should_receive('exists').with_args('/etc/borgmatic.d').and_return(False)
    mock_path.should_receive('isdir').with_args('config.yaml').and_return(False)
    mock_path.should_receive('isdir').with_args('/etc/borgmatic.d').and_return(True)

    config_filenames = tuple(module.collect_config_filenames(config_paths))

    assert config_filenames == ('config.yaml',)


def test_collect_config_filenames_skips_non_canonical_etc_borgmatic_dot_d_if_it_does_not_exist():
    config_paths = ('config.yaml', '/etc/../etc/borgmatic.d')
    mock_path = flexmock(module.os.path)
    mock_path.should_receive('exists').with_args('config.yaml').and_return(True)
    mock_path.should_receive('exists').with_args('/etc/../etc/borgmatic.d').and_return(False)
    mock_path.should_receive('isdir').with_args('config.yaml').and_return(False)
    mock_path.should_receive('isdir').with_args('/etc/../etc/borgmatic.d').and_return(True)

    config_filenames = tuple(module.collect_config_filenames(config_paths))

    assert config_filenames == ('config.yaml',)


def test_collect_config_filenames_includes_other_directory_if_it_does_not_exist():
    config_paths = ('config.yaml', '/my/directory')
    mock_path = flexmock(module.os.path)
    mock_path.should_receive('exists').with_args('config.yaml').and_return(True)
    mock_path.should_receive('exists').with_args('/my/directory').and_return(False)
    mock_path.should_receive('isdir').with_args('config.yaml').and_return(False)
    mock_path.should_receive('isdir').with_args('/my/directory').and_return(True)

    config_filenames = tuple(module.collect_config_filenames(config_paths))

    assert config_filenames == config_paths
