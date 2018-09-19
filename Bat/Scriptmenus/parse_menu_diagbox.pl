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
my $LOG3 = undef;

sub check_args
{
	###############################
    # Tests du nombre d'arguments #
    ###############################
    if (! (scalar(@ARGV) == 1)){
        print "usage: Perl  parse_menu_diagbox.pl arg1 \n";            
        print "arg1 : Dossier de données applicatives menus\n";        
        die   "ERROR : Nombre de parametres incorrect\n";
    }

    ###################################
    # Tests d'existence des arguments #
    ###################################

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
    my $contentFile;
    my $nb_MenuScreen;  
    my $containsJumpToMarkerNo;
    my $posc;
    my $posl;
    my $manyMenuScreen;        
    my $line;      
    # Parcours des fichiers
    foreach my $file(@files)
    {                
        print "\rTraitement du menu \"". $file . "\" ... (" . floor(($num_file/scalar(@files))*100) . "%)";        
        open(FILEIN, "<", $file) or die $!;
        my @lines = <FILEIN>;
        close(FILEIN);
        $contentFile = '';
        $nb_MenuScreen = 0;  
        $containsJumpToMarkerNo = 0;
        $posc = 0;
        $posl = 0;
        $manyMenuScreen = 0;        
        $line = '';                         
        foreach my $line (@lines)
        {
            if(($line =~ /<MenuScreen.*posc=(\d{1,}).*posl=(\d{1,})/))             
            {               	         	            	
            	if ($nb_MenuScreen == 0)
            	{
            	   $posc = $1;
            	   $posl = $2;
            	   $nb_MenuScreen++;
            	}
            	if ($posc != $1 || $posl != $2)
            	{
            		$manyMenuScreen = 1;   
            		$posc = $1;
                    $posl = $2;
            		$nb_MenuScreen++;            		         		
            	}            	            	
            	if (!($line =~ /JumpToMarker *=/))
            	{
            	   $line =~ s/>/ JumpToMarker="YES">/g;
            	   $fileModified = 1;            	   
            	}
            	else
            	{ 
            	   if ($line =~ /JumpToMarker *= *"NO"/i)
            	   {
            	       $containsJumpToMarkerNo = 1; 	            		
            	   }
            	}            	
            }
            $contentFile.=$line;            
        }
        if ($fileModified == 1)
        {
        	print $LOG1 "- " . $file . "\n";
        	open(FILEOUT, '>', $file) or die $!;
            print FILEOUT $contentFile;
            close FILEOUT;
            $fileModified = 0; 
        }
        else
        {
        	print $LOG2 "- ". $file . "\n";
        }
        if ($containsJumpToMarkerNo == 1)
        {
        	print $LOG3 "- " . $file . ": contient JumpToMarker=\"NO\"\n";        	
        }
        if ($manyMenuScreen == 1)
        {
            print $LOG3 "- " . $file . ": contient " . $nb_MenuScreen. " MenuScreen dans différentes cellules\n";          
        }      
        $num_file++;
    }        
}

sub main
{
    system("cls");  # Effacement de la console
    open($LOG1, ">modified_files.log") || die "Erreur E/S:$!\n";
    print $LOG1 "Liste des fichiers modifiés : \n";
    open($LOG2, ">unmodified_files.log") || die "Erreur E/S:$!\n";
    print $LOG2 "Liste des fichiers non modifiés : \n";
    open($LOG3, ">warning_files.log") || die "Erreur E/S:$!\n";
    print $LOG3 "Liste des fichiers avec des warnings : \n"; 
     
    check_args();
        
    add_JumpToMarker_attribute();
        
    close $LOG1;
    close $LOG2;
    close $LOG3;
    print "\nFin du traitement ....\n"
    
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