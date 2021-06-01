# Description

LuaLove is a package for [Sublime Text 2/3/4](http://www.sublimetext.com) with support for the Löve2D API. It is based on [SublimeLove](https://github.com/minism/SublimeLove), [LuaSublime](https://github.com/rorydriscoll/LuaSublime), and [lua_snippet](https://github.com/yinqiang/lua_snippet).

## Installation

You can install this package through [Package Control](https://sublime.wbond.net/installation), simply use Command Palette: Package Control Install Package -> Lua Love.

Alternatively, you can install this package by running the following command in your Packages directory:

    git clone git://github.com/szensk/subllualove.git

## Error checking

By default any Lua file will be run through `luac -p` and the first encountered error is outlined. The error is displayed in the status bar and from Sublime Text build 4050 also in right-hand edge of the view.

## Settings
To change settings, copy default settings from `Preferences > Package Settings -> Lua Love -> Settings - Default` to `Preferences > Package Settings -> Lua Love -> Settings - User` and modify them as you want

## Syntax highlighting

![Syntax hightlighting example](https://i.imgur.com/xT91wN3.png "syntax hightlighting, auto completion and error checking")

Command Palette: Set Syntax: LÖVE 11.3.

If you want better GLSL syntax highlighting (as normally it is just C syntax highlighting), install GLSL syntax plugin

## Snippets

There are snippets for most built-in Lua functions (ex: coroutine.resume), some LuaJIT functions (ex: bit.bor).

## Auto completion

Pressing Ctrl+Space in an open Lua file will show the autocompletions for the Löve2D API as well as Lua function snippets.

Those Löve2D functions which are not overloaded (only one possible argument combination), will fill in the argument names for you.

## Build systems

Go to Tools > Build System and select "Love".

* Command Palette: "Love2D" will execute Love on the current project path (requires love on your system PATH).

* Command Palette: "ldoc: File" will run ldoc on the current file (requires ldoc on your system PATH).

* Command Palette: "ldoc: Project" will run ldoc on the current project (requires ldoc on your system PATH).

* Build (Ctrl+B): execute current file with Lua.

* Run (Ctrl+Shift+B): execute current file with LuaJIT (requires luajit on your system PATH).

The build system will automatically be selected for .lua files.
