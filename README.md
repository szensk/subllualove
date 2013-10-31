Description
===========

LuaLove is a package for [Sublime Text 2](http://www.sublimetext.com/2) with support for Love2D. Based on [SublimeLove](https://github.com/minism/SublimeLove), [LuaSublime](https://github.com/rorydriscoll/LuaSublime), and [lua_snippet](https://github.com/yinqiang/lua_snippet).

Installation
============

You can install this package by running the following command in your ST2 Packages directory:
    
    git clone git://github.com/szensk/subllualove.git

Error checking
--------------
By default any Lua file will be run through luac -p and the first encountered error is outlined. The error is displayed in the status bar.

To disable this behavior

    "live_parser": false 
	
in LuaLove > User Settings. 

To change the outline to a more subtle dot or circle in the gutter

    "live_parser_style": "{dot|circle|outline}"
	
in LuaLove > User Settings. 

Syntax highlighting
-------------------
Command Palette: Set Syntax: Lua (Love).

If you create a new pixel effect, and make the argument a multi-line string, then Sublime will use C syntax highlighting for the GLSL content.

Auto completion
---------------
Pressing Ctrl+Space in an open Love file will show the autocompletions for the API functions.  ST2 currently has some issues with autocomplete that other plugins are also dealing with, so its not perfect yet.  One major issue is that the period key breaks tokens and doesn't get included as part of the autocomplete query.

Those Love2D functions which are not overloaded (only one possible argument combination), will fill in the argument names for you.

Build systems
-------------
Go to Tools > Build System and select "Love".  

* Command Palette: "Love2D" will execute Love (requires love on your system PATH).

* Command Palette: "ldoc: File" will run ldoc on the current file (requires ldoc on your system PATH).

* Command Palette: "ldoc: Project" will run ldoc on the current project (requires ldoc on your system PATH).

* Build (Ctrl+B): execute current file with Lua.

* Run (Ctrl+Shift+B): execute current file with LuaJIT.

The build system will automatically be selected for .lua files.
