cd DSD
deltree /y *.*
cd ..

ECHO descente Master CD07.C (derniere archive Complète)
svn export --force http://budiag1/4077/mespp2000/tags/CD07C/V15.12.0  DSD --username %USERNAME%

ECHO descente Tags CD08A
svn export --force http://budiag1/4077/mespp2000/tags/CD08A/v16.1.0  DSD --username %USERNAME%
svn export --force http://budiag1/4077/mespp2000/tags/CD08A/v16.2.0  DSD --username %USERNAME%
svn export --force http://budiag1/4077/mespp2000/tags/CD08A/v16.3.0  DSD --username %USERNAME%
svn export --force http://budiag1/4077/mespp2000/tags/CD08A/v16.4.0  DSD --username %USERNAME%
svn export --force http://budiag1/4077/mespp2000/tags/CD08A/v16.5.0  DSD --username %USERNAME%
svn export --force http://budiag1/4077/mespp2000/tags/CD08A/v16.6.0  DSD --username %USERNAME%

ECHO Mise à plat des fichiers
md DSD\DSD
Copy E:\Generationbases\DSD\bsi\DSD\*.* E:\Generationbases\DSD\dsd\*.*
Copy E:\Generationbases\DSD\confort\DSD\*.* E:\Generationbases\DSD\dsd\*.*
Copy E:\Generationbases\DSD\sous_capot\DSD\*.* E:\Generationbases\DSD\dsd\*.*

md DSD\IDENT
Copy E:\Generationbases\DSD\bsi\IDENT\*.* E:\Generationbases\DSD\ident\*.*
Copy E:\Generationbases\DSD\confort\IDENT\*.* E:\Generationbases\DSD\ident\*.*
Copy E:\Generationbases\DSD\sous_capot\IDENT\*.* E:\Generationbases\DSD\ident\*.*


ECHO Copy des schemas
md DSD\EcuLayer
Copy E:\Gpcgen\Eculayer\CD08A\*.* E:\Generationbases\DSD\EcuLayer

ECHO effacement repertoire BSI / SS_CAPOT / CONFORT
cd DSD
rd /S /Q sous_capot
deltree /y bsi
deltree /y confort
pause