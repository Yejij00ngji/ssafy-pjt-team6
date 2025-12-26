@echo off
echo ===========================================
echo Windows 시간 동기화 강제 재설정 중...
echo ===========================================

:: 1. 시간 서비스 중지
net stop w32time

:: 2. 시간 서비스 등록 취소 및 재등록
w32tm /unregister
w32tm /register

:: 3. 시간 서비스 시작
net start w32time

:: 4. 시간 서버 목록 설정 (구글 및 윈도우 공식 서버)
:: /manualpeerlist 뒤에 서버 주소들을 넣고 /syncfromflags:manual로 설정합니다.
w32tm /config /manualpeerlist:"time.google.com,0x1 time.windows.com,0x1" /syncfromflags:manual /reliable:YES /update

:: 5. 즉시 동기화 명령 발송
echo.
echo 시간을 동기화하는 중입니다. 잠시만 기다려 주세요...
w32tm /resync /force

echo.
echo ===========================================
echo 설정이 완료되었습니다. 
echo '명령이 성공적으로 완료되었습니다'라는 문구가 떴는지 확인하세요.
echo ===========================================
pause

@REM @echo off
@REM echo 관리자 권한으로 실행 중인지 확인하세요.
@REM echo.

@REM :: 서비스 중지 및 재등록
@REM net stop w32time
@REM w32tm /unregister
@REM timeout /t 2 > nul
@REM w32tm /register
@REM timeout /t 2 > nul

@REM :: 서비스 시작
@REM net start w32time
@REM timeout /t 3 > nul

@REM :: 서버 목록 설정 (국내 LG U+ 및 공식 서버 포함)
@REM w32tm /config /manualpeerlist:"time.bora.net,0x1 time.google.com,0x1 time.windows.com,0x1" /syncfromflags:manual /reliable:YES /update

@REM :: 설정 적용을 위해 서비스 다시 시작
@REM net stop w32time
@REM net start w32time
@REM timeout /t 5 > nul

@REM :: 동기화 시도
@REM echo 동기화를 시도합니다...
@REM w32tm /resync /force

@REM pause