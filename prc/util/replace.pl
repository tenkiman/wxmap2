#!/usr/bin/env perl
#
# NAME
#   replace.pl - replace a character string with another string.
#
# SYNOPSIS:
#   replace.pl <old_string> <new_string> <filename|directory>
# 
# DESCRIPTION
#   This program acts like a text filter: it replaces a text 
#   string or a substring expression from the input buffer with
#   a new string. It operate on a file or a directory. If directory
#   is given, then all files in that directory is filtered.
#   The original text is saved to a file with .Bak extension.
#

# Perl program library directory <on my system>
@INC=("/home1/GCC/lib/perl5") ;

  $DEBUG = 0 ;

  if ( $DEBUG ) {
     print "Number of arguments is : $#ARGV \n" ;
  }

# Parse command line arguments and assign each argumet's value to
# a variable.
# 
  ((($old_str,$new_str,$source) = @ARGV) == 3 ) || die
      "Usage: $0 <old_string> <new_string> <filename|directory> \n" ;

  $index=0 ;
  if ( -d $source ) {
# 
# Target is a directory: build a list of filenames for that directory.
#
      print "Scanning directory $source\n" ;
      open(INPUT,"ls $source |") || die "Can't list directory $wkdir\n" ;
      while ( <INPUT> ) {
         chop ;
# build fullpath name
         $file = $source . "/" . $_ ;
# file is a greater file and has size greater than 0 
         next unless -f $file && ! -z $file ;
         $flist[$index] = $file ;
         $index++ ;
     }
  } else {
#
# Target is a regular file: add filename to the list.
#
    -e $source || die "Error: $source does not exist\n" ;
    $flist[$index] = $source ;
    $index++ ;
  }

#
# Build a list of filenames to be operated on, remove any file
# with extension .bak/.BAK from this list.
#
  @flist = &filter_input_list(@flist) ;

  if ( $DEBUG ) {
     &printarray(@flist) ;
  }

# Operate on each file, replace old string with new string
#
  foreach $file (@flist) {
     replacestring($old_str,$new_str,$file) ;
  }

  print "done\n" ;
#
# End of the perl program
#
#
#
# ************************************************************* #
sub printarray {
  local($object) ;
  foreach $object (@_) {
     print "$object \n" ;
  }   
}

sub makecopy {
  local($object) ;
  foreach $object (@_) {
     
# Remove old copy of backup file
         $objbak= $object . ".bak" ;
         print "copy $object $objbak\n" ;
         system("cp $object $objbak") ;
  } 
}

sub filter_input_list {
#  local($pattern,@list) = @_ ;
  local($object,$index) ;
  $index = 0 ; 
  foreach $object (@_) {
#
# Remove old copy of backup file from the list (match any filename ending
# with a suffix of .bak or .BAK
#
     if ( $object =~ /.bak$/i ) {
         ;
#         print "Removing $object from input list\n" ;
     } else {
         $list[$index++]= $object ;
     }
  }
  return @list
}

sub basename {
  local(@object) = @_ ;
  (@parselist)=split(/\//,$object[0]) ;
  $base=$parselist[$#parselist] ;
  return $base ;
}

# compute remainder of a division ops
sub remainder {
   local($top,$bot) = @_ ;
   $top = &absval($top) ;
   $bot = &absval($bot) ;
   while ( $top >= $bot ) {
      $top = $top - $bot ;
   }
   return $top ;
}

# Return the absolute value
sub absval {
   local($val) = @_ ;
   if ( $val < 0 ) {
      $val = $val * (-1) ;
   }
   return $val ;
}

# ==========================================
sub replacestring {

    local($old_str,$new_str,$source) = @_ ;

# Check if the input file is a regular text file
    if ( ! -T $source ) {
       print "Warning: $source is not a text file, " ;
       print "string replacement is not performed\n" ;
       return 0 ;
    }

    open(INPUT,$source) || die "Error: Can't open $source\n" ;

# create a temporary file to store the result
    $destination = $source . ".tmpxx" ;
    open(OUTPUT,"> $destination") || die "Error: Can't open tmpfile: $destination$\n" ;

    print "processing $source \n" ;


    while (<INPUT>) {
       s/$old_str/$new_str/g ;
       print OUTPUT ;
    }

    close INPUT ;
    close OUTPUT ;
#
# Rotate files: move old file to *.bak and 
# new file to the input file
#
    $backup = $source . ".bak" ;
    if ( rename($source,$backup) == 0 ) {
       system("rm $destination") ;
       print "Error: Can't make backup copy of the original file\n" ;
       print "No change to original file made\n" ;
       die ;
    }
    rename($destination,$source) ;

    return 1 ;
}
