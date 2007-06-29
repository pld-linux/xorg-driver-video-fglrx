#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%bcond_with	verbose		# verbose build (V=1)

%define		x11ver		x710

%if !%{with kernel}
%undefine with_dist_kernel
%endif

%ifarch %{ix86}
%define		arch_sufix	""
%define		arch_dir	x86
%else
%define		arch_sufix	_64a
%define		arch_dir	x86_64
%endif

Summary:	Linux Drivers for ATI graphics accelerators
Summary(pl.UTF-8):	Sterowniki do akceleratorów graficznych ATI
Name:		xorg-driver-video-fglrx
Version:	8.38.6
%define		_rel	1
Release:	%{_rel}
License:	ATI Binary (parts are GPL)
Group:		X11
Source0:	http://dlmdownloads.ati.com/drivers/linux/ati-driver-installer-%{version}-x86.x86_64.run
# Source0-md5:	750eb0b5fa996d40b3ca52542c78154b
Patch0:		%{name}-kh.patch
URL:		http://www.ati.com/support/drivers/linux/radeon-linux.html
%{?with_userspace:BuildRequires:	OpenGL-GLU-devel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
%{?with_userspace:BuildRequires:	qt-devel}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-recordproto-devel
BuildRequires:	xorg-proto-xf86miscproto-devel
BuildRequires:	xorg-proto-xf86vidmodeproto-devel
Requires:	xorg-xserver-libglx
Requires:	xorg-xserver-server
Provides:	OpenGL = 2.0
Obsoletes:	Mesa
Obsoletes:	Mesa-libGL
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	X11-driver-firegl < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-driver-firegl < 1:7.0.0
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

%package devel
Summary:	Header files for development for the ATI Radeon cards proprietary driver
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania z użyciem własnościowego sterownika dla kart ATI Radeon
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
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
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraries for development for the ATI proprietary driver for
ATI Radeon graphic cards.

%description static -l pl.UTF-8
Biblioteki statyczne do programowania z użyciem własnościowego
sterownika ATI dla kart graficznych ATI Radeon.

%package -n kernel%{_alt_kernel}-video-firegl
Summary:	ATI kernel module for FireGL support
Summary(pl.UTF-8):	Moduł jądra oferujący wsparcie dla ATI FireGL
Release:	%{_rel}@%{_kernel_ver_str}
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
%{?with_dist_kernel:%patch0 -p1}
cd -

install -d common%{_prefix}/{%{_lib},bin}
cp -r %{x11ver}%{arch_sufix}%{_prefix}/X11R6/%{_lib}/* common%{_libdir}
cp -r arch/%{arch_dir}%{_prefix}/X11R6/%{_lib}/* common%{_libdir}
cp -r arch/%{arch_dir}%{_prefix}/X11R6/bin/* common%{_bindir}

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/env.d,%{_bindir},%{_libdir}/xorg/modules,%{_includedir}/{X11/extensions,GL}}

install common%{_bindir}/{fgl_glxgears,fglrxinfo,aticonfig,fglrx_xgamma} \
	$RPM_BUILD_ROOT%{_bindir}
cp -r common%{_libdir}/lib* $RPM_BUILD_ROOT%{_libdir}
cp -r common%{_libdir}/modules/* $RPM_BUILD_ROOT%{_libdir}/xorg/modules

ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so
ln -sf libGL.so.1.2 $RPM_BUILD_ROOT%{_libdir}/libGL.so.1

install common%{_includedir}/GL/*.h $RPM_BUILD_ROOT%{_includedir}/GL
install common%{_prefix}/X11R6/include/X11/extensions/*.h $RPM_BUILD_ROOT%{_includedir}/X11/extensions
echo "LIBGL_DRIVERS_PATH=%{_libdir}/xorg/modules/dri" > $RPM_BUILD_ROOT%{_sysconfdir}/env.d/LIBGL_DRIVERS_PATH

cd $RPM_BUILD_ROOT%{_libdir}
for f in libfglrx_dm libfglrx_gamma libfglrx_pp libfglrx_tvout; do
	ln -s $f.so.* $f.so
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
%doc ATI_LICENSE.TXT common%{_docdir}/fglrx/*.html common%{_docdir}/fglrx/articles common%{_docdir}/fglrx/release-notes common%{_docdir}/fglrx/user-manual
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/env.d/LIBGL_DRIVERS_PATH
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %{_libdir}/libGL.so.1
%attr(755,root,root) %{_libdir}/libGL.so
%attr(755,root,root) %{_libdir}/libfglrx_dm.so.*.*
%attr(755,root,root) %{_libdir}/libfglrx_gamma.so.*.*
%attr(755,root,root) %{_libdir}/libfglrx_pp.so.*.*
%attr(755,root,root) %{_libdir}/libfglrx_tvout.so.*.*
%attr(755,root,root) %{_libdir}/xorg/modules/dri/fglrx_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/fglrx_drv.so
%attr(755,root,root) %{_libdir}/xorg/modules/linux/libfglrxdrm.so
%attr(755,root,root) %{_libdir}/xorg/modules/glesx.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfglrx_*so
%{_includedir}/GL/glATI.h
%{_includedir}/GL/glxATI.h
%{_includedir}/X11/extensions/fglrx_gamma.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libfglrx_*.a
%{_libdir}/xorg/modules/esut.a
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-firegl
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
