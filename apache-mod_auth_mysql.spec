%define		mod_name	auth_mysql
Summary:	This is the MySQL authentication module for Apache
Summary(pl):	Modu³ autentykacji MySQL dla Apache
Name:		apache-mod_%{mod_name}
Version:	0.3
Release:	3
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.kcilink.com/pub/mod_%{mod_name}.c.gz
Patch0:		%{name}-name.patch
BuildRequires:	mysql-devel
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache(EAPI)-devel
Prereq:		/usr/sbin/apxs
Requires:	apache(EAPI)
URL:		http://modntlm.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using mysql RDBMS.

%description -l pl
To jest modu³ autentykacji dla Apache pozwalaj±cy na autentykacjê
klientów HTTP z u¿yciem bazy danych mysql.

%prep 
%setup -q -T -c
gzip -dc %{SOURCE0} > mod_%{mod_name}.c
%patch -p1

%build
/usr/sbin/apxs -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lmysqlclient

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
