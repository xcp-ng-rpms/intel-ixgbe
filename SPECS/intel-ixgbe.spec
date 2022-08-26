%global package_speccommit 0ddfdf6305632dfc248bb734dd0fc865bd1ee90a
%global usver 5.9.4
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 5.9.4
%define vendor_name Intel
%define vendor_label intel
%define driver_name ixgbe

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 5.9.4
Release: %{?xsrel}%{?dist}
License: GPL
Source0: intel-ixgbe-5.9.4.tar.gz

BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

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

%{?_cov_results_package}

%changelog
* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 5.9.4-2
- CP-38416: Enable static analysis

* Fri Jan 21 2022 Deli Zhang <deli.zhang@citrix.com> - 5.9.4-1
- CP-37630: Upgrade ixgbe driver to version 5.9.4

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 5.5.2-3
- CP-35517: Fix the build for koji

* Wed Dec 05 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 5.5.2-2
- CA-302474: Fix race when VF driver does a reset

* Fri Nov 23 2018 Deli Zhang <deli.zhang@citrix.com> - 5.5.2-1
- CP-29858: Upgrade ixgbe driver to version 5.5.2
