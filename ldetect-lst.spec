%bcond_with	bootstrap

Summary:	Hardware list for the light detection library
Name:		ldetect-lst
Version:	0.1.316
Release:	1
Group:		System/Kernel and hardware
License:	GPLv2+
URL:		http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/ldetect-lst/trunk/
Source0:	%{name}-%{version}.tar.xz
Requires(post):	perl-base
Requires(post):	gzip
Requires(preun):perl-base
BuildRequires:	perl-MDK-Common
%if !%{with bootstrap}
# for testsuite:
BuildRequires:	drakx-kbd-mouse-x11
# needed to create fallback-modules.alias
BuildRequires:	kernel-desktop
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
BuildArch:	noarch

%description
The hardware device lists provided by this package are used as lookup 
table to get hardware autodetection.

%package	devel
Summary:	Devel for ldetect-lst
Group:		Development/Perl
Requires:	ldetect-lst = %{version}-%{release}

%description	devel
This package provides merge2pcitable, a tool that enables to merge in hardware
databases new entries pacakged in eg /usr/share/ldetect-lst/pcitable.d.

%prep
%setup -q

%apply_patches

%build
%if %{with bootstrap}
pushd lst
touch hardcoded-modules.alias fallback-modules.alias preferred-modules.alias
popd
%endif

%make

%check
%if !%{with bootstrap}
#make check
%endif

%install
%makeinstall slibdir=%{buildroot}/lib

%preun -p "/usr/sbin/update-ldetect-lst --clean"

%post -p /usr/sbin/update-ldetect-lst

# trigger is needed to upgrade from a package having
# /usr/share/ldetect-lst/pcitable in the package to the new scheme
# trigger* seems broken, use direct check for file instead

%postun
if [ -f /usr/share/ldetect-lst/pcitable ]; then
    if [ -x /usr/sbin/update-ldetect-lst ]; then
	/usr/sbin/update-ldetect-lst
    fi
fi

%files
%doc AUTHORS
%{_datadir}/usb.ids
%{_datadir}/oui.txt
%{_datadir}/pci.ids
%{_datadir}/misc/pnp.ids
%{_datadir}/%{name}
%{_sbindir}/*
/lib/module-init-tools/ldetect-lst-modules.alias

%files devel
%doc convert/README.pcitable
%{_bindir}/*

%changelog
* Tue Jan  7 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.1.316-1
- (mostly) merge with upstream mandriva branch, switching to it
  (PS: several commits has not been merged and should really be merged
  from ROSA branch..)

* Wed Nov 28 2012 akdengi <akdengi> 0.1.315-1
- Version 0.1.315
- Drop RIVA 128 cards due nv not supported anymore. Set it's like VESA
- fix NVIDIA card naming
- Newly use nvidia-long-lived and nvidia-current drivers separatelly
- enable sisimedia driver and drop fglrx-legacy for Xorg 13 support

* Wed Oct 31 2012 akdengi <akdengi> 0.1.313-1
- update pcitable from Catalyst 9.010
- update ids
- enable nvidia173 driver
- fix empty pci and usbtable lists build

* Wed Oct 29 2012 akdengi <akdengi> 0.1.312-1
- new ATI/AMD detect mechanism
- usign fglrx-legacy driver
- update to kernel 3.6.4
- update to Catalyst 12.10
- update to NVidia 304.60

* Wed Oct 10 2012 Alexander Kazancev <kazancas@mandriva.org> 0.1.310-1
- update oui, usb and pci ids
- add kernel_alias_pci and kernel_alias_usb to mapping with KMOD and modules.alias (maps deprecated for now)
- update modules mapping for kernel 3.5.5

* Fri Aug 17 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.1.302-1
+ Revision: 815201
- add support for fglrx-legacy driver

* Mon Aug 13 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.1.301-1
+ Revision: 814524
- package should be noarch
- cleanups
- new version:
  	o update ids from the proprietary nvidia-current-295.59
  	o update AMD/ATI Cards+ entries from the proprietary and free driver
  	  (HD 4000 and below are no longer supported by it, so the free driver
  	  is now always used for those)
  	o switch NVIDIA NVD9/GF119 cards from vesa to nouveau
  	o add new AMD ids from the proprietary and free drivers
  	o restructure AMD/ATI Cards+ entries for HD 2000 and newer
  	  - separate those that support usermode modesetting
  	  - add the necessary FIRMWARE and DRIVER_NO_FIRMWARE entries as per
  	    mga bug #3466
  	  - do not assign anything to the old unmaintained radeonhd driver
  	o Monitor DB
  	  - add Samsung SMS19A100
  	o add another intel id from kernel-3.3.6
  	o drop DKMS data about r8192se_pci & rt3090sta* (mga#5681)
  	o use fbdev for "Poulsbo US15W(GMA500)" (mga#5633)

* Sun May 27 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.1.300-1
+ Revision: 800794
- kernel-latest is gone
- update to new version 0.1.300
- spec file clean

* Tue Aug 16 2011 Andrey Bondrov <abondrov@mandriva.org> 0.1.292-1
+ Revision: 694710
- New version: 0.1.292

* Tue Jul 26 2011 Andrey Bondrov <abondrov@mandriva.org> 0.1.291-4
+ Revision: 691757
- Add patches from Mageia for new hardware support etc

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.291-3
+ Revision: 666067
- mass rebuild

* Wed Mar 23 2011 Thomas Backlund <tmb@mandriva.org> 0.1.291-2
+ Revision: 647806
- fix missing pcitable

* Tue Mar 22 2011 Thomas Backlund <tmb@mandriva.org> 0.1.291-1
+ Revision: 647697
- add new NVIDIA ids from the proprietary driver
- add new ATI ids from the prorietary driver and the free driver
- update ATI ids from xf86-video-ati-6.14.1

* Sun Dec 19 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.290-1mdv2011.0
+ Revision: 623201
- new version 0.1.290
  o add new NVIDIA ids from the proprietary driver
  o update pci.ids usb.ids oui.txt

* Fri Oct 22 2010 Anssi Hannula <anssi@mandriva.org> 0.1.289-1mdv2011.0
+ Revision: 587535
- new version 0.1.289
  o add new NVIDIA ids from the proprietary driver
  o add new ATI ids from the free ati driver and the proprietary driver

* Wed Aug 18 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.1.288-1mdv2011.0
+ Revision: 571141
- cosmetics
- new release, 0.1.288:
  	o update to latest usb.ids
  	o add product names for Samsung's 4G USB modems

* Fri Jun 11 2010 Anssi Hannula <anssi@mandriva.org> 0.1.287-1mdv2010.1
+ Revision: 547916
- 0.1.287
  o add new NVIDIA ids from the proprietary driver (#59714), assigning the
    Fermi cards to a new GF400+ class for vesa/nvidia-current

* Tue May 11 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 0.1.286-1mdv2010.1
+ Revision: 544495
- 0.1.286:
- switch back 0x10de:0x0110 to using the proprietary driver (#57539)
- remove imwheel support (replace with evdev)
- switch ATI cards now supported by radeon to it from vesa
  (HD 5000 series cards)

* Tue Mar 30 2010 Anssi Hannula <anssi@mandriva.org> 0.1.285-1mdv2010.1
+ Revision: 529685
- new version 0.1.285
  o add new NVIDIA ids from nvidia-current
  o add new ATI ids from fglrx
  o switch ATI cards now supported by radeon to it from vesa
  o re-enable ATI proprietary driver

* Thu Feb 25 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.1.284-1mdv2010.1
+ Revision: 511124
- 0.1.284
- drop patch from .spec which was integrated in the source tarball
- make imstt cards use vesa driver (imstt driver doesn't exist since 2009.1)
- make MediaGX cards use geode instead of cyrix
- make Intel Vermilion cards use vesa since vermilion doesn't work
- drop vga driver which is no longer working
- drop i810 driver which is no longer working
- add support for Intel Atom "Pineview G" and "Pineview GM" integrated
  graphics adapters
- add support for desktop and mobile Intel Core i3/i5 integrated
- add support for Intel B43 graphics adapter
- disable NVidia propretary driver on 0x10de:0x0110 as it segfaults on
  2010.0
- add new ATI ids from fglrx 8.690 (10.1)

* Wed Jan 13 2010 Frederic Crozat <fcrozat@mandriva.com> 0.1.283-1mdv2010.1
+ Revision: 490869
- Release 0.1.283 :
 - resync list
 - move pci.ids to correct location and really obsolete pciids

* Fri Jan 08 2010 Frederic Crozat <fcrozat@mandriva.com> 0.1.282-1mdv2010.1
+ Revision: 487685
- Release 0.1.282 :
 - package usb.ids, pnp.ids, pci.ids, oui.txt in ldetect-lst

* Sun Jan 03 2010 Anssi Hannula <anssi@mandriva.org> 0.1.281-1mdv2010.1
+ Revision: 486063
- new version
  o disable ATI propretary driver for now, it doesn't support X.org
    server 1.7+
  o update various ATI ids as per current free driver ID lists (some
    cards were switched from radeonhd to radeon, and some to vesa)
  o remove ATI IDs that are not supported by any driver

* Thu Dec 24 2009 Anssi Hannula <anssi@mandriva.org> 0.1.280-1mdv2010.1
+ Revision: 481925
- 0.1.280:
- Monitor DB
  o add entry for 'Samsung SyncMaster 2233SW (Charles A Edwards)
  o add entry for 'Samsung SyncMaster 2494HS' (Marek Laane)
- add new NVIDIA ids from nvidia-current 190.42
- add new ATI ids from fglrx 8.671, 8.681 assigned to
  fglrx+radeonhd
- switch all HD 5000 series ATI ids from ati to radeonhd
- use nouveau as default free driver for NVIDIA cards, except for
  Riva 128 (NV03) which is not supported by it
- re-enable proprietary NVIDIA driver on G105M, issue fixed upstream

* Mon Nov 23 2009 Claudio Matsuoka <claudio@mandriva.com> 0.1.279-2mdv2010.1
+ Revision: 469396
- Make p54pci preferred over prism54 module (Bug 52018)

  + Olivier Blin <blino@mandriva.org>
    - add bootstrap flag to build without kernel, drakxtools-backend and drakx-kbd-mouse-x11
      (because kernel installs require drakxtools, which requires ldetect/ldetect-lst to be built)
    - remove doble perl-MDK-Common buildrequire

* Tue Oct 27 2009 Thierry Vignaud <tv@mandriva.org> 0.1.279-1mdv2010.0
+ Revision: 459463
- really tag for 10de:06ec as not working with nvidia driver (#54862)
- use nvidia173 for 10de:2362 (#54768)

* Thu Oct 15 2009 Thierry Vignaud <tv@mandriva.org> 0.1.278-1mdv2010.0
+ Revision: 457650
- select openchrome driver for 0x1106:0x1122
- Monitor DB
  o add entry for 'Iiyama Prolite E2607WS' (#54225)
  o add entry for 'MAG LT717s' and default to 1280x1024 (#49656)
  o add entry for 'Samsung SyncMaster 2343BW' (Dick Gevers)

* Thu Oct 08 2009 Olivier Blin <blino@mandriva.org> 0.1.277-1mdv2010.0
+ Revision: 456149
- 0.1.277
- use lower horizsync for 800x480 (28.8 kHz for WeSurf and Compal Jax10)
- add LCD Panel 1366x768 entry (#47706)
- add monitor entry for Asus 1101HA (#47706)
- add Samsung SyncMaster 732NW (from Sergio Rafael Lemke)
- use psb video driver for Intel 0x8108 and 0x8109

* Wed Oct 07 2009 Olivier Blin <blino@mandriva.org> 0.1.276-1mdv2010.0
+ Revision: 455431
- 0.1.276
- enable to automatically add new ATI cards from
  dkms-modules-info/dkms-modules.alias where fglrx declares what it
  supports
- add Cards+ entry for Intel Poulsbo US15W (GMA500), using the psb
  driver
- Monitor DB
  - add Samsung SyncMaster 2243SN (Reinout van Schouwen)

* Fri Sep 25 2009 Thierry Vignaud <tv@mandriva.org> 0.1.275-2mdv2010.0
+ Revision: 448828
- rename .lzma as .xz so that new tar can work
- add support for 0x10de:0x06ec (G98M [GeForce G 105M]) which only
  works with nv (#54000)
- add quite a lot of new nvidia cards definition from NV_WHQL.inf from
  windows driver 186.82)
- remove quite a lot of usb devices descriptions that came from usb.ids

* Wed Sep 23 2009 Thierry Vignaud <tv@mandriva.org> 0.1.274-1mdv2010.0
+ Revision: 448071
- BR drakx-kbd-mouse-x11 for testsuite
- radeonhd failed on 0x1002:0x9480 (#53183)
- run testsuite

* Wed Sep 23 2009 Thierry Vignaud <tv@mandriva.org> 0.1.273-1mdv2010.0
+ Revision: 447962
- dc2xx is now obsoleted by userspace
- drop obsolete 'cs46xx', 'cs5535', 'maestro', 'maestro3', & 'ymfpci'
  entries
- kill all 0x10ec:0x8139:*:* entries (ldetect now try to choose
  bettwen "8139cp" & "8139too" according to PCI revision like
  performed by the kernel)

* Tue Sep 22 2009 Thierry Vignaud <tv@mandriva.org> 0.1.271-1mdv2010.0
+ Revision: 447528
- auerswald, hp5300, hpusbscsi, rio500 & tiglusb are obsoleted by
  userspace
- fix obsoleted drivers:
  o CDCEther => cdc_ether
  o hci_usb => btusb
  o mtouchusb => usbtouchscreen
  o ov518_decomp => gspca_ov519
  o phidgetservo => hid
  o touchkitusb => usbtouchscreen

* Tue Sep 22 2009 Thierry Vignaud <tv@mandriva.org> 0.1.270-1mdv2010.0
+ Revision: 447288
- fix obsoleted drivers:
  o b2c2_usb => b2c2-flexcop-usb
  o cy82c693 => pata_cypress
  o dtc => initio
  o generic => ata_generic and ide-pci-generic
  o maestro3 => snd_maestro3
  o snd_gina3g => snd-echo3g
  o sonypi => i2c-piix4
  o sonicvibes => snd-sonicvibes

* Tue Sep 22 2009 Thierry Vignaud <tv@mandriva.org> 0.1.269-1mdv2010.0
+ Revision: 447258
- add new ATI ids from fglrx
- mod_quicikame doesn't exist anymore (#52176)
- tag one more "nVidia Geforce2 MX/MX" as GeForce 3 so that it can
  uses 3D (#53841)

* Fri Sep 18 2009 Thierry Vignaud <tv@mandriva.org> 0.1.268-1mdv2010.0
+ Revision: 444410
- fix 2 Matrox entries
- Monitor DB
  o sync with latest Fedora (new Dell monitors)

* Fri Sep 18 2009 Thierry Vignaud <tv@mandriva.org> 0.1.267-1mdv2010.0
+ Revision: 444254
- add support for the last missing from Matrox card
- fix invalid Horzsync for 6 'Generic CRT Display; Monitor' and a
  couple Acer & Philips monitors (#48063)
- use fglrx again with ATI Mobility Radeon HD 3400 (now working)

* Wed Sep 16 2009 Thierry Vignaud <tv@mandriva.org> 0.1.266-1mdv2010.0
+ Revision: 443330
- sync ati list with latest driver

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 0.1.265-1mdv2010.0
+ Revision: 443281
- sync nvidia list with latest driver

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 0.1.264-1mdv2010.0
+ Revision: 443270
- add support for one Matrox card (#53564)

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 0.1.263-1mdv2010.0
+ Revision: 435710
- add support for ION video card (#53515)
- Monitor DB
  o sync with latest Fedora (new Dell monitors)

* Thu Aug 13 2009 Thierry Vignaud <tv@mandriva.org> 0.1.262-1mdv2010.0
+ Revision: 416049
- update usbtable to get proper descriptions for USB devices
- add GeForce 9400 (nvidia-current / vesa)
- use newer intel driver for 8086:3582:1179:0002, fixes bug #44371
- do not choose siimage when pata_sil680 works too since the former
  seems no longuer to work (#52736)
- fix loading '8139too' over '8139cp' on 10ec:8139:5853:0001 (#51520)

* Thu Apr 23 2009 Thierry Vignaud <tv@mandriva.org> 0.1.261-1mdv2009.1
+ Revision: 368835
- propagate the following changes from ansi (2009-04-01) into
  pcitable.x86_64 too, thus fixing wrongly using 'vesa' driver on some
  machines:
  o prefer "ati"/"radeon" driver over "radeonhd"
  o add new ATI ids from fglrx, ati and radeonhd
  o do not use fglrx with old Radeon cards

* Tue Apr 21 2009 Thierry Vignaud <tv@mandriva.org> 0.1.260-1mdv2009.1
+ Revision: 368522
- Monitor DB
  o sync with latest Fedora (new Dell monitors)
- drop amd64_agp entries (#43870)

* Mon Apr 20 2009 Thierry Vignaud <tv@mandriva.org> 0.1.259-1mdv2009.1
+ Revision: 368451
- fix preferring pata_marvell over ahci (#43975)

* Tue Apr 14 2009 Thierry Vignaud <tv@mandriva.org> 0.1.258-1mdv2009.1
+ Revision: 366885
- do not try to use nv for 0x10de:0x053e (#48684)
- do not use fglrx with ATI Mobility Radeon HD 3400 (Andriy Rysin reported
  a failure with fglrx 8.600)
- Monitor DB
  o add Samsung SyncMaster 2043NW (Jaanus Ojangu)
- prefer pata_marvell over ahci since ahci need marvel_enabled=1 to make it work (#43975)
- prism2_plx was removed from kernel, switch the only entry that was
  using it to orinoco_tmd (0x15e8:0x0131)
- remove dpc7146 entry since it was dropped from kernel
- use radeonhd instead of ati for ATI Radeon HD 3200 0x9610 (#49824)

* Wed Apr 01 2009 Anssi Hannula <anssi@mandriva.org> 0.1.257-1mdv2009.1
+ Revision: 363405
- 0.1.257:
- only use Intel 810 for a specic subvendor/subdevice of 0x8086:0x3582
- Monitor DB
  o add a lot of Proview monitors (Yannick56, #49104)
  o add Samsung SyncMaster 2253BW
- prefer "ati"/"radeon" driver over "radeonhd"
- add new ATI ids from fglrx, ati and radeonhd
- do not use fglrx with old Radeon cards
- add "GeForce (nouveau driver, experimental)" to allow users to test nouveau
  by selecting it in XFdrake

* Tue Mar 24 2009 Thierry Vignaud <tv@mandriva.org> 0.1.256-1mdv2009.1
+ Revision: 360810
- fix driver for "nVidia Corporation|NV11 [GeForce2 MX/MX 400]" (#48928)
- add new NVIDIA ids from 180.41
- use e100 instead of eepro100 since kernel team disabled the latest (#49085)
- Monitor DB
  o add Sony TV Bravia KDL-32D3000 (fcrozat)
  o add Samsung SyncMaster 2053BW (dams)

* Wed Mar 18 2009 Anssi Hannula <anssi@mandriva.org> 0.1.255-1mdv2009.1
+ Revision: 357450
- new release 0.1.255
  o re-enable fglrx driver
  o use (old) Intel 810 driver for 0x8086:0x3582, fixes bug #44371

* Mon Mar 16 2009 Thierry Vignaud <tv@mandriva.org> 0.1.254-1mdv2009.1
+ Revision: 355710
- Monitor DB
  o add Acer AL1716 (Steve Morris)
  o add Iiyama Prolite H481S (aapgorilla)
  o add Packard Bell Viseo 223Ws (patrick)

* Thu Mar 05 2009 Thierry Vignaud <tv@mandriva.org> 0.1.253-1mdv2009.1
+ Revision: 348999
- disable fglrx and nvidia71xx as they do not support X.org server 1.6
  (IgnoreABI does not work for them)
- use nvidia173 for non-SSE processors as well, the support was restored
- Monitor DB
  o add back "LCD Panel 800x480"
  o add ViewSonic VX2260WM (Donald Stewart)
  o sync with latest Fedora

* Thu Jan 29 2009 Adam Williamson <awilliamson@mandriva.org> 0.1.252-1mdv2009.1
+ Revision: 335352
- new release 0.1.252: add new NVIDIA IDs

* Fri Jan 16 2009 Adam Williamson <awilliamson@mandriva.org> 0.1.251-1mdv2009.1
+ Revision: 330356
- new release 0.1.251:
  	+ re-work the blacklist	of cards that don't work with nv to be more
  	  general and include more confirmed IDs

* Mon Jan 12 2009 Adam Williamson <awilliamson@mandriva.org> 0.1.250-1mdv2009.1
+ Revision: 328480
- new release 0.1.250:
  	+ add NVIDIA GeForce 9400 GT into modified 7050 group (cards that don't
  	  work with nv)

* Wed Dec 24 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.249-1mdv2009.1
+ Revision: 318194
- new release 0.1.249:
  	+ add new NVIDIA IDs from 180.18
  	+ add new ATI IDs from 8.12

* Wed Dec 03 2008 Thierry Vignaud <tv@mandriva.org> 0.1.248-1mdv2009.1
+ Revision: 309718
- Monitor DB
  o remove duplicated entries
  o sync with latest Fedora

* Tue Dec 02 2008 Thierry Vignaud <tv@mandriva.org> 0.1.247-1mdv2009.1
+ Revision: 309198
- Monitor DB
 o further sync with Fedora

* Tue Dec 02 2008 Thierry Vignaud <tv@mandriva.org> 0.1.246-1mdv2009.1
+ Revision: 309177
- fix "INTERNAL ERROR: good_default_monitor (Generic|*) is unknown in
  MonitorsDB" after syncing with redhat

* Sun Nov 30 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.245-1mdv2009.1
+ Revision: 308299
- new version 0.1.245:
  	+ NSC chips now use geode driver, nsc driver no longer builds
  	+ drop the special case for VIA K8M800, works OK with openchrome now
  	+ add new NVIDIA and ATI IDs from new driver versions
  	+ add "Flat Panel 1600x900" (#45091)
  	+ Monitor DB
  		o sync monitor vendor names with Fedora
  		o sync with Fedora
  	+ use "i810" instead of "intel" driver on older i810 because it
  	  segfaults when using XAA acceleration (#43916)

* Thu Nov 13 2008 Olivier Blin <blino@mandriva.org> 0.1.244-1mdv2009.1
+ Revision: 302767
- 0.1.244
- add new mouse definition (Logitech G5v2)
- vesa not framebuffer for ST Kyro, per dams
- disable 3D on ATI Rage 128-based cards (hard lock the machine on x86_64)
- use pata_cs5536 for Geode IDE controllers
- default to 800x480 on TECO TR2350 (Omatek netbook)

* Thu Oct 02 2008 Thierry Vignaud <tv@mandriva.org> 0.1.243-1mdv2009.0
+ Revision: 290839
- update dkms modules info

* Wed Oct 01 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.242-1mdv2009.0
+ Revision: 290414
- 0.1.242:
  	+ drop separate Radeon HD 4xxx category: radeonhd supports these now

* Tue Sep 30 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.241-1mdv2009.0
+ Revision: 290258
- new release 0.1.241:
  	+ add ID 0605 for NVIDIA GeForce 9800 GT (reported and tested by Zoida A)

* Thu Sep 25 2008 Thierry Vignaud <tv@mandriva.org> 0.1.240-1mdv2009.0
+ Revision: 288014
- update dkms modules info

* Thu Sep 18 2008 Olivier Blin <blino@mandriva.org> 0.1.239-1mdv2009.0
+ Revision: 285674
- 0.1.239
- update dkms modules info (mainly for rt2860 and rtl8187se)

  + Adam Williamson <awilliamson@mandriva.org>
    - new release 0.1.238:
      	+ support Intel G41 graphics chips
      	+ use vesa not nv for GeForce 7050 chips (#38391)

* Thu Sep 04 2008 Olivier Blin <blino@mandriva.org> 0.1.237-1mdv2009.0
+ Revision: 280833
- 0.1.237
- use pata_jmicron for jmicron controllers

* Wed Sep 03 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.236-1mdv2009.0
+ Revision: 279752
- add three new NVIDIA IDs from driver 177.70

  + Thierry Vignaud <tv@mandriva.org>
    - synd dkms data with latest prebuild packages

* Fri Aug 29 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.235-1mdv2009.0
+ Revision: 277400
- new release 0.1.235:
  	+ support Logitech MX400 mouse
  	+ no need to prefer madwifi over ath5k now, per #41988

* Thu Aug 21 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.234-1mdv2009.0
+ Revision: 274448
- new release 0.1.234:
  	+ NVIDIA: go back to 173 for FX and 177 for all later (177 going stable)
  	+ NVIDIA: add some new IDs from 177 driver headers
  	+ ATI: add some new IDs from Catalyst 8.8 driver headers

* Sun Aug 10 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.233-1mdv2009.0
+ Revision: 270583
- new release 0.1.233:
  	+ use new sisimedia driver for SiS 670/671 gfx cards (it actually works)

* Wed Aug 06 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.232-1mdv2009.0
+ Revision: 264467
- new release 0.1.232:
  	+ use NVIDIA 177.x only for GTX 2xx series, 173.x for earlier cards

* Thu Jul 24 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.231-1mdv2009.0
+ Revision: 245945
- new release 0.1.231:
  	+ add two new monitors (Pixel and AdamW)
  	+ add three new Intel video IDs (from xf86-video-intel-2.4.0) (AdamW)

* Fri Jun 20 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.230-1mdv2009.0
+ Revision: 227580
- new release 0.1.230:
  	+ add new ATI IDs (r700 family), adjust categories as these are not
          supported by radeonhd (or radeon) yet

* Wed Jun 18 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.229-1mdv2009.0
+ Revision: 223996
- new release 0.1.229:
  	+ split Mach 64 and Rage 128 graphics cards up again as driver split upstream

* Wed Jun 18 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.228-1mdv2009.0
+ Revision: 223822
- new release 0.1.228:
  	+ add two new NVIDIA cards
  	+ adjust NVIDIA card groups for upcoming driver branching

* Sat May 31 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.227-1mdv2009.0
+ Revision: 213586
- new release 0.1.227: several updated and added definitions for new ATI and NVIDIA drivers

* Wed May 28 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.226-1mdv2009.0
+ Revision: 212700
- new release 0.1.226: use geode for two devices it supports (on advice of upstream)

  + Thierry Vignaud <tv@mandriva.org>
    - improved description

* Tue May 27 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.225-1mdv2009.0
+ Revision: 212145
- new release 0.1.225: rs780 now supported by radeonhd, drop separate definition

* Fri May 16 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.224-1mdv2009.0
+ Revision: 208021
- new release 0.1.224: revert geode changes for now, pending hardware testing / advice from upstream
- new release 0.1.223: support two AMD / NatSemi Geode chips with the geode driver

* Wed Apr 23 2008 Olivier Blin <blino@mandriva.org> 0.1.222-1mdv2009.0
+ Revision: 197060
- explicitely buildrequire drakxtools-backend >= 10.30
- 0.1.222
- use libata pata modules by default

  + Adam Williamson <awilliamson@mandriva.org>
    - 0.1.221: add new NVIDIA IDs, simplify NVIDIA groups again for new driver

* Mon Apr 14 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.220-1mdv2009.0
+ Revision: 192827
- 0.1.220: drop a should-now-be-unneeded workaround, add two new Radeon IDs

* Thu Apr 03 2008 Olivier Blin <blino@mandriva.org> 0.1.219-1mdv2008.1
+ Revision: 192276
- 0.1.219
- blacklist HD 2400 XT from using radeonhd (the one we have at aboukir has problems)
- typo fix in usbtable (#39531)
- simplify long monitor names (#39222)

* Wed Mar 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.218-1mdv2008.1
+ Revision: 190206
- refresh tarball - adjust HD 3200 again (actually, fglrx supports it but ati does not)
- new release 0.218:
  	+ add USB ID for Epson Expression 10000XL (salem)
  	+ handle some more mice with back/forward buttons (adamw)
  	+ some adjustments to driver mapping for a few ATI Radeons (adamw)

* Thu Mar 20 2008 Pixel <pixel@mandriva.com> 0.1.217-1mdv2008.1
+ Revision: 189161
- 0.217: all "Acer Aspire" are not laptops (#38875)

* Tue Mar 18 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.216-1mdv2008.1
+ Revision: 188625
- 0.216: add NVIDIA 8800 GS (thanks Christophe Amrein-Marie) and 9800 GX2, change NVIDIA category names

* Tue Mar 18 2008 Olivier Blin <blino@mandriva.org> 0.1.215-1mdv2008.1
+ Revision: 188558
- 0.1.215
- add hardcoded alias for jmicron (#38343)

* Tue Mar 11 2008 Pixel <pixel@mandriva.com> 0.1.214-1mdv2008.1
+ Revision: 185875
- 0.1.214:
- Cards+:
  o nvidia-current now require processor with SSE, defaulting to nvidia96xx
    if no SSE

* Tue Mar 11 2008 Thierry Vignaud <tv@mandriva.org> 0.1.213-1mdv2008.1
+ Revision: 185246
- synd dkms data with latest prebuild packages

* Wed Mar 05 2008 Tiago Salem <salem@mandriva.com.br> 0.1.212-1mdv2008.1
+ Revision: 180200
- add "HP PSC 1310 series" (#34631)

* Mon Feb 18 2008 Pixel <pixel@mandriva.com> 0.1.211-2mdv2008.1
+ Revision: 171531
- add BuildRequires kernel-latest, needed to create fallback-modules.alias
  (it is now needed since basesystem-minimal creation)
- 0.1.211:
- lst/MonitorsDB:
  o add 1024x600 (used on Samsung Q1Ultra) (#37889)
  o add "Hanns.G HG216D" (from cooker@)
  o add "Philips 190C" (from cooker@)
- lst/Cards+: add NEEDVIDEORAM for Tseng cards (#37704)

* Fri Feb 08 2008 Thierry Vignaud <tv@mandriva.org> 0.1.210-1mdv2008.1
+ Revision: 164073
- add 2 monitors (from cooker@)
- synd dkms data with latest prebuild packages

* Tue Feb 05 2008 Pixel <pixel@mandriva.com> 0.1.209-1mdv2008.1
+ Revision: 162696
- new release 0.1.209:
  	+ add "Flat Panel 800x480" (used on belinea s.book) (#37486)

* Thu Jan 24 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.208-1mdv2008.1
+ Revision: 157674
- new release 0.1.208:
  	+ adjust Chrome9 driver mapping (#37032)
  	+ add latest ATI IDs from upstream Windows driver

* Thu Jan 24 2008 Thierry Vignaud <tv@mandriva.org> 0.1.207-1mdv2008.1
+ Revision: 157589
- latest kernel PCI ids

* Wed Jan 02 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.206-1mdv2008.1
+ Revision: 140250
- new release 0.1.206:
  	+ blacklist ATI FireGL Mobility T2 from using proprietary driver as per report from Jan Ciger that it does not work

* Thu Dec 27 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.205-1mdv2008.1
+ Revision: 138400
- new release 0.1.205 (use plain 'fglrx' for all post-9500 radeons again now we only have one version of the driver once more)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 19 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.204-1mdv2008.1
+ Revision: 133421
- new release 0.1.204:
  	+ add several new Intel graphics chip IDs from upstream driver source (adamw)

* Tue Dec 18 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.203-1mdv2008.1
+ Revision: 132987
- new release 0.1.203:
  	+ add new NVIDIA IDs from upstream Windows driver (adamw)
  	+ add new ATI IDs from upstream Windows driver (adamw)
  	+ add new ATI IDs from upstream developer ID list (adamw)
  	+ rename 'radeon 9500 to radeon x850' group to 'radeon 9500 to radeon x1050' (x1050 exists and is rebadged 9550/9600) (adamw)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Nov 22 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.202-1mdv2008.1
+ Revision: 111315
- new release 0.1.202:
  	+ add two new monitors (pixel)
  	+ add new NVIDIA card definitions (from upstream Windows driver header) (adamw)

* Tue Oct 30 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.201-1mdv2008.1
+ Revision: 103658
- new release 0.201: adjust to new fglrx 8.42.3 (Radeon 9500 and later all use fglrx-hd2000, except all FireGL cards use fglrx. also add a couple of missing cards)

* Wed Oct 17 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.200-1mdv2008.1
+ Revision: 99491
- 0.1.200 (anniversary release!)
  	+ the ATI Brave New World. in the Brave New World, radeonhd works for all X1xxx and HD 2xxx cards, and fglrx-hd2000 works for all HD 2xxx cards. disclaimer: Brave New World may have minor, or indeed major, discrepancies from reality.
  	+ lst/MonitorsDB: fix hsync range for 2405FPW
  	+ lst/MonitorsDB: add ViewSonic G90fB
  	+ do not prefer snd_usb_audio instead of some zc0301/uvcvideo/quickcam_messenger webcams

* Fri Oct 05 2007 Thierry Vignaud <tv@mandriva.org> 0.1.199-2mdv2008.0
+ Revision: 95557
- fix changelog

* Thu Oct 04 2007 Olivier Blin <blino@mandriva.org> 0.1.199-1mdv2008.0
+ Revision: 95480
- add explicit alias for modules in ide/sata categories, not to use ata_generic
- pcitable: replace more hyphens by underscores in module names
- dmitable: load acer_acpi module on for Acer Aspiron laptops (#32990)

* Wed Oct 03 2007 Thierry Vignaud <tv@mandriva.org> 0.1.198-1mdv2008.0
+ Revision: 94952
- update dkms aliases

* Mon Oct 01 2007 Thierry Vignaud <tv@mandriva.org> 0.1.197-1mdv2008.0
+ Revision: 94117
- update dkms aliases

* Fri Sep 28 2007 Olivier Blin <blino@mandriva.org> 0.1.196-1mdv2008.0
+ Revision: 93748
- 0.1.196
- use intel driver for Mobile GM965/GL960 (from Damien Lallement)
- use vboxvideo in VirtualBox guests (from Frederic Crozat)

* Fri Sep 28 2007 Thierry Vignaud <tv@mandriva.org> 0.1.195-1mdv2008.0
+ Revision: 93578
- update dkms aliases

* Fri Sep 28 2007 Olivier Blin <blino@mandriva.org> 0.1.194-1mdv2008.0
+ Revision: 93444
- 0.1.194
- prefer ipw3945 over iwl3945, which has some stability/performance issues

* Sun Sep 23 2007 Olivier Blin <blino@mandriva.org> 0.1.193-1mdv2008.0
+ Revision: 92386
- 0.1.193
- prefer piix over ata_piix when appropriate

* Thu Sep 20 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.192-1mdv2008.0
+ Revision: 91670
- 0.1.192 (use via driver for a specific unichrome card, it's better than openchrome - #33535)

* Mon Sep 17 2007 Thierry Vignaud <tv@mandriva.org> 0.1.191-1mdv2008.0
+ Revision: 89351
- fix driver for anydata usb modem (#31631)

  + Adam Williamson <awilliamson@mandriva.org>
    - 0.1.190 (use proprietary driver for a few more HD 2xxx cards)
    - new release 0.1.189 (add several new NVIDIA IDs from the latest Windows beta driver)
    - new release 0.1.188 (refine Radeon HD 2xxx support further, add several new Radeon chips)
    - new release 0.1.187 (support new fglrx-hd2000 driver for Radeon 2xxx series)

* Tue Sep 11 2007 Olivier Blin <blino@mandriva.org> 0.1.186-1mdv2008.0
+ Revision: 84499
- add conflicts with module-init-tools using preferred-modules.alias
- update conflicts with ldetect
- 0.1.186
- install preferred-modules.alias as /lib/module-init-tools/ldetect-lst-modules.alias

  + Adam Williamson <awilliamson@mandriva.org>
    - update tarball again with some SiS changes
    - update tarball with new changes
    - 0.1.185: refine support for (uni)chrome cards

* Fri Sep 07 2007 Olivier Blin <blino@mandriva.org> 0.1.184-1mdv2008.0
+ Revision: 81783
- 0.1.184
- fix preferred-modules.alias build by using fallback-modules.alias
  (modules.alias for current kernel may not be available if run in chroot)

* Fri Sep 07 2007 Olivier Blin <blino@mandriva.org> 0.1.183-1mdv2008.0
+ Revision: 81745
- 0.1.183: fix fields order in dkms-modules.alias

* Fri Sep 07 2007 Olivier Blin <blino@mandriva.org> 0.1.182-1mdv2008.0
+ Revision: 81487
- 0.1.182
- provide default module aliases for PCI/USB devices matching
  multiple modules in preferred-modules.alias (not complete yet),
  to be used in libmodprobe and thus in ldetect
- merge ldetect-lst.conf modprobe file in preferred-modules.alias

* Thu Sep 06 2007 Pixel <pixel@mandriva.com> 0.1.181-1mdv2008.0
+ Revision: 80605
- 0.1.181:
- nicely sort MonitorsDB (needed by XFdrake):
  have "Flat Panel 800x600" before "Flat Panel 1024x768"
- add dkms-modules.alias and dkms-modules.description
  (gathered from pre-built dkms modules, to be used in ldetect)

* Thu Aug 30 2007 Thierry Vignaud <tv@mandriva.org> 0.1.180-1mdv2008.0
+ Revision: 75593
- add an oddball GeForce 7950 reported by Jason Carson on forums
  (adamw)
- add ViewSonic VX2025wm (#29569)
- fix wrong driver for RTL8139 (#32927)
- kill some wrong entries (#31331)
- use software cursor for openchrome as per pcpa (adamw)

* Tue Aug 21 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.179-1mdv2008.0
+ Revision: 68713
- 0.1.179: improve Unichrome configuration (don't use 3D where it's broken, use software cursor, add new device IDs)

* Mon Aug 20 2007 Olivier Blin <blino@mandriva.org> 0.1.178-1mdv2008.0
+ Revision: 67867
- 0.1.178 (use '_' in modules name)

* Thu Aug 16 2007 Thierry Vignaud <tv@mandriva.org> 0.1.177-1mdv2008.0
+ Revision: 64338
- first attempt to shrink usbtable

* Mon Aug 13 2007 Pixel <pixel@mandriva.com> 0.1.176-1mdv2008.0
+ Revision: 62633
- add fallback-modules.alias to be used in a chroot
  (where we don't have the modules.alias corresponding to the running kernel)

* Sun Aug 12 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.175-1mdv2008.0
+ Revision: 62343
- update drakx-kbd-mouse-x11 conflict to 0.21 for recent nvidia changes
- switch to avivo as free driver for Radeon X1xxx series (temporarily)

* Wed Aug 08 2007 Pixel <pixel@mandriva.com> 0.1.174-1mdv2008.0
+ Revision: 60551
- rename nvidia97xx into nvidia-current (Anssi Hannula)

  + Thierry Vignaud <tv@mandriva.org>
    - correct some ATI definitions (adamw)
    - drop description field in pcitable (kept for usbtable for now)
    - kill e1000 lines since the eepro1000 alternative is dead
    - restore gdth entries as its driver isn't module.pcimap compliant

* Sat Aug 04 2007 Thierry Vignaud <tv@mandriva.org> 0.1.172-1mdv2008.0
+ Revision: 58842
- shrink pcitable now that we got drivers from modalias resolution and descriptions from pci.ids

* Wed Jul 11 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.171-1mdv2008.0
+ Revision: 51150
- add new ATI and NVIDIA cards (adamw)
- add new wacom tablets (fcrozat)

* Fri May 18 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.170-1mdv2008.0
+ Revision: 28299
- 0.1.170 (use vesa instead of fbdev as backup for radeon cards not supported by radeon driver)

* Thu May 10 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.169-1mdv2008.0
+ Revision: 26186
- add more ATI definitions from website and Windows driver

* Mon Apr 30 2007 Thierry Vignaud <tv@mandriva.org> 0.1.168-1mdv2008.0
+ Revision: 19606
- use intel driver instead of i810
- cleanup card entries (adam):
  o merge i810-i830 and i845-i965 definitions
  o NVIDIA: G80 cards now supported by nv, add new IDs for new G80
    series cards
  o rationalize C&T, Digital TGA, permedia / glint entries, old S3
    entries and S3 ViRGE entries


* Tue Apr 03 2007 Olivier Blin <oblin@mandriva.com> 0.1.167-1mdv2007.1
+ Revision: 150452
- do not use amd video driver, revert to old behavior

* Tue Apr 03 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.166-1mdv2007.1
+ Revision: 150432
- just use free driver with all xpress200 since their support seems
  broken on x86_64 with fglrx (damien)

* Tue Apr 03 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.165-1mdv2007.1
+ Revision: 150411
- blacklist yet another radeon on x86_64 (RC410 [Radeon Xpress 200) (damien)

* Sat Mar 31 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.164-1mdv2007.1
+ Revision: 150061
- disable fglrx on x86_64 with some cards known to make fglrx crashes (#29256)

* Fri Mar 23 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.163-1mdv2007.1
+ Revision: 148651
- use Vesa on 1 Intel card which is too new for the intel driver (arnaud)

* Thu Mar 22 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.162-1mdv2007.1
+ Revision: 148185
- enable DRI for OpenChrome (#27167)

* Wed Mar 21 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.161-1mdv2007.1
+ Revision: 147180
- add prefered resolution for Dell M770 (Javier Martinez Villacampa)
- do not package big ChangeLog

* Wed Mar 14 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.160-1mdv2007.1
+ Revision: 143700
- MonitorsDB:
  o add BenQ FP71G & Philips 190S monitors (Javier Martinez
    Villacampa)
  o cleanups
  o merge identical monitors
- sync pcitable with kernel-tmb-desktop-2.6.20.3-1mdv

* Wed Mar 14 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.159-1mdv2007.1
+ Revision: 143498
- add Acer AL1916W & LG L1730S (Javier Martinez Villacampa)
- add another Flatron L204WT (lezard)
- set preferred resolution for Samsung SyncMaster 753DF(X) & Viewsonic
  E771-4 (Javier Martinez Villacampa)

* Tue Mar 13 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.158-1mdv2007.1
+ Revision: 142424
- add LG Flatron L226WT (Javier Martinez Villacampa)
- sync monitor DB with fedora
- use AMD driver for Geode GX/LX

* Mon Mar 12 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.157-1mdv2007.1
+ Revision: 141815
- From Adam Williamson:
- add a couple more SiS / XGI cards
- add a couple of snd-hda-intel IDs from the driver source
- add MCP67 ethernet IDs
- add support for ENE sdhci SD card reader
- add support for a few Matrox cards
- add support fir one more apm card
- add support Quadro FX 4600 and 5600 (with NVIDIA driver 9755)
- add support two more Radeons
- clean up SiS definitions
- convert ar5k definitions to madwifi as ar5k is obsolete
- enable 3D on tdfx
- fix FireGL3000 option for glint
- kill a bogus entry for secondary output
- merge  definitions
- sanitize 3DFX, APM, Epson, i128, i740, IMS, madwifi, Matrox, Silicon
  Motion & Sun definitions
- set fb for VIA CLE266 (disabled in openchrome source)
- set NVidia G80 cores to vesa
- use VESA driver for Parhelia and newer cards

* Thu Mar 08 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.156-1mdv2007.1
+ Revision: 138513
- add 2 missing NVIDIA card (adamw)
- clean up ATI definitions (adamw)
- clean up Tseng definitions (adamw)
- support ATI Xpress 1200 (adamw)
- add 2 missing NVIDIA card (adamw)
- clean up ATI definitions (adamw)
- clean up Tseng definitions (adamw)
- support ATI Xpress 1200 (adamw)

* Wed Mar 07 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.155-1mdv2007.1
+ Revision: 134521
- reduce number of Cirrus Logic, C&T & S3 entries (adamw)
- sanitize a couple of ATI entries (adamw)
- unify Kyro entries (adamw)

* Tue Mar 06 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.154-1mdv2007.1
+ Revision: 134001
- a couple x800 are supported by the free driver (adamw, #29188)
- add ATI definitions for a bunch of previously 'unknown' cards
  (adamw, #29188)
- clean and update Intel integrated adapter definitions and add
  support for i752 (adamw, #29191)

* Tue Mar 06 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.153-1mdv2007.1
+ Revision: 133955
- sanitize NVidia entries (adamw, #29183)
- use free driver for some ATI cards that are no longer supported (adamw, #28682)

* Tue Mar 06 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.152-1mdv2007.1
+ Revision: 133880
- switch 4 drivers from OSS to ALSA since kernelteam disabled them (#28990)

* Fri Mar 02 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.1.151-1mdv2007.1
+ Revision: 131342
- fix mispelled drakx-kbd-mouse-x11 conflict
- add Philips 170x6 (pixel)
- add "Samsung SyncMaster 225BW" monitor (S. Teletchea)
- add a monitor (pixel, #28408)
- add support for an unsupported nvidia card (#26235)
- do not use fglxrx on radeon 7xxx since it doesn't support them anymore (#26473)
- match more HP laptops (pixel, Luca Berra)
- sync with latest pci.ids
- sync with kernel-tmb-desktop-2.6.19.2-3mdv-1
- use fglrx for ATI Xpress 200 RC410 (blino)
- use nvidia97xx instead of nvidia and nvidia71xx instead of NVIDIA_LEGACY (pixel)
- use XkbModel inspiron instead of pc105 on some laptops (pixel)
- kill dead old comment

  + Pixel <pixel@mandriva.com>
    - add conflicts on drakx-kbd-mouse-x11 < 0.7
      (for XFdrake using nvidia97xx instead of nvidia, and nvidia71xx instead of NVIDIA_LEGACY)

* Fri Dec 22 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.150-1mdv2007.1
+ Revision: 101459
- Import ldetect-lst

* Fri Dec 22 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.150-1mdv2007.1
- add "Acer; ACR AL2023" monitor (#26294)
- add "Acer AL1722" monitor (#26294)
- add monitor (#26713)
- ati xpress200 rs480 is unworkable with ati proprietary driver
- GL apps make X crash with Voodoo cards (Gerard Delafond)
- defaulting to ALSA driver instead of radio driver for 0x125d:0x1978
  (#26119)
- switch 0x1274:0x5880 from OSS to ALSA (#26045)
- sync at76 IDs for at76_usb module (blino, #26125)

* Wed Sep 20 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.149-1mdv2007.0
- rename "SiS" as "SiS generic", thus fixing vendor tree in XFdrake (#25981)
- tag Acer TravelMate systems as laptops (blino, #25915)

* Wed Sep 20 2006 Olivier Blin <oblin@mandriva.com> 0.1.148-1mdv2007.0
- add /etc/modprobe.d/ldetect-lst.conf support
- add explicit alias to hostap_cs for an USR Wireless PC Card (#25911)
- add 4 entries for "Intel 965" (pixel)

* Wed Sep 20 2006 Pixel <pixel@mandriva.com> 0.1.147-1mdv2007.0
- add "Intel 965" in Cards+
- add LiveBox USB id (blino)
- switch a intel sound card from OSS to ALSA (thierry)

* Sat Sep 16 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.146-1mdv2007.0
- add support for openchrome driver (#24021)
- use snd-intel8x0m on nc6220 (blino)

* Sat Sep 16 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.145-1mdv2007.0
- do not use anymore kernel-2.4.x module names since:
  o we cannot rely on /lib/module-init-tools/modprobe.compat at
    install time (#8814)
  o we do not support anymore kernel-2.4.x

* Fri Sep 15 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.144-1mdv2007.0
- add zd1211rw device IDs because of kernel issues (blino)

* Thu Sep 14 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.143-1mdv2007.0
- add support for more new ATI cards
- fix a bogus ATI secondary entry (#25399)
- kill all secondary entries with an ati driver (which surprisingly :-)
  are all unknown to the ati driver) since they're likely to break
  systems
- sync with latest pci.ids

* Wed Sep 13 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.142-1mdv2007.0
- use ati for 0x1002:0x4c59 (#25562)

* Tue Sep 12 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.141-1mdv2007.0
- add "Samsung SyncMaster 757NF" (Jure Repinc)
- ati x700 is supported by fglrx
- do not set a drver for a secondary ATI head

* Wed Sep 06 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.140-1mdv2007.0
- sync with kernel-2.6.17.4mdv

* Wed Sep 06 2006 Pixel <pixel@mandriva.com> 0.1.139-1mdv2007.0
- add entry for Logitech MX510 mouse

* Wed Sep 06 2006 Pixel <pixel@mandriva.com> 0.1.138-1mdv2007.0
- change the format used for "imwheel" mice: imwheel:MX700 instead of imwheel|MX700 
- add entries for MX310 (no evdev (?), generic imwheel), MX500, MX518, MX1000

* Sat Sep 02 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.137-1mdv2007.0
- use evdev+imwheel for logitech MX700 & MX1000 (pixel)
- a couple of r[23]50 are not (yet?) managed by xorg ati driver
- do not favor fbdev over ati for a couple of r[23]0 ati cards
- free driver doesn't manage ati r5xx (eg: X1600 & X7600): use either
  fglrx or fbdev instead (#24992)
- use vesa rather than fbdev for "ATI M56P [Radeon Mobility X1600]" (#24992)

* Fri Sep 01 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.136-1mdv2007.0
- don't use EXA anymore on ATI Radeon 8500 QL
- fix 2 ATI entries (#24981)

* Sat Aug 26 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.135-1mdv2007.0
- add Proview 775N (#19874)
- add support for X1300 (#24287)
- blindly set driver for a few scores of radeon cards
- fix driver for a DVB card (#15118)
- fix support for X1600 (#24286)

* Fri Aug 25 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.134-1mdv2007.0
- add GeForce FX 350 (chandra, #24678)
- add some nvidia cards (pixel)
- add support for ATI Radeon X1400 (Danny Tholen)
- fix driver for V370 Radeon X600 (chandra, #24676)
- fix 2nd card of dual head radeon X600 (chandra, #24676)
- use EXA by default on ATI Radeon 8500 QL in order to have working
  composite

* Sun Aug 13 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.133-1mdv2007.0
- fix "S3 UniChrome" entry (pixel, #24021)
- prefer dmfe over tulip (#23813)
- sync with kernel-2.6.17.2mdv
- sync with latest pci.ids

* Wed Jul 26 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.132-1mdv2007.0
- sync with kernel-multimedia-desktop-2.6.17.6-1mdv
- sync with kernel-tmb-desktop-2.6.17.7-1mdv
- sync with latest pci.ids
- fix entries for which the kernel driver has changed over the last
  monthes
- tag some ISDN cards as such

* Wed Jul 26 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.131-1mdv2007.0
- add support for Matrox G200SE
- fix support for "MGA G200e [Pilot] ServerEngines (SEP1)" (#23912)
- sync with kernel-2.6.17.1mdk

* Thu Jul 13 2006 Olivier Blin <oblin@mandriva.com> 0.1.130-1mdv2007.0
- tag Acer.* Aspire.* systems with "laptop" type (#23197)

* Sat Jul 08 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.129-1mdv2007.0
- fix 3 ATI entries (#22666, #23349)
- switch an Intel card from OSS to ALSA
- scanner data for SANE 1.0.18 (till)
- handle Epson's "epkowa" SANE backend (till)

* Wed May 24 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.128-1mdk
- add support for Broadcom 4319 802.11a/b/g
- add support for HighPoint RocketRAID 3xxx Controller
- cleanup MonitorsDB to match what XFdrake generates (pixel)
- fix detecting the cardbus bridge on an HP nc6320
- handle the new drivers that replace sk98lin (#22669)
- ueagle-atm replaced eagle-usb

* Wed May 10 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.127-1mdk
- add another slamr modem (ThinkPad R50) (blino)
- add Option GlobeTrotter 3G/EDGE (nozomi driver) (blino)
- disable DRI on old ATI cards (Damien Lallement)
- sync with latest pci.ids
- sync with kernel-tmb-desktop-2.6.16.13
- sync with kernel-2.6.17-rc3-mm1

* Tue Apr 25 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.126-1mdk
- add MCP61 support
- add 2 geforce cards (Pierre Brieudes)
- add realtek RTL-8168 id (gb)
- add support for SB600
- fix i945GM id for intel-agp (gb)
- merge new nvidia ids from 1.0-8756 driver (gb)
- migrate some mptscsih to mptspi and mptfc (gb)
- sync with kernel-linus-2.6.17.rc2.17mdk
- sync with kernel-2.6.17-rc1-mm2
- sync with latest pci.ids
- sync with xorg-7+'s main drivers:
  o add quite a lot of new ati & nvidia cards
  o add support for nsc driver
  o fix some entries (wrongly listing their kernel FB driver instead
    of their X driver)
  o fix a bogus entry (it's nsc, not ATI)
- update a description
- update a card entry (Samuel Clara)

* Tue Mar 21 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.125-1mdk
- add EMC EF-836 monitor (pablo)
- sync with latest pci.ids
- sync with kernel-2.6.16

* Thu Mar 09 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.124-1mdk
- add one more ATI card
- handle Intel PRO/Wireless 3945ABG
- sync with kernel-2.6.16-rc5-mm3
- sync with latest pci.ids

* Thu Feb 16 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.123-1mdk
- sanitize some PATA entries (aka prefer standard ide drivers over
  their ported over libata version)
- add 4 new cards from DRI's CVS: 2 i945GM, 1 voodoo & 1 SiS
- kill a few bogus description

* Tue Feb 14 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.122-1mdk
- sync with latest pci.ids
- sync with kernel-2.6.16-rc2-mm1
- add support for more SIS devices
- add support for Leadtek Winfast TV 2000xp delux

* Fri Jan 27 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.121-1mdk
- add support for new snd-als300 sound driver
- add support for nVidia MCP51
- sync with kernel-2.6.16-rc1-mm1
- updated for SANE 1.0.17 (till)
- added lines for SCSI-over-parallel scanner kernel modules (till)

* Wed Jan 11 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.120-1mdk
- add support for Intel ICH8
- add HIQ500a (Andres Kaaber)
- sync with kernel-2.6.15-mm3 and latest pci.ids

* Thu Jan 05 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.1.119-1mdk
- add support for AMD CS5536
- clean some ALSA entries
- sync with kernel-2.6.15-mm1
- sync with kernel-multimedia-2.6.14-0.mm.3mdk
- sync with latest pci.ids

* Fri Nov 25 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.118-1mdk
- sync with latest pci.ids
- sync with kernel-2.6.15-rc2-mm1
- fill in some descriptions
- kill some buggy entries

* Mon Nov 07 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.117-1mdk
- sync with latest pciutils
- sync with kernel-multimedia-2.6.12-12.mm.7mdk and kernel-2.6.14
- homogeneize companies names (erwan)
- fill a cople void decriptions (erwan)
- add 2 ATI entries (erwan)

* Wed Oct 19 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.116-1mdk
- add 5 pci modem entries (blino)
- sync with kernel-2.6.14-rc4-mm1 and with latest pci.ids
- usbtable: remove description of 0x0471:0x0311 as both PCVC740K and
  PCVC840K share the same ids; let the kernel extract the right name
  out of the USB device (#18946)

* Tue Sep 20 2005 Pixel <pixel@mandriva.com> 0.1.114-1mdk
- fix update-ldetect-lst ordering of mixed *.lst and *.lst.gz

* Mon Sep 19 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.113-1mdk
- prevent writing unparsable xorg.conf files

* Sat Sep 17 2005 Olivier Blin <oblin@mandriva.com> 0.1.112-1mdk
- use slamr or hsf instead of snd-intel8x0m on some Dell laptops

* Fri Sep 16 2005 Pixel <pixel@mandriva.com> 0.1.111-1mdk
- fix entries for Acer Aspire 1362: we had Card for bridges and unknown for the card
  (thanks to Torbjorn Turpeinen)

* Sat Sep 10 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.110-1mdk
- sync with latest pci.ids
- add sata_mv

* Thu Sep 08 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.109-1mdk
- sync with kernel-2.6.13-mm1

* Wed Sep 07 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.108-1mdk
- sync with latest pci.ids
- workaround kernel failling to report the proper driver to use (#17688)

* Tue Sep 06 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.107-1mdk
- replace all "mptspi" references by "mptscsih" (the former is a
  subfile of the latter)
- fix on a laptop with fglxrc (pixel)
- add brazilian Motorola SM56 modem (blino)

* Tue Aug 30 2005 Frederic Lepied <flepied@mandriva.com> 0.1.106-1mdk
- use the ati driver for the radeon and r128 video cards

* Tue Aug 30 2005 Olivier Blin <oblin@mandriva.com> 0.1.105-1mdk
- add some ATI X700 pro and X850 cards
- from Thierry Vignaud:
  o switch one i810 from OSS to ALSA (#17905)
  o add support for snd-asihpi
  o sanitize: use the same driver than the device w/o sub
    ids for this device with sub ids
  o lst/pcitable: sync with latest pci.ids

* Fri Aug 26 2005 Pixel <pixel@mandriva.com> 0.1.104-1mdk
- modify merge2pcitable.pl to handle compressed pcitable

* Thu Aug 25 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.103-1mdk
- updated scanner database for SANE 1.0.16 (till)
- switch a cople network cards from eepro100 to e100

* Thu Aug 25 2005 Pixel <pixel@mandriva.com> 0.1.102-1mdk
- gzip pcitable, usbtable and dmitable (to win space), 
  use a hard link when possible to win even more room
- update prereq
- add a cople new monitor
- add support for a new SiS SATA controller (tv)
- add support for SiS966 (tv)
- add support for SATA300 TX4 Controller (tv)
- add support for AAR-1420SA (tv)
- add support for snd-riptide (tv)
- add support for 3 new tg3 netwrod cards (tv)
- add support for a slamr modem (blino)

* Sat Jul 30 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.101-1mdk
- add support for RS480 5955
- describe ATI|RS480 5954

* Fri Jul 29 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.100-1mdk
- sync with kernel-2.6.13-rc3-mm2
- fix a cople SCSI entry
- fix frequency range of Belinea 101715 (#15158)
- fix a network card (#15393)

* Fri Jul 22 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.99-1mdk
- fix two adaptec entries (arnaud patard)

* Tue Jul 19 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.98-1mdk
- add support for nvidia MCP51
- describe nvidia MCP55
- sync with kernel-2.6.13-rc3-mm1
- add Motorola V180 Cell Phone (stew)

* Tue Jul 12 2005 Frederic Lepied <flepied@mandriva.com> 0.1.97-1mdk
- fixed URL
- added a few Intel ids (i945...)

* Sat Jul 09 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.96-1mdk
- sync with kernel-2.6.13-rc2-mm1
- add support for more SATA cards
- fix a few entries

* Wed Jul 06 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.95-1mdk
- add support for ATI on x86_64

* Tue Jul 05 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.94-1mdk
- fix a few entries b/c of some kernel changes
- sync with kernels 2.6.12.3mdk-1-1mdk and 2.6.13-rc1-mm1

* Sat Jul 02 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.93-1mdk
- add another ATI modem managed by ALSA
- add more USB DVB devices
- add support for more ISDN USB devices
- sync with kernels 2.6.12-mm1 & 2.6.12-rc6
- fix slmodem wrongly detected as hsfmodem (blino)

* Tue Jun 07 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.92-1mdk
- fix detection of some ISDN modems by drakconnect
- sync with kernel-2.6.12-rc5-mm2

* Tue May 31 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.91-1mdk
- sync with kernel-2.6.12-rc5-mm1

* Sat May 28 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.90-1mdk
- add support for Broadcom NetXtreme II BCM5706 1000Base-T
- add support for PDC40519 (FastTrak TX4200)
- sync SATA drivers with kernel-multimedia

* Wed May 25 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.89-1mdk
- add more subids for orinoco (in order to ease future conflicts
  between orinoco vs hostap conflicts)
- add suport for SII 32xx SATA controllers (needs to patch the kernel)
- replate an ata_piix by a piix (incore ide driver was winning anyway
  and it confuesed vmware) (Pascal Terjan)

* Fri May 20 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.88-1mdk
- fix hostap_pci vs orinoco_pci conflict by using sub ids (blino, #11393)
- pcitable: sync with kernel-multimedia-2.6.11-7.mm.16mdk
- usbtable: sync with kernel-2.6.11-8mdk

* Sat May 14 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.87-1mdk
- add support for VIA VT8251/VT8237A HD-Audio controllers
- add support for ATI HD Audio support in SB450 south bridge
- sync with kernel-2.6.12-rc4-mm1 (mainly DVB updates)
- sync with hwdata-0.157 (monitors & 2 video cards)
- sync with latest pci.ids

* Tue May 10 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.86-1mdk
- sync with latest pci.ids
- sync with kernel-multimedia-2.6.11-7.mm.11mdk (1 more gigabit card
  and lots of new SATA controllers)

* Thu May 05 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.1.85-1mdk
- add a new tg3 network card from kernel-2.6.12-rc3-mm2
- add a new ATI SATA controller from kernel-2.6.11.8mdk
- sync with kernel-2.6.12-rc3
- use slmodem on X-Book (blino)

* Tue Apr 26 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.84-1mdk
- sync with kernel-multimedia-2.6.11-7.mm.1mdk
- sync with latest pci.ids
- use orinoco instead of hostap for a Prism 2.5 card (blino, #15566)
- hfc_usb is an ISDN driver

* Sat Apr 16 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.83-1mdk
- add support for Gallant Odyssey Sound 4
- add full support for Intel ESB2 DID
- fix a cxgb entry
- fix install on new Dell laptops
- update ata_adma entries from kernel-multimedia-2.6.10-3.mm.25mdk
- update a couple void descriptions from pci.ids
- sync with kernel-2.6.12-rc2-mm2
- add D-Link DWL-G510 Rev B (blino)

* Wed Apr 06 2005 Olivier Blin <oblin@mandrakesoft.com> 0.1.82-1mdk
- use slmodem driver for some ICH4 modems (Arnaud de Lorbeau)

* Tue Apr 05 2005 Pixel <pixel@mandrakesoft.com> 0.1.81-1mdk
- add graphic card entry for laptop nx6110

* Fri Apr 01 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.80-1mdk
- check pcitable consistency vs kernel's module.pcimap and fix:
  o one Adaptec entry (aic79xx -> aic7xxx)
  o one wireless entry (orinoco_plx -> hostap_plx)
  o one Intel SATA entry (ahci -> ata_piix)
  o two ATI SATA entries (atiixp -> sata_sil)
- qla6322 has been obsoleted by qla6312 and no more exists

* Thu Mar 31 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.79-1mdk
- explicitely list all devices supported by megaraid_mbox (workaround
  *part* of #13855)
- add 2 more O2 Micro PCMCIA controllers (but ldetect class matching
  should catch them anyway)

* Thu Mar 31 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.78-1mdk
- support new nvidia ids from X.Org 6.8.2

* Thu Mar 31 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.77-1mdk
- add Fastrate USB 100 modem (blino)
- add support for NX6600GT (chandra, #14977)
- sync with kernel-2.6.12-rc1-mm2

* Wed Mar 23 2005 Pixel <pixel@mandrakesoft.com> 0.1.76-1mdk
- force overrideValidateMode on neomagic (which has pbs detecting the size of the LCD panel)
- allow 3D on S3 UniChrome

* Tue Mar 22 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.75-1mdk
- switch ES1983S Maestro-3i PCI Audio Accelerator from OSS to ALSA
  (#14573)
- sync usbtable with kernel

* Mon Mar 21 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.74-1mdk
- add a new SATA driver: ata_adma
- replace no more existing xircom_tulip_cb driver by xircom_cb

* Mon Mar 21 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.73-1mdk
- sync with kernel-2.6.11-mm3
- add support for production version of ATI RN50/ES1000
- MonitorsDB: misc cleanups (pixel & me)

* Tue Mar 15 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.72-1mdk
- fix driver after alsa naming change
- fix S3 UniChrome entries (fredl)
- replace a "GeForce2 DDR" by a "GeForce FX"

* Mon Mar 14 2005 Pixel <pixel@mandrakesoft.com> 0.1.71-1mdk
- add dmitable

* Wed Mar 09 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.70-1mdk
- sync with kernel-2.6.11-1mdk and kernel-2.6.11-mm2

* Tue Mar 08 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.69-1mdk
- sync with latest pci.ids & usb.ids
- add a new megaraid SAS driver

* Tue Mar 08 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.68-1mdk
- sync with xorg-x11-6.8.2-2mdk's nv driver
- add Xbox support (stew)
- ScannerDB: updates for parallel scanners (especially auto-detection
  with "umax_pp" driver) (till)

* Thu Feb 24 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.67-1mdk
- add support for VT6410
- add support for Pacific Digital SATA QStor
- fix a GeForce FX entry

* Tue Feb 22 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.66-1mdk
- usbtable: sync with kernel-2.6.10-3mdk

* Mon Feb 21 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.65-1mdk
- fill in missing Radeon descriptions
- update scanner database for SANE 1.0.15 (till)

* Fri Feb 18 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.64-1mdk
- fix one missing iteraid -> it821x (#13740)
- one more VIA SATA controller
- sync Monitors DB with hwdata-0.150
- Rev B iMac as the same eisa id as Rev A (danny)

* Fri Feb 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.63-1mdk
- fix kernel-2.4.x support for some i810-tco
- fix dtc SCSI driver used instead of dmx3191d
- add r8180 wireless driver (from kernel-multimedia)
- sync with latest usb.ids

* Fri Feb 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.62-1mdk
- sync with kernel-2.6.10-3mdk (one new ULI SATA controller & two Intel LPC)
- add a couple of Radeon graphic cards

* Thu Feb 10 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.61-1mdk
- add a new us robotics gibabit card (arnaud)
- add a new EMC monitor (Funda Wang)
- fill in a few descriptions for Digigram sound cards
- update contributors list

* Wed Feb 09 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.60-1mdk
- add 2 missing mxser entries from kernel-2.6.10-1mdk
- add a radeon LE
- fix a cople of descriptions (mostly ipw2200 and i915)
- fix support for one modem (vincent guardiola)

* Tue Feb 08 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.59-1mdk
- sync with latest usb.ids
- sync with latest pci.ids
- fix a nv SATA controller description

* Tue Feb 08 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.58-1mdk
- fix wrong qla1280 entry
- sync with kernel-2.6.11-rc3-mm1
- Xbox X driver support (stew)

* Mon Feb 07 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.57-1mdk
- sync with kernel-multimedia-2.6.10-1.mm.11mdk:
  o add one new ipw2200 entry
  o handle new driver qla4xxx
  o handle new sata_promise driver
- add support for "ARECA (ARC1110/1120/1130/1160/1210/1220/1230/1260)
  SATA RAID HOST Controller" (new driver in kernel-2.6.11-rc3-mm1)

* Mon Feb 07 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.56-1mdk
- add one new ATI graphic card
- add one new Intel graphic card
- add E-Tech/Amigo AMX-CA80U ADSL modem (pablo)
- handle quite a few more Intel & ALI AGP bridges
- handle new vrc4173_cardu PCMCIA driver (from kernel-2.6.11-rc3)
- replace uli526x by tulip driver
- handle new ISDN USB driver hfc4s8s_l1
- fix support for some ISDN drivers in drakconnect (namely c4, divas,
  hysdn and one hisax)
- sync with kernel-2.6.11-rc3

* Wed Feb 02 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.55-1mdk
- add 2 new intel sata controllers
- sync with kernel-multimedia-2.6.10-1.mm.9mdk

* Fri Jan 28 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.54-1mdk
- add one intel ide controller (from lkml)
- add a new LG monitor (Angelo Naselli)
- add 2 new apple monitors (danny)
- sync with kernel-2.6.11-rc2-mm1

* Tue Jan 25 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.53-1mdk
- fix support for SB Live! Value EMU10k1X

* Mon Jan 24 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.52-1mdk
- add support for one ATI and two ICH7 SATA controllers
- add a new Samsung monitor (Albert Astals Cid)

* Thu Jan 20 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.51-1mdk
- "snd-audigyls" ALSA driver was renamed "snd-ca0106"
- add SATA support for ICH7

* Thu Jan 20 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.50-1mdk
- fix conflict between 8139cp and 8139too
- add AC'97 Audio support for Intel ICH7
- add eisa id for Panasonic E70i monitor (neoclust)
- add 2 new monitors (one ADI and one Hyundai) (Neoclust)

* Thu Jan 13 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.49-1mdk
- add a new Sony monitor (Neoclust)
- switch a realtek driver (#12982)

* Tue Jan 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.48-1mdk
- add another zaptel device (Stefan van der Eijk)
- switch from ata_piix to ahci

* Tue Jan 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.47-1mdk
- list zd1201 driver
- manually merge driver that don't export ids of devices they managed

* Tue Jan 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.46-1mdk
- sync with ide drivers from 2.6.10-ac8
- add a new Samsung monitor (Albert Astals Cid)
- add 2 zaptel devices (Stefan van der Eijk)

* Mon Jan 10 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.45-1mdk
- add a new Philips monitor (Albert Astals Cid)
- add limited/partial support for zaptel
- list ivtv driver

* Mon Jan 10 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.44-1mdk
- add a new Lite-On monitor (Berthy)
- add a new Princeton monitor (Thomas Spuhler)
- add a new Sony monitor (Angelo Naselli)

* Fri Jan 07 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.43-1mdk
- add a Belinea monitor (Michael Braun)
- add two LG monitors (Neoclust)
- add support for Intel ICH7 sound card

* Fri Jan 07 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.42-1mdk
- add a Samsung monitor (Andres Kaaber)

* Fri Jan 07 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.41-1mdk
- sync with kernel-2.6.9-1mdk
- add a LG monitor (Andres Kaaber)

* Thu Jan 06 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.40-1mdk
- add a new monitor (Marek Laane)
- pcitable: fix wrong driver for a wifi card (#11393)
- usbtable: sync with latest usb.ids

* Wed Jan 05 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.39-1mdk
- sync with kernel-2.6.10-mm1
- clean DVB entries
- remove bogus usbcore entries
- solve a few conflicts regarding devices claimed by modules
- fix a wrongly identified card (pixel, #12871)

* Thu Dec 23 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.38-1mdk
- add support for Digigram PCXHR sound cards
- fix description of a couple DELL cards and a couple Digigram cards
- sync with kernels 2.6.10-rc3-mm1 and 2.6.8-10-rc3-bk16

* Fri Dec 03 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.37-1mdk
- disambiguate names of media devices (eg: DVB vs TV cards)
- update incomplete descriptions from {pci,usb}.ids
- sync i2c with 2.6.10-rc2-mm4
- one extra sound card from pci-26.lst file from debian's
  discover1-data

* Thu Dec 02 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.36-1mdk
- sync with debian's discover

* Thu Dec 02 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.35-1mdk
- add two new geforce cards and a score of fiber channel cards

* Thu Dec 02 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.34-1mdk
- sync with pci.ids, usb.ids, kernel-2.6.9-ac12, kernel-2.6.10-rc2-mm4

* Thu Dec 02 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.33-1mdk
- enable DRI on i915 and onMach64 since it is now supported in X.org-6.8.x

* Wed Dec 01 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.32-1mdk
- handle Alan Cox's new "voodoo" driver from x.org-6.8.x

* Fri Nov 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.31-1mdk
- since yenta_socket driver claims to support any pci card whose class
  is PCI_CLASS_BRIDGE_CARDBUS, assign it to all pcmcia/cardbus
  controllers

* Fri Nov 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.30-1mdk
- handle PCI device IDs set to PCI_ANY_ID in kernel's pcimap:
  o this especially fix PCMCIA support on O2 Micro controllers
  o this also add support for a couple of Adaptec SCSI controllers

* Thu Nov 25 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.29-1mdk
- MonitorsDB:
  o update, sync with hwdata-0.148
  o fix a few entry
  o add "Samsung SyncMaster 910N/912N" (pablo)
- pcitable:
  o fill in a few descriptions
  o sync with serial, DVB and SMB Host controllers drivers from
    kernel-2.6.10-rc2-mm3
  o add support for Intel's High Definition Audio Controller
  o sync with ALSA's CVS
- usbtable:
  o sync with usb.ids and with kernel-2.6.8.1.22mdk's usbmap
  o add "Pinnacle Systems, Inc.|Pinnacle Bungee (PAL)" (Stefan Siegel)

* Fri Nov 19 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.28-1mdk
- ALI SATA controllers:
  o fill in descriptions
  o fix duplicated entry

* Fri Nov 19 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.27-1mdk
- pcitable:
  o sync with:
    * ALSA-1.0.7 as in kernel-2.6.10-rc2-mm1
    * pci.ids from kernel-2.6.10-rc2-mm1
    * userland pci.ids
  o update/fill in ATI sound-cards description from ALSA sound driver
  o add two new controllers from ULI & VIA SATA controllers (from
    bk-sata)
- usbtable: add "Logitech Inc.|QuickCam Communicate" (Stefan Siegel)

* Wed Nov 17 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.26-1mdk
- sync with hwdata-0.147
- sync with latest usb.ids
- sync with latest pci.ids

* Wed Nov 17 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.25-1mdk
- pcitable:
  o sync with kernel-tmb-2.6.7-2.tmb.6mdk
  o sync with 2.8.10-rc1-mm5's libata & serial driver
  o fill driver field for EIDE/ATA controllers
  o s/3c90x/3c59x/ since the former is dead for years
  o fix a couble of bogus entries
	* lst/pcitable: sync with 2.8.10-rc1-mm5's

* Wed Nov 10 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.24-1mdk
- disambiguate media devices (eg: TV cards vs SAT cards)
- add I2C modules
- workaround sound on some VIA VT8233 (#10859)
- sync with pci.ids, hwdata-0.145 and kernel-2.6.8.1.21mdk
- use yenta_socket for PCI7420 CardBus Controller

* Fri Oct 29 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.23-1mdk
- add Philips Semiconductors DSL card (blino)
- use new megaraid_mbox for the following cards:
  + 0x1000 0x0408  "megaraid_mbox" "LSI Logic / Symbios Logic|MegaRAID"
  + 0x1000 0x0409  "megaraid_mbox" "LSI Logic / Symbios Logic|MegaRAID"
  + 0x1028 0x0013  "megaraid_mbox" "Dell|PowerEdge Expandable RAID controller 4"

* Fri Oct 29 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.22-1mdk
- add nVidia Quadro FX 1100 card ID
- add support for FreeBox v4 via USB link (buggy device make kernel
  failed to map usbnet to it) [ Thierry Vignaud ]

* Fri Oct 22 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.21-1mdk
- add nVidia Quadro FX 3400 PCI-Express card ID

* Tue Oct 12 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.20-1mdk
- speculatively use aic79xx for Adaptec ASC-39320[AB] cards

* Tue Oct 12 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.19-1mdk
- fix sound on one ensoniq sound card

* Wed Sep 29 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.18-1mdk
- added ath_pci entries

* Sat Sep 25 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.17-1mdk
- lst/usbtable: merged kernel 2.6.8.1.10mdk entries to be able to
 list them during install.
- lst/pcitable: o update ATI pciids (Nicolas)
                o add new NVidia 6800 (Nicolas)

* Wed Sep 15 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.16-6mdk
- fix some CAPI entries (blino)

* Wed Sep 15 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.16-5mdk
- add support for xDSL over CAPI (eg: AVM cards) (blino)
- add some Apple hardware (Christiaan Welvaar)
- sync pcitable with kernel-2.6.8.1.10mdk

* Thu Sep 09 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.16-4mdk
o pcitable:
	* added entries for slamr and rt2500
	* added entries for IPW2200
	* Intel Corporation => Intel Corp.
 o usbtable:
	* added slusb
	* added driver for NetGear MA111
	* put newhidups driver for MGE UPS entries.
	* fixed wacom entries.

* Wed Sep 01 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.16-3mdk
- pcitable:
  o sync with kernel-2.6.8.1.5mdk
  o switch one nForce2 from OSS to ALSA
  o in 2.6.x kernel, pwcd was splited between pcwd_pci and pcwd_usb
  o in both 2.4.x and 2.6.x kernels:
    * 3c359 replaced 3c559
    * donauboe replaced toshoboe
    * hw_random replaced both amd7xx_tco, amd768_rng and i810_rngb
    * pc300 replaced pc300too
    * tmspci replaced sktr
    * tulip replaced tulip_old (#10965)
  o remove bogus 0xffff 0xffff entry
  o introduce bt878
  o introduce sata_sx4 instead of sata_promise for one controller
  o fix a few wrong entries (according to kernel's pcimap):
    * one s/dmfe/tulip/
    * one s/qla2200/qla2100/
    * one s/tulip/de2104x/
    * one s/yenta_socket/i82092/
    * one s/yenta_socket/pd6729/

* Sat Aug 28 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.16-2mdk
- use 3w-9xxx for 3ware 9XXX-series ATA-RAID

* Fri Aug 27 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.16-1mdk
- usbtable: sync with kernel-2.6.8.1.1mdk (kernel-2.6.8.1.3mdk equals
  1mdk regarding pcitable & usbtable)
- switch Intel/ICH6 sound card from OSS to ALSA b/c of sound recording
  issues

* Thu Aug 19 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.15-1mdk
- sync pcitable with kernel-2.6.8.1.1mdk
- fill some empty strings (Erwan Velu)
- add support for several ati & nvidia gfx cards (greg)

* Thu Aug 05 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.14-1mdk
- usbtable: 
  o sync with kernel-2.6.8-0.rc2.2mdk
  o merge descriptions with usbutils

* Wed Aug 04 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.13-1mdk
- pcitable: 
  o merge with kernel-2.6.8-0.rc2.2mdk
  o merge with pciids.sf.net
  o update missing descriptions

* Fri Jul 30 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.12-1mdk
- usbtable: updated descriptions

* Tue Jul 27 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.11-1mdk
- monitor DB:
  o add a Princeton monitor (#2633)
  o add a LCD monitor (Sylvain Vignaud)
  o fix a typo
  o sync with rh's hwdata-0.123 (new monitors, ...)
  o increase a few DELL monitors frequency ranges (from hwdata-0.123)
  o remove a few old duplicated entries
- use b44 rather than bcm4400 (nicolas, #9742)
- use tg3 rather than bcm5700  (nicolas, #9742)
- add NVIDIA PCI-express 5750 Card Add Matrox P750 Add NVIDIA GO 5600 (greg)
- fix #8295 (no ADSL over Accton Ethernet card)

* Wed Jun 16 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.10-1mdk
- add madwifi_pci for 16c8 0013 (arnaud)
- add module yenta_socket for the 0x1217 0x7114 (arnaud)
- add slamr (slmodem) for 10b9 5457 (arnaud)
- adding usb modules for dell PE750 (erwan)
- CB1410 Cardbus Controller works with yenta_socket (arnaud)
- default to tg3 instead of bcm5700 for a few chip names (arnaud)
- list some cardbus controlers from pciids.sourceforge.net (arnaud)
- rename "NeoMagic (laptop/notebook)" to "NeoMagic MagicGraph
  (laptop/notebook)" (pixel) (#4686)

* Tue May 25 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.9-16mdk
- Add Quadro FX 1300 entry
- Fix module loading initio -> a100u2w (nicolas)
- Updating cciss & cpqarray pci ids (erwan)
- Adding some aacraid missing entries (erwan)
- pcitable: remove the few remaining "Server:SVGA" since we don't have XF3 anymore (Pixel)
- Cards+: drop XFree3 related data (Pixel)

* Tue Apr 27 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.9-15mdk
- add Tatung C7BZR monitor specs
- revert GeForce FX 5700 change as XFree86 4.3 "nv" driver doesn't get it right
- sync with kernel-2.6.3-10mdk and rh's hwdata-0.117 (tv)

* Sat Apr 17 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.9-14mdk
- add "iteraid" (IT8212) controller
- fix GeForce FX 5700/5950, Quadro FX 1100 entries
- fix empty strings (Erwan)
- add a new samsung monitor (Alojz Stanich)
- GeForce 4 => FX (cosmetic change from Thierry)
