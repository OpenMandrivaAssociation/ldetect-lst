%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

Name:		ldetect-lst
Version:	0.1.290
Release:	%mkrel 1
Summary:	Hardware list for the light detection library
URL:		http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/ldetect-lst/trunk/
Source0:	%{name}-%{version}.tar.lzma
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-buildroot
License:	GPLv2+
Requires(post):	perl-base gzip
Requires(preun): perl-base
BuildRequires:	perl-MDK-Common
%if !%{bootstrap}
# for testsuite:
BuildRequires:	drakx-kbd-mouse-x11
# needed to create fallback-modules.alias
BuildRequires:	kernel-latest
# for list_modules.pm
BuildRequires:	drakxtools-backend >= 10.30
%endif
Conflicts:	ldetect < 0.7.18
Conflicts:	module-init-tools < 3.3-pre11.29mdv2008.0
Conflicts:	usbutils < 0.86-2mdv
Conflicts:	pnputils < 0.1-6mdv
Obsoletes:	pciids <= 1:0.7-1.20091201mdv2010.1
Provides:	pciids
Provides:	hwdata
# for XFdrake using nvidia-current instead of nvidia-97xx
Conflicts:	drakx-kbd-mouse-x11 < 0.21

%package	devel
Summary:	Devel for ldetect-lst
Group:		Development/Perl
Requires:	ldetect-lst = %{version}

%description
The hardware device lists provided by this package are used as lookup 
table to get hardware autodetection.

%description	devel
This package provides merge2pcitable, a tool that enables to merge in hardware
databases new entries pacakged in eg /usr/share/ldetect-lst/pcitable.d.

%prep
%setup -q

%build
%if %{bootstrap}
pushd lst
touch hardcoded-modules.alias fallback-modules.alias preferred-modules.alias
popd
%endif

%make

%check
%if !%{bootstrap}
make check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall slibdir=$RPM_BUILD_ROOT/lib

%clean
rm -rf $RPM_BUILD_ROOT

# trigger is needed to upgrade from a package having
# /usr/share/ldetect-lst/pcitable in the package to the new scheme
%triggerpostun -- %{name}
if [ -x /usr/sbin/update-ldetect-lst ]; then
  /usr/sbin/update-ldetect-lst
fi

%preun -p "/usr/sbin/update-ldetect-lst --clean"

%post -p /usr/sbin/update-ldetect-lst

%files
%defattr(-,root,root)
%doc AUTHORS 
%{_datadir}/usb.ids
%{_datadir}/oui.txt
%{_datadir}/pci.ids
%{_datadir}/misc/pnp.ids
%{_datadir}/%{name}
%{_sbindir}/*
/lib/module-init-tools/ldetect-lst-modules.alias

%files devel
%defattr(-,root,root)
%doc convert/README.pcitable
%{_bindir}/*
