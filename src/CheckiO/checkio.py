import sublime
import sublime_plugin
import subprocess
import sys
import shlex


class RunCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.set_timeout_async(self.run_release, 0)

    def run_release(self):
        window = self.view.window()

        code = self.view.substr(sublime.Region(0, self.view.size()))
        sublime.active_window().run_command("save")
        sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": False})
        window.focus_group(window.active_group())
        first_line = code.strip().splitlines()[0]
        print(first_line)
        if not first_line.startswith('#!') or 'checkio' not in first_line:
            print('It is not a CheckiO solution')
            return
        self.run_next(code, first_line[2:])

    def run_next(self, code, first_line):
        self.exec_command(first_line + ' ' + self.view.file_name())

    def exec_command(self, exec_line):
        print('>>> {}'.format(exec_line))
        commands = shlex.split(exec_line)
        proc = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while proc.poll() is None:
            data = proc.stdout.readline().decode('utf-8')
            print(data, end="")
        print(proc.stderr.read().decode('utf-8'))
        print('<<< Done')

class CheckCommand(RunCommand):
    def run_next(self, code, first_line):
        self.exec_command(first_line + ' ' + self.view.file_name() + ' --check')
