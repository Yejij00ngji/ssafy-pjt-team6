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