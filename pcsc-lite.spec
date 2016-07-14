%define major 1
%define pcscspy_major 0
%define libname %mklibname pcsclite %{major}
%define libpcscspy %mklibname pcscspy %{pcscspy_major}
%define devname %mklibname pcsclite -d

Summary:	M.U.S.C.L.E. PC/SC Framework for Linux
Name:		pcsc-lite
Version:	1.8.17
Release:	2
License:	BSD-like
Group:		System/Servers
Url:		http://pcsclite.alioth.debian.org
Source0:	https://alioth.debian.org/frs/download.php/4126/pcsc-lite-%{version}.tar.bz2
Source1:	org.debian.pcsc-lite.policy
BuildRequires:	doxygen
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(polkit-agent-1)
Requires:	%{libname} = %{version}
Requires:	polkit
Requires:	ccid

%description
The purpose of PC/SC Lite is to provide a Windows(R) SCard interface
in a very small form factor for communicating to smartcards and
readers.  PC/SC Lite uses the same winscard API as used under
Windows(R).  This package includes the PC/SC Lite daemon, a resource
manager that coordinates communications with smart card readers and
smart cards that are connected to the system, as well as other command
line tools.

%package -n %{libname}
Summary:	Muscle PCSC Framework for Linux libraries
Group:		System/Libraries
Provides:	libpcsclite%{major} = %{version}-%{release}

%description -n	%{libname}
The purpose of PCSC Lite is to provide a Windows(R) SCard interface in a
very small form factor for communicating to smartcards and readers.
PCSC Lite uses the same winscard api as used under Windows(R).

This package was tested to work with A.E.T. Europe B.V. SafeSign. This
package is suported by A.E.T. Europe B.V. when used in combination with
SafeSign.

%package -n pcsc-spy
Summary:	PCSC API spy
Group:		System/Libraries
Requires:	python
Requires:	pcsc-lite
Requires:	%{libpcscspy} = %{version}

%description -n	pcsc-spy
The purpose of pcsc-spy is to spy all the calls between the PC/SC client
and the PC/SC library.

%package -n %{libpcscspy}
Summary:	PCSC Smart Card Library
Group:		System/Libraries

%description -n	%{libpcscspy}
Supporting library for the PC/SC spy tool.

%package -n %{devname}
Summary:	Muscle PCSC Framework for Linux development files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libpcscspy} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The %{name}-devel package contains the header files and libraries
needed for compiling PCSC Lite programs. If you want to develop PCSC Lite-aware
programs, you'll need to install this package.

%package doc
Summary:	PC/SC Lite developer documentation
Group:		Development/Other
Buildarch:	noarch

%description doc
%{summary}.

%prep
%setup -q

%build
%serverbuild
%configure \
    --disable-static \
    --enable-ipcdir=%{_localstatedir}/run \
    --enable-polkit \
    --enable-libusb \
    --with-systemdsystemunitdir=%{_systemunitdir} \
    --enable-usbdropdir=%{_libdir}/pcsc/drivers

%make
doxygen doc/doxygen.conf; rm -f doc/api/*.{map,md5}

%install
%makeinstall_std

rm -f %{buildroot}%{_datadir}/polkit-1/actions/org.debian.pcsc-lite.policy
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/polkit-1/actions/

# Create empty directories
mkdir -p %{buildroot}%{_sysconfdir}/reader.conf.d
mkdir -p %{buildroot}%{_libdir}/pcsc/drivers
mkdir -p %{buildroot}%{_localstatedir}/run/pcscd

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/pcsc-lite.preset << EOF
enable pcscd.socket
EOF

%files
%doc AUTHORS DRIVERS HELP INSTALL NEWS README SECURITY
%doc doc/README.DAEMON
%dir %{_sysconfdir}/reader.conf.d/
%dir %{_libdir}/pcsc/
%dir %{_libdir}/pcsc/drivers/
%ghost %dir %{_localstatedir}/run/pcscd/
%{_presetdir}/pcsc-lite.preset
%{_unitdir}/*
%{_sbindir}/*
%{_datadir}/polkit-1/actions/*.policy
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/libpcsc*.so.%{major}*

%files -n pcsc-spy
%{_bindir}/pcsc-spy
%{_mandir}/man1/pcsc-spy.1.*

%files -n %{libpcscspy}
%{_libdir}/libpcscspy.so.%{pcscspy_major}*

%files -n %{devname}
%doc ChangeLog COPYING
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so

%files doc
%doc doc/api/ doc/example/pcsc_demo.c COPYING
