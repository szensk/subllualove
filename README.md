# Description

LuaLove is a package for [Sublime Text 2/3/4](http://www.sublimetext.com) which brings Löve2D API syntax highlighting and more. It is based on [SublimeLove](https://github.com/minism/SublimeLove), [LuaSublime](https://github.com/rorydriscoll/LuaSublime), and [lua_snippet](https://github.com/yinqiang/lua_snippet).

![Syntax highlighting example](https://i.imgur.com/xT91wN3.png "Syntax highlighting, auto completions and error checking (on Ubuntu)")

## Features

* Löve 2D syntax highlighting (including GLSL shaders code and LDoc comments)
* Auto completions (with description and link to manual, see [below](#auto-completions-and-snippets))
* Some Lua snippets
* Errors highlighting (requires luac in PATH)
* Build systems

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

Settings are saved in [JSON](https://www.json.org/json-en.html) format. You can view default settings at `Preferences > Package Settings > Lua Love > Settings - Default` and you can customize your settings at `Preferences > Package Settings > Lua Love > Settings - User`.

### Available settings

`"live_parser"` *boolean*  
Whatever to enable live parser

`"live_parser_style"` *string*  
Style of live parser error highlighting. Available styles are `outline`, `dot` and `circle`

`"live_parser_annotations"` *boolean*  
Whatever to show errors messages on right hand edge of the view in addition to status bar. Available since Sublime Text 4 (ignored in older versions)

`"live_parser_persistent"` *boolean*  
Whatever make error highlighting persist across sessions

`"live_parser_timeout"` *number*  
Timeout for luac to execute (in ms)

`"luac_path"` *string*  
Path to luac executable. Change only if luac is not in your PATH

## Error checking

By default any Lua file or file with LÖVE 11.3 syntax highlighting will be run through `luac -p` and the first encountered error (if any) is highlighted. The error is displayed in the status bar and from Sublime Text 4 also in right-hand edge of the view.

## Syntax highlighting

Set syntax using `View > Syntax > LÖVE 11.3` or in command palette `Set Syntax: LÖVE 11.3`.

If you are using shaders and wants better GLSL syntax highlighting, install some GLSL syntax plugin, as if no GLSL syntax is found, it will fallback to C syntax. C code in `ffi.cdef` is highlighted as C.

## Auto completions and snippets

There are auto completions for love functions (like `love.graphics.setColor`), all Lua functions and variables (ex: `coroutine.resume`) and LuaJIT function and variables (ex: `ffi.cdef`, `bit.bor`). Lua and LuaJIT functions and variables have metadata - kind and details with link to manual displayed since Sublime Text 4. Metadata for löve, socket and utf8 functions and variables is not yet done (support welcome).

Pressing `Ctrl`+`Space` in an open Lua file or file with LÖVE 11.3 set as syntax will show the auto completions for the Löve2D API as well as Lua function snippets.

Those Löve2D functions which are not overloaded (only one possible argument combination), will fill in the argument names for you.

## Build systems

Build systems are available there to launch your project by just pressing `Ctrl`+`B` (`Cmd`+`B` on Mac) or `F7`.

To set up build system, go to `Tools > Build System` and select `LuaLove`.

### Build systems variants

First time you build your project, you will be asked to select one of the variants described below. You can change them anytime by pressing `Ctrl`+`Shift`+`B` (`Cmd`+`Shift`+`B` on Mac)

* **LuaLove** - starts Löve2D in current opened folder

* **LuaLove - LuaJIT Run File** - runs current file using LuaJIT (requires LuaJIT in your system PATH)

* **LuaLove - Lua Run File** - runs current file using Lua (requires Lua in your system PATH)

* **LuaLove - ldoc: File** - runs ldoc with current file and outputs markdown file in `doc` folder

* **LuaLove - ldoc: Project** - runs ldoc with `src` folder in current opened folder and outputs markdown files in `doc` folder