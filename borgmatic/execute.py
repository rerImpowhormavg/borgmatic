import logging
import subprocess

logger = logging.getLogger(__name__)


ERROR_OUTPUT_MAX_LINE_COUNT = 25
BORG_ERROR_EXIT_CODE = 2


def execute_and_log_output(full_command, output_log_level, shell):
    last_lines = []
    process = subprocess.Popen(
        full_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell
    )

    while process.poll() is None:
        line = process.stdout.readline().rstrip().decode()
        if not line:
            continue

        # Keep the last few lines of output in case the command errors, and we need the output for
        # the exception below.
        last_lines.append(line)
        if len(last_lines) > ERROR_OUTPUT_MAX_LINE_COUNT:
            last_lines.pop(0)

        logger.log(output_log_level, line)

    remaining_output = process.stdout.read().rstrip().decode()
    if remaining_output:  # pragma: no cover
        logger.log(output_log_level, remaining_output)

    exit_code = process.poll()
    if exit_code >= BORG_ERROR_EXIT_CODE:
        # If an error occurs, include its output in the raised exception so that we don't
        # inadvertently hide error output.
        if len(last_lines) == ERROR_OUTPUT_MAX_LINE_COUNT:
            last_lines.insert(0, '...')

        raise subprocess.CalledProcessError(
            exit_code, ' '.join(full_command), '\n'.join(last_lines)
        )


def execute_command(full_command, output_log_level=logging.INFO, shell=False):
    '''
    Execute the given command (a sequence of command/argument strings) and log its output at the
    given log level. If output log level is None, instead capture and return the output. If
    shell is True, execute the command within a shell.
    '''
    logger.debug(' '.join(full_command))

    if output_log_level is None:
        output = subprocess.check_output(full_command, shell=shell)
        return output.decode() if output is not None else None
    else:
        execute_and_log_output(full_command, output_log_level, shell=shell)
