@echo off
cd /d C:\Users\TATUM\lao-lotto-archive
echo ========================================
echo Lao Lottery Auto Update
echo %DATE% %TIME%
echo ========================================

:: รันสคริปต์ดึงข้อมูล
python lottoscrape-sanook.py

:: Commit และ push ขึ้น GitHub
git add .
git commit -m "Auto-update: %DATE% %TIME%"
git push origin master

echo.
echo Update completed at %TIME%
