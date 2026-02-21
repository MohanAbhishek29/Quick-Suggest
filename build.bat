@echo off
echo Compiling C++ Backend...
g++ server.cpp -o server.exe -lws2_32 -static-libgcc -static-libstdc++
if %errorlevel% neq 0 (
    echo Compilation Failed!
    pause
    exit /b
)
echo Compilation Successful!
echo Open run.bat to start the server.
pause
