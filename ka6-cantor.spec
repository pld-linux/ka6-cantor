#
# Conditional build:
%bcond_without	luajit		# build without luajit
%bcond_with	tests		# build with tests
#
%ifarch x32
%undefine	with_luajit
%endif

%define		kdeappsver	25.04.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		cantor
Summary:	Cantor
Name:		ka6-%{kaname}
Version:	25.04.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	c7ae35251617a97ebd3f1b9745a0427a
URL:		https://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Help-devel
BuildRequires:	Qt6Network-devel >= 5.11.1
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6WebEngine-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	R
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-analitza-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kpty-devel >= %{kframever}
BuildRequires:	kf6-ktexteditor-devel >= %{kframever}
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kf6-syntax-highlighting-devel >= %{kframever}
BuildRequires:	libmarkdown-devel
BuildRequires:	libqalculate-devel >= 2.8.2
%{?with_luajit:BuildRequires:	luajit-devel}
BuildRequires:	ninja
BuildRequires:	poppler-qt6-devel
BuildRequires:	qt6-assistant
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname} < %{version}
ExcludeArch:	i686 x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cantor is a KDE Application aimed to provide a nice Interface for
doing Mathematics and Scientific Computing. It doesn't implement its
own Computation Logic, but instead is built around different Backends.

Available Backends
- Julia Programming Language: http://julialang.org/
- KAlgebra for Calculation and Plotting: http://edu.kde.org/kalgebra/
  %{?with_luajit:- Lua Programming Language: http://lua.org/}
- Maxima Computer Algebra System: http://maxima.sourceforge.net/
- Octave for Numerical Computation: https://gnu.org/software/octave/
- Python 2 Programming Language: http://python.org/
- Python 3 Programming Language: http://python.org/
- Qalculate Desktop Calculator: http://qalculate.sourceforge.net/
- R Project for Statistical Computing: http://r-project.org/
- Sage Mathematics Software: http://sagemath.org/
- Scilab for Numerical Computation: http://scilab.org/

%description -l pl.UTF-8
Cantor jest programem KDE, którego celem jest dostarczenie miłego
interfejsu do obliczeń naukowych. Cantor nie implementuje własnej
logiki obliczeń, zamiast tego jest zbudowany wokół różnych backendów.

Dostępne backendy:
- język programowania Julia: http://julialang.org/
- KAlgebra do obliczeń i rysowania: http://edu.kde.org/kalgebra/
  %{?with_luajit:- język Lua: http://lua.org/}
- system komputerowej algebry Maxima: http://maxima.sourceforge.net/
- Octave do obliczeń numerycznych: https://gnu.org/software/octave/
- język Python 3: http://python.org/
- kalkulator biurkowy Qalculate: http://qalculate.sourceforge.net/
- projekt R do obliczeń statystycznych: http://r-project.org/
- oprogramowanie matematyczne Sage: http://sagemath.org/
- Scilab do obliczeń numerycznych: http://scilab.org/

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%{?with_luajit:%{_datadir}/knsrcfiles/cantor_lua.knsrc}
%attr(755,root,root) %{_bindir}/cantor_pythonserver
%attr(755,root,root) %{_libdir}/cantor_pythonbackend.so
%ghost %{_libdir}/libcantorlibs.so.28
%{_datadir}/cantor/octave/graphic_packages.xml
%{_datadir}/cantor/python/graphic_packages.xml
%{_datadir}/config.kcfg/pythonbackend.kcfg
%{_datadir}/knsrcfiles/cantor.knsrc
%{_datadir}/knsrcfiles/cantor_kalgebra.knsrc
%{_datadir}/knsrcfiles/cantor_maxima.knsrc
%{_datadir}/knsrcfiles/cantor_octave.knsrc
%{_datadir}/knsrcfiles/cantor_python.knsrc
%{_datadir}/knsrcfiles/cantor_qalculate.knsrc
%{_datadir}/knsrcfiles/cantor_r.knsrc
%{_datadir}/knsrcfiles/cantor_sage.knsrc
%{_datadir}/knsrcfiles/cantor_scilab.knsrc
%attr(755,root,root) %{_bindir}/cantor
%attr(755,root,root) %{_bindir}/cantor_rserver
%attr(755,root,root) %{_bindir}/cantor_scripteditor
%attr(755,root,root) %{_libdir}/libcantor_config.so
%attr(755,root,root) %{_libdir}/libcantorlibs.so.*.*.*
%dir %{_libdir}/qt6/plugins/cantor_plugins
%dir %{_libdir}/qt6/plugins/cantor_plugins/assistants
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_advancedplotassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_creatematrixassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_differentiateassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_eigenvaluesassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_eigenvectorsassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_importpackageassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_integrateassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_invertmatrixassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_plot2dassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_plot3dassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_qalculateplotassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_runscriptassistant.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/assistants/cantor_solveassistant.so
%dir %{_libdir}/qt6/plugins/cantor_plugins/backends
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_kalgebrabackend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_luabackend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_maximabackend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_octavebackend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_pythonbackend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_qalculatebackend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_rbackend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_sagebackend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/backends/cantor_scilabbackend.so
%dir %{_libdir}/qt6/plugins/cantor_plugins/panels
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/panels/cantor_documentationpanelplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/panels/cantor_filebrowserpanelplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/panels/cantor_helppanelplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/panels/cantor_tocpanelplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/cantor_plugins/panels/cantor_variablemanagerplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/parts/cantorpart.so
%{_desktopdir}/org.kde.cantor.desktop
%dir %{_datadir}/cantor
%{_datadir}/cantor/latex
%{_datadir}/cantor/maximabackend
%{_datadir}/cantor/octavebackend
%dir %{_datadir}/cantor/octave
%dir %{_datadir}/cantor/python
%{_datadir}/cantor/xslt
%{_datadir}/config.kcfg/cantor.kcfg
%{_datadir}/config.kcfg/cantor_libs.kcfg
%{_datadir}/config.kcfg/kalgebrabackend.kcfg
%{_datadir}/config.kcfg/maximabackend.kcfg
%{_datadir}/config.kcfg/qalculatebackend.kcfg
%{_datadir}/config.kcfg/rserver.kcfg
%{_datadir}/config.kcfg/sagebackend.kcfg
%{_datadir}/config.kcfg/scilabbackend.kcfg
%{_iconsdir}/hicolor/128x128/apps/cantor.png
%{_iconsdir}/hicolor/16x16/apps/cantor.png
%{_iconsdir}/hicolor/22x22/apps/cantor.png
%{_iconsdir}/hicolor/32x32/apps/cantor.png
%{_iconsdir}/hicolor/48x48/apps/cantor.png
%{_iconsdir}/hicolor/48x48/apps/juliabackend.png
%{_iconsdir}/hicolor/48x48/apps/kalgebrabackend.png
%{?with_luajit:%{_iconsdir}/hicolor/48x48/apps/luabackend.png}
%{_iconsdir}/hicolor/48x48/apps/maximabackend.png
%{_iconsdir}/hicolor/48x48/apps/octavebackend.png
%{_iconsdir}/hicolor/48x48/apps/pythonbackend.png
%{_iconsdir}/hicolor/48x48/apps/qalculatebackend.png
%{_iconsdir}/hicolor/48x48/apps/rbackend.png
%{_iconsdir}/hicolor/48x48/apps/sagebackend.png
%{_iconsdir}/hicolor/48x48/apps/scilabbackend.png
%{_iconsdir}/hicolor/64x64/apps/cantor.png
%{_datadir}/metainfo/org.kde.cantor.appdata.xml
%{?with_luajit:%{_datadir}/config.kcfg/luabackend.kcfg}
%{_datadir}/mime/packages/cantor.xml
%{_datadir}/config.kcfg/octavebackend.kcfg.in
%{_datadir}/knsrcfiles/cantor-documentation.knsrc

%files devel
%defattr(644,root,root,755)
%{_includedir}/cantor
%{_libdir}/libcantorlibs.so
%{_libdir}/cmake/Cantor
