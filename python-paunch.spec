
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

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
Source13:   netns-placeholder.service
Source14:   91-netns-placeholder.preset
Source15:   paunch-start-podman-container

BuildArch:  noarch

%description
%{common_desc}

%package -n python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:    Library and utility to launch and manage containers using YAML based configuration data

BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-devel
BuildRequires:  openstack-macros
BuildRequires:  git
# test requires
BuildRequires:  python3-cliff
BuildRequires:  python3-jmespath
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-psutil
BuildRequires:  python3-subunit
BuildRequires:  python3-stestr
BuildRequires:  python3-tenacity >= 3.2.1

Requires:   python3-cliff
Requires:   python3-jmespath
Requires:   python3-pbr
Requires:   python3-tenacity >= 3.2.1
Requires:   python3-psutil
Requires:   podman
Requires:   findutils
Requires:   paunch-services

BuildRequires:  python3-PyYAML
Requires:       python3-PyYAML

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python3-%{pypi_name}-doc
Summary: Documentation for paunch library and utility

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description -n python3-%{pypi_name}-doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%package -n python3-%{pypi_name}-tests
Summary: Tests for paunch library and utility

Requires:  python3-%{pypi_name}
Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-subunit
Requires:  python3-stestr
Requires:  python3-tenacity >= 3.2.1

%description -n python3-%{pypi_name}-tests
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
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py3_build

%install
%py3_install

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
sphinx-build-3 -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%check
PYTHON=%{__python3} %{__python3} setup.py test

%post -n paunch-services
%systemd_post paunch-container-shutdown.service
%systemd_post netns-placeholder.service

%preun -n paunch-services
%systemd_preun paunch-container-shutdown.service
%systemd_preun netns-placeholder.service

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*
%exclude %{python3_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python3-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests

%files -n paunch-services
%license LICENSE
%{_libexecdir}/paunch-container-shutdown
%{_libexecdir}/paunch-start-podman-container
%{_unitdir}/paunch-container-shutdown.service
%{_presetdir}/91-paunch-container-shutdown.preset
%{_unitdir}/netns-placeholder.service
%{_presetdir}/91-netns-placeholder.preset

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/paunch/commit/?id=d0e81c22ca4ed596af2396fb4665dc0535d1a75e
