Summary:	Device driver/utilities for Equinox SST SuperSerial family
Summary(pl.UTF-8):   Sterowniki do karty Equinox SST SuperSerial
Name:		eqnx
Version:	4.04
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	%{name}-%{version}-1.tar.gz
# Source0-md5:	3b335ac7f525036ad3147907adcd0ec8
Patch0:		%{name}-misc.patch
URL:		http://www.equinox.com/
BuildRequires:	rpmbuild(macros) >= 1.268
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Provides device driver and diagnostic utilities for Equinox
SuperSerial multiport and expandable host controller boards. This
driver supports ISA, EISA and PCI versions of the 2, 4, 8 and 16 port
boards as well as the expandable 64 and 128 port boards and the 4RJ
and 8RJ boards. ISA and EISA are not available on Itanium systems.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik i narzędzia diagnostyczne dla kart
wieloportowych i rozszerzalnych kontrolerów Equinox SuperSerial. Ten
sterownik obsługuje wersje ISA, EISA i PCI kart 2, 4, 8 i
16-portowych, a także rozszerzalne karty 64 i 128-portowe oraz karty
4RJ i 8RJ. ISA i EISA nie są dostępne w systemach Itanium.

%prep
%setup -q -n %{name}-%{version}-1
%patch0 -p1

%build
%{__make} build CC=%{kgcc} OPT="%{rpmcflags}" SMP=0
mv drv/eqnx.o drv/eqnx.o-up
%{__make} clean
%{__make} build CC=%{kgcc} OPT="%{rpmcflags}" SMP=1

%install
rm -rf $RPM_BUILD_ROOT
exit 1
%{__make} install OBJROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add eqnx
%service eqnx restart

%preun
if [ "$1" = 0 ]; then
	# check driver usage.  If ports in use, disallow the remove
	/sbin/service eqnx status > /dev/null 2>&1
	if [ $? != 0 ]; then
		echo "eqnx driver in use, unable to unload"
		echo "Please stop all processes running on SST ports"
		exit 1
	fi

	# stop the driver + remove device files
	%service eqnx stop
	/sbin/chkconfig --del eqnx

	# remove eqnx from startup scripts
	/usr/sbin/eqnx-installrc -u
fi

%files
%defattr(644,root,root,755)
%doc inst/INSTALL.TXT
%doc inst/RELEASE.TXT
%doc utils/ssdiag/README.ssdiag
%attr(754,root,root) /etc/rc.d/init.d/eqnx
/lib/modules/*/*/*
%attr(755,root,root) %{_bindir}/sscode
%attr(755,root,root) %{_bindir}/ssdiag
%attr(755,root,root) %{_bindir}/ssmkn
%attr(755,root,root) %{_bindir}/ssrm
%attr(755,root,root) %{_bindir}/sstty
%attr(755,root,root) %{_sbindir}/rpmvar
%attr(755,root,root) %{_sbindir}/eqnx-cfg
%attr(755,root,root) %{_sbindir}/eqnx-installrc
%{_libdir}/sst/ss.hlp
