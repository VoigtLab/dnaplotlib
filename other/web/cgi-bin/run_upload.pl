#!/usr/bin/perl

use Getopt::Long;
use CGI qw/param/;

my $home = "/Users/peng";

#regulation option
my $out_pdf = param ('out_pdf');
my $params  = param ('params');
my $parts   = param ('parts');
my $designs = param ('designs');
my $reg     = param ('reg');
my $id      = param ('id');

$params  =~ s/newline/\n/g;
$parts   =~ s/newline/\n/g;
$designs =~ s/newline/\n/g;
$reg     =~ s/newline/\n/g;
$params  =~ s/semicolon/\;/g;
$parts   =~ s/semicolon/\;/g;
$designs =~ s/semicolon/\;/g;
$reg     =~ s/semicolon/\;/g;

my $dir = "../results/";
my $params_csv  = $dir . $id . "_params.csv";
my $parts_csv   = $dir . $id . "_parts.csv";
my $designs_csv = $dir . $id . "_designs.csv";
my $reg_csv     = $dir . $id . "_reg.csv";


system("echo \"$params\"  | grep \, > $params_csv");
system("echo \"$parts\"   | grep \, > $parts_csv");
system("echo \"$designs\" | grep \, > $designs_csv");
system("echo \"$reg\" | grep \, > $reg_csv");

my $command = "$home/anaconda/bin/python -W ignore $home/MIT-BroadFoundry/dnaplotlib/plot_SBOL_designs.py";
my $options = "";
$options .= " -params $params_csv";
$options .= " -parts $parts_csv";
$options .= " -designs $designs_csv";
if( length($reg) > 10) {
    $options .= " -regulation $reg_csv";
}
$options .= " -output ../results/" . $out_pdf;

print "$command $options\n";
system("echo \"$command $options\" > upload/command.txt");
my $result = qx{$command $options};


