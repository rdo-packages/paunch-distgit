# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pydefault 3
%else
%global pydefault 2
%endif

%global pydefault_bin python%{pydefault}
%global pydefault_sitelib %python%{pydefault}_sitelib
%global pydefault_install %py%{pydefault}_install
%global pydefault_build %py%{pydefault}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name paunch

%global common_desc \
Library and utility to launch and manage containers using YAML based configuration data.

Name:       python-%{pypi_name}
Version:    XXX
Release:    XXX
Summary:    Library and utility to launch and manage containers using YAML based configuration data

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
Source10:   paunch-container-shutdown
Source11:   paunch-container-shutdown.service
Source12:   91-paunch-container-shutdown.preset

BuildArch:  noarch
Requires:   docker
Requires:   podman
Requires:   findutils
Requires:   paunch-services


%description
%{common_desc}

%package -n python%{pydefault}-%{pypi_name}
%{?python_provide:%python_provide python%{pydefault}-%{pypi_name}}
Summary:    Library and utility to launch and manage containers using YAML based configuration data

BuildRequires:  python%{pydefault}-setuptools
BuildRequires:  python%{pydefault}-pbr
BuildRequires:  python%{pydefault}-devel

# test requires
BuildRequires:  python%{pydefault}-mock
BuildRequires:  python%{pydefault}-oslotest
BuildRequires:  python%{pydefault}-subunit
BuildRequires:  python%{pydefault}-testrepository
BuildRequires:  python%{pydefault}-testscenarios
BuildRequires:  python%{pydefault}-tenacity >= 3.2.1

Requires:   python%{pydefault}-cliff
Requires:   python%{pydefault}-pbr
Requires:   python%{pydefault}-tenacity >= 3.2.1

%if %{pydefault} == 2
BuildRequires:  PyYAML
Requires:       PyYAML
%else
BuildRequires:  python%{pydefault}-PyYAML
Requires:       python%{pydefault}-PyYAML
%endif

%description -n python%{pydefault}-%{pypi_name}
%{common_desc}

%package -n python%{pydefault}-%{pypi_name}-doc
Summary: Documentation for paunch library and utility

BuildRequires: python%{pydefault}-sphinx
BuildRequires: python%{pydefault}-oslo-sphinx
BuildRequires: python%{pydefault}-openstackdocstheme
BuildRequires: openstack-macros

%description -n python%{pydefault}-%{pypi_name}-doc
%{common_desc}

This package contains auto-generated documentation.

%package -n python%{pydefault}-%{pypi_name}-tests
Summary: Tests for paunch library and utility

Requires:  python%{pydefault}-%{pypi_name}
Requires:  python%{pydefault}-mock
Requires:  python%{pydefault}-oslotest
Requires:  python%{pydefault}-subunit
Requires:  python%{pydefault}-testrepository
Requires:  python%{pydefault}-testscenarios
Requires:  python%{pydefault}-tenacity >= 3.2.1

%description -n python%{pydefault}-%{pypi_name}-tests
%{common_desc}

This package contains library and utility tests.

%package -n paunch-services
Summary: Services related to paunch
BuildRequires:  systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description -n paunch-services
This package contains service definitions related to paunch


%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%pydefault_build

%install
%pydefault_install

# Install shutdown script
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_libexecdir}/paunch-container-shutdown

# Install systemd units
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/paunch-container-shutdown.service

# Install systemd preset
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_presetdir}/91-paunch-container-shutdown.preset

# generate html docs
%{pydefault_bin} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%check -n python%{pydefault}-%{pypi_name}
PYTHON=python%{pydefault} %{pydefault_bin} setup.py test

%post -n paunch-services
%systemd_post paunch-container-shutdown.service

%preun -n paunch-services
%systemd_preun paunch-container-shutdown.service

%files -n python%{pydefault}-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{pydefault_sitelib}/%{pypi_name}*
%exclude %{pydefault_sitelib}/%{pypi_name}/tests

%files -n python%{pydefault}-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%files -n python%{pydefault}-%{pypi_name}-tests
%license LICENSE
%{pydefault_sitelib}/%{pypi_name}/tests

%files -n paunch-services
%license LICENSE
%{_libexecdir}/paunch-container-shutdown
%{_unitdir}/paunch-container-shutdown.service
%{_presetdir}/91-paunch-container-shutdown.preset

%changelog
