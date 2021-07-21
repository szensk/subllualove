import sublime, sublime_plugin
import os
import re
import threading, subprocess
from shlex import quote

PACKAGE_DIR = os.path.splitext(os.path.basename(os.path.dirname(__file__)))[0]

# Command object with timeout
class Command(object):
	def __init__(self, cmd, text):
		self.cmd = cmd
		self.text = text
		self.process = None
		self.result = None

	def run(self, timeout):
		def target():
			self.process = subprocess.Popen(self.cmd, bufsize=-1, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			self.result = self.process.communicate(self.text.encode('utf-8'))[1]

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			self.process.terminate()
			thread.join()

		return self.result

class ParseLuaCommand(sublime_plugin.EventListener):

	settings = sublime.load_settings("LuaLove.sublime-settings")

	scope_regex = re.compile('^([\S]+)')

	parser_window = settings.get("live_parser_window", 200)
	ST = 3000 if sublime.version() == '' else int(sublime.version())

	def __init__(self):
		self.pending = 0

		self.detected_parser = None

		if self.settings.get('live_parser_type', 'auto') == 'auto':
			try:
				subprocess.Popen(self.settings.get('luajit_path', 'luajit'))
				if '.sublime-package' in PACKAGE_DIR:
					raise Exception('Lua Love is packaged, unable to use luajit')
			except:
				try:
					subprocess.Popen(self.settings.get('luac_path', 'luac'))
				except:
					print('Neither luajit nor luac found, no live parser will be available')
				else:
					self.detected_parser = 'luac'
			else:
				self.detected_parser = 'luajit'


	def onchange(self, view):
		if not self.settings.get("live_parser"):
			return False
		filename = view.file_name()

		if 'source.lua.love' not in self.scope_regex.findall(view.scope_name(view.sel()[-1].b)) and (not filename or not filename.endswith('.lua')):
			view.erase_regions('lua')
			return False

		self.pending = self.pending + 1
		return True

	def on_modified(self, view):
		if self.ST < 3000 and self.onchange(view):
			sublime.set_timeout(lambda: self.parse(view), self.parser_window)

	def on_modified_async(self, view):
		if self.ST >= 3000 and self.onchange(view):
			sublime.set_timeout_async(lambda: self.parse(view), self.parser_window)

	def parse(self, view):
		# Don't bother parsing if there's another parse command pending
		if self.pending > 1:
			self.pending -= 1
			return

		# Run parser with the parse immediate option
		text = view.substr(sublime.Region(0, view.size()))

		parser_type = self.settings.get('live_parser_type', 'luac')

		if parser_type == 'luajit' or (parser_type == 'auto' and self.detected_parser == 'luajit'):
			command = Command(self.settings.get('luajit_path', 'luajit') + ' ' + quote(os.path.dirname(__file__) + '/LuaJIT-parser.lua'), text)
		elif parser_type == 'luac' or (parser_type == 'auto' and self.detected_parser == 'luac'):
			command = Command(self.settings.get('luac_path', 'luac') + ' -p -', text)
		elif parser_type == 'custom' and self.settings.get('live_parser_custom_command'):
			command = Command(self.settings.get('live_parser_custom_command'), text)
		else:
			self.pending -= 1
			return False

		# Attempt to parse and grab output, fail after one second
		errors = command.run(timeout=self.settings.get("live_parser_timeout", 1))

		# Nothing to do if it parsed successfully
		if errors:
			errors = errors.decode("utf-8")
		else:
			# Clear out any old region markers
			view.erase_regions('lua')

			sublime.status_message('')
			self.pending -= 1
			return

		# Add regions and place the error message in the status bar
		errors = errors.replace("luac: stdin:", "Line ")

		if self.settings.get('live_parser_status_bar', True):
			sublime.status_message(errors)

		pattern = re.compile(r'Line ([0-9]+):')
		regions = [view.full_line(view.text_point(int(match) - 1, 0)) for match in pattern.findall(errors)]

		# Persistence of error highlights
		persistent = 0
		if self.settings.get("live_parser_persistent", False):
			persistent = sublime.PERSISTENT
		style = self.settings.get("live_parser_style")

		if self.ST >= 4050 and self.settings.get("live_parser_annotations"):
			pattern = re.compile(r'Line [0-9]+:\s?(.+)')

			# Escape < and > as annotations are in HTML format
			annotations = [match.replace('<', '&lt;').replace('>', '&gt;') for match in pattern.findall(errors)]

			if style == "outline":
				view.add_regions('lua', regions, 'invalid', '', sublime.DRAW_OUTLINED | persistent, annotations)
			elif style == "dot":
				view.add_regions('lua', regions, 'invalid', 'dot', sublime.HIDDEN | persistent, annotations)
			elif style == "circle":
				view.add_regions('lua', regions, 'invalid', 'circle', sublime.HIDDEN | persistent, annotations)
		else:

			if style == "outline":
				view.add_regions('lua', regions, 'invalid', '', sublime.DRAW_OUTLINED | persistent)
			elif style == "dot":
				view.add_regions('lua', regions, 'invalid', 'dot', sublime.HIDDEN | persistent)
			elif style == "circle":
				view.add_regions('lua', regions, 'invalid', 'circle', sublime.HIDDEN | persistent)

		self.pending -= 1

# Settings command
class LualoveEditSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('edit_settings', {
			'base_file': '${packages}/' + PACKAGE_DIR + '/LuaLove.sublime-settings',
			'default': '// Settings in here override those in "LuaLove.sublime-settings"\n{\n\t$0\n}\n',
		})

# Provide custom build target, inherited from exec, to patch some settings
from Default.exec import ExecCommand

class LualoveRun(ExecCommand):
	def __init__(self, window):
		self.window = window
		super().__init__(window)

	def run(self, *args, **kwargs):
		settings = sublime.load_settings("LuaLove.sublime-settings")

		# No idea why Windows needs this, but at least on Ubuntu, it is causing troubles
		# (when cmd is array of multiple strings and shell = True, working with cmd being only
		# array of one string, but then spaces or ' or " can cause troubles as they are not escaped...)
		if sublime.platform() == 'windows':
			kwargs['shell'] = True

		if 'type' in kwargs:
			if settings.get('build_system.' + kwargs['type'] + '.cmd'):
				# Get variable values
				variables = self.window.extract_variables()
				# Replace variables with their values and replace command
				kwargs['cmd'] = [sublime.expand_variables(arg, variables) for arg in settings.get('build_system.' + kwargs['type'] + '.cmd')]
			if settings.get('build_system.' + kwargs['type'] + '.env'):
				kwargs['env'] = settings.get('build_system.' + kwargs['type'] + '.env')

			# ExecCommand is not expecting type and would cause error
			del kwargs['type']

		# Run original
		super().run(*args, **kwargs)