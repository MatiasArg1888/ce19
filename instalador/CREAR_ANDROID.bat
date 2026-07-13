@echo off
cd /d "%~dp0\.."
"%~dp0..\env\Scripts\flet.exe" build apk --project codigo_escondido_19 --artifact "CODIGO ESCONDIDO 19" --product "CODIGO ESCONDIDO 19" --description "Aplicacion Codigo Escondido 19" --company "CODIGO ESCONDIDO 19" --org com.flet --bundle-id com.flet.app_ce_19 --android-adaptive-icon-background "#71106F" --splash-color "#71106F" --splash-dark-color "#71106F" --build-version 1.0.0 --no-rich-output --yes --skip-flutter-doctor
pause
