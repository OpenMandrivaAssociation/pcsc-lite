%define major 1
%define pcscspy_major 0
%define libname %mklibname pcsclite %{major}
%define pcscspy_libname %mklibname pcscspy %{pcscspy_major}
%define develname %mklibname pcsclite -d

Summary:	M.U.S.C.L.E. PC/SC Framework for Linux
Name:		pcsc-lite
Version:	1.8.8
Release:	6
License:	BSD-like
Group:		System/Servers
URL:		http://pcsclite.alioth.debian.org
Source0:	https://alioth.debian.org/frs/download.php/3695/pcsc-lite-%{version}.tar.bz2
Source1:	https://alioth.debian.org/frs/download.php/3695/pcsc-lite-%{version}.tar.bz2.asc

BuildRequires:	doxygen
BuildRequires:	udev-devel
BuildRequires:	pkgconfig(libusb-1.0)

Requires:	%{libname} = %{version}

%description
The purpose of PC/SC Lite is to provide a Windows(R) SCard interface
in a very small form factor for communicating to smartcards and
readers.  PC/SC Lite uses the same winscard API as used under
Windows(R).  This package includes the PC/SC Lite daemon, a resource
manager that coordinates communications with smart card readers and
smart cards that are connected to the system, as well as other command
line tools.

%package -n	%{libname}
Summary:	Muscle PCSC Framework for Linux libraries
Group:		System/Libraries
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

%package -n	pcsc-spy
Summary:	PCSC API spy
Group:		System/Libraries

Requires:	python
Requires:	pcsc-lite
Requires:	%{pcscspy_libname} = %{version}

%description -n	pcsc-spy
The purpose of pcsc-spy is to spy all the calls between the PC/SC client
and the PC/SC library.

%package -n	%{pcscspy_libname}
Summary:	PCSC Smart Card Library
Group:		System/Libraries

%description -n	%{pcscspy_libname}
Supporting library for the PC/SC spy tool.

%package -n	%{develname}
Summary:	Muscle PCSC Framework for Linux development files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{pcscspy_libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libpcsclite-devel = %{version}-%{release}
Obsoletes:	%mklibname -d pcsclite 1

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

%package	doc
Summary:	PC/SC Lite developer documentation
Group:		Development/Other
Buildarch:	noarch

%description	doc
%{summary}.


%prep
%setup -q

%build
%serverbuild
%configure2_5x --disable-static \
   --enable-ipcdir=%{_localstatedir}/run \
   --enable-usbdropdir=%{_libdir}/pcsc/drivers
%make
doxygen doc/doxygen.conf; rm -f doc/api/*.{map,md5}

%install
%makeinstall_std

# service files
install -d %{buildroot}%{_unitdir}
install -m 644 etc/pcscd.service %{buildroot}%{_unitdir}/pcscd.service
install -m 644 etc/pcscd.socket %{buildroot}%{_unitdir}/pcscd.socket

rm -f %{buildroot}/%{_libdir}/*.la

# Create empty directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/reader.conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pcsc/drivers
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/pcscd

%post
%_post_service pcscd
# systemd hack #1 (fix if you know how to do sockets better :))
if /bin/mountpoint -q /sys/fs/cgroup/systemd; then
	/bin/systemctl disable pcscd.service > /dev/null 2>&1
	/bin/systemctl enable pcscd.socket > /dev/null 2>&1

	# Initial installation
	if [ $1 -eq 1 ] ; then
		/bin/systemctl start pcscd.socket > /dev/null 2>&1
	fi
fi

%preun
# systemd hack #2
if /bin/mountpoint -q /sys/fs/cgroup/systemd; then
	# Removal, not upgrade
	if [ $1 -eq 0 ] ; then
		/bin/systemctl disable pcscd.socket > /dev/null 2>&1
		/bin/systemctl stop pcscd.socket > /dev/null 2>&1
	fi
fi

%_preun_service pcscd

%postun
if /bin/mountpoint -q /sys/fs/cgroup/systemd; then
	/bin/systemctl daemon-reload
fi

%files
%doc AUTHORS DRIVERS HELP INSTALL NEWS README SECURITY
%doc doc/README.DAEMON
%dir %{_sysconfdir}/reader.conf.d/
%dir %{_libdir}/pcsc/drivers/
%{_unitdir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sbindir}/*

%files -n %{libname}
%doc COPYING
%{_libdir}/libpcsc*.so.%{major}*

%files -n pcsc-spy
%{_bindir}/pcsc-spy
%{_mandir}/man1/pcsc-spy.1.*

%files -n %{pcscspy_libname}
%{_libdir}/libpcscspy.so.%{pcscspy_major}*

%files -n %{develname}
%doc ChangeLog
%{_libdir}/pkgconfig/* 
%{_includedir}/*
%{_libdir}/*.so

%files doc
%doc doc/api/ doc/example/pcsc_demo.c COPYING

