ECHO Montage des lecteurs r�seaux
net use F: \\ACTIANT1\PROJETS   /PERSISTENT:no >NUL
net use H: \\ACTIANT1\TMP       /PERSISTENT:no >NUL
net use I: \\ACTIANT1\ISO9001   /PERSISTENT:no >NUL
net use O: \\actiant1\Organisa  /PERSISTENT:no >NUL
net use N: \\vm-file-server1\actia_automotive /PERSISTENT:no >NUL
net use S: \\Actiant1\Structur  /PERSISTENT:no >NUL
net use P: \\ACTIANT1\PRODUITS  /PERSISTENT:no >NUL
net use X: \\actiant1\outils    /PERSISTENT:no >NUL

ECHO Creation des repertoires sur H
ping -n 10 127.0.0.1 >nul
mkdir h:\Jeje
mkdir h:\BSI
mkdir h:\Incidents


