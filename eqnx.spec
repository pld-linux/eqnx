Summary:	Device driver/utilities for Equinox SST SuperSerial family
Summary(pl):	Sterowniki do karty Equinox SST SuperSerial
Name:		eqnx
Version:	4.04
Release:	1
License:	GPL
Vendor:		Equinox Systems, Inc.
Group:		Applications/Communications
Source0:	%{name}-%{version}-1.tar.gz
Patch0:		%{name}-misc.patch
URL:		http://www.equinox.com/
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Provides device driver and diagnostic utilities for Equinox
SuperSerial multiport and expandable host controller boards. This
driver supports ISA, EISA and PCI versions of the 2, 4, 8 and 16 port
boards as well as the expandable 64 and 128 port boards and the 4RJ
and 8RJ boards. ISA and EISA are not available on Itanium systems.

%description -l pl
Ten pakiet zawiera sterownik i narzêdzia diagnostyczne dla kart
wieloportowych i rozszerzealnych kontrolerów Equinox SuperSerial. Ten
sterownik obs³uguje wersje ISA, EISA i PCI kart 2, 4, 8 i
16-portowych, a tak¿e rozszerzalne karty 64 i 128-portowe oraz karty
4RJ i 8RJ. ISA i EISA nie s± dostêpne w systemach Itanium.

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

%preun
# check driver usage.  If ports in use, disallow the remove
if [ -e /sbin/chkconfig ]
then
	/sbin/chkconfig eqnx
	if [ $? != 0 ]
	then
		exit 0
	fi
fi

if [ -f /etc/rc.d/init.d/eqnx ]
then
	/etc/rc.d/init.d/eqnx status > /dev/null 2>&1
	if [ $? != 0 ]
	then
		echo "eqnx driver in use, unable to unload"
		echo "Please stop all processes running on SST ports"
		exit 1
	fi
fi

# stop the driver + remove device files
if [ -f /etc/rc.d/init.d/eqnx ]
then
	/etc/rc.d/init.d/eqnx stop
fi

# remove eqnx from startup scripts
if [ -e /usr/sbin/eqnx-installrc ]
then
	/usr/sbin/eqnx-installrc -u
fi

%post
echo "To complete installation of the Equinox SST product:"
echo "   1. /etc/rc.d/init.d/eqnx start"
echo "   2. ensure this script is invoked at boot-time"
echo "	    (such as chkconfig --add eqnx, for redhat, etc.)"
echo "   Refer to installation notes for more information".

%files
%defattr(644,root,root,755)
%doc inst/INSTALL.TXT
%doc inst/RELEASE.TXT
%doc utils/ssdiag/README.ssdiag
/etc/rc.d/init.d/eqnx
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
