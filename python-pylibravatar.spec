#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		libravatar
%define		egg_name	pyLibravatar
%define		pypi_name	pyLibravatar
Summary:	Python module for Libravatar
Name:		python-pylibravatar
Version:	1.6
Release:	1
Group:		Development/Libraries
# The full text of the license isn't shipped
License:	MIT
Source0:	http://pypi.python.org/packages/source/p/%{egg_name}/%{egg_name}-%{version}.tar.gz
# Source0-md5:	41b4d3aee39fb4656ee156e0dac18e73
# https://code.launchpad.net/~ralph-bean/pylibravatar/tcp-dns/+merge/263157
Patch0:		%{name}-dns-srv-tcp.patch
# https://bugs.launchpad.net/pylibravatar/+bug/1173603
URL:		http://pypi.python.org/pypi/pyLibravatar
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pydns
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-py3dns
%endif
%endif
Requires:	python-pydns
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyLibravatar is an easy way to make use of the federated Libravatar
avatar hosting service from within your Python applications.

%package -n python3-pylibravatar
Summary:	Python module for Libravatar
Group:		Development/Libraries
Requires:	python3-py3dns

%description -n python3-pylibravatar
PyLibravatar is an easy way to make use of the federated Libravatar
avatar hosting service from within your Python applications.

%prep
%setup -q -n %{egg_name}-%{version}
%patch0

# Correct wrong-file-end-of-line-encoding rpmlint issue
sed -i 's/\r//' README.txt
sed -i 's/\r//' Changelog.txt

%build
%if %{with python2}
%py_build
%endif
%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%files
%defattr(644,root,root,755)
# Upstream doesn't ship the license full text
# https://bugs.launchpad.net/pylibravatar/+bug/1173603
%doc README.txt Changelog.txt
%{py_sitescriptdir}/%{module}.py*
%{py_sitescriptdir}/%{egg_name}-%{version}*
%endif

%if %{with python3}
%files -n python3-pylibravatar
%defattr(644,root,root,755)
# Upstream doesn't ship the license full text
# https://bugs.launchpad.net/pylibravatar/+bug/1173603
%doc README.txt Changelog.txt
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/*%{module}*
%{py3_sitescriptdir}/%{egg_name}-%{version}-*
%endif
