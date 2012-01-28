#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	multigl		# package libGL in a way allowing concurrent install with nvidia/fglrx drivers

%define		x11ver		xpic

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%ifarch %{ix86}
%define		arch_sufix	%{nil}
%define		arch_dir	x86
%else
%define		arch_sufix	_64a
%define		arch_dir	x86_64
%endif

%define		rel	3
%define		pname		xorg-driver-video-fglrx
Summary:	Linux Drivers for AMD/ATI graphics accelerators
Summary(pl.UTF-8):	Sterowniki do akceleratorów graficznych AMD/ATI
Name:		%{pname}
Version:	12.1
Release:	%{rel}%{?with_multigl:.mgl}
Epoch:		1
License:	AMD Binary (parts are GPL)
Group:		X11
Source0:	http://dlmdownloads.ati.com/drivers/linux/amd-driver-installer-%(echo %{version} | tr . -)-x86.x86_64.run
# Source0-md5:	6396d0f6f70b89d605bac896feb2b7c9
Source1:	atieventsd.init
Source2:	atieventsd.sysconfig
Source3:	gl.pc.in
Source4:	10-fglrx.conf
Patch0:		%{pname}-kh.patch
Patch1:		%{pname}-smp.patch
Patch2:		%{pname}-x86genericarch.patch
Patch3:		%{pname}-desktop.patch
Patch4:		%{pname}-nofinger.patch
Patch5:		%{pname}-GPL-only.patch
Patch6:		%{pname}-WARN.patch
Patch7:		%{pname}-kernel-fpu.patch
URL:		http://ati.amd.com/support/drivers/linux/linux-radeon.html
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	sed >= 4.0
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Requires:	xorg-xserver-server
Requires:	xorg-xserver-server(videodrv-abi) <= 11.0
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0
Suggests:	%{name}-config
Suggests:	kernel-video-firegl
Provides:	xorg-driver-video
Provides:	xorg-xserver-module(glx)
Obsoletes:	X11-driver-firegl < 1:7.0.0
Obsoletes:	XFree86-driver-firegl < 1:7.0.0
Obsoletes:	xorg-driver-video-fglrx-libdri
Obsoletes:	xorg-driver-video-fglrx-libglx
%if %{without multigl}
Conflicts:	xorg-driver-video-nvidia
Conflicts:	xorg-xserver-libglx
%endif
ExclusiveArch:	i586 i686 athlon pentium3 pentium4 %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ccver	%(rpm -q --qf "%{VERSION}" gcc | sed 's/\\..*//')

%define		_noautoreqdep			libGL.so.1
%define		no_install_post_check_so	1

%description
Display driver files for the ATI Radeon 8500, 9700, Mobility M9 and
the FireGL 8700/8800, E1, Z1/X1 graphics accelerators. This package
provides 2D display drivers and hardware accelerated OpenGL.

%description -l pl.UTF-8
Sterowniki do kart graficznych ATI Radeon 8500, 9700, Mobility M9 oraz
graficznych akceleratorów FireGL 8700/8800, E1, Z1/X1. Pakiet
dostarcza sterowniki obsługujące wyświetlanie 2D oraz sprzętowo
akcelerowany OpenGL.

%package libs
Summary:	OpenGL (GL and GLX) ATI/AMD libraries
Summary(pl.UTF-8):	Biblioteki OpenGL (GL i GLX) ATI/AMD
Group:		X11/Development/Libraries
Requires(post,postun):	/sbin/ldconfig
# 4.0 for Radeon HD 5000 Series
Provides:	OpenGL = 3.3
Provides:	OpenGL-GLX = 1.4
%if %{without multigl}
Obsoletes:	Mesa
Conflicts:	Mesa-libGL
%endif
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
Requires:	%{pname}-devel = %{epoch}:%{version}-%{release}

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

%package config
Summary:	Xorg configuration file to use fglrx module
Summary(pl.UTF-8):	Plik konfiguracyjny modułu fglrx dla Xorg
Group:		X11
Requires:	%{name} = %{epoch}:%{version}-%{rel}

%description config
Without configuration file Xorg doesn't use fglrx module. If you want
to use it you should install this package or create own configuration
file.

%description config -l pl.UTF-8
Bez odpowiedniej konfiguracji Xorg nie będzie używał modułu fglrx. Aby
to umożliwić należy zainstalować tą paczkę lub stworzyć własny plik
konfiguracyjny.

%package -n kernel%{_alt_kernel}-video-firegl
Summary:	ATI kernel module for FireGL support
Summary(pl.UTF-8):	Moduł jądra oferujący wsparcie dla ATI FireGL
Release:	%{rel}@%{_kernel_ver_str}
License:	ATI
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
%if "%{_alt_kernel}" != "%{nil}"
Provides:	kernel-video-firegl = %{epoch}:%{version}-%{rel}@%{_kernel_ver_str}
%endif
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-video-firegl
ATI kernel module for FireGL support.

%description -n kernel%{_alt_kernel}-video-firegl -l pl.UTF-8
Moduł jądra oferujący wsparcie dla ATI FireGL.

%prep
%setup -q -c -T

sh %{SOURCE0} --extract .

cp arch/%{arch_dir}/lib/modules/fglrx/build_mod/* common/lib/modules/fglrx/build_mod

%if %{with dist_kernel}
%patch0 -p1
%patch1 -p0
%patch2 -p0
%endif
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0
%patch7 -p0

install -d common{%{_prefix}/{%{_lib},bin,sbin},/etc}
cp -r %{x11ver}%{arch_sufix}/usr/X11R6/%{_lib}/* common%{_libdir}
mv common%{_libdir}/modules/extensions/{fglrx/fglrx-libglx.so,libglx.so}
cp -r arch/%{arch_dir}/usr/X11R6/%{_lib}/* common%{_libdir}
cp -r arch/%{arch_dir}/usr/X11R6/%{_lib}/modules common%{_libdir}/xorg
cp -r arch/%{arch_dir}/usr/X11R6/bin/* common%{_bindir}
cp -r arch/%{arch_dir}/usr/bin/* common%{_bindir}
cp -r arch/%{arch_dir}/usr/sbin/* common%{_sbindir}
cp -r arch/%{arch_dir}/usr/%{_lib}/*.so* common%{_libdir}
mv common%{_libdir}/{fglrx/fglrx-libGL.so.1.2,libGL.so.1.2}
cp -r arch/%{arch_dir}/etc/* common/etc

%build
%if %{with kernel}
cd common/lib/modules/fglrx/build_mod
cp -f 2.6.x/Makefile .
%build_kernel_modules -c -m fglrx GCC_VER_MAJ=%{_ccver}
cd -
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m common/lib/modules/fglrx/build_mod/fglrx -d misc
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{ati,env.d,X11/xorg.conf.d},%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_datadir}/ati,%{_mandir}/man8} \
	$RPM_BUILD_ROOT{%{_libdir}/xorg/modules,%{_includedir}/{X11/extensions,GL}} \
	$RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atieventsd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/atieventsd
install %{SOURCE4} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
cp -r common%{_datadir}/doc/fglrx/examples/etc/acpi $RPM_BUILD_ROOT/etc
install -p common/etc/OpenCL/vendors/*.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors

install common%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}
install common/usr/X11R6/bin/* $RPM_BUILD_ROOT%{_bindir}
install common%{_sbindir}/* $RPM_BUILD_ROOT%{_sbindir}

rm $RPM_BUILD_ROOT%{_sbindir}/atigetsysteminfo.sh

cp -r common%{_libdir}/modules/* $RPM_BUILD_ROOT%{_libdir}/xorg/modules
ln -s %{_libdir}/xorg/modules/dri $RPM_BUILD_ROOT%{_libdir}
cp -r common%{_sysconfdir}/ati/control $RPM_BUILD_ROOT%{_sysconfdir}/ati/control
cp -r common%{_sysconfdir}/ati/signature $RPM_BUILD_ROOT%{_sysconfdir}/ati/signature
cp -r common%{_sysconfdir}/ati/amdpcsdb.default $RPM_BUILD_ROOT%{_sysconfdir}/ati/amdpcsdb.default
cp -r common%{_sysconfdir}/ati/atiogl.xml $RPM_BUILD_ROOT%{_sysconfdir}/ati/atiogl.xml

cp -r common%{_datadir}/ati/* $RPM_BUILD_ROOT%{_datadir}/ati
cp -r common%{_datadir}/icons/*.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

cp -r common%{_desktopdir}/*.desktop $RPM_BUILD_ROOT%{_desktopdir}

cp -r common%{_mandir}/man8/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%if %{with multigl}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ld.so.conf.d,%{_libdir}/fglrx}

echo %{_libdir}/fglrx >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/fglrx.conf

cp -r common%{_libdir}/lib*.a $RPM_BUILD_ROOT%{_libdir}
cp -r common%{_libdir}/lib*.so* $RPM_BUILD_ROOT%{_libdir}/fglrx
cp -r common%{_libdir}/lib*.cap $RPM_BUILD_ROOT%{_libdir}/fglrx

mv -f $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/{libglx.so,libglx.so.%{version}}
ln -sf libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/libglx.so

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/fglrx
ln -sf fglrx/libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so
%else
cp -r common%{_libdir}/lib* $RPM_BUILD_ROOT%{_libdir}

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so
%endif

install common%{_includedir}/GL/*.h $RPM_BUILD_ROOT%{_includedir}/GL
#install common/usr/X11R6/include/X11/extensions/*.h $RPM_BUILD_ROOT%{_includedir}/X11/extensions
echo "LIBGL_DRIVERS_PATH=%{_libdir}/xorg/modules/dri" > $RPM_BUILD_ROOT%{_sysconfdir}/env.d/LIBGL_DRIVERS_PATH

cd $RPM_BUILD_ROOT%{_libdir}
for f in libfglrx_dm; do
%if %{with multigl}
	ln -s fglrx/$f.so.*.* $f.so
%else
	ln -s $f.so.*.* $f.so
%endif
done
%endif

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__sed} -e 's|@@prefix@@|%{_prefix}|g;s|@@libdir@@|%{_libdir}|g;s|@@includedir@@|%{_includedir}|g;s|@@version@@|%{version}|g' < %{SOURCE3} \
	> $RPM_BUILD_ROOT%{_pkgconfigdir}/gl.pc

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with multigl}
%post
if [ ! -e %{_libdir}/xorg/modules/extensions/libglx.so ]; then
	ln -sf libglx.so.%{version} %{_libdir}/xorg/modules/extensions/libglx.so
fi
%endif

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

%post	-n kernel%{_alt_kernel}-video-firegl
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-video-firegl
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc LICENSE.TXT common%{_docdir}/fglrx/*.html common%{_docdir}/fglrx/articles common%{_docdir}/fglrx/user-manual
%dir %{_sysconfdir}/ati
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/control
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/signature
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/amdpcsdb.default
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/atiogl.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/env.d/LIBGL_DRIVERS_PATH
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/amdnotifyui
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.xpm
%{_datadir}/ati
%if %{with multigl}
%ghost %{_libdir}/xorg/modules/extensions/libglx.so
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/libglx.so.%{version}
%else
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/libglx.so
%endif
%{_libdir}/dri
%attr(755,root,root) %{_libdir}/xorg/modules/dri/fglrx_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/fglrx_drv.so
%dir %{_libdir}/xorg/modules/linux
%attr(755,root,root) %{_libdir}/xorg/modules/linux/libfglrxdrm.so
%attr(755,root,root) %{_libdir}/xorg/modules/amdxmm.so
%attr(755,root,root) %{_libdir}/xorg/modules/glesx.so

%files libs
%defattr(644,root,root,755)
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%{_sysconfdir}/OpenCL/vendors/*.icd
%if %{with multigl}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/fglrx.conf
%dir %{_libdir}/fglrx
%attr(755,root,root) %{_libdir}/fglrx/libAMDXvBA.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libAMDXvBA.so.1
%attr(755,root,root) %{_libdir}/fglrx/libOpenCL.so.1
%attr(755,root,root) %{_libdir}/fglrx/libSlotMaximizerAg.so
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/fglrx/libSlotMaximizerBe.so
%endif
%attr(755,root,root) %{_libdir}/fglrx/libXvBAW.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libXvBAW.so.1
%{_libdir}/fglrx/libAMDXvBA.cap
%attr(755,root,root) %{_libdir}/fglrx/libamdocl*.so
%attr(755,root,root) %{_libdir}/fglrx/libatiadlxx.so
%attr(755,root,root) %{_libdir}/fglrx/libaticalcl.so
%attr(755,root,root) %{_libdir}/fglrx/libaticaldd.so
%attr(755,root,root) %{_libdir}/fglrx/libaticalrt.so
%attr(755,root,root) %{_libdir}/fglrx/libatiuki.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libGL.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libGL.so.1
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_dm.so.*.*
%else
%attr(755,root,root) %{_libdir}/libAMDXvBA.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libAMDXvBA.so.1
%attr(755,root,root) %{_libdir}/libOpenCL.so.1
%attr(755,root,root) %{_libdir}/libSlotMaximizerAg.so
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/libSlotMaximizerBe.so
%endif
%attr(755,root,root) %{_libdir}/libXvBAW.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libXvBAW.so.1
%{_libdir}/libAMDXvBA.cap
%attr(755,root,root) %{_libdir}/libamdocl*.so
%attr(755,root,root) %{_libdir}/libatiadlxx.so
%attr(755,root,root) %{_libdir}/libaticalcl.so
%attr(755,root,root) %{_libdir}/libaticaldd.so
%attr(755,root,root) %{_libdir}/libaticalrt.so
%attr(755,root,root) %{_libdir}/libatiuki.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libatiuki.so.1
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGL.so.1
%attr(755,root,root) %{_libdir}/libGL.so
%attr(755,root,root) %{_libdir}/libfglrx_dm.so.*.*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfglrx_dm.so
%{_includedir}/GL
%if %{with multigl}
%attr(755,root,root) %{_libdir}/libGL.so
%endif
%{_pkgconfigdir}/gl.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfglrx_dm.a

%files atieventsd
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/atieventsd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/atieventsd
%attr(755,root,root) %{_sbindir}/atieventsd
%attr(755,root,root) %{_sysconfdir}/acpi/ati-powermode.sh
%{_sysconfdir}/acpi/events/*
%{_mandir}/man8/atieventsd.8*

%files config
%defattr(644,root,root,755)
%{_sysconfdir}/X11/xorg.conf.d/10-fglrx.conf
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-firegl
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
