%define		mod_name	auth_mysql
%define 	apxs		/usr/sbin/apxs
Summary:	This is the MySQL authentication module for Apache
Summary(cs):	Základní autentizace pro WWW server Apache pomocí MySQL
Summary(da):	Autenticering for webtjeneren Apache fra en MySQL-database
Summary(de):	Authentifizierung für den Apache Web-Server, der eine MySQL-Datenbank verwendet
Summary(es):	Autenticación vía MySQL para Apache
Summary(fr):	Authentification de base pour le serveur Web Apache utilisant une base de données MySQL
Summary(it):	Autenticazione di base per il server Web Apache mediante un database MySQL
Summary(ja):	MySQL ¥Ç¡¼¥¿¥Ù¡¼¥¹¤ò»È¤Ã¤¿ Apache Web ¥µ¡¼¥Ð¡¼¤Ø¤Î´ðËÜÇ§¾Ú
Summary(no):	Autentisering for webtjeneren Apache fra en MySQL-database
Summary(pl):	Modu³ autentykacji MySQL dla Apache
Summary(pt_BR):	Autenticação via MySQL para o Apache
Summary(sv):	Grundläggande autenticering för webbservern Apache med en MySQL-databas
Name:		apache-mod_%{mod_name}
Version:	2.20a
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://web.oyvax.com/src/mod_auth_mysql-%{version}.tar.gz
URL:		http://www.diegonet.com/support/mod_auth_mysql.shtml
BuildRequires:	mysql-devel
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Requires(post,preun):	%{_sbindir}/apxs
Requires:	apache(EAPI)
Requires:	apache-mod_auth
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using mysql RDBMS.

%description -l cs
Balíèek mod_auth_mysql slou¾í pro omezení pøístupu k dokumentùm, které
poskytuje WWW server Apache. Jména a hesla jsou ulo¾ena v databázi
MySQL.

%description -l de
mod_auth_mysql kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschränken, indem es die Daten in
einer MySQL-Datenbank prüft.

%description -l es
mod_auth_mysql puede usarse para limitar el acceso a documentos
servidos por un servidor web verificando datos en una base de datos
MySQL.

%description -l fr
mod_auth_mysql peut être utilisé pour limiter l'accès à des documents
servis par un serveur Web en vérifiant les données dans une base de
données MySQL.

%description -l it
mod_auth_mysql può essere usato per limitare l'accesso a documenti
serviti da un server Web controllando i dati in un database MySQL.

%description -l ja
mod_auth_mysql ¤Ï¡¢MySQL ¥Ç¡¼¥¿¥Ù¡¼¥¹¤Î¥Ç¡¼¥¿¤ò¥Á¥§¥Ã¥¯¤¹¤ë¤³¤È
¤Ë¤è¤Ã¤Æ¡¢Web ¥µ¡¼¥Ð¡¼¤¬Äó¶¡¤¹¤ë¥É¥­¥å¥á¥ó¥È¤Ø¤Î¥¢¥¯¥»¥¹¤òÀ©¸Â¤¹¤ë¤³¤È
¤¬¤Ç¤­¤Þ¤¹¡£

%description -l pl
To jest modu³ autentykacji dla Apache pozwalaj±cy na autentykacjê
klientów HTTP z u¿yciem bazy danych mysql.

%description -l pt_BR
Com o mod_auth_mysql você pode fazer autenticação no Apache usando o
MySQL.

%description -l sv
mod_auth_mysql kan användas för att begränsa åtkomsten till dokument
servade av en webbserver genom att kontrollera data i en
MySQL-databas.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
aclocal
%{__autoconf}
%configure \
	--with-apxs=%{apxs} \
	--with-mysql=%{_prefix}

%{apxs} -c -I %{_includedir}/mysql mod_%{mod_name}.c -o mod_%{mod_name}.so -lmysqlclient

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

gzip -9nf README* USAGE

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_pkglibdir}/*
