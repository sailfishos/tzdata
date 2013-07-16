Summary: Time zone and daylight-saving time data
Name: tzdata
Version: 2013d
%define tzdata_version %{version}
%define tzcode_version %{version}
Release: 1
License: Public Domain
Group: System/Base
URL: ftp://ftp.iana.org/tz/
Source0: tzdata%{tzdata_version}.tar.gz
Conflicts: glibc-common <= 2.3.2-63
BuildArch: noarch

%description
This package contains data required for the implementation of
standard local time for many representative locations around the
globe. It is updated periodically to reflect changes made by
political bodies to time zone boundaries, UTC offsets, and
daylight-saving rules.

%prep
%setup -q -c -n tzdata

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
           backward \
           systemv \
           pacificnew \
           solar87 \
           solar88 \
           solar89"

# Build the "default" version
for zone in $TIMEZONES; do \
  /usr/sbin/zic -d tzgen -L /dev/null -y yearistype.sh ${zone}
done

# Build the "posix" and "right" versions
for zone in $TIMEZONES; do
   /usr/sbin/zic -d tzgen/posix -L /dev/null -y yearistype.sh ${zone}
   /usr/sbin/zic -d tzgen/right -L leapseconds -y tzgen/yearistype.sh ${zone}
done

# Generate a posixrules file
/usr/sbin/zic -d tzgen -p America/New_York

# Replace hardlinks by symlinks
cd tzgen
fdupes -1 -H -q -r . | while read line ; do
    set -- ${line}
    tgt="${1##./}"
    shift
    while [ "$#" != 0 ] ; do
	link="${1##./}"
	reltgt="$(echo $link | sed -e 's,[^/]\+$,,g' -e 's,[^/]\+,..,g')${tgt}"
	ln -sf ${reltgt} ${link}
	shift
    done
done
cd -

%install
rm -fr $RPM_BUILD_ROOT
install -d %{buildroot}%{_datadir}/zoneinfo
cp -r tzgen/* %{buildroot}%{_datadir}/zoneinfo
install -m 644 iso3166.tab %{buildroot}%{_datadir}/zoneinfo
install -m 644 zone.tab %{buildroot}%{_datadir}/zoneinfo

%check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/zoneinfo
