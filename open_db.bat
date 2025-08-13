@echo off

rem Opening the SQLite DB with "DB Browser for SQLite"

set exe="E:\PortableApps\PortableApps\SQLiteDatabaseBrowserPortable\SQLiteDatabaseBrowserPortable.exe"
set db="E:\Dropbox\Dev\Projects\Python\automidjourney\automidjourney.db"

start "" /b %exe% %db%
exit
