@echo off
echo ========================================================
echo   Augustuna Admin Hub - Criar Atalho no Ambiente de Trabalho
echo ========================================================

set SCRIPT_DIR=%~dp0
set TARGET=%SCRIPT_DIR%run_admin.bat
set SHORTCUT=%USERPROFILE%\Desktop\Augustuna Admin Hub.lnk
set ICON=%SCRIPT_DIR%..\Logo oficial 2.ico

:: Create VBS script to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\create_shortcut.vbs"
echo sLinkFile = "%SHORTCUT%" >> "%TEMP%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut.vbs"
echo oLink.TargetPath = "%TARGET%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Description = "Augustuna Admin Hub - Gestao de Conteudo" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut.vbs"

cscript //nologo "%TEMP%\create_shortcut.vbs"
del "%TEMP%\create_shortcut.vbs"

echo.
echo [+] Atalho criado com sucesso no Ambiente de Trabalho!
echo     Ficheiro: %SHORTCUT%
pause
