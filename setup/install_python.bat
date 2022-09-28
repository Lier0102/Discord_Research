@echo off

goto check_perm
check_perm:
    echo "[ SYSTEM ] 관리자 권한 감지중..."

    net session > nul 2>&1
    if %errorlevel% == 0 (
        echo "[ GOOD ] 관리자 권한이 켜져 있으므로 파이썬 설치 및 구성을 시작합니다."
        goto main
    ) else (
        echo "[ BAD ] 권한 부족 에러. 관리자 권한으로 실행시켜주세요."
        exit 
    )    

main:
    echo "[ 다운 ] Python Installer" && curl -L -O https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe
    echo "[ 설치 ] Python Installer" && python-3.10.5-amd64.exe /quiet PrependPath=1 Include_test=0
    echo "[ 삭제 ] Python Installer" && del python-3.10.5-amd64.exe
    color 02 && echo "[ 끝 ]" && echo "파이썬 (비교적 최근 버전) 설치됨." && start .