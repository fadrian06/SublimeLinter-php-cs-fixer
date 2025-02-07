SublimeLinter-php-cs-fixer
==========================

This linter plugin for [SublimeLinter][docs] provides an interface to [php-cs-fixer](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer). It will be used with files that have the “php” syntax.

The purpose of this plugin is to highlight things that would normally be fixed by running php-cs-fixer on your file. This will allow you to identify code changes that you need to make while coding instead of relying on the tool to do it for you.

## Installation

SublimeLinter 3 must be installed in order to use this plugin.

Please install via [Package Control](https://packagecontrol.io).

Before using this plugin, you must ensure that `php-cs-fixer >= 2.7` is installed on your system, or in your project (via composer).

## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

For `"phpcsfixer"` you can optionally specify:

- "config_file": the path to the config file to use (globally or in your project using `${folder}/path/to//Users/koenlageveen/peppered-local/deklap/.php-cs-fixer.dist.php`). 
- "version": by default PHP-CS-Fixer V3 is used. Set this value to `2` to use V2.

