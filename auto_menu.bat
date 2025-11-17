@echo off

title AutoMidjourney Menu

:menu

echo.
echo ========================================
echo    AutoMidjourney Menu
echo ========================================
echo.
echo    [A] Run Auto Midjourney script
echo    [D] Refresh database from Google Sheets
echo    [X] Exit
echo.
set /p choice=Enter your choice (A/D/X): 

if /i "%choice%"=="A" goto run_script
if /i "%choice%"=="a" goto run_script
if /i "%choice%"=="D" goto refresh_db
if /i "%choice%"=="d" goto refresh_db
if /i "%choice%"=="X" goto exit
if /i "%choice%"=="x" goto exit

echo Invalid choice. Please try again.
goto menu

:run_script
echo.
echo Starting Auto Midjourney script...
call "E:\Dropbox\Dev\Projects\POD Projects\automidjourney\auto400.bat"
echo Script execution completed.
goto menu

:refresh_db
echo.
echo Refreshing database from Google Sheets...
cd /d E:\Dropbox\Dev\Projects\POD Projects\automidjourney
uv run auto_midjourney.py --update_db
echo Database refresh completed.
goto menu

:exit
echo.
echo Exiting script.
pause

