%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name paunch
Name:       python-%{pypi_name}
Version:    1.5.5
Release:    1%{?dist}
Summary:    Library and utility to launch and manage containers using YAML based configuration data

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:  noarch
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python2-devel
BuildRequires:  PyYAML

# test requires
BuildRequires:  python-mock
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios

Requires:   python-cliff
Requires:   docker
Requires:   python-pbr
Requires:   PyYAML

%description
Library and utility to launch and manage containers using YAML based configuration data.

This package contains the paunch python library code and the command utility.

%package doc
Summary: Documentation for paunch library and utility

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
Library and utility to launch and manage containers using YAML based configuration data.

This package contains auto-generated documentation.

%package tests
Summary: Tests for paunch library and utility

Requires:  python-%{pypi_name}
Requires:  python-mock
Requires:  python-oslotest
Requires:  python-testrepository
Requires:  python-testscenarios

%description tests
Library and utility to launch and manage containers using YAML based configuration data.

This package contains library and utility tests.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build

%py2_build

%install
%py2_install

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%check
%{__python2} setup.py test

%files
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}*
%exclude %{python2_sitelib}/%{pypi_name}/tests

%files doc
%doc doc/build/html
%license LICENSE

%files tests
%license LICENSE
%{python2_sitelib}/%{pypi_name}/tests

%changelog
* Tue Mar 13 2018 RDO <dev@lists.rdoproject.org> 1.5.5-1
- Update to 1.5.5

* Wed Dec 13 2017 RDO <dev@lists.rdoproject.org> 1.5.3-1
- Update to 1.5.3

* Thu Nov 23 2017 RDO <dev@lists.rdoproject.org> 1.5.2-1
- Update to 1.5.2

* Tue Nov 07 2017 RDO <dev@lists.rdoproject.org> 1.5.1-1
- Update to 1.5.1

* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 1.5.0-1
- Update to 1.5.0

