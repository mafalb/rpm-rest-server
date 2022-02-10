%bcond_without check
%global debug_package %{nil}

%global goipath         github.com/restic/rest-server
Version:                0.10.0

%gometa

%global common_description %{expand:
Rest Server is a high performance HTTP server that implements restic's REST backend API. It provides secure and efficient way to backup data remotely, using restic backup client via the rest: URL.}

Name:    rest-server
Release: 2%{?dist}
Summary: High performance HTTP server that implements restic's REST backend API

License: BSD
URL:     %{gourl}
Source0: %{gosource}
Source1: rest-server.logrotate
Source2: rest-server.service
Source3: rest-server.sysconfig
Source4: rest-server.sysusers

# is already fixed in HEAD
Patch0: TestJoin.patch

# from the spec file for restic:
# Restic does not compile for the following archs
ExcludeArch: s390x

BuildRequires: golang(github.com/gorilla/handlers)
BuildRequires: golang(github.com/miolini/datacounter)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus/promhttp)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(goji.io)
BuildRequires: golang(goji.io/middleware)
BuildRequires: golang(goji.io/pat)
BuildRequires: golang(golang.org/x/crypto/bcrypt)
BuildRequires: systemd-rpm-macros

# we need htpasswd command
Requires: httpd-tools

%description
%{common_description}

%prep
%goprep
%patch0 -p1

%build
%gobuild -o %{gobuilddir}/bin/rest-server %{goipath}/cmd/rest-server

%install
# Install rest-server
install -m 755 -vd %{buildroot}%{_libexecdir}
install -p -m 755 %{gobuilddir}/bin/rest-server %{buildroot}%{_libexecdir}

# Install logrotate config
install -m 755 -vd %{buildroot}/etc/logrotate.d
install -m 644 -p %{SOURCE1} %{buildroot}/etc/logrotate.d/rest-server

# Install systemd service file
install -m 755 -vd %{buildroot}%{_unitdir}
install -p -m 755 %{SOURCE2} %{buildroot}%{_unitdir}/rest-server.service

# Install environment file
install -m 755 -vd %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/rest-server

# Install log dir
install -m 700 -vd %{buildroot}%{_localstatedir}/log/rest-server

# Install data dir
install -m 700 -vd %{buildroot}%{_sharedstatedir}/rest-server

%pre
%sysusers_create_compat %{SOURCE4}

%post
if [ $1 -gt 1 ] ; then
install -m 640 -u root -g rest-server %{_sharedstatedir}/rest-server/.htpasswd
fi

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc CHANGELOG.md README.md
%config(noreplace) %{_sysconfdir}/logrotate.d/rest-server
%config(noreplace) %{_sysconfdir}/sysconfig/rest-server
%{_libexecdir}/rest-server
/%{_unitdir}/rest-server.service
%attr(0700,root,root) %dir %{_localstatedir}/log/rest-server
%attr(0700,rest-server,rest-server) %dir %{_sharedstatedir}/rest-server
%{_sysusersdir}/rest-server.conf

%changelog
* Sat Jan 22 2022 Markus Falb <jeremy@mafalb.at> - 0.10.0-1
  Initial Package Build  
