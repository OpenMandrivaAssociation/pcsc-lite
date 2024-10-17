%define _disable_rebuild_configure 1

%define major 1
%define pcscspy_major 0
%define libname %mklibname pcsclite %{major}
%define libpcscspy %mklibname pcscspy %{pcscspy_major}
%define devname %mklibname pcsclite -d

Summary:	M.U.S.C.L.E. PC/SC Framework for Linux
Name:		pcsc-lite
Version:	2.0.3
Release:	1
License:	BSD-like
Group:		System/Servers
Url:		https://pcsclite.alioth.debian.org
Source0:	https://github.com/LudovicRousseau/PCSC/archive/refs/tags/%{version}.tar.gz
Source1:	org.debian.pcsc-lite.policy
BuildRequires:	flex
BuildRequires:	doxygen
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-rpm-macros
BuildRequires:	autoconf-archive
Requires:	%{libname} = %{version}
Requires:	polkit
Requires:	ccid
%systemd_requires

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

%description -n %{libname}
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
Requires:	pcsc-lite >= %{version}
Requires:	%{libpcscspy} = %{version}

%description -n	pcsc-spy
The purpose of pcsc-spy is to spy all the calls between the PC/SC client
and the PC/SC library.

%package -n %{libpcscspy}
Summary:	PCSC Smart Card Library
Group:		System/Libraries

%description -n %{libpcscspy}
Supporting library for the PC/SC spy tool.

%package -n %{devname}
Summary:	Muscle PCSC Framework for Linux development files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libpcscspy} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
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
%autosetup -n PCSC-%{version} -p1
./bootstrap

%build
%configure \
    --disable-static \
    --enable-ipcdir=%{_rundir} \
    --enable-polkit \
    --enable-libudev \
    --disable-libusb \
    --with-systemdsystemunitdir=%{_unitdir} \
    --enable-usbdropdir=%{_libdir}/pcsc/drivers

%make_build
doxygen doc/doxygen.conf; rm -f doc/api/*.{map,md5}

%install
%make_install

rm -f %{buildroot}%{_datadir}/polkit-1/actions/org.debian.pcsc-lite.policy
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/polkit-1/actions/

# Create empty directories
mkdir -p %{buildroot}%{_sysconfdir}/reader.conf.d
mkdir -p %{buildroot}%{_libdir}/pcsc/drivers
mkdir -p %{buildroot}%{_localstatedir}/run/pcscd

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-pcsc-lite.preset << EOF
enable pcscd.socket
EOF

# (tpg) remove not needed docs
rm -rf %{buildroot}%{_docdir}/pcsc-lite

%post
%systemd_post pcscd.socket

%preun
%systemd_preun pcscd.socket

%postun
%systemd_postun_with_restart pcscd.socket

%files
%dir %{_sysconfdir}/reader.conf.d/
%dir %{_libdir}/pcsc/
%dir %{_libdir}/pcsc/drivers/
%ghost %dir %{_localstatedir}/run/pcscd/
%{_presetdir}/86-pcsc-lite.preset
%{_unitdir}/*
%{_sbindir}/*
%{_datadir}/polkit-1/actions/*.policy
%doc %{_mandir}/man5/*
%doc %{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/libpcsc*.so.%{major}*

%files -n pcsc-spy
%{_bindir}/pcsc-spy
%doc %{_mandir}/man1/pcsc-spy.1.*

%files -n %{libpcscspy}
%{_libdir}/libpcscspy.so.%{pcscspy_major}*

%files -n %{devname}
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so

%files doc
%doc AUTHORS HELP INSTALL NEWS README SECURITY ChangeLog COPYING
%doc doc/api/ doc/example/pcsc_demo.c
