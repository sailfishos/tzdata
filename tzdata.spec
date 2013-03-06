#specfile originally created for Fedora, modified for Moblin Linux
Summary: Timezone data
Name: tzdata
Version: 2011e
%define tzdata_version %{version}
%define tzcode_version 2011e
Release: 1
License: Public Domain
Group: System/Base
URL: ftp://elsie.nci.nih.gov/pub/

# The tzdata-base-0.tar.bz2 is a simple building infrastructure and
# test suite.  It is occasionally updated from glibc sources, and as
# such is under LGPLv2+, but none of this ever gets to be part of
# final zoneinfo files.
Source0: tzdata-base-0.tar.bz2
# These are official upstream.
Source1: ftp://elsie.nci.nih.gov/pub/tzdata%{tzdata_version}.tar.gz
Source2: ftp://elsie.nci.nih.gov/pub/tzcode%{tzcode_version}.tar.gz
Conflicts: glibc-common <= 2.3.2-63
BuildArch: noarch

%description
This package contains data files with rules for various timezones around
the world.

%prep
%setup -q -n tzdata
mkdir tzdata%{tzdata_version}
tar xzf %{SOURCE1} -C tzdata%{tzdata_version}
mkdir tzcode%{tzcode_version}
tar xzf %{SOURCE2} -C tzcode%{tzcode_version}
sed -e 's|@objpfx@|'`pwd`'/obj/|' \
    -e 's|@datadir@|%{_datadir}|' \
  Makeconfig.in > Makeconfig

%build
make
grep -v tz-art.htm tzcode%{tzcode_version}/tz-link.htm > tzcode%{tzcode_version}/tz-link.html

%install
rm -fr $RPM_BUILD_ROOT
sed -i 's|@install_root@|%{buildroot}|' Makeconfig
make install

#cp -pr zoneinfo/java $RPM_BUILD_ROOT%{_datadir}/javazi

%check
echo ====================TESTING=========================
make check
echo ====================TESTING END=====================

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/zoneinfo
%doc tzcode%{tzcode_version}/README
%doc tzcode%{tzcode_version}/Theory
%doc tzcode%{tzcode_version}/tz-link.html
