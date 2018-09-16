#!/usr/bin/perl -w

########################################################################################
# Author: Jamel INOUBLI <jamel.inoubli@ardia.com.tn>                                   #
# Script: version 1.0                                                                  #
# Evolution :                                                                          #
# Description: - Parcourir un répertoire et extrait les fichiers de type               # 
#                MENU__XXX.s                                                           #
#              - Ajouter un attribut JumpToMarker à la balise MenuScreen dont la       #
#                valeur est YES                                                        #                              #
########################################################################################

$| = 1;

use strict;
use IO::Handle;
use POSIX;

my $ime2_folder = $ARGV[0];
my $LOG1 = undef;
my $LOG2 = undef;

sub check_args
{
    if (! (scalar(@ARGV) == 1)){
        print "usage: Perl  parse_menu_diagbox.pl arg1 \n";            
        print "arg1 : Dossier de données applicatives menus\n";        
        die   "ERROR : Nombre de parametres incorrect\n";
    }

    #"""""""""""""""""""""""""""""""""""""""""""
    # Tests d'existence des arguments #
    #"""""""""""""""""""""""""""""""""""""""""""

    if (!-d $ime2_folder){
        die ("FATAL ERROR : le dossier de données applicatives \"$ime2_folder\" n'existe pas.");
    }   
}

sub add_JumpToMarker_attribute
{
    print "\rFiltrage des menus ...";
    my @files = ListFiles($ime2_folder, '.s');
    
    my $num_file = 1;
    my $fileModified = 0;
    # Parcours des fichiers
    foreach my $file(@files)
    {        
        system("cls");  # Effacement de la console
        print "\rTraitement du menu \"". $file . "\" ... (" . floor(($num_file/scalar(@files))*100) . "%)";        
        open(FILEIN, "<", $file) or die $!;
        my @lines = <FILEIN>;
        close(FILEIN);
        my $contentFile = '';
        my $nb_MenuScreen = 0;  
        my $i = 0;
        my $line;                         
        foreach my $line (@lines)
        {
            if($line =~ /<MenuScreen/ && !($line =~ /JumpToMarker=/))
            {
            	$line =~ s/>/ JumpToMarker="YES">/g;
            	$fileModified = 1;
            	$nb_MenuScreen++;
            }
            $contentFile.=$line;
            $i++;
        }
        if ($nb_MenuScreen>=1)
        {
        	print $LOG1 "- " . $file . ": ".$nb_MenuScreen." MenuScreen(s)\n";
        }
        else
        {
        	print $LOG2 "- ". $file . "\n";        	
        }
        if ($fileModified == 1)
        {
        	open(FILEOUT, '>', $file) or die $!;
            print FILEOUT $contentFile;
            close FILEOUT;
        }        
        $num_file++;
    }    
    print "\n";
}

sub save
{
    my ($file,$twig)=@_;
    
    my $ptrFile;
    #Fichier à ouvrir en écriture
    open($ptrFile, ">", $file) || die "Unable to create the $file file!";
    $twig->print(\*$ptrFile,pretty_print => 'indented');
    
    # Libérer mémoire
    $twig->purge();
    $twig->dispose();
        
    if (defined($ptrFile)){
        close($ptrFile);
    }
}

sub main
{
    system("cls");  # Effacement de la console
    open($LOG1, ">modified_files.log") || die "Erreur E/S:$!\n";
    print $LOG1 "Liste des fichiers modifiés : \n";
    open($LOG2, ">unmodified_files.log") || die "Erreur E/S:$!\n";
    print $LOG2 "Liste des fichiers non modifiés : \n"; 
     
    check_args();
        
    add_JumpToMarker_attribute();
        
    close $LOG1;
    close $LOG2;
    print "\tend process ....\n"
    
}

##############################################################
# Fonction : ListFiles
#--------------------------------------------------------------------------------------------------------------------------
# retourne les fichiers d'un répertoire
#--------------------------------------------------------------------------------------------------------------------------
# Entrees :   
# - $dir : le répertoire en question
# - $ext : l'extension des fichiers à rechercher
# 
# Sorties :
# - la liste des fichiers contenus dans le répertoire
##############################################################
sub ListFiles
{
    my ($dir, $ext) = @_;
    my @files;
    
    # Ouverture du repertoire
    opendir (my $pdir, $dir) or die "Impossible d'ouvrir le répertoire $dir\n";

    # Liste des fichiers et répertoires ne commencant pas par .
    my @contentDir = grep { !/^\./ } readdir($pdir);

    # Fermeture du répertoire
    closedir ($pdir);
    
    # On récupère tous les fichiers
    foreach my $name ( @contentDir )
    {
        # Fichiers se terminant par la bonne extension
        if ( -f "$dir/$name" && index(lc("$dir\\$name"), lc($ext)) >= 0 && (($name =~ /^MENU__/i || $name eq "menu_b0_adc.s")) && $name ne "MENU__DAE__EFFPARAM.s")
        {
            push ( @files, "$dir\\$name" );
        }
        # Repertoires
        elsif (-d "$dir/$name")
        {
            # recursivité
            push (@files, ListFiles("$dir\\$name", $ext));
        }
    }

    return @files;
}

main();

1;