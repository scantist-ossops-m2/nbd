%def_disable debug
%def_enable syslog
%def_enable lfs
%def_with gznbd
%def_with static_client

%define Name NBD
Name: nbd
Version: 2.9.7
Release: alt2
Summary: Tools for using the Network Block Device
License: GPL
Group: Networking/Other
URL: http://%name.sourceforge.net/
Source:	%name-%version.tar.bz2
Patch0:	%name-types.patch
Patch1:	%name-2.9.6-gznbd.patch
Patch2: %name-2.9.7-prerun.patch
BuildRequires: glib2-devel >= 2.6.0
%{?_with_gznbd:BuildRequires: zlib-devel}
%{?_with_static_client:BuildRequires: dietlibc}

%description
%Name contains the tools needed to export a network block device and to
use a network block device. The nbd module is part of the 2.2 kernels
and higher.
If you have a kernel patched for it, you can use the network block
device to swap over the net, which is particularly useful for diskless
workstations.


%package doc
Summary: %Name docs
Group: Documentation

%description doc
%Name docs.


%package server
Summary: %Name server
Group: Networking/Other

%description server
%Name server needed to export a network block device.


%package client
Summary: %Name client
Group: Networking/Other

%description client
%Name client needed to use a network block device.
You can use the network block device to swap over the net, which is
particularly useful for diskless workstations.


%if_with static_client
%package client-static
Summary: %Name client
Group: Networking/Other

%description client-static
%Name client needed to use a network block device.
You can use the network block device to swap over the net, which is
particularly useful for diskless workstations.

This package contains static %name-client (can be used for initrd).
%endif


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
%configure \
    %{subst_enable debug} \
    %{subst_enable syslog} \
    %{subst_enable lfs}
%if_with static_client
%make_build CC="diet -Os %__cc" %name-client
mv %name-client{,.static}
%make_build clean
%endif
%make_build
%{?_with_gznbd:%make_build -C gznbd CFLAGS="%optflags -DMY_NAME='\"gznbd\"'"}


%install
install -d %buildroot%_sysconfdir/%name-server
%make_install DESTDIR=%buildroot install
%{?_with_static_client:install -m 0755 %name-client.static %buildroot%_sbindir/}
%{?_with_gznbd:install -m 0755 gznbd/gznbd %buildroot/%_bindir/}


%files doc
%doc README


%files server
%_bindir/*
%dir %_sysconfdir/nbd-server
%_man1dir/*
%_man5dir/*


%files client
%_sbindir/%name-client
%_man8dir/*


%if_with static_client
%files client-static
%_sbindir/%name-client.static
%endif


%changelog
* Sun Oct 14 2007 Led <led@altlinux.ru> 2.9.7-alt2
- added %name-client.static
- added %name-2.9.7-prerun.patch

* Fri Sep 21 2007 Led <led@altlinux.ru> 2.9.7-alt1
- 2.9.7

* Mon Aug 06 2007 Led <led@altlinux.ru> 2.9.6-alt1
- 2.9.6
- updated %name-2.9.6-gznbd.patch

* Sat Jun 16 2007 Led <led@altlinux.ru> 2.9.3-alt1
- 2.9.3

* Fri Mar 16 2007 Led <led@altlinux.ru> 2.9.0-alt0.1
- initial build