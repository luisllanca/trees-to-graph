@echo off
CALL conda activate base

SET ENV1=practica4
SET SCRIPT1=calculate_d1_egr.py

SET ENV2=practica
SET SCRIPT2=calculate_d1_wrf.py

SET ENV3=r-env
SET SCRIPT3=calculate_d1_inf.R

SET ENV4=ete_env
SET SCRIPT4=calculate_d1_rf_asd.py

CALL :ejecutar_script %ENV1% %SCRIPT1%
CALL :ejecutar_script %ENV2% %SCRIPT2%
CALL :ejecutar_script %ENV3% %SCRIPT3%
CALL :ejecutar_script %ENV4% %SCRIPT4%

echo Todos los scripts se ejecutaron correctamente.
PAUSE
EXIT /B

:ejecutar_script
echo Activando el ambiente %1...
CALL conda activate %1

FOR /F "tokens=1-4 delims=:.," %%a IN ("%time%") DO (
    SET /A start_h=1%%a%%100 - 100
    SET /A start_m=1%%b%%100 - 100
    SET /A start_s=1%%c%%100 - 100
    SET /A start_ms=1%%d%%100 - 100
)

echo Ejecutando el script %2...
IF /I "%~x2" == ".py" (
    python %2
) ELSE IF /I "%~x2" == ".R" (
    Rscript %2
) ELSE (
    echo Tipo de archivo desconocido: %2
    GOTO :EOF
)

FOR /F "tokens=1-4 delims=:.," %%a IN ("%time%") DO (
    SET /A end_h=1%%a%%100 - 100
    SET /A end_m=1%%b%%100 - 100
    SET /A end_s=1%%c%%100 - 100
    SET /A end_ms=1%%d%%100 - 100
)

CALL :calcular_tiempo
CALL conda deactivate
echo Ambiente %1 desactivado.
GOTO :EOF

:calcular_tiempo
setlocal
set /a start_total=(%start_h%*3600) + (%start_m%*60) + %start_s%
set /a end_total=(%end_h%*3600) + (%end_m%*60) + %end_s%
set /a elapsed=end_total-start_total
if %elapsed% lss 0 set /a elapsed+=86400
echo Tiempo transcurrido: %elapsed% segundos
endlocal
GOTO :EOF