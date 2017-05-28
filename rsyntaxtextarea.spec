%{?_javapackages_macros:%_javapackages_macros}

%define oname RSyntaxTextArea
%define name %(echo %oname | tr [:upper:] [:lower:])

Summary:	A syntax highlighting, code folding text editor for Java Swing applications
Name:		rsyntaxtextarea
Version:	2.6.1
Release:	0
License:	BSD
Group:		Development/Java
Url:		https://github.com/bobbylight/%{oname}
Source0:	https://github.com/bobbylight/%{oname}/archive/%{version}/%{name}-%{version}.tar.gz
Patch1:		%{name}-%{version}-gradle-remove-coverall-plugin.patch
BuildArch:	noarch

BuildRequires:	javapackages-local
#BuildRequires:	gradle-local
BuildRequires:	maven-local
BuildRequires:	checkstyle
BuildRequires:	mvn(junit:junit)
BuildRequires:	x11-server-xvfb

Requires:	java-headless

%description
RSyntaxTextArea is a customizable, syntax highlighting text component for
Java Swing applications. Out of the box, it supports syntax highlighting
for 40+ programming languages, code folding, search and replace, and has
add-on libraries for code completion and spell checking. Syntax highlighting
for additional languages can be added via tools such as JFlex.

%files -f .mfiles
%doc src/main/dist/readme.txt
%doc src/main/dist/%{oname}.License.txt

#---------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc src/main/dist/%{oname}.License.txt

#---------------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{version}
# Delete all JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Apply all patches
%patch1 -p1 -b .coverall

%build
xvfb-run -a gradle build javadoc install -x test --offline -s
%mvn_artifact build/poms/pom-default.xml build/libs/%{name}-%{version}.jar

%install
%mvn_install -J build/docs/javadoc

