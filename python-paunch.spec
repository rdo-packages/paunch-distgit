%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name paunch
Name:       python-%{pypi_name}
Version:    XXX
Release:    XXX
Summary:    Library and utility to launch and manage containers using YAML based configuration data

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:  noarch
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires:   python-cliff
Requires:   docker-common

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

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

%build

%py2_build

%install
%py2_install

# remove tests
rm -fr %{buildroot}%{python2_sitelib}/%{pypi_name}/tests

# generate html docs
%{__python2} setup.py build_sphinx

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}*

%files doc
%doc html
%license LICENSE

%changelog
