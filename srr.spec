
# Conditional build:
# _without_dist_kernel	- without sources of distribution kernel

Summary:	QNX4 Style Send/Receive/Reply Messaging for Linux
Summary(pl):	Komunikowanie poprzez Send/Receive/Reply w stylu QNX
Name:		srr
Version:	1.3.12
%define _rel	1
Release:	%{_rel}
License:	GPL
Group:		Libraries/Development
######		Unknown group!
Source0:	ftp://developers.cogentrts.com/pub/linux/%{name}-%{version}.tgz
URL:		http://developers.cogentrts.com/srr.html
%{!?_without_dist_kernel:BuildRequires:	kernel-source}
BuildRequires:	%{kgcc_package}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
We think the UN*X world has something to learn from QNX, and high on
that list is the Send/Receive/Reply messaging and synchronization
mechanism that is one of QNX's hallmarks. The SRRIPC kernel module for
Linux allows you to write new code with S/R/R messaging on a single
Linux machine, and to quickly port applications between QNX4 and
Linux.

%package -n kernel-misc-srripc
Summary:	Kernel modules for QNX4 Style IPC
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		modutils >= 2.4.6-4
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-misc-srripc
Kernel modules for QNX4 Style IPC.

%package -n kernel-smp-misc-srripc
Summary:	Kernel modules for QNX4 Style IPC
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		modutils >= 2.4.6-4
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-misc-srripc
Kernel modules for QNX4 Style IPC.

%prep
%setup -q

%build
%{__make} \
	CC="%{kgcc}"

%{__make} -C mod clean all \
	CC="%{kgcc}" \
	CFLAGS="%{rpmcflags} -Wall -D__KERNEL__ -DMODULE -DLINUX -D__SMP__ -I%{_kernelsrcdir}/include -I../inc"
mv mod/srripc.o mod/srripc-smp.o

%{__make} -C mod clean all \
	CC="%{kgcc}" \
	CFLAGS="%{rpmcflags} -Wall -D__KERNEL__ -DMODULE -DLINUX -I%{_kernelsrcdir}/include -I../inc"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

%{__make} i_prefix i_exe i_devel \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	modprefix=$RPM_BUILD_ROOT%{_libdir}/modules

install mod/srripc-smp.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/srripc.o
install mod/srripc.o		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/srripc.o

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-misc-srripc
/sbin/depmod -a

%postun -n kernel-misc-srripc
/sbin/depmod -a

%post -n kernel-smp-misc-srripc
/sbin/depmod -a

%postun -n kernel-smp-misc-srripc
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.html NOTES TODO
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*.h
%{_includedir}/*/*.h
%{_libdir}/*.a

%files -n kernel-misc-srripc
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/srripc*

%files -n kernel-smp-misc-srripc
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/srripc*
