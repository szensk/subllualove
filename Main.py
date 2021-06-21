import sublime, sublime_plugin
import os
import re
import threading, subprocess

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

	TIMEOUT_MS = settings.get("live_parser_timeout", 200)
	ST = 3000 if sublime.version() == '' else int(sublime.version())

	def __init__(self):
		self.pending = 0

		self.detected_parser = None

		if self.settings.get('live_parser_type', 'auto') == 'auto':
			try:
				subprocess.Popen(self.settings.get('luajit_path', 'luajit'))
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
			sublime.set_timeout(lambda: self.parse(view), self.TIMEOUT_MS)

	def on_modified_async(self, view):
		if self.ST >= 3000 and self.onchange(view):
			sublime.set_timeout_async(lambda: self.parse(view), self.TIMEOUT_MS)

	def parse(self, view):
		# Don't bother parsing if there's another parse command pending
		if self.pending > 1:
			self.pending -= 1
			return

		# Run parser with the parse immediate option
		text = view.substr(sublime.Region(0, view.size()))

		parser_type = self.settings.get('live_parser_type', 'luac')

		if parser_type == 'luajit' or (parser_type == 'auto' and self.detected_parser == 'luajit'):
			command = Command(self.settings.get('luajit_path', 'luajit') + ' ' + os.path.dirname(__file__) + '/LuaJIT-parser.lua', text)
		elif parser_type == 'luac' or (parser_type == 'auto' and self.detected_parser == 'luac'):
			command = Command(self.settings.get('luac_path', 'luac') + ' -p -', text)
		else:
			self.pending -= 1
			return False

		# Attempt to parse and grab output, bail after one second
		errors = command.run(timeout=1)

		# Clear out any old region markers
		view.erase_regions('lua')

		# Nothing to do if it parsed successfully
		if errors:
			errors = errors.decode("utf-8")
		else:
			sublime.status_message('')
			self.pending -= 1
			return

		# Add regions and place the error message in the status bar
		errors = errors.replace("luac: stdin:", "Line:")
		sublime.status_message(errors)

		pattern = re.compile(r':([0-9]+):')
		regions = [view.full_line(view.text_point(int(match) - 1, 0)) for match in pattern.findall(errors)]


		# Persistence of error highlights
		persistent = 0
		if self.settings.get("live_parser_persistent", False):
			persistent = sublime.PERSISTENT
		style = self.settings.get("live_parser_style")

		if self.ST >= 4050 and self.settings.get("live_parser_annotations"):
			pattern = re.compile(r':[0-9]+:(.*)$')
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

class LualoveEditSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('edit_settings', {
			'base_file': '${packages}/' + PACKAGE_DIR + '/LuaLove.sublime-settings',
			'default': '// Settings in here override those in "LuaLove.sublime-settings"\n{\n\t$0\n}\n',
		})