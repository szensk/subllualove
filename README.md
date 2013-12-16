Description
===========

LuaLove is a package for [Sublime Text 2/3](http://www.sublimetext.com) with support for the Love2D API. It is based on [SublimeLove](https://github.com/minism/SublimeLove), [LuaSublime](https://github.com/rorydriscoll/LuaSublime), and [lua_snippet](https://github.com/yinqiang/lua_snippet).

Installation
============

You can install this package through [Package Control](https://sublime.wbond.net/installation), simply use Command Palette: Package Control Install Package -> Lua Love.

Alternatively, you can install this package by running the following command in your Packages directory:

    git clone git://github.com/szensk/subllualove.git

Error checking
--------------
By default any Lua file will be run through luac -p and the first encountered error is outlined. The error is displayed in the status bar.

To disable or change this behavior

```json
{
   	"live_parser": true,
   	"live_parser_style": "{dot|circle|outline}",
   	"live_parser_persistent:" false,
   	"luac_path": "luac"
}
```

in Lua Love > User Settings.

Syntax highlighting
-------------------
![alt text](https://i.imgur.com/OEESOtU.png "syntax hightlighting")

Command Palette: Set Syntax: Lua (Love).

If you create a new shader, and make the argument a multi-line string, then Sublime will use C syntax highlighting for the GLSL within.

Snippets
--------
There are snippets for most built-in Lua functions (ex: coroutine.resume), some LuaJIT functions (ex: bit.bor), and LuaDoc tags are available in comments. For example. "@param" expands to "-- @param type name desc".

Auto completion
---------------
Pressing Ctrl+Space in an open Lua file will show the autocompletions for the Love2D API as well as Lua function snippets.

Those Love2D functions which are not overloaded (only one possible argument combination), will fill in the argument names for you.

Build systems
-------------
Go to Tools > Build System and select "Love".

* Command Palette: "Love2D" will execute Love on the current project path (requires love on your system PATH).

* Command Palette: "ldoc: File" will run ldoc on the current file (requires ldoc on your system PATH).

* Command Palette: "ldoc: Project" will run ldoc on the current project (requires ldoc on your system PATH).

* Build (Ctrl+B): execute current file with Lua.

* Run (Ctrl+Shift+B): execute current file with LuaJIT (requires luajit on your system PATH).

The build system will automatically be selected for .lua files.
