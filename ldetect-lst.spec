%define name ldetect-lst
%define version 0.1.184
%define release %mkrel 1

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Hardware list for the light detection library
URL: http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/ldetect-lst/trunk/
Source: %{name}-%{version}.tar.bz2
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL
Requires(post): perl-base gzip
Requires(preun): perl-base
BuildRequires: perl-MDK-Common
Conflicts: ldetect < 0.7.5
Provides: hwdata
# for XFdrake using nvidia-current instead of nvidia-97xx
Conflicts: drakx-kbd-mouse-x11 < 0.21

%package devel
Summary: Devel for ldetect-lst
Group: Development/Perl
Requires: ldetect-lst = %{version}

%description
The hardware device lists provided by this package are used as lookup 
table to get hardware autodetection

%description devel
see ldetect-lst

%prep
%setup -q

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

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
%{_datadir}/%{name}
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%doc convert/README.pcitable
%{_bindir}/*


