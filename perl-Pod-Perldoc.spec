%{?scl:%scl_package perl-Pod-Perldoc}

%bcond_without tk

Name:           %{?scl_prefix}perl-Pod-Perldoc
# let's overwrite the module from perl.srpm
Version:        3.25
Release:        367%{?dist}
Summary:        Look up Perl documentation in Pod format
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Pod-Perldoc/
Source0:        http://www.cpan.org/authors/id/M/MA/MALLEN/Pod-Perldoc-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(warnings)
# Run-time:
# Pod::Perldoc::ToMan executes roff
%if 0%{?rhel} < 7
BuildRequires:  groff
%else
BuildRequires:  groff-base
%endif
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(Encode)
BuildRequires:  %{?scl_prefix}perl(Fcntl)
BuildRequires:  %{?scl_prefix}perl(File::Basename)
BuildRequires:  %{?scl_prefix}perl(File::Spec::Functions)
# File::Temp 0.22 not used by tests
# HTTP::Tiny not used by tests
# IO::Handle not used by tests
BuildRequires:  %{?scl_prefix}perl(IO::Select)
# IPC::Open3 not used by tests
BuildRequires:  %{?scl_prefix}perl(parent)
# POD2::Base is optional
# Pod::Checker is not needed if Pod::Simple::Checker is available
BuildRequires:  %{?scl_prefix}perl(Pod::Man) >= 2.18
BuildRequires:  %{?scl_prefix}perl(Pod::Simple::Checker)
BuildRequires:  %{?scl_prefix}perl(Pod::Simple::RTF) >= 3.16
BuildRequires:  %{?scl_prefix}perl(Pod::Simple::XMLOutStream) >= 3.16
BuildRequires:  %{?scl_prefix}perl(Pod::Text)
BuildRequires:  %{?scl_prefix}perl(Pod::Text::Color)
BuildRequires:  %{?scl_prefix}perl(Pod::Text::Termcap)
# Symbol not used by tests
# Text::ParseWords not used by tests
BuildRequires:  %{?scl_prefix}perl(vars)
# Tests:
BuildRequires:  %{?scl_prefix}perl(Test::More)
# Optional tests:
%if !%{defined perl_bootstrap}
%if !%{defined perl_small}
%if %{with tk}
BuildRequires:  %{?scl_prefix}perl(Tk)
# Tk::FcyEntry is optional
BuildRequires:  %{?scl_prefix}perl(Tk::Pod)
%endif
%endif
%endif
# Pod::Perldoc::ToMan executes roff
%if 0%{?rhel} < 7
Requires:       groff
%else
Requires:       groff-base
%endif
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl(File::Temp) >= 0.22
Requires:       %{?scl_prefix}perl(HTTP::Tiny)
Requires:       %{?scl_prefix}perl(IO::Handle)
Requires:       %{?scl_prefix}perl(IPC::Open3)
# POD2::Base is optional
# Pod::Checker is not needed if Pod::Simple::Checker is available
Requires:       %{?scl_prefix}perl(Pod::Simple::Checker)
Requires:       %{?scl_prefix}perl(Pod::Simple::RTF) >= 3.16
Requires:       %{?scl_prefix}perl(Pod::Simple::XMLOutStream) >= 3.16
Requires:       %{?scl_prefix}perl(Text::ParseWords)
# Tk is optional
Requires:       %{?scl_prefix}perl(Symbol)

# Remove underspecified dependencies
%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
%filter_from_requires /^%{?scl_prefix}perl(Pod::Man)$/d
%filter_from_requires /^%{?scl_prefix}perl(Pod::Simple::XMLOutStream)$/d
%filter_from_requires /^%{?scl_prefix}perl(Pod::Simple::RTF)$/d
%?perl_default_filter
}
%else
# RPM 4.9 style
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{?scl_prefix}perl\\((Pod::Man|Pod::Simple::XMLOutStream|Pod::Simple::RTF)\\)$
%endif

%description
perldoc looks up a piece of documentation in .pod format that is embedded
in the perl installation tree or in a perl script, and displays it via
"groff -man | $PAGER". This is primarily used for the documentation for
the perl library modules.

%prep
%setup -q -n Pod-Perldoc-%{version}

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=$RPM_BUILD_ROOT%{?scl:'}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc Changes README
%{_bindir}/perldoc
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Mon Jul 11 2016 Petr Pisar <ppisar@redhat.com> - 3.25-367
- SCL

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.25-349
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Petr Pisar <ppisar@redhat.com> - 3.25-348
- Current generator detects dependency on Encode and Pod::Man properly

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.25-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-2
- Perl 5.22 rebuild

* Fri Feb 13 2015 Petr Pisar <ppisar@redhat.com> - 3.25-1
- 3.25 bump

* Mon Sep 15 2014 Petr Pisar <ppisar@redhat.com> - 3.24-4
- Enable perl(Tk) tests

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.24-3
- Perl 5.20 re-rebuild of bootstrapped packages
- Disable Perl(Tk) tests temporarily until Perl-Tk works with perl-5.20

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.24-2
- Perl 5.20 rebuild

* Fri Aug 22 2014 Petr Pisar <ppisar@redhat.com> - 3.24-1
- 3.24 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Petr Pisar <ppisar@redhat.com> - 3.23-1
- 3.23 bump

* Mon Jan 06 2014 Petr Pisar <ppisar@redhat.com> - 3.21-1
- 3.21 bump

* Mon Oct 07 2013 Petr Pisar <ppisar@redhat.com> - 3.20-7
- Correct perldoc.pod location (bug #1010057)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-6
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 3.20-4
- Specify all dependencies

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.20-3
- Link minimal build-root packages against libperl.so explicitly

* Thu May 23 2013 Petr Pisar <ppisar@redhat.com> - 3.20-2
- Specify all dependencies

* Mon Apr 29 2013 Petr Pisar <ppisar@redhat.com> - 3.20-1
- 3.20 bump

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 3.19.01-1
- 3.19_01 bump

* Mon Jan 28 2013 Petr Pisar <ppisar@redhat.com> - 3.19.00-1
- 3.19 bump

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 3.17.00-241
- Do not build-require perl(Tk) on RHEL >= 7
- Depend on perl(HTTP::Tiny)

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.17.00-240
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.17-8
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 3.17-7
- Perl 5.16 rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 3.17-6
- Require groff-base because Pod::Perldoc::ToMan executes roff

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.17-5
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 3.17-4
- Omit optional Tk tests on bootstrap

* Wed May 30 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.17-3
- conditionalize optional BR tests

* Tue May 15 2012 Petr Pisar <ppisar@redhat.com> - 3.17-2
- Fix perldoc synopsis (bug #821632)

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 3.17-1
- 3.17 bump
- Fix displaying long POD in groff

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> 3.15-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr from spec code.
- perl(Config) BR removed
- Source URL fixed to point to BDFOY author
- Do not require unversioned perl(Pod::Simple::RTF)
