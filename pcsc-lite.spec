%define major 1
%define libname %mklibname pcsclite %{major}
%define develname %mklibname pcsclite -d
%define staticname %mklibname pcsclite -d -s

Summary:	M.U.S.C.L.E. PC/SC Framework for Linux
Name:		pcsc-lite
Version:	1.6.4
Release:	%mkrel 1
License:	BSD-like
Group:		System/Servers
URL:		http://pcsclite.alioth.debian.org
Source0:	https://alioth.debian.org/frs/download.php/2479/pcsc-lite-%{version}.tar.bz2
Source1:	https://alioth.debian.org/frs/download.php/2480/pcsc-lite-%{version}.tar.bz2.asc
Source2:	pcscd.script
BuildRequires:	chkconfig 
BuildRequires:	flex
BuildRequires:	libusb-devel
BuildRequires:	tetex-latex
Requires(pre):	rpm-helper
Requires:	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{libname}
Summary:	Muscle PCSC Framework for Linux libraries
Group:		System/Libraries
Conflicts:	%name < 1.1.2-5mdk
Provides:	libpcsclite%{major} = %{version}-%{release}

%description -n	%{libname}
The purpose of PCSC Lite is to provide a Windows(R) SCard interface in a
very small form factor for communicating to smartcards and readers.
PCSC Lite uses the same winscard api as used under Windows(R).

The %{name}-devel package contains the header files and libraries
needed for compiling PCSC Lite programs. If you want to develop PCSC Lite-aware
programs, you'll need to install this package.

This package was tested to work with A.E.T. Europe B.V. SafeSign. This
package is suported by A.E.T. Europe B.V. when used in combination with
SafeSign.

%package -n	%{develname}
Summary:	Muscle PCSC Framework for Linux development files
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libpcsclite-devel = %{version}-%{release}
Obsoletes:	%mklibname -d pcsclite 1
Conflicts:	%mklibname -d pcsclite 0

%description -n	%{develname}
The purpose of PCSC Lite is to provide a Windows(R) SCard interface in a
very small form factor for communicating to smartcards and readers.
PCSC Lite uses the same winscard api as used under Windows(R).

The %{name}-devel package contains the header files and libraries
needed for compiling PCSC Lite programs. If you want to develop PCSC Lite-aware
programs, you'll need to install this package.

This package was tested to work with A.E.T. Europe B.V. SafeSign. This
package is suported by A.E.T. Europe B.V. when used in combination with
SafeSign.

%package -n	%{staticname}
Summary:	Muscle PCSC Framework for Linux development files
Group:		Development/Other
Requires:	%{develname} = %version
Provides:	%name-static-devel = %version-%release
Obsoletes:	%mklibname -d -s pcsclite 1

%description -n	%{staticname}
The purpose of PCSC Lite is to provide a Windows(R) SCard interface in a
very small form factor for communicating to smartcards and readers.
PCSC Lite uses the same winscard api as used under Windows(R).

The %{name}-static-devel package contains the static header files and libraries
needed for compiling PCSC Lite programs. If you want to develop PCSC Lite-aware
programs, you may need to install this package.

This package was tested to work with A.E.T. Europe B.V. SafeSign. This
package is suported by A.E.T. Europe B.V. when used in combination with
SafeSign.

%prep
%setup -q

%build
%serverbuild
%configure2_5x --enable-static \
   --enable-usbdropdir=%{_libdir}/pcsc/drivers/ \
   --disable-libhal --enable-libusb
%make

# pdf
make -C doc ifdhandler-3.pdf

%install
rm -rf %{buildroot}

%makeinstall_std

mkdir -p %{buildroot}/%{_initrddir}
cp %SOURCE2 %{buildroot}/%{_initrddir}/pcscd

# remove unpackaged files
rm -f %{buildroot}%{_datadir}/pcscd.startup
rm -rf %{buildroot}/%{_docdir}/*

%post
%_post_service pcscd

%preun
%_preun_service pcscd      

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING DRIVERS HELP INSTALL NEWS README SECURITY
%doc doc/README.DAEMON
%attr(755,root,root) %{_initrddir}/pcscd
%{_mandir}/*/*
%{_sbindir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libpcsc*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc ChangeLog doc/ifdhandler-3.pdf
%{_libdir}/pkgconfig/* 
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.so

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/*.a
