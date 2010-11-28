Summary:	The compatibility libraries needed by old libc.so.5 applications
Name:		libc
Version:	5.3.12
Release:	%mkrel 45
Exclusivearch:	%{ix86}
Exclusiveos:	Linux
License:	Distributable
Group:		System/Libraries
Source0:	libc-5.3.12-bins.tar.bz2
Autoreqprov:	no
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Older Linux systems (including the Red Hat Linux system between 2.0
and 4.2, inclusive) were based on libc version 5. The libc package
includes the libc5 libraries and other libraries based on libc5.  With
these libraries installed, old applications which need them will be
able to run on your glibc (libc version 6) based system.

The libc package should be installed if you need to run older applications
which need libc version 5.

%package	base
Summary:	Old libc.so.5 and libm.so.5 compatibility libraries
Group:		System/Libraries
Requires(pre,post): grep coreutils
Provides:	libc = %{version} libc.so.5 libm.so.5
Requires:	ld.so1
Autoreqprov:	no

%description	base
This package provides old libc.so.5 and libm.so.5 libraries needed to run 
old applications based on libc5 libraries.

%package	extras
Summary:	Extra old libc5 based compatibility libraries
Group:		System/Libraries
Requires(pre,post): grep coreutils
Provides:	libstdc++.so.27 libg++.so.27 
Requires:	%{name}-base
Autoreqprov:	no

%description	extras
This package provides extra libraries (other than libc.so.5 and
libm.so.5) needed to run old applications based on libc5 libraries.

%prep
%setup -c -q

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/i486-linux-libc5/lib
for n in *; do
    install -m 755 $n $RPM_BUILD_ROOT/usr/i486-linux-libc5/lib
done

%post base
grep -q "^/usr/i486-linux-libc5/lib$" /etc/ld.so.conf || echo "/usr/i486-linux-libc5/lib" >> /etc/ld.so.conf
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%postun base
if [ "$1" = "0" ]; then
    rm -f /etc/ld.so.conf.new
    grep -v '^/usr/i486-linux-libc5/lib$' /etc/ld.so.conf > /etc/ld.so.conf.new 2>/dev/null
    mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%if %mdkversion < 200900
%post extras -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun extras -p /sbin/ldconfig
%endif

%files base
%defattr(-,root,root)
%dir /usr/i486-linux-libc5
%dir /usr/i486-linux-libc5/lib
/usr/i486-linux-libc5/lib/libc.so*
/usr/i486-linux-libc5/lib/libm.so*

%files extras
%defattr(-,root,root)
/usr/i486-linux-libc5/lib/libICE*
/usr/i486-linux-libc5/lib/libPEX*
/usr/i486-linux-libc5/lib/libSM*
/usr/i486-linux-libc5/lib/libX*
/usr/i486-linux-libc5/lib/libform*
/usr/i486-linux-libc5/lib/libg*
/usr/i486-linux-libc5/lib/libmenu*
/usr/i486-linux-libc5/lib/libncurs*
/usr/i486-linux-libc5/lib/libpanel*
/usr/i486-linux-libc5/lib/libstdc++*
/usr/i486-linux-libc5/lib/libtermcap*
/usr/i486-linux-libc5/lib/libvga*

%clean
rm -rf $RPM_BUILD_ROOT

