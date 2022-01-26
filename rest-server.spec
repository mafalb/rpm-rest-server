# https://github.com/restic/restic
%global goipath         github.com/restic/rest-server
Version:                0.10.0

%gometa

%global common_description %{expand:
Rest Server is a high performance HTTP server that implements restic's REST backend API. It provides secure and efficient way to backup data remotely, using restic backup client via the rest: URL.}

%global golicenses    LICENSE


Name:    rest-server
Release: 0%{?dist}
Summary: High performance HTTP server that implements restic's REST backend API
URL:     %{gourl}
License: BSD
Source0: %{gosource}
# TestJoin is already fixed in HEAD
Patch0: TestJoin.patch

# ?
#Restic does not compile for the following archs
ExcludeArch: s390x

# ?
BuildRequires: golang(github.com/coreos/go-systemd/activation)

BuildRequires: golang(github.com/gorilla/handlers)
BuildRequires: golang(github.com/minio/sha256-simd)
BuildRequires: golang(github.com/miolini/datacounter)

BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus/promhttp)

BuildRequires: golang(github.com/spf13/cobra)

# ?
BuildRequires: golang(golang.org/x/crypto/bcrypt)

BuildRequires: golang(github.com/gorilla/handlers)
BuildRequires: golang(github.com/goji/goji)

Requires: restic


%description
%{common_description}

%prep
%goprep
%patch0 -p1


%build
%gobuild -o %{gobuilddir}/bin/%{name} %{goipath}/cmd/%{name}


%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -p -m 755 %{gobuilddir}/bin/%{name} %{buildroot}%{_bindir}


%check
%gocheck


%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/%{name}


%changelog
* Sat Jan 22 2022 Markus Falb <jeremy@mafalb.at> - 0.10.0
  Initial Package Build  
