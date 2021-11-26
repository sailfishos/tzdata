Summary: Time zone and daylight-saving time data
Name: tzdata
%define tzversion 2021a
Version: %{tzversion}+git2
Release: 1
License: Public Domain
URL: https://www.iana.org/time-zones
Source0: %{name}%{tzversion}.tar.gz
BuildRequires: fdupes
BuildRequires: glibc-common
BuildArch: noarch

%description
This package contains data required for the implementation of
standard local time for many representative locations around the
globe. It is updated periodically to reflect changes made by
political bodies to time zone boundaries, UTC offsets, and
daylight-saving rules.

%prep
%setup -q -c

%build
# The build setup is adapted from Ubuntu tzdata package version
# 2012e-0ubuntu0.12.04.1
TIMEZONES="africa \
	   antarctica \
	   asia \
	   australasia \
           europe \
           northamerica \
           southamerica \
           etcetera \
           factory \
           backward"

# Build the "default" version
for zone in $TIMEZONES; do \
  /usr/sbin/zic -d tzgen -L /dev/null ${zone}
done

# Build the "posix" and "right" versions
for zone in $TIMEZONES; do
   /usr/sbin/zic -d tzgen/posix -L /dev/null ${zone}
   /usr/sbin/zic -d tzgen/right -L leapseconds ${zone}
done

# Generate a posixrules file
/usr/sbin/zic -d tzgen -p America/New_York

%install
rm -fr $RPM_BUILD_ROOT
install -d %{buildroot}%{_datadir}/zoneinfo
cp -prd tzgen/* %{buildroot}%{_datadir}/zoneinfo
install -m 644 iso3166.tab %{buildroot}%{_datadir}/zoneinfo
install -m 644 zone.tab %{buildroot}%{_datadir}/zoneinfo
install -m 644 zone1970.tab %{buildroot}%{_datadir}/zoneinfo

# Deduplicate files, use hardlinks here, see JB#52707
fdupes -1 -q -r %{buildroot}%{_datadir}/zoneinfo | while read line ; do
    set -- ${line}
    while [ "$#" -ge 2 ] ; do
	ln -f "$1" "$2"
	shift
    done
done

%files
%defattr(-,root,root)
%license LICENSE
%{_datadir}/zoneinfo
