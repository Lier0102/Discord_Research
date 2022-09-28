@echo off
@MODE 100,35

rem These scripts are made in Korean version.
rem Please Attention.

echo "프로그램 명시 파일 삭제중..." && del firstfile
echo "필요한 모듈 다운중..." && pip install --force--reinstall -r requirements.txt

cls && cd MAIN && python main.py 
pause>nul && color 07 && exit