use strict;

# Example Perl plugin.
#
# This example can be freely used for any purpose.

# Run it from the build directory like this:
#
#   ./src/nbdkit -f -v ./plugins/perl/.libs/nbdkit-perl-plugin.so  \
#       script=./plugins/perl/example.pl test1=foo test2=bar
#
# You can connect to the server using guestfish or qemu:
#
#   guestfish --format=raw -a nbd://localhost run

# This is the string used to store the emulated disk (initially all
# zero bytes).  There is one disk per nbdkit instance.  You could also
# put this into the handle, so there would be a fresh disk per handle.
my $disk = "\0" x (1024*1024);

# This just prints the extra command line parameters, but real plugins
# should parse them and reject any unknown parameters.
sub config
{
    my $key = shift;
    my $value = shift;

    print "$0: ignored parameter $key=$value\n";
}

sub open
{
    my $readonly = shift;

    printf ("$0: open: readonly=%d\n", $readonly);

    # You can return any Perl value from open, and the same Perl value
    # will be passed as the first arg to the other callbacks [in the
    # client connected phase].  In most cases it's convenient to use a
    # hashref.
    my $h = { readonly => $readonly };

    return $h;
}

sub get_size
{
    my $h = shift;

    return length ($disk);
}

sub pread
{
    my $h = shift;
    my $count = shift;
    my $offset = shift;

    return substr ($disk, $offset, $count);
}

sub pwrite
{
    my $h = shift;
    my $buf = shift;
    my $count = length ($buf);
    my $offset = shift;

    substr ($disk, $offset, $count) = $buf;
}