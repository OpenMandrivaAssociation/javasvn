%define gcj_support     1


Name:           javasvn
Version:        1.1.0
Release:        %mkrel 1
Epoch:          0
Summary:        Pure Java Subversion client library

Group:          Development/Java
# License located at http://tmate.org/svn/license.html
License:        BSD
URL:            http://tmate.org/svn/
Source0:        http://tmate.org/svn/org.tmatesoft.svn_%{version}.beta5.src.tar.bz2
Source1:        %{name}-license.html
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  ant
BuildRequires:	jpackage-utils >= 0:1.6
%if %{gcj_support}
BuildRequires:		java-gcj-compat-devel
Requires(post):		java-gcj-compat
Requires(postun):	java-gcj-compat
%else
BuildRequires:		java-devel >= 0:1.4.2
%endif

%if %{gcj_support}
ExclusiveArch:		%{ix86} x86_64 ppc ia64
%else
BuildArch:		noarch
%endif

BuildRequires:          ganymed-ssh2 >= 0:209
Requires:               ganymed-ssh2 >= 0:209


%description
JavaSVN is a pure Java Subversion client library. You would like to use JavaSVN
when you need to access or modify Subversion repository from your Java
application, be it a standalone program, plugin or web application. Being a
pure Java program, JavaSVN doesn't need any additional configuration or native
binaries to work on any OS that runs Java.

%package javadoc
Summary:        Javadoc for JavaSVN
Group:          Development/Java

%description javadoc
Javadoc for JavaSVN.


%prep
%setup -q -n %{name}-src-%{version}.beta5
%{__cp} -a %{SOURCE1} license.html

# delete the jars that are in the archive
rm contrib/ganymed/ganymed.jar
ln -sf %{_javadir}/ganymed-ssh2.jar contrib/ganymed/ganymed.jar
rm contrib/junit/junit.jar

# fixing wrong-file-end-of-line-encoding warnings
sed -i 's/\r$//' README.txt doc/examples/*.iml
find doc/examples -name \*.java -exec sed -i 's/\r$//' {} \;


%build
export CLASSPATH=
export OPT_JAR_LIST=
%ant

# Link source files to fix -debuginfo generation.
rm -f org
ln -s javasvn/src/org
rm -f de
ln -s contrib/sequence/src/de


%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
find doc/javadoc -name \*.html -exec sed -i 's/\r$//' {} \;
sed -i 's/\r$//' doc/javadoc/package-list
cp -pr doc/javadoc/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# gcj support
%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

pushd $RPM_BUILD_ROOT%{_javadir}/
ln -s %{name}-%{version}.jar %{name}.jar
popd

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%{_javadir}/*
%doc COPYING README.txt changelog.txt license.html doc/examples

%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}


