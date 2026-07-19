@echo off
title NEMESIS Setup
echo === NEMESIS Setup ===
echo.
echo Installing Python modules...
python -m pip install --upgrade pip --user >nul 2>&1
python -m pip install customtkinter --user >nul 2>&1
python -m pip install pyinstaller --user >nul 2>&1
python -m pip install pillow --user >nul 2>&1
python -m pip install opencv-python --user >nul 2>&1
python -m pip install requests --user >nul 2>&1
echo.
echo All modules installed!
echo.
echo Start GUI: nemesis_py_builder.exe
echo Start CMD: Nemesis.exe
pause