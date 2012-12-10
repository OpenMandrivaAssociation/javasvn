%define gcj_support     1


Name:           javasvn
Version:        1.1.0
Release:        %mkrel 6
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
BuildRequires:	java-rpmbuild >= 0:1.6
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




%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1.0-6mdv2011.0
+ Revision: 619784
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0:1.1.0-5mdv2010.0
+ Revision: 429596
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0:1.1.0-4mdv2009.0
+ Revision: 247396
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.1.0-2mdv2008.1
+ Revision: 136503
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)


* Tue Oct 31 2006 David Walluck <walluck@mandriva.org> 1.1.0-1mdv2007.0
+ Revision: 74304
- bump release
- 1.1.0.beta5
- Import javasvn

* Fri Sep 01 2006 David Walluck <walluck@mandriva.org> 0:1.1.0-0.3.beta4mdv2007.0
- release

* Tue Aug 29 2006 Robert Marcano <robert@marcanoonline.com> 1.1.0-0.3.beta4
- Rebuild

* Fri Aug 04 2006 Robert Marcano <robert@marcanoonline.com> 1.1.0-0.2.beta4
- Fix bad relase tag

* Tue Aug 01 2006 Robert Marcano <robert@marcanoonline.com> 1.1.0-0.beta4
- Update to upstream version 1.1.0.beta4, required by subclipse 1.1.4

* Sat Jul 29 2006 Robert Marcano <robert@marcanoonline.com> 1.0.6-2
- Rebuilt to pick up the changes in GCJ (bug #200490)

* Tue Jun 27 2006 Robert Marcano <robert@marcanoonline.com> 1.0.6-1
- Update to upstream version 1.0.6

* Mon Jun 26 2006 Robert Marcano <robert@marcanoonline.com> 1.0.4-4
- created javadoc subpackage
- dependency changed from ganymed to ganymed-ssh2

* Mon Jun 12 2006 Robert Marcano <robert@marcanoonline.com> 1.0.4-3
- rpmlint fixes and debuginfo generation workaround
- doc files added

* Mon May 29 2006 Robert Marcano <robert@marcanoonline.com> 1.0.4-2
- review updates

* Mon May 08 2006 Robert Marcano <robert@marcanoonline.com> 1.0.4-1
- initial version

