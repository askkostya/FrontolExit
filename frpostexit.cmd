@ECHO OFF
SET path_eou_logs=C:\ProgramData\ATOL\EoU\logs

sc stop EoU
del %path_eou_logs%\* /F /Q
call notepad.exe

rem shutdown -r -t 0