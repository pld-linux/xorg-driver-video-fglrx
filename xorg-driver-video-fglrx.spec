# TODO:
# - prepare libglx and libdri for multigl (possible only using separate X-server instances)
# - merge libglx and libdri back into driver package?
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	multigl		# package libGL in a way allowing concurrent install with nvidia/fglrx drivers

%define		x11ver		x740

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

%define		rel	3.1
%define		pname		xorg-driver-video-fglrx
Summary:	Linux Drivers for ATI graphics accelerators
Summary(pl.UTF-8):	Sterowniki do akceleratorów graficznych ATI
Name:		%{pname}%{_alt_kernel}
Version:	8.12
Release:	%{rel}%{?with_multigl:.mgl}
Epoch:		1
License:	ATI Binary (parts are GPL)
Group:		X11
Source0:	http://dlmdownloads.ati.com/drivers/linux/ati-driver-installer-8-12-x86.x86_64.run
# Source0-md5:	2a62d8c5173f091379e458371782a580
Source1:	%{pname}.desktop
Patch0:		%{pname}-kh.patch
Patch1:		%{pname}-smp.patch
URL:		http://ati.amd.com/support/drivers/linux/linux-radeon.html
%{?with_userspace:BuildRequires:	OpenGL-GLU-devel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
%{?with_userspace:BuildRequires:	qt-devel}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-recordproto-devel
BuildRequires:	xorg-proto-xf86miscproto-devel
BuildRequires:	xorg-proto-xf86vidmodeproto-devel
Requires:	%{pname}-libdri = %{epoch}:%{version}-%{release}
Requires:	%{pname}-libglx = %{epoch}:%{version}-%{release}
Requires:	xorg-xserver-server
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0
Requires:	xorg-xserver-server(videodrv-abi) <= 4.1
Provides:	OpenGL = 2.0
Provides:	OpenGL-GLX = 1.4
# hack to make OpenGL ABI compatible
%ifarch %{x8664}
Provides:	libGL.so.1()(64bit)
%else
Provides:	libGL.so.1
%endif
%if !%{with multigl}
Obsoletes:	Mesa
Conflicts:	Mesa-libGL
%endif
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	X11-driver-firegl < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-driver-firegl < 1:7.0.0
# Fallback:
Suggests:	Mesa-dri-driver-swrast
ExclusiveArch:	i586 i686 athlon pentium3 pentium4 %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ccver	%(rpm -q --qf "%{VERSION}" gcc | sed 's/\\..*//')

%define		_noautoreqdep	libGL.so.1

%description
Display driver files for the ATI Radeon 8500, 9700, Mobility M9 and
the FireGL 8700/8800, E1, Z1/X1 graphics accelerators. This package
provides 2D display drivers and hardware accelerated OpenGL.

%description -l pl.UTF-8
Sterowniki do kart graficznych ATI Radeon 8500, 9700, Mobility M9 oraz
graficznych akceleratorów FireGL 8700/8800, E1, Z1/X1. Pakiet
dostarcza sterowniki obsługujące wyświetlanie 2D oraz sprzętowo
akcelerowany OpenGL.

%package libdri
Summary:	DRI extension library for X.org server with fglrx driver
Summary(pl.UTF-8):	Biblioteka rozszerzenia DRI dla serwera X.org ze sterownikiem fglrx
Group:		X11/Servers
Provides:	xorg-xserver-module(dri)
Conflicts:	xorg-driver-video-nvidia
Conflicts:	xorg-xserver-libdri

%description libdri
DRI extension library for X.org server with fglrx driver.

%description libdri -l pl.UTF-8
Biblioteka rozszerzenia DRI dla serwera X.org with fglrx driver.

%package libglx
Summary:	GLX extension library for X.org server with fglrx driver
Summary(pl.UTF-8):	Biblioteka rozszerzenia GLX dla serwera X.org ze sterownikiem fglrx
Group:		X11/Servers
Provides:	xorg-xserver-module(glx)
Conflicts:	xorg-driver-video-nvidia
Conflicts:	xorg-xserver-libglx

%description libglx
GLX extension library for X.org server with fglrx driver.

%description libglx -l pl.UTF-8
Biblioteka rozszerzenia GLX dla serwera X.org with fglrx driver.

%package devel
Summary:	Header files for development for the ATI Radeon cards proprietary driver
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania z użyciem własnościowego sterownika dla kart ATI Radeon
Group:		X11/Development/Libraries
Requires:	%{pname} = %{epoch}:%{version}-%{release}
# or more?
Requires:	xorg-proto-glproto-devel

%description devel
Header files for development for the ATI proprietary driver for
ATI Radeon graphic cards.

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

%package -n kernel%{_alt_kernel}-video-firegl
Summary:	ATI kernel module for FireGL support
Summary(pl.UTF-8):	Moduł jądra oferujący wsparcie dla ATI FireGL
Release:	%{rel}@%{_kernel_ver_str}
License:	ATI
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-video-firegl
ATI kernel module for FireGL support.

%description -n kernel%{_alt_kernel}-video-firegl -l pl.UTF-8
Moduł jądra oferujący wsparcie dla ATI FireGL.

%prep
%setup -q -c -T

sh %{SOURCE0} --extract .

cp arch/%{arch_dir}/lib/modules/fglrx/build_mod/* common/lib/modules/fglrx/build_mod

cd common
%if %{with dist_kernel}
%patch0 -p2
%patch1 -p0
%endif
cd -

install -d common%{_prefix}/{%{_lib},bin,sbin}
cp -r %{x11ver}%{arch_sufix}/usr/X11R6/%{_lib}/* common%{_libdir}
cp -r arch/%{arch_dir}/usr/X11R6/%{_lib}/* common%{_libdir}
cp -r arch/%{arch_dir}/usr/X11R6/bin/* common%{_bindir}
cp -r arch/%{arch_dir}/usr/sbin/* common%{_sbindir}

%build
%if %{with kernel}
cd common/lib/modules/fglrx/build_mod
cp -f 2.6.x/Makefile .
%build_kernel_modules -m fglrx GCC_VER_MAJ=%{_ccver}
cd -
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m common/lib/modules/fglrx/build_mod/fglrx -d misc
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{ati,env.d},%{_bindir},%{_sbindir},%{_pixmapsdir},%{_desktopdir},%{_datadir}/ati,%{_libdir}/xorg/modules,%{_includedir}/{X11/extensions,GL}}

install common%{_bindir}/{amdcccle,aticonfig,atiodcli,atiode,fgl_glxgears,fglrx_xgamma,fglrxinfo} \
	$RPM_BUILD_ROOT%{_bindir}
install common%{_sbindir}/{amdnotifyui,atieventsd} \
	$RPM_BUILD_ROOT%{_sbindir}
cp -r common%{_libdir}/modules/* $RPM_BUILD_ROOT%{_libdir}/xorg/modules
cp -r common%{_sysconfdir}/ati/control $RPM_BUILD_ROOT%{_sysconfdir}/ati/control
cp -r common%{_sysconfdir}/ati/signature $RPM_BUILD_ROOT%{_sysconfdir}/ati/signature
cp -r common%{_sysconfdir}/ati/amdpcsdb.default $RPM_BUILD_ROOT%{_sysconfdir}/ati/amdpcsdb.default
cp -r common%{_sysconfdir}/ati/atiogl.xml $RPM_BUILD_ROOT%{_sysconfdir}/ati/atiogl.xml

cp -r common%{_datadir}/ati/* $RPM_BUILD_ROOT%{_datadir}/ati
cp -r %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -r common%{_datadir}/icons/*.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

%if %{with multigl}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ld.so.conf.d,%{_libdir}/fglrx}

echo %{_libdir}/fglrx >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/fglrx.conf

cp -r common%{_libdir}/lib*.a $RPM_BUILD_ROOT%{_libdir}
cp -r common%{_libdir}/lib*.so* $RPM_BUILD_ROOT%{_libdir}/fglrx

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/fglrx
ln -sf fglrx/libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so
%else
cp -r common%{_libdir}/lib* $RPM_BUILD_ROOT%{_libdir}

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so
%endif

install common%{_includedir}/GL/*.h $RPM_BUILD_ROOT%{_includedir}/GL
install common/usr/X11R6/include/X11/extensions/*.h $RPM_BUILD_ROOT%{_includedir}/X11/extensions
echo "LIBGL_DRIVERS_PATH=%{_libdir}/xorg/modules/dri" > $RPM_BUILD_ROOT%{_sysconfdir}/env.d/LIBGL_DRIVERS_PATH

cd $RPM_BUILD_ROOT%{_libdir}
for f in libfglrx_dm libfglrx_gamma libfglrx_pp libfglrx_tvout; do
%if %{with multigl}
	ln -s fglrx/$f.so.*.* $f.so
%else
	ln -s $f.so.*.* $f.so
%endif
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n kernel%{_alt_kernel}-video-firegl
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-video-firegl
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc ATI_LICENSE.TXT common%{_docdir}/fglrx/*.html common%{_docdir}/fglrx/articles common%{_docdir}/fglrx/user-manual
%dir %{_sysconfdir}/ati
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/control
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/signature
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/amdpcsdb.default
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ati/atiogl.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/env.d/LIBGL_DRIVERS_PATH
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.xpm
%{_datadir}/ati
%if %{with multigl}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/fglrx.conf
%dir %{_libdir}/fglrx
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_libdir}/fglrx/libAMDXvBA.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libAMDXvBA.so.1
%attr(755,root,root) %{_libdir}/fglrx/libXvBAW.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libXvBAW.so.1
%{_libdir}/fglrx/libAMDXvBA.cap
%endif
%attr(755,root,root) %{_libdir}/fglrx/libatiadlxx.so
%attr(755,root,root) %{_libdir}/fglrx/libGL.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libGL.so.1
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_dm.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_gamma.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_gamma.so.1
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_pp.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_tvout.so.*.*
%attr(755,root,root) %{_libdir}/fglrx/libfglrx_tvout.so.1
%else
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_libdir}/libAMDXvBA.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libAMDXvBA.so.1
%attr(755,root,root) %{_libdir}/libXvBAW.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libXvBAW.so.1
%{_libdir}/libAMDXvBA.cap
%endif
%attr(755,root,root) %{_libdir}/libatiadlxx.so
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGL.so.1
%attr(755,root,root) %{_libdir}/libGL.so
%attr(755,root,root) %{_libdir}/libfglrx_dm.so.*.*
%attr(755,root,root) %{_libdir}/libfglrx_gamma.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfglrx_gamma.so.1
%attr(755,root,root) %{_libdir}/libfglrx_pp.so.*.*
%attr(755,root,root) %{_libdir}/libfglrx_tvout.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfglrx_tvout.so.1
%endif
%attr(755,root,root) %{_libdir}/xorg/modules/dri/fglrx_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/fglrx_drv.so
%attr(755,root,root) %{_libdir}/xorg/modules/linux/libfglrxdrm.so
%attr(755,root,root) %{_libdir}/xorg/modules/amdxmm.so
%attr(755,root,root) %{_libdir}/xorg/modules/glesx.so
%attr(755,root,root) %{_libdir}/xorg/modules/esut.a

%files libdri
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/libdri.so

%files libglx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/libglx.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfglrx_dm.so
%attr(755,root,root) %{_libdir}/libfglrx_gamma.so
%attr(755,root,root) %{_libdir}/libfglrx_pp.so
%attr(755,root,root) %{_libdir}/libfglrx_tvout.so
%{_includedir}/GL/glATI.h
%{_includedir}/GL/glxATI.h
%{_includedir}/X11/extensions/fglrx_gamma.h
%if %{with multigl}
%attr(755,root,root) %{_libdir}/libGL.so
%endif

%files static
%defattr(644,root,root,755)
%{_libdir}/libfglrx_dm.a
%{_libdir}/libfglrx_gamma.a
%{_libdir}/libfglrx_pp.a
%{_libdir}/libfglrx_tvout.a
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-firegl
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
