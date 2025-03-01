from re import search
from typing import Iterator

from sublime import Region

from SublimeLinter.lint import ComposerLinter
from SublimeLinter.lint.linter import LintMatch


class PhpCsFixer(ComposerLinter):
    """Provides an interface to php-cs-fixer."""
    cmd = (
        'php-cs-fixer',
        'check',
        '${file}',
        '--diff',
        '--no-ansi',
        '--show-progress=none',
        '--using-cache=no',
        '--stop-on-violation',
        '-v',
        '${args}'
    )

    defaults = {
        'selector': 'embedding.php'
    }

    default_type = 'warning'

    def find_errors(self, output: str) -> Iterator[LintMatch]:
        file_content = self.view.substr(Region(0, self.view.size()))
        file_lines = file_content.splitlines()
        matches = []
        output_lines = output.splitlines()
        lines_to_remove = {}
        lines_to_add = {}
        file_line = 0
        rule_name_pattern = r'\((.*?)\)'
        rule_name = ''
        rule_description = ''

        for output_line in output_lines:
            output_first_character = output_line[0:1]
            filtered_output_line = output_line[1:]

            search_result = search(rule_name_pattern, filtered_output_line)

            if search_result:
                rule_name = search_result.group(1)

                found, executable = self.context_sensitive_executable_path([
                    'php-cs-fixer'
                ])

                if found:
                    cmd = [executable, 'describe', rule_name, '--no-ansi']
                    rule_description = self.run(cmd, '')

            if '++' in filtered_output_line or '--' in filtered_output_line:
                continue

            if output_first_character not in ('+', '-'):
                continue

            if output_first_character == '-':
                file_line = file_lines.index(filtered_output_line) + 1
                lines_to_remove[file_line] = filtered_output_line
                lines_to_add.setdefault(file_line, [])

            if output_first_character == '+':
                lines_to_add[file_line].append(filtered_output_line)

        for line_number in lines_to_remove.keys():
            if lines_to_remove[line_number] == '':
                continue

            line_content = lines_to_remove[line_number]
            message = '\n'.join(lines_to_add[line_number])
            col = 0

            for char in line_content:
                if char == ' ' or char == '\t':
                    col += 1
                else:
                    break

            matches.append(LintMatch({
                'line': line_number - 1,
                'message': f'{message}\n/*\n{rule_description}*/',
                'col': col,
                'end_col': len(line_content),
                'code': rule_name
            }))

        return iter(matches)
