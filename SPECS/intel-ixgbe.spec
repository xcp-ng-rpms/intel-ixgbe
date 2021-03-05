%define vendor_name Intel
%define vendor_label intel
%define driver_name ixgbe

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 5.5.2
Release: 2.1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-intel-ixgbe/archive?at=5.5.2-2&format=tgz&prefix=driver-intel-ixgbe-5.5.2#/intel-ixgbe-5.5.2.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-intel-ixgbe/archive?at=5.5.2-2&format=tgz&prefix=driver-intel-ixgbe-5.5.2#/intel-ixgbe-5.5.2.tar.gz) = 458ea819a145f82c2a38fcc7e9b570a065472fa1

# XCP-ng patches
Patch1000: intel-ixgbe-5.5.2-fix-memory-leak.backport.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Mar 05 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 5.5.2-2.1
- Attempt to fix memory leak
- Add intel-ixgbe-5.5.2-fix-memory-leak.backport.patch
- Related to https://xcp-ng.org/forum/topic/2507/alert-control-domain-memory-usage

* Wed Dec 05 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 5.5.2-2
- CA-302474: Fix race when VF driver does a reset

* Fri Nov 23 2018 Deli Zhang <deli.zhang@citrix.com> - 5.5.2-1
- CP-29858: Upgrade ixgbe driver to version 5.5.2
