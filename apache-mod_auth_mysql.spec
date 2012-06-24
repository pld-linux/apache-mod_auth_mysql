%define		mod_name	auth_mysql
%define		apxs		/usr/sbin/apxs
Summary:	This is the MySQL authentication module for Apache
Summary(cs):	Z�kladn� autentizace pro WWW server Apache pomoc� MySQL
Summary(da):	Autenticering for webtjeneren Apache fra en MySQL-database
Summary(de):	Authentifizierung f�r den Apache Web-Server, der eine MySQL-Datenbank verwendet
Summary(es):	Autenticaci�n v�a MySQL para Apache
Summary(fr):	Authentification de base pour le serveur Web Apache utilisant une base de donn�es MySQL
Summary(it):	Autenticazione di base per il server Web Apache mediante un database MySQL
Summary(ja):	MySQL �ǡ����١�����Ȥä� Apache Web �����С��ؤδ���ǧ��
Summary(nb):	Autentisering for webtjeneren Apache fra en MySQL-database
Summary(pl):	Modu� uwierzytelnienia MySQL dla Apache
Summary(pt_BR):	Autentica��o via MySQL para o Apache
Summary(sv):	Grundl�ggande autenticering f�r webbservern Apache med en MySQL-databas
Name:		apache-mod_%{mod_name}
Version:	4.3.9
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.debian.org/debian/pool/main/liba/libapache-mod-auth-mysql/libapache-mod-auth-mysql_%{version}.orig.tar.gz
# Source0-md5:	9c1ecbe5fb64d4c93444311ff34bfe35
Patch0:		%{name}-ac.patch
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	apr-util >= 1:1.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mysql-devel
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_auth
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using MySQL RDBMS.

%description -l cs
Bal��ek mod_auth_mysql slou�� pro omezen� p��stupu k dokument�m, kter�
poskytuje WWW server Apache. Jm�na a hesla jsou ulo�ena v datab�zi
MySQL.

%description -l de
mod_auth_mysql kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschr�nken, indem es die Daten in
einer MySQL-Datenbank pr�ft.

%description -l es
mod_auth_mysql puede usarse para limitar el acceso a documentos
servidos por un servidor web verificando datos en una base de datos
MySQL.

%description -l fr
mod_auth_mysql peut �tre utilis� pour limiter l'acc�s � des documents
servis par un serveur Web en v�rifiant les donn�es dans une base de
donn�es MySQL.

%description -l it
mod_auth_mysql pu� essere usato per limitare l'accesso a documenti
serviti da un server Web controllando i dati in un database MySQL.

%description -l ja
mod_auth_mysql �ϡ�MySQL �ǡ����١����Υǡ���������å����뤳��
�ˤ�äơ�Web �����С����󶡤���ɥ�����ȤؤΥ������������¤��뤳��
���Ǥ��ޤ���

%description -l pl
To jest modu� uwierzytelnienia dla Apache pozwalaj�cy na
uwierzytelnianie klient�w HTTP z u�yciem bazy danych MySQL.

%description -l pt_BR
Com o mod_auth_mysql voc� pode fazer autentica��o no Apache usando o
MySQL.

%description -l sv
mod_auth_mysql kan anv�ndas f�r att begr�nsa �tkomsten till dokument
servade av en webbserver genom att kontrollera data i en
MySQL-databas.

%prep
%setup -q -n mod-auth-mysql-%{version}
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--disable-apache13 \
	--enable-apache2 \
	--with-apxs2=%{apxs} \
	--with-mysql=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

libtool install apache2_mod_%{mod_name}.la $RPM_BUILD_ROOT%{_pkglibdir}
rm -f $RPM_BUILD_ROOT%{_pkglibdir}/*.{l,}a

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc DIRECTIVES USAGE
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
