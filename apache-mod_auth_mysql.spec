%define		mod_name	auth_mysql
Summary:	This is the MySQL authentication module for Apache
Summary(es):	Autenticación vía MySQL para Apache
Summary(pl):	Modu³ autentykacji MySQL dla Apache
Summary(pt_BR):	Autenticação via MySQL para o Apache
Name:		apache-mod_%{mod_name}
Version:	0.11
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.kcilink.com/pub/mod_%{mod_name}.c.gz
Source1:	ftp://ftp.kciLink.com/pub/mysql-group-auth.txt
Patch0:		%{name}-name.patch
BuildRequires:	mysql-devel
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache(EAPI)-devel
Prereq:		/usr/sbin/apxs
Requires:	apache(EAPI)
Requires:	apache-mod_auth
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using mysql RDBMS.

%description -l es
Autenticación vía MySQL para Apache.

%description -l pl
To jest modu³ autentykacji dla Apache pozwalaj±cy na autentykacjê
klientów HTTP z u¿yciem bazy danych mysql.

%description -l pt_BR
Com o mod_auth_mysql você pode fazer autenticação no Apache usando o
MySQL.

%prep 
%setup -q -T -c
gzip -dc %{SOURCE0} > mod_%{mod_name}.c
%patch -p1

%build
%{_sbindir}/apxs -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lmysqlclient

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

install %{SOURCE1} .

gzip -9nf *.txt

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
%doc *.gz
%attr(755,root,root) %{_pkglibdir}/*
