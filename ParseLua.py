import sublime
import sublime_plugin
import re
from subprocess import Popen, PIPE

class ParseLuaCommand(sublime_plugin.EventListener):

	TIMEOUT_MS = 200
	ST = 3000 if sublime.version() == '' else int(sublime.version())

	def __init__(self):
		self.pending = 0

	def onchange(self, view):
		self.settings = sublime.load_settings("LuaLove.sublime-settings")
		if not self.settings.get("live_parser"):
			return False
		filename = view.file_name()
		if not filename or not filename.endswith('.lua'):
			return False
		self.pending = self.pending + 1
		return True

	def on_modified(self, view):
		if self.ST >= 3000:
			return
		if self.onchange(view):
			sublime.set_timeout(lambda: self.parse(view), self.TIMEOUT_MS)

	def on_modified_async(self, view):
		if self.ST < 3000:
			return
		if self.onchange(view):
			sublime.set_timeout_async(lambda: self.parse(view), self.TIMEOUT_MS)

	def parse(self, view):
		# Don't bother parsing if there's another parse command pending
		self.pending = self.pending - 1
		if self.pending > 0:
			return
		# Grab the path to luac from the settings
		luac_path = self.settings.get("luac_path", "luac")
		# Run luac with the parse option
		p = Popen(luac_path + ' -p -', stdin=PIPE, stderr=PIPE, shell=True)
		text = view.substr(sublime.Region(0, view.size()))
		errors = p.communicate(text.encode('utf-8'))[1]
		result = p.wait()
		#luac: stdin:
		# Clear out any old region markers
		view.erase_regions('lua')
		# Nothing to do if it parsed successfully
		if result == 0:
			return
		# Add regions and place the error message in the status bar
		errors = errors.decode("utf-8")
		errors = errors.replace("luac: stdin:", "Line:")
		sublime.status_message(errors)
		pattern = re.compile(r':([0-9]+):')
		regions = [view.full_line(view.text_point(int(match) - 1, 0)) for match in pattern.findall(errors)]
		# view.add_regions('lua', regions, 'invalid', 'DOT', sublime.HIDDEN)
		style = self.settings.get("live_parser_style")
		if style == "outline":
			view.add_regions('lua', regions, 'invalid', '', sublime.DRAW_OUTLINED | sublime.PERSISTENT)
		elif style == "dot":
			view.add_regions('lua', regions, 'invalid', 'DOT', sublime.HIDDEN)
		elif style == "circle":
			view.add_regions('lua', regions, 'invalid', 'CIRCLE', sublime.HIDDEN)

