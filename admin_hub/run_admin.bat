@echo off
echo ========================================================
echo   VERIFICANDO DEPENDENCIAS DO AUGUSTUNA ADMIN HUB
echo ========================================================

python -c "import customtkinter" 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    echo [!] A biblioteca 'customtkinter' esta em falta.
    echo A instalar customtkinter...
    pip install customtkinter Pillow
) else (
    echo [+] 'customtkinter' ja instalado.
)

python -c "import PIL" 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    echo [!] A biblioteca 'Pillow' esta em falta.
    echo A instalar Pillow...
    pip install Pillow
) else (
    echo [+] 'Pillow' ja instalado.
)

echo.
echo A inciar app Administrativa...
python admin_hub.py
pause
