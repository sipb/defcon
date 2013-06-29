#!/usr/bin/perl

use lib '/mit/defcon/lib/perl5';
use CGI;
use Text::ParseWords;
use Data::Dumper;
use JSON::Syck;
use Apache::Session::File;
use Authen::Htpasswd;

my $q = new CGI;

my $sid = $q->cookie("defcon_sid") || $q->param("sid");

my %session;
mkdir("/tmp/defcon");
tie %session, 'Apache::Session::File', $sid, {
    Directory => '/tmp/defcon'
    };

my $pwfile = Authen::Htpasswd->new("data/htpasswd", { encrypt_hash => 'sha1' });

my %response;

my $request = $q->param("request");

if ($request eq "login") {
    my $username = $q->param("username");
    my $password = $q->param("password");
    eval {
    if ($pwfile->check_user_password($username, $password)) {
	$session{username} = $username;
	$session{authorized} = 1;
	$response{status} = 200;
	$response{message} = "SIPB Athena Defcon Access Level One";
    } else {
	$session{authorized} = 0;
	$response{status} = 401;
    }};
    if ($@) {
	$session{authorized} = 0;
	$response{status} = 500;
	$response{message} = $@;
    }
} elsif ($request eq "command" && $session{authorized}) {
    $response{status} = 404;
    my ($command, @args) = shellwords($q->param("command"));
    if ($command =~ m|^help|i) {
	$response{status} = 200;
	$response{message} = "Help not implemented.";
    } elsif ($command =~ m|^useradd|i) {
	my ($username, $password) = @args;
	eval {
	    $pwfile->add_user($username, $password);
	};
	if ($@) {
	    $response{status} = 500;
	    $response{message} = $@;
	} else {
	    $response{status} = 200;
	    $response{message} = "User $username created successfully.";
	}
    } elsif ($command =~ m|^passwd|i) {
	my ($username, $password) = @args;
	eval {
	    $pwfile->update_user($username, $password);
	};
	if ($@) {
	    $response{status} = 500;
	    $response{message} = $@;
	} else {
	    $response{status} = 200;
	    $response{message} = "Password set for $username.";
	}
    } elsif ($command =~ m|defcon|i) {
	$response{message} = "Unable to communicate with Defcon sign. Defcon must be set manually.";
    }
} else {
    $response{status} = 403;
    $response{message} = "Invalid or no authentication provided. Please logout and try again.";
    #$response{message} = Dumper($command, \%session);
}

my $sidcookie = $q->cookie(-name=>"defcon_sid", -value=>$session->{_session_id}, -expires=>"+1h");
print $q->header(-type=>"application/json", -cookie=>$sidcookie);
$response{sid} = $session{_session_id};
print JSON::Syck::Dump(\%response);
