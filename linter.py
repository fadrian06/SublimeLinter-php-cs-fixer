import logging
import os

from SublimeLinter.lint import Linter, util


logger = logging.getLogger('SublimeLinter.plugin.php-cs-fixer')


def find_configuration_file(file_name):
    if not file_name:
        return None

    checked = []
    check_dir = os.path.dirname(file_name)
    candidates = ['.php-cs-fixer.php', '.php-cs-fixer.dist.php', '.php_cs', '.php_cs.dist']
    while check_dir not in checked:
        for candidate in candidates:
            configuration_file = os.path.join(check_dir, candidate)
            if os.path.isfile(configuration_file):
                return configuration_file

        checked.append(check_dir)
        check_dir = os.path.dirname(check_dir)

    return None


class PhpCsFixer(Linter):
    """Provides an interface to php-cs-fixer."""

    defaults = {
        'selector': 'embedding.php, source.php, text.html.basic'
    }
    regex = (
        r'^\s+\d+\)\s+.+\s+\((?P<message>.+)\)[^\@]*'
        r'\@\@\s+\-\d+,\d+\s+\+(?P<line>\d+),\d+\s+\@\@'
        r'[^-+]+[-+]?\s+[^\n]*'
    )
    multiline = True
    tempfile_suffix = 'php'
    error_stream = util.STREAM_STDOUT
    line_col_base = (-2, 1)

    def cmd(self):
        """Read cmd from inline settings."""
        command = ['php-cs-fixer']
        command.append('fix')
        command.append('${temp_file}')
        command.append('--dry-run')
        command.append('--show-progress=none')
        command.append('--stop-on-violation')

        if self.settings.get('version') == 2:
            command.append('--diff-format=udiff')
        else:
            command.append('--diff')

        command.append('--using-cache=no')
        command.append('--no-ansi')
        command.append('-vv')

        config_file = self.settings.get('config_file')
        if not config_file:
            config_file = find_configuration_file(self.view.file_name())
        if config_file:
            command.append('--config=' + config_file)

        return command
