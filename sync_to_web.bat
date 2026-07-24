@echo off
cd /d H:\web-bao-cao
echo Dang dong bo du lieu moi len Web...
git add .
git commit -m "Auto update daily KPI data"
git push origin main
echo Dong bo thanh cong!
