#
# Conditional build:
%bcond_without	dist_kernel	# without sources of distribution kernel
#
Summary:	QNX4 Style Send/Receive/Reply Messaging for Linux
Summary(pl):	Komunikowanie poprzez Send/Receive/Reply w stylu QNX
Name:		srr
Version:	1.3.12
%define _rel	1
Release:	%{_rel}
License:	GPL
Group:		Development/Libraries
Source0:	ftp://developers.cogentrts.com/pub/linux/%{name}-%{version}.tgz
# Source0-md5:	b61edee0962a3c2b62d87ad9ea4d46f8
URL:		http://developers.cogentrts.com/srr.html
%{?with_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
We think the UN*X world has something to learn from QNX, and high on
that list is the Send/Receive/Reply messaging and synchronization
mechanism that is one of QNX's hallmarks. The SRRIPC kernel module for
Linux allows you to write new code with S/R/R messaging on a single
Linux machine, and to quickly port applications between QNX4 and
Linux.

%description -l pl
Niektórzy uwa¿aj±, ¿e ¶wiat un*ksowy powinien siê czego¶ nauczyæ z
QNX-a, a wysoko na tej li¶cie jest mechanizm komunikowania i
synchronizacji poprzez Send/Receive/Reply, bêd±cy jedn± z
charakterystycznych cech QNX-a. Modu³ j±dra SRRIPC dla Linuksa pozwala
na pisanie nowego kodu u¿ywaj±cego komunikacji S/R/R na maszynie
linuksowej i szybkie portowanie aplikacji miêdzy systemem QNX4 a
Linuksem.

%package -n kernel-misc-srripc
Summary:	Linux kernel modules for QNX4 Style IPC
Summary(pl):	Modu³y j±dra Linuksa do IPC w stylu QNX4
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod

%description -n kernel-misc-srripc
Linux kernel modules for QNX4 Style IPC.

%description -n kernel-misc-srripc -l pl
Modu³y j±dra Linuksa do IPC w stylu QNX4.

%package -n kernel-smp-misc-srripc
Summary:	Linux SMP kernel modules for QNX4 Style IPC
Summary(pl):	Modu³y j±dra Linuksa SMP do IPC w stylu QNX4
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-srripc
Linux SMP kernel modules for QNX4 Style IPC.

%description -n kernel-smp-misc-srripc -l pl
Modu³y j±dra Linuksa SMP do IPC w stylu QNX4.

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

%post	-n kernel-misc-srripc
%depmod %{_kernel_ver}

%postun -n kernel-misc-srripc
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-srripc
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-misc-srripc
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc *.html NOTES TODO
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*.h
%{_includedir}/sys/*.h
%{_libdir}/*.a

%files -n kernel-misc-srripc
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/srripc*

%files -n kernel-smp-misc-srripc
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/srripc*
