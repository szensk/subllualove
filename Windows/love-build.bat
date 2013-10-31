@echo off
for /R %CD% %%D in (*.lua) do ( call :Work %%D )
goto End

:Work
set var=%1
set dire=%var%
set dire=%dire:~0,-8%
set var=%var:~-8%
if "%var%"=="main.lua" love %dire% & break
GOTO :EOF

:End
@echo on
