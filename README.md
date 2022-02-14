# Lua Love

[![LOVE](https://img.shields.io/badge/L%C3%96VE-11.4-EA316E.svg)](https://love2d.org/)
[![Downloads](https://img.shields.io/packagecontrol/dt/Lua%20Love.svg)](https://packagecontrol.io/packages/Lua%20Love)

LuaLove is a package for [Sublime Text](http://www.sublimetext.com) which brings LÖVE 2D API syntax highlighting and more. It is based on [SublimeLove](https://github.com/minism/SublimeLove), [LuaSublime](https://github.com/rorydriscoll/LuaSublime), and [lua_snippet](https://github.com/yinqiang/lua_snippet).

![Syntax highlighting example](https://i.imgur.com/m4nmthh.png "Syntax highlighting, auto completions and error checking (on Ubuntu)")

## Features

* LÖVE 2D syntax highlighting (including GLSL shaders code, ffi.cdef and LDoc comments)
* Auto completions with metadata (see [below](#auto-completions-and-snippets))
* Some Lua snippets
* Errors highlighting (configurable)
* Build systems (configurable)

## Installation

### Using [Package Control](https://packagecontrol.io/installation)

1. Open Command Palette (`Ctrl`+`Shift`+`P` or `Cmd`+`Shift`+`P` on Mac). Alternatively go to `Tools > Command Palette...`
2. Enter `Package Control: Install Package`
3. Find and install `Lua Love` package

### Manual

1. Go to `Packages` directory by `Preferences > Browse Packages...`
2. Download and extract [.zip](https://github.com/szensk/subllualove/archive/master.zip) or clone git repository by running:
```bash
git clone git://github.com/szensk/subllualove.git
```

## Settings

Settings are saved in [JSON](https://www.json.org/json-en.html) format. You can change settings in `Preferences > Package Settings > Lua Love` or by running `Preferences: LuaLove Settings` in command Palette.

## Error checking

By default any Lua file or file with LOVE syntax will be run through selected live parser and the first encountered error (if any) is highlighted. The error is displayed in the status bar and from Sublime Text 4 also in annotation.

## Syntax highlighting

Set syntax using `View > Syntax > LOVE` or in command palette `Set Syntax: LOVE`.

If you are using shaders and wants better GLSL syntax highlighting, install some GLSL syntax plugin, as if no GLSL syntax is found, it will fallback to C syntax. C code in `ffi.cdef` is highlighted as C.

## Auto completions and snippets

There are auto completions for LOVE functions and variables (like `love.graphics.setColor`), Lua and LuaJIT functions and variables (like `coroutine.resume`, `ffi.cdef`, `bit.bor`). Functions and variables have metadata - kind (function, variable, ...) and details with link to the manual displayed since Sublime Text 4.

Pressing `Ctrl`+`Space` (`Cmd`+`Space` on Mac) in an open Lua file or file with LOVE set as syntax will show the auto completions for the Löve2D API as well as Lua function snippets.

To enable auto completions for LDoc without pressing `Ctrl`+`Space` (`Cmd`+`Space` on Mac), add `{"selector": "comment.block.documentation.lua"}` to `auto_complete_triggers` in settings.

## Build systems

Build systems are available there to launch your project by just pressing `Ctrl`+`B` (`Cmd`+`B` on Mac) or `F7`.

To set up build system, go to `Tools > Build System` and select `LuaLove`.

If you don't have `love` in your PATH or you would like to tweak some build system settings, see `build_system.(variant).*` options in [settings](#settings)

### Variants

First time you build your project, you will be asked to select one of the variants described below. You can change them anytime by pressing `Ctrl`+`Shift`+`B` (`Cmd`+`Shift`+`B` on Mac)

| Build system variant | Description |
| --- | --- |
| **LuaLove** | starts LÖVE 2D in current opened folder |
| **LuaLove - LuaJIT Run File** | runs current file using LuaJIT |
| **LuaLove - Lua Run File** | runs current file using Lua |
| **LuaLove - ldoc: File** | runs ldoc with current file and outputs markdown file in `doc` folder |
| **LuaLove - ldoc: Project** | runs ldoc with `src` folder in current opened folder and outputs markdown files in `doc` folder |