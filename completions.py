#completions.py
import sublime
import sublime_plugin
import re

class LoveCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        seps = view.settings().get("word_separators")
        seps = seps.replace('.', '')
        view.settings().set("word_separators", seps)
