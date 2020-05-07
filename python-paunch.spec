# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global pypi_name paunch

%global common_desc \
Library and utility to launch and manage containers using YAML based configuration data.

Name:       python-%{pypi_name}
Version:    5.3.2
Release:    1%{?dist}
Summary:    Library and utility to launch and manage containers using YAML based configuration data

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
Source10:   paunch-container-shutdown
Source11:   paunch-container-shutdown.service
Source12:   91-paunch-container-shutdown.preset
Source13:   netns-placeholder.service
Source14:   91-netns-placeholder.preset
Source15:   paunch-start-podman-container

BuildArch:  noarch

%description
%{common_desc}

%package -n python%{pyver}-%{pypi_name}
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
Summary:    Library and utility to launch and manage containers using YAML based configuration data

BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-devel
BuildRequires: openstack-macros
# test requires
BuildRequires:  python%{pyver}-cliff
BuildRequires:  python%{pyver}-jmespath
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-psutil
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-tenacity >= 3.2.1

Requires:   python%{pyver}-cliff
Requires:   python%{pyver}-jmespath
Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-tenacity >= 3.2.1
Requires:   python%{pyver}-psutil
Requires:   podman
Requires:   findutils
Requires:   paunch-services

%if %{pyver} == 2
BuildRequires:  PyYAML
Requires:       PyYAML
%else
BuildRequires:  python%{pyver}-PyYAML
Requires:       python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python%{pyver}-%{pypi_name}-doc
Summary: Documentation for paunch library and utility

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python%{pyver}-%{pypi_name}-doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%package -n python%{pyver}-%{pypi_name}-tests
Summary: Tests for paunch library and utility

Requires:  python%{pyver}-%{pypi_name}
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-subunit
Requires:  python%{pyver}-stestr
Requires:  python%{pyver}-tenacity >= 3.2.1

%description -n python%{pyver}-%{pypi_name}-tests
%{common_desc}

This package contains library and utility tests.

%package -n paunch-services
Summary: Services related to paunch
BuildRequires:  systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: iproute

%description -n paunch-services
This package contains service definitions related to paunch


%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%pyver_build

%install
%pyver_install

# Install shutdown script
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_libexecdir}/paunch-container-shutdown

# Install podman start script
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_libexecdir}/paunch-start-podman-container

# Install systemd units
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/paunch-container-shutdown.service

# Install systemd preset
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_presetdir}/91-paunch-container-shutdown.preset

# Install netns unit
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/netns-placeholder.service

# Install systemd preset for netns unit
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_presetdir}/91-netns-placeholder.preset

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%check
PYTHON=python%{pyver} %{pyver_bin} setup.py test

%post -n paunch-services
%systemd_post paunch-container-shutdown.service
%systemd_post netns-placeholder.service

%preun -n paunch-services
%systemd_preun paunch-container-shutdown.service
%systemd_preun netns-placeholder.service

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}*
%exclude %{pyver_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python%{pyver}-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/%{pypi_name}/tests

%files -n paunch-services
%license LICENSE
%{_libexecdir}/paunch-container-shutdown
%{_libexecdir}/paunch-start-podman-container
%{_unitdir}/paunch-container-shutdown.service
%{_presetdir}/91-paunch-container-shutdown.preset
%{_unitdir}/netns-placeholder.service
%{_presetdir}/91-netns-placeholder.preset

%changelog
* Thu May 07 2020 RDO <dev@lists.rdoproject.org> 5.3.2-1
- Update to 5.3.2

* Mon Jan 06 2020 RDO <dev@lists.rdoproject.org> 5.3.1-1
- Update to 5.3.1

* Mon Oct 21 2019 RDO <dev@lists.rdoproject.org> 5.3.0-1
- Update to 5.3.0

