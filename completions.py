#completions.py
import sublime
import sublime_plugin
import re

class LoveCompletions(sublime_plugin.EventListener):
    ST = 3000 if sublime.version() == '' else int(sublime.version())

    def on_query_completions(self, view, prefix, locations):
        if self.ST < 3000 and ("lua" in view.scope_name(locations[0])):
            seps = view.settings().get("word_separators")
            seps = seps.replace('.', '')
            view.settings().set("word_separators", seps)
