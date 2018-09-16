@echo off
:menu
echo -----------------
echo -- Script menu --
echo -----------------
echo.
echo 1.MAJ_SVN
echo 2.Demarrage
echo 3.Suivi_EI
echo 4.MAJ_SVN_Ican
echo 5.Clean_SVN
::commentaire1
REM commentaire2
echo 6.Quitter
echo 7.Commandes dos
echo 8.Recuperation des extracts de Bugzilla
echo.

set /p reponse="Quel programme voulez-vous executer ? "

If /i "%reponse%"=="1" goto :batch1
If /i "%reponse%"=="2" goto :batch2
If /i "%reponse%"=="3" goto :batch3
If /i "%reponse%"=="4" goto :batch4
If /i "%reponse%"=="5" goto :batch5
If /i "%reponse%"=="7" goto :batch7
If /i "%reponse%"=="8" goto :batch8
If /i "%reponse%"=="6" goto :fin

:batch1
cls
call D:\Bat\MAJ.bat
cls
goto :menu

:batch2
cls
call D:\Bat\demarage.bat
cls
goto :menu

:batch3
cls
call D:\Bat\Suivi_Ei.bat
cls
goto :menu

:batch4
cls
call D:\Bat\MAJSVN_ICAN.bat
cls
goto :menu

:batch5
cls
call D:\Bat\CleanSVN.bat
cls
goto :menu

:batch7
cls
call cmd

:batch8
cls
ECHO Recuperation des extracts de Bugzilla
copy \\budiag4\donconvergence\ExtractsBugzilla\*.xls D:\Boulot\Main\Macros\Extra_BZ\*.xls
cls
goto :menu


:fin
exit

