%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name paunch

%global common_desc \
Library and utility to launch and manage containers using YAML based configuration data.

Name:       python-%{pypi_name}
Version:    2.5.0
Release:    1%{?dist}
Summary:    Library and utility to launch and manage containers using YAML based configuration data

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
Source10:   paunch-container-shutdown
Source11:   paunch-container-shutdown.service
Source12:   91-paunch-container-shutdown.preset

BuildArch:  noarch
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
BuildRequires:  python2-devel
BuildRequires:  python2-psutil
BuildRequires:  PyYAML
BuildRequires:  systemd-units

# test requires
BuildRequires:  python2-mock
BuildRequires:  python2-oslotest
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-tenacity >= 3.2.1

Requires:   python2-cliff
Requires:   docker
Requires:   python2-pbr
Requires:   python2-psutil
Requires:   PyYAML
Requires:   python2-tenacity >= 3.2.1
Requires:   findutils

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
%{common_desc}

This package contains the paunch python library code and the command utility.

%package doc
Summary: Documentation for paunch library and utility

BuildRequires: python2-sphinx
BuildRequires: python2-oslo-sphinx
BuildRequires: openstack-macros

%description doc
%{common_desc}

This package contains auto-generated documentation.

%package tests
Summary: Tests for paunch library and utility

Requires:  python-%{pypi_name}
Requires:  python2-mock
Requires:  python2-oslotest
Requires:  python2-testrepository
Requires:  python2-testscenarios
Requires:  python2-tenacity >= 3.2.1

%description tests
%{common_desc}

This package contains library and utility tests.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let's handle dependencies ourseleves
%py_req_cleanup

%build

%py2_build

%install
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

%check
%{__python2} setup.py test

%post
%systemd_post paunch-container-shutdown.service

%preun
%systemd_preun paunch-container-shutdown.service

%files
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}*
%{_libexecdir}/paunch-container-shutdown
%{_unitdir}/paunch-container-shutdown.service
%{_presetdir}/91-paunch-container-shutdown.preset
%exclude %{python2_sitelib}/%{pypi_name}/tests

%files doc
%doc doc/build/html
%license LICENSE

%files tests
%license LICENSE
%{python2_sitelib}/%{pypi_name}/tests

%changelog
* Tue Apr 10 2018 RDO <dev@lists.rdoproject.org> 2.5.0-1
- Update to 2.5.0

* Tue Mar 27 2018 Jon Schlueter <jschluet@redhat.com> 2.4.0-1
- Update to 2.4.0

* Mon Mar 05 2018 RDO <dev@lists.rdoproject.org> 2.3.0-1
- Update to 2.3.0

