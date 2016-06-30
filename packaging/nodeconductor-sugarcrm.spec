Name: nodeconductor-sugarcrm
Summary: SugarCRM plugin for NodeConductor
Group: Development/Libraries
Version: 0.2.1
Release: 1.el7
License: Copyright 2015 OpenNode LLC.  All rights reserved.
Url: http://nodeconductor.com
Source0: %{name}-%{version}.tar.gz

Requires: nodeconductor > 0.102.2
Requires: nodeconductor-openstack >= 0.4.1
Requires: python-sugarcrm >= 0.1.1

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

%description
NodeConductor SugarCRM adds SugarCRM support to NodeConductor.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Thu Jun 30 2016 Jenkins <jenkins@opennodecloud.com> - 0.2.1-1.el7
- New upstream release

* Thu Jun 16 2016 Jenkins <jenkins@opennodecloud.com> - 0.2.0-1.el7
- New upstream release

* Thu Oct 29 2015 Juri Hudolejev <juri@opennodecloud.com> - 0.1.0-1.el7
- Initial version of the package
