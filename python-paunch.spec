%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >= 28
%global with_python3 1
%endif

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
Requires:   findutils
Requires:   paunch-services


%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary:    Library and utility to launch and manage containers using YAML based configuration data
%{?python_provide:%python_provide python2-%{pypi_name}}
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
BuildRequires:  python2-devel
BuildRequires:  PyYAML

# test requires
BuildRequires:  python2-mock
BuildRequires:  python2-oslotest
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-tenacity >= 3.2.1

Requires:   python2-cliff
Requires:   python2-pbr
Requires:   PyYAML
Requires:   python2-tenacity >= 3.2.1

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:    Library and utility to launch and manage containers using YAML based configuration data
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-devel
BuildRequires:  python3-PyYAML

# test requires
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-tenacity >= 3.2.1

Requires:   python3-cliff
Requires:   python3-pbr
Requires:   python3-PyYAML
Requires:   python3-tenacity >= 3.2.1

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%package -n python2-%{pypi_name}-doc
Summary: Documentation for paunch library and utility

BuildRequires: python2-sphinx
BuildRequires: python2-oslo-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: openstack-macros

%description -n python2-%{pypi_name}-doc
%{common_desc}

This package contains auto-generated documentation.



%if 0%{?with_python3}
%package -n python3-%{pypi_name}-doc
Summary: Documentation for paunch library and utility

BuildRequires: python3-sphinx
BuildRequires: python3-oslo-sphinx
BuildRequires: python3-openstackdocstheme
BuildRequires: openstack-macros

%description -n python3-%{pypi_name}-doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%package -n python2-%{pypi_name}-tests
Summary: Tests for paunch library and utility

Requires:  python2-%{pypi_name}
Requires:  python2-mock
Requires:  python2-oslotest
Requires:  python2-testrepository
Requires:  python2-testscenarios
Requires:  python2-tenacity >= 3.2.1

%description -n python2-%{pypi_name}-tests
%{common_desc}

This package contains library and utility tests.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}-tests
Summary: Tests for paunch library and utility

Requires:  python3-%{pypi_name}
Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-testrepository
Requires:  python3-testscenarios
Requires:  python3-tenacity >= 3.2.1

%description -n python3-%{pypi_name}-tests
%{common_desc}

This package contains library and utility tests.
%endif

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
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{pypi_name}\
   %{buildroot}%{_bindir}/%{pypi_name}-py3
%endif
%py2_install

# Install shutdown script
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_libexecdir}/paunch-container-shutdown

# Install systemd units
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/paunch-container-shutdown.service

# Install systemd preset
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_presetdir}/91-paunch-container-shutdown.preset

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%check -n python2-%{pypi_name}
%{__python2} setup.py test

%if 0%{?with_python3}
%check -n python3-%{pypi_name}
%{__python3} setup.py test
%endif

%post -n paunch-services
%systemd_post paunch-container-shutdown.service

%preun -n paunch-services
%systemd_preun paunch-container-shutdown.service

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}*
%exclude %{python2_sitelib}/%{pypi_name}/tests

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}-py3
%{python3_sitelib}/%{pypi_name}*
%exclude %{python3_sitelib}/%{pypi_name}/tests
%endif

%files -n python2-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{pypi_name}/tests

%if 0%{?with_python3}
%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests
%endif

%files -n paunch-services
%license LICENSE
%{_libexecdir}/paunch-container-shutdown
%{_unitdir}/paunch-container-shutdown.service
%{_presetdir}/91-paunch-container-shutdown.preset


%changelog
