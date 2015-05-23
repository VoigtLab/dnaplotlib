#!/usr/bin/perl

use Getopt::Long;
use CGI qw/param/;

my $HOME = "/Users/peng";

my $in_text = param ('in_text');
my $out_pdf = param ('out_pdf');

my $result = qx{$HOME/anaconda/bin/python $HOME/MIT-BroadFoundry/dnaplotlib/quick.py -input '$in_text' -output ../results/$out_pdf};



