%bcond_without check
%global debug_package %{nil}

%global goipath         github.com/restic/rest-server
Version:                0.10.0

%gometa

%global common_description %{expand:
Rest Server is a high performance HTTP server that implements restic's REST backend API. It provides secure and efficient way to backup data remotely, using restic backup client via the rest: URL.}

Name:    rest-server
Release: 1%{?dist}
Summary: High performance HTTP server that implements restic's REST backend API

License: BSD
URL:     %{gourl}
Source0: %{gosource}

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

Requires: restic

%description
%{common_description}

%prep
%goprep
%patch0 -p1

%build
%gobuild -o %{gobuilddir}/bin/rest-server %{goipath}/cmd/rest-server

%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -p -m 755 %{gobuilddir}/bin/rest-server %{buildroot}%{_bindir}

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/rest-server

%changelog
* Sat Jan 22 2022 Markus Falb <jeremy@mafalb.at> - 0.10.0-1
  Initial Package Build  
