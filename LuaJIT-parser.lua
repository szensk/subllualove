#!/usr/bin/luajit

local ok, msg = loadfile()

if not ok then
	msg = msg:gsub('^stdin:', 'Line ')
	io.stderr:write(msg)
	os.exit(1)
end