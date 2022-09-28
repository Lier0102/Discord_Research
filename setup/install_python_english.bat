@echo off

goto check_perm
check_perm:
    echo "[ Detecting ] Administrative permissions..."

    net session > nul 2>&1
    if %errorlevel% == 0 (
        echo "[ Success ] Administrative permissions confirmed."
        goto main
    ) else (
        echo "[ Failure ] permission is inadequate"
        exit
    )    

main:
    echo "[ Download ] Python Installer" && curl -L -O https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe
    echo "[ Running ] Python Installer" && python-3.10.5-amd64.exe /quiet PrependPath=1 Include_test=0
    echo "[ Removing ] Python Installer" && del python-3.10.5-amd64.exe
    color 02 && echo "[ DONE ]" && echo "PYTHON(3.10.5) INSTALLED" && start .