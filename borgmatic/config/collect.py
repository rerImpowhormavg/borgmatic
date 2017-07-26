import os


def collect_config_filenames(config_paths):
    '''
    Given a sequence of config paths, both filenames and directories, resolve that to just an
    iterable of files. Accomplish this by listing any given directories looking for contained config
    files. This is non-recursive, so any directories within the given directories are ignored.

    Return paths even if they don't exist on disk, so the user can find out about missing
    configuration paths. However, skip /etc/borgmatic.d if it's missing, so the user doesn't have to
    create it unless they need it.
    '''
    for path in config_paths:
        exists = os.path.exists(path)

        if os.path.realpath(path) == '/etc/borgmatic.d' and not exists:
            continue

        if not os.path.isdir(path) or not exists:
            yield path
            continue

        for filename in os.listdir(path):
            full_filename = os.path.join(path, filename)
            if not os.path.isdir(full_filename):
                yield full_filename
