%define major 1
%define libname %mklibname pcsclite %{major}
%define develname %mklibname pcsclite -d
%define staticname %mklibname pcsclite -d -s

%define with_debug 1
%{?_with_debug: %{expand: %%global with_debug 1}}

Name: pcsc-lite
Summary: M.U.S.C.L.E. PC/SC Framework for Linux
Version: 1.4.4
Release: %mkrel 1
License: BSD
Group: System/Servers
Source0: https://alioth.debian.org/download.php/2106/pcsc-lite-%{version}.tar.gz
Source1: https://alioth.debian.org/download.php/2107/pcsc-lite-%{version}.tar.gz.asc
Source1: pcscd.script
URL: http://pcsclite.alioth.debian.org
BuildRequires: chkconfig 
BuildRequires: flex
BuildRequires: libusb-devel
BuildRequires: pkgconfig
BuildRequires: tetex-latex
BuildRoot: %{_tmppath}/%{name}-root
Requires(pre): rpm-helper
Requires: rpm-helper

%post
%_post_service pcscd

%preun
%_preun_service pcscd      

%description
pcscd is the daemon program for PC/SC Lite. It is a resource 
manager that coorinates communications with Smart Card readers and Smart 
Cards that are connected to the system.

The purpose of PCSC Lite is to provide a Windows(R) SCard interface in a 
very small form factor for communicating to smartcards and readers.
PCSC Lite uses the same winscard api as used under Windows(R)

This package was tested to work with A.E.T. Europe SafeSign. This
package is supported by A.E.T. Europe B.V. when used in combination with
SafeSign.

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING DRIVERS HELP INSTALL NEWS README SECURITY
%doc doc/pcsc-lite.pdf doc/ifdhandler-3.pdf doc/README.DAEMON
%attr(755,root,root) %{_initrddir}/pcscd
%dir %{_sysconfdir}/reader.conf.d
%{_sysconfdir}/reader.conf.d/*
%{_mandir}/*/*
%{_sbindir}/*
%{_libdir}/pcsc

#---------------------------------------------------------

%package -n %{libname}
Summary: Muscle PCSC Framework for Linux libraries
Group: System/Libraries
Conflicts: %name < 1.1.2-5mdk
Provides: libpcsclite%{major} = %{version}-%{release}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%description -n %{libname}
The purpose of PCSC Lite is to provide a Windows(R) SCard interface in a
very small form factor for communicating to smartcards and readers.
PCSC Lite uses the same winscard api as used under Windows(R).

The %{name}-devel package contains the header files and libraries
needed for compiling PCSC Lite programs. If you want to develop PCSC Lite-aware 
programs, you'll need to install this package.

This package was tested to work with A.E.T. Europe B.V. SafeSign. This
package is suported by A.E.T. Europe B.V. when used in combination with
SafeSign.

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libpcsc*.so.*

#---------------------------------------------------------

%package -n %{develname}
Summary: Muscle PCSC Framework for Linux development files
Group: Development/Other
Requires: %{libname} = %{version}
Provides: %{name}-devel = %{version}-%{release}
Provides: libpcsclite-devel = %{version}-%{release}
Obsoletes: %mklibname -d pcsclite 1
Conflicts: %mklibname -d pcsclite 0

%description -n %{develname}
The purpose of PCSC Lite is to provide a Windows(R) SCard interface in a
very small form factor for communicating to smartcards and readers.
PCSC Lite uses the same winscard api as used under Windows(R).

The %{name}-devel package contains the header files and libraries
needed for compiling PCSC Lite programs. If you want to develop PCSC Lite-aware 
programs, you'll need to install this package.

This package was tested to work with A.E.T. Europe B.V. SafeSign. This
package is suported by A.E.T. Europe B.V. when used in combination with
SafeSign.

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/pkgconfig/* 
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.so

#---------------------------------------------------------

%package -n %{staticname}
Summary: Muscle PCSC Framework for Linux development files
Group: Development/Other
Requires: %{develname}
Obsoletes: %mklibname -d -s pcsclite 1

%description -n %{staticname}
The purpose of PCSC Lite is to provide a Windows(R) SCard interface in a
very small form factor for communicating to smartcards and readers.
PCSC Lite uses the same winscard api as used under Windows(R).

The %{name}-static-devel package contains the static header files and libraries
needed for compiling PCSC Lite programs. If you want to develop PCSC Lite-aware 
programs, you may need to install this package.

This package was tested to work with A.E.T. Europe B.V. SafeSign. This
package is suported by A.E.T. Europe B.V. when used in combination with
SafeSign.

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/*.a

#---------------------------------------------------------

%prep
%setup -q

%build
%serverbuild
%configure2_5x \
   --enable-usbdropdir=%{_libdir}/pcsc/drivers/ \
   --enable-muscledropdir=%{_libdir}/pcsc/services/ \
   --enable-scf \
   --enable-runpid=%{_var}/run/pcscd.pid \
%if %{with_debug}
   --enable-debugatr \
   --enable-musclecarddebug \
%endif
   --enable-extendedapdu

# No distributed proc
make

# pdf
make -C doc pcsc-lite.pdf ifdhandler-3.pdf

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pcsc/{services,drivers} $RPM_BUILD_ROOT%{_sysconfdir}/reader.conf.d

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
cp %SOURCE1  $RPM_BUILD_ROOT/%{_initrddir}/pcscd

# remove unpackaged files
rm -f	$RPM_BUILD_ROOT%{_datadir}/pcscd.startup
rm -rf  $RPM_BUILD_ROOT/%{_docdir}/*

%clean
rm -rf $RPM_BUILD_ROOT

