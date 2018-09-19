@ECHO OFF
ECHO Génération des extracts de Bugzilla
start "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "https://budiag4.actia.fr/bugzilla-applicative/report-excel.cgi?type_rapport=ANOMALIE&type_incident=EI_&product=POLUX"
REM | CHOICE /C:AB /T:A,%15 > NUL

ping -n 11 127.0.0.1 >nul

ECHO Ouverture de la macro excel
start excel.exe "D:\Boulot\Main\Macros\Suivi_auto.xlsm"

start "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "https://budiag4.actia.fr/bugzilla-applicative/report-excel.cgi?type_rapport=DESCRIPTION&type_incident=EI_&product=POLUX"
start "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "https://budiag4.actia.fr/bugzilla-applicative/report-excel.cgi?type_rapport=ANOMALIE&type_incident=FI_JIRA_&product=POLUX"
start "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "https://budiag4.actia.fr/bugzilla-applicative/report-excel.cgi?type_rapport=DESCRIPTION&type_incident=FI_JIRA_&product=POLUX"



ECHO.	
ECHO Validez lorsque les extract de Bugzilla seront terminés pour les récupérer.
PAUSE
copy \\budiag4\donconvergence\ExtractsBugzilla\*.xls E:\Boulot\Main\Macros\Extra_BZ\*.xls

