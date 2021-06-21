#!/usr/bin/luajit

local ok, msg = loadfile()

if not ok then
	io.stderr:write(msg)
	os.exit(1)
end