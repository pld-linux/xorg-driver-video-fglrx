# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%bcond_with	verbose		# verbose build (V=1)

%define		x11ver		xpic

%if %{without kernel}
%undefine	with_dist_kernel
%endif

# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%undefine	with_userspace
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%ifarch %{ix86}
%define		arch_sufix	%{nil}
%define		arch_dir	x86
%else
%define		arch_sufix	_64a
%define		arch_dir	x86_64
%endif

%define		intver		14.10.1006
%define		betaver		1.3
#define		rel		0.beta%{betaver}.3

%define		rel		3
%define		pname		xorg-driver-video-fglrx
Summary:	Linux Drivers for AMD/ATI graphics accelerators
Summary(pl.UTF-8):	Sterowniki do akceleratorów graficznych AMD/ATI
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	14.4
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
Epoch:		1
License:	AMD Binary (parts are GPL)
Group:		X11
# http://support.amd.com/ click through "download drivers", desktop -> radeon hd -> 7xxx -> linux
#Source0:	http://www2.ati.com/drivers/linux/amd-catalyst-%{version}-linux-x86.x86_64.zip
#Source0:	amd-catalyst-%{version}-betav%{betaver}-linux-x86.x86_64.zip
%define		vver	%(echo %{version} | tr . -)
Source0:	amd-catalyst-%{vver}-linux-x86-x86-64.zip
# Source0-md5:	00c2677c7b32520c2440b869ab34e660
Source1:	atieventsd.init
Source2:	atieventsd.sysconfig
Source3:	gl.pc.in
Source4:	10-fglrx.conf
Source5:	10-fglrx-modules.conf
Patch0:		%{pname}-kh.patch
Patch1:		%{pname}-smp.patch
Patch2:		%{pname}-x86genericarch.patch
Patch3:		%{pname}-desktop.patch
Patch4:		%{pname}-nofinger.patch
Patch5:		%{pname}-GPL-only.patch
Patch7:		%{pname}-kernel-fpu.patch
Patch8:		linux-3.14.patch
URL:		http://ati.amd.com/support/drivers/linux/linux-radeon.html
%{?with_dist_kernel:%{expand:%kbrs}}
BuildRequires:	rpmbuild(macros) >= 1.678
BuildRequires:	sed >= 4.0
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Requires:	xorg-xserver-server
Requires:	xorg-xserver-server(videodrv-abi) <= 15.0
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0
Suggests:	kernel-video-firegl
Provides:	xorg-driver-video
Provides:	xorg-xserver-module(glx)
Obsoletes:	X11-driver-firegl < 1:7.0.0
Obsoletes:	XFree86-driver-firegl < 1:7.0.0
Obsoletes:	xorg-driver-video-fglrx-config
Obsoletes:	xorg-driver-video-fglrx-libdri
Obsoletes:	xorg-driver-video-fglrx-libglx
ExclusiveArch:	i586 i686 athlon pentium3 pentium4 %{x8664}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

%define		_ccver	%(rpm -q --qf "%{VERSION}" gcc | sed 's/\\..*//')

%define		_noautoreqdep			libGL.so.1
%define		no_install_post_check_so	1

%description
AMD display driver which allows for hardware accelerated rendering
with ATI Mobility, FireGL and Desktop GPUs. Some of the Desktop and
Mobility GPUs supported are the Radeon HD 5xxx series to the
Radeon HD 7xxx series.

%description -l pl.UTF-8
Sterownik AMD umożliwiający sprzętowo akcelerowany rendering do kart
graficznych ATI Mobility, FireGL i Desktopowych. Niektóre ze
wspieranych Desktopowych i Mobilnych kart to Radeon HD 5xxx do
Radeon HD 7xxx.

%package libs
Summary:	OpenGL (GL and GLX) ATI/AMD libraries
Summary(pl.UTF-8):	Biblioteki OpenGL (GL i GLX) ATI/AMD
Group:		X11/Development/Libraries
Requires(post,postun):	/sbin/ldconfig
# 4.0 for Radeon HD 5000 Series
Provides:	OpenGL = 3.3
Provides:	OpenGL-GLX = 1.4
Obsoletes:	X11-OpenGL-core < 1:7.0.0
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-core < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0

%description libs
ATI/AMD OpenGL (GL and GLX only) implementation libraries.

%description libs -l pl.UTF-8
Implementacja OpenGL (tylko GL i GLX) firmy ATI/AMD.

%package devel
Summary:	Header files for development for the ATI Radeon cards proprietary driver
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania z użyciem własnościowego sterownika dla kart ATI Radeon
Group:		X11/Development/Libraries
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
# or more?
Requires:	xorg-proto-glproto-devel
# 4.0 for Radeon HD 5000 Series
Provides:	OpenGL-GLX-devel = 1.4
Provides:	OpenGL-devel = 3.3
Obsoletes:	X11-OpenGL-devel-base
Obsoletes:	XFree86-OpenGL-devel-base

%description devel
Header files for development for the ATI proprietary driver for ATI
Radeon graphic cards.

%description devel -l pl.UTF-8
Pliki nagłówkowe do programowania z użyciem własnościowego sterownika
ATI dla kart graficznych Radeon.

%package static
Summary:	Static libraries for development for the ATI Radeon cards proprietary driver
Summary(pl.UTF-8):	Biblioteki statyczne do programowania z użyciem własnościowego sterownika dla kart ATI Radeon
Group:		X11/Development/Libraries
Requires:	%{pname}-devel = %{epoch}:%{version}-%{rel}

%description static
Static libraries for development for the ATI proprietary driver for
ATI Radeon graphic cards.

%description static -l pl.UTF-8
Biblioteki statyczne do programowania z użyciem własnościowego
sterownika ATI dla kart graficznych ATI Radeon.

%package atieventsd
Summary:	ATI external events daemon
Summary(pl.UTF-8):	Demon zewnętrznych zdarzeń ATI
Group:		Daemons
Requires:	%{pname} = %{epoch}:%{version}-%{rel}
Requires:	acpid
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description atieventsd
The ATI External Events Daemon is a user-level application that
monitors various system events such as ACPI or hotplug, then notifies
the driver via the X extensions interface that the event has occured.

%description atieventsd -l pl.UTF-8
Demon zewnętrznych zdarzeń ATI jest aplikacją monitorującą różne
zdarzenia systemowe, takie jak ACPI lub hotplug, a następnie
informującą sterownik poprzez interfejs rozszerzeń X, że zaszło
zdarzenie.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-video-firegl\
Summary:	ATI kernel module for FireGL support\
Summary(pl.UTF-8):	Moduł jądra oferujący wsparcie dla ATI FireGL\
Release:	%{rel}@%{_kernel_ver_str}\
License:	ATI\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%if %{with dist_kernel}\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
%endif\
Provides:	kernel%{_alt_kernel}-video-firegl = %{epoch}:%{version}-%{rel}@%{_kernel_ver_str}\
\
%description -n kernel%{_alt_kernel}-video-firegl\
ATI kernel module for FireGL support.\
\
%description -n kernel%{_alt_kernel}-video-firegl -l pl.UTF-8\
Moduł jądra oferujący wsparcie dla ATI FireGL.\
\
%if %{with kernel}\
%files -n kernel%{_alt_kernel}-video-firegl\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/misc/*.ko*\
%endif\
\
%post	-n kernel%{_alt_kernel}-video-firegl\
%depmod %{_kernel_ver}\
\
%postun -n kernel%{_alt_kernel}-video-firegl\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
cp -pf common/lib/modules/fglrx/build_mod/2.6.x/Makefile common/lib/modules/fglrx/build_mod\
%build_kernel_modules -C common/lib/modules/fglrx/build_mod -m fglrx GCC_VER_MAJ=%{_ccver}\
%install_kernel_modules -D installed -m common/lib/modules/fglrx/build_mod/fglrx -d misc\
%{nil}

%{?with_kernel:%{expand:%kpkg}}

%prep
#%setup -q -c -T
%setup -q -c
#sh %{SOURCE0} --extract .
#sh amd-catalyst-%{version}-linux-x86.x86_64.run --extract .
cd fglrx-%{intver}
sh amd-driver-installer-%{intver}-x86.x86_64.run --extract .

cp -p arch/%{arch_dir}/lib/modules/fglrx/build_mod/* common/lib/modules/fglrx/
cat >>common/lib/modules/fglrx/build_mod/2.6.x/Makefile <<EOF
\$(M)/libfglrx_ip.a:
	ln -s \$(LIBIP_PREFIX)/libfglrx_ip.a \$(M)
EOF

%if %{with dist_kernel}
%patch0 -p1
%patch1 -p0
%patch2 -p0
%endif
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch7 -p0
%patch8 -p0

install -d common{%{_prefix}/{%{_lib},bin,sbin},/etc}
cp -a %{x11ver}%{arch_sufix}/usr/X11R6/%{_lib}/* common%{_libdir}
mv common%{_libdir}/modules/extensions/{fglrx/fglrx-libglx.so,libglx.so}
cp -a arch/%{arch_dir}/usr/X11R6/%{_lib}/* common%{_libdir}
cp -a arch/%{arch_dir}/usr/X11R6/%{_lib}/modules common%{_libdir}/xorg
cp -a arch/%{arch_dir}/usr/X11R6/bin/* common%{_bindir}
cp -a arch/%{arch_dir}/usr/bin/* common%{_bindir}
cp -a arch/%{arch_dir}/usr/sbin/* common%{_sbindir}
cp -a arch/%{arch_dir}/usr/%{_lib}/*.so* common%{_libdir}
mv common%{_libdir}/{fglrx/fglrx-libGL.so.1.2,libGL.so.1.2}
cp -a arch/%{arch_dir}/etc/* common/etc

%build
cd fglrx-%{intver}
%{?with_kernel:%{expand:%bkpkg}}

%install
rm -rf $RPM_BUILD_ROOT

cd fglrx-%{intver}

%if %{with kernel}
install -d $RPM_BUILD_ROOT
cp -a installed/* $RPM_BUILD_ROOT
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{ati,env.d,X11/xorg.conf.d,ld.so.conf.d} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_includedir}/GL} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_datadir}/ati,%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_libdir}/{fglrx,xorg/modules/extensions/fglrx} \
	$RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atieventsd
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/atieventsd

cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
cp -p %{SOURCE5} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
sed -i -e 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/10-fglrx-modules.conf

cp -a common%{_datadir}/doc/fglrx/examples/etc/acpi $RPM_BUILD_ROOT/etc
install -p common/etc/OpenCL/vendors/*.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors

install -p common%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}
install -p common/usr/X11R6/bin/* $RPM_BUILD_ROOT%{_bindir}
install -p common%{_sbindir}/* $RPM_BUILD_ROOT%{_sbindir}

rm $RPM_BUILD_ROOT%{_sbindir}/atigetsysteminfo.sh

cp -a common%{_libdir}/modules/* $RPM_BUILD_ROOT%{_libdir}/xorg/modules
ln -s %{_libdir}/xorg/modules/dri $RPM_BUILD_ROOT%{_libdir}
cp -a common%{_sysconfdir}/ati/control $RPM_BUILD_ROOT%{_sysconfdir}/ati/control
cp -a common%{_sysconfdir}/ati/signature $RPM_BUILD_ROOT%{_sysconfdir}/ati/signature
cp -a common%{_sysconfdir}/ati/amdpcsdb.default $RPM_BUILD_ROOT%{_sysconfdir}/ati/amdpcsdb.default

cp -a common%{_datadir}/ati/* $RPM_BUILD_ROOT%{_datadir}/ati
cp -a common%{_datadir}/icons/*.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

cp -r common%{_desktopdir}/*.desktop $RPM_BUILD_ROOT%{_desktopdir}

cp -a common%{_mandir}/man8/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%ifarch %{x8664}
echo %{_libdir}/fglrx > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/fglrx64.conf
%else
echo %{_libdir}/fglrx > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/fglrx.conf
%endif

cp -a common%{_libdir}/lib* $RPM_BUILD_ROOT%{_libdir}/fglrx

mv -f $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/{,fglrx}/libglx.so

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/fglrx
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/fglrx/libGL.so
(cd $RPM_BUILD_ROOT%{_libdir}/fglrx ; ln -sf libfglrx_dm.so.*.* libfglrx_dm.so)

cp -p common%{_includedir}/GL/*.h $RPM_BUILD_ROOT%{_includedir}/GL
echo "LIBGL_DRIVERS_PATH=%{_libdir}/xorg/modules/dri" > $RPM_BUILD_ROOT%{_sysconfdir}/env.d/LIBGL_DRIVERS_PATH

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__sed} -e 's|@@prefix@@|%{_prefix}|g;s|@@libdir@@|%{_libdir}|g;s|@@includedir@@|%{_includedir}|g;s|@@version@@|%{version}|g' < %{SOURCE3} \
	> $RPM_BUILD_ROOT%{_pkgconfigdir}/gl.pc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post atieventsd
/sbin/chkconfig --add atieventsd
%service atieventsd restart

%preun atieventsd
if [ "$1" = "0" ]; then
	%service -q atieventsd stop
	/sbin/chkconfig --del atieventsd
fi

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc fglrx-%{intver}/{LICENSE.TXT,common%{_docdir}/fglrx/*.html,common%{_docdir}/fglrx/articles,common%{_docdir}/fglrx/user-manual}
%dir %{_sysconfdir}/ati
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/control
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/signature
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/amdpcsdb.default
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/env.d/LIBGL_DRIVERS_PATH
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/amdnotifyui
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.xpm
%{_datadir}/ati
%dir %{_libdir}/xorg/modules/extensions/fglrx
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/fglrx/libglx.so
%{_libdir}/dri
%attr(755,root,root) %{_libdir}/xorg/modules/dri/fglrx_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/fglrx_drv.so
%dir %{_libdir}/xorg/modules/linux
%attr(755,root,root) %{_libdir}/xorg/modules/linux/libfglrxdrm.so
%attr(755,root,root) %{_libdir}/xorg/modules/amdxmm.so
%attr(755,root,root) %{_libdir}/xorg/modules/glesx.so
%{_sysconfdir}/X11/xorg.conf.d/10-fglrx.conf
%{_sysconfdir}/X11/xorg.conf.d/10-fglrx-modules.conf

%files libs
%defattr(644,root,root,755)
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%{_sysconfdir}/OpenCL/vendors/*.icd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/fglrx*.conf
%dir %{_libdir}/fglrx
%attr(755,root,root) %{_libdir}/fglrx/libAMDXvBA.so.*.*
%attr(755,root,root) %ghost %{_libdir}/fglrx/libAMDXvBA.so.1
%attr(755,root,root) %{_libdir}/fglrx/libOpenCL.so.1
%attr(755,root,root) %{_libdir}/fglrx/libXvBAW.so.*.*
%attr(755,root,root) %ghost %{_libdir}/fglrx/libXvBAW.so.1
%{_libdir}/fglrx/libAMDXvBA.cap
%attr(755,root,root) %{_libdir}/fglrx/libamdocl*.so
%attr(755,root,root) %{_libdir}/fglrx/libatiadlxx.so
%attr(755,root,root) %{_libdir}/fglrx/libaticalcl.so
%attr(755,root,root) %{_libdir}/fglrx/libaticaldd.so
%attr(755,root,root) %{_libdir}/fglrx/libaticalrt.so
%attr(755,root,root) %{_libdir}/fglrx/libatiuki.so.*.*
%attr(755,root,root) %ghost %{_libdir}/fglrx/libatiuki.so.1
%attr(755,root,root) %{_libdir}/fglrx/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/fglrx/libGL.so.1
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_dm.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_dm.so
%attr(755,root,root) %{_libdir}/fglrx/libGL.so
%{_includedir}/GL
%{_pkgconfigdir}/gl.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/fglrx/libfglrx_dm.a

%files atieventsd
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/atieventsd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/atieventsd
%attr(755,root,root) %{_sbindir}/atieventsd
%attr(755,root,root) %{_sysconfdir}/acpi/ati-powermode.sh
%{_sysconfdir}/acpi/events/*
%{_mandir}/man8/atieventsd.8*
%endif
