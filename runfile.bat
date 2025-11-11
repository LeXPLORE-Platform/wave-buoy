@echo off
setlocal enabledelayedexpansion

:: Ensure correct location
cd "C:\Users\Seatronic 1147\Documents\Data_Lexplore\git\wave-buoy"

:: Ensure repo is up to date
:: git stash
:: git pull

:: Load input variables
call "scripts\input_batch.bat"

:: Backup files
md %backup%
robocopy %in% %backup% /NFL /NDL /NJH /NJS /nc /ns /np

:: Process meteostation data
for %%a in (%in%"\*.txt") do (
	%pythonenv% %script% "%%a"
	move "%%a" %level0%
)

:: Push changes to remote repository
git add --all
git commit -m "Auto Upload"
git push

