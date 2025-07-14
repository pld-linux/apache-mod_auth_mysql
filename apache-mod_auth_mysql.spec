%define		mod_name	auth_mysql
%define		apxs		/usr/sbin/apxs
Summary:	This is the MySQL authentication module for Apache
Summary(cs.UTF-8):	Základní autentizace pro WWW server Apache pomocí MySQL
Summary(da.UTF-8):	Autenticering for webtjeneren Apache fra en MySQL-database
Summary(de.UTF-8):	Authentifizierung für den Apache Web-Server, der eine MySQL-Datenbank verwendet
Summary(es.UTF-8):	Autenticación vía MySQL para Apache
Summary(fr.UTF-8):	Authentification de base pour le serveur Web Apache utilisant une base de données MySQL
Summary(it.UTF-8):	Autenticazione di base per il server Web Apache mediante un database MySQL
Summary(ja.UTF-8):	MySQL データベースを使った Apache Web サーバーへの基本認証
Summary(nb.UTF-8):	Autentisering for webtjeneren Apache fra en MySQL-database
Summary(pl.UTF-8):	Moduł uwierzytelnienia MySQL dla Apache
Summary(pt_BR.UTF-8):	Autenticação via MySQL para o Apache
Summary(sv.UTF-8):	Grundläggande autenticering för webbservern Apache med en MySQL-databas
Name:		apache-mod_%{mod_name}
Version:	4.3.9
Release:	0.2
License:	GPL
Group:		Networking/Daemons/HTTP
Source0:	http://ftp.debian.org/debian/pool/main/liba/libapache-mod-auth-mysql/libapache-mod-auth-mysql_%{version}.orig.tar.gz
# Source0-md5:	9c1ecbe5fb64d4c93444311ff34bfe35
Patch0:		%{name}-ac.patch
# Needs review:
#  https://rhn.redhat.com/errata/RHSA-2009-0259.html
BuildRequires:	security(CVE-2008-2384)
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	apr-util >= 1:1.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_auth
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using MySQL RDBMS.

%description -l cs.UTF-8
Balíček mod_auth_mysql slouží pro omezení přístupu k dokumentům, které
poskytuje WWW server Apache. Jména a hesla jsou uložena v databázi
MySQL.

%description -l de.UTF-8
mod_auth_mysql kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschränken, indem es die Daten in
einer MySQL-Datenbank prüft.

%description -l es.UTF-8
mod_auth_mysql puede usarse para limitar el acceso a documentos
servidos por un servidor web verificando datos en una base de datos
MySQL.

%description -l fr.UTF-8
mod_auth_mysql peut être utilisé pour limiter l'accès à des documents
servis par un serveur Web en vérifiant les données dans une base de
données MySQL.

%description -l it.UTF-8
mod_auth_mysql può essere usato per limitare l'accesso a documenti
serviti da un server Web controllando i dati in un database MySQL.

%description -l ja.UTF-8
mod_auth_mysql は、MySQL データベースのデータをチェックすること
によって、Web サーバーが提供するドキュメントへのアクセスを制限すること
ができます。

%description -l pl.UTF-8
To jest moduł uwierzytelnienia dla Apache pozwalający na
uwierzytelnianie klientów HTTP z użyciem bazy danych MySQL.

%description -l pt_BR.UTF-8
Com o mod_auth_mysql você pode fazer autenticação no Apache usando o
MySQL.

%description -l sv.UTF-8
mod_auth_mysql kan användas för att begränsa åtkomsten till dokument
servade av en webbserver genom att kontrollera data i en
MySQL-databas.

%prep
%setup -q -n mod-auth-mysql-%{version}
%patch -P0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--disable-static \
	--disable-apache13 \
	--enable-apache2 \
	--with-apxs2=%{apxs} \
	--with-mysql=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

libtool install apache2_mod_%{mod_name}.la $RPM_BUILD_ROOT%{_pkglibdir}
rm -f $RPM_BUILD_ROOT%{_pkglibdir}/*.{l,}a

echo 'LoadModule %{mod_name}_module	modules/apache2_mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc DIRECTIVES USAGE
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
