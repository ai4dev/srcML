#!/bin/bash

# test framework
source $(dirname "$0")/framework_test.sh

# xslt identity transformation (archive of single file)
define identity_xslt <<- 'STDOUT'
	<xsl:stylesheet
	xmlns="http://www.srcML.org/srcML/src"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:cpp="http://www.srcML.org/srcML/cpp"
	xmlns:src="http://www.srcML.org/srcML/src"
	version="1.0">
	<xsl:template match="@*|node()">
	  <xsl:copy>
	   <xsl:apply-templates select="@*|node()"/>
	  </xsl:copy>
	 </xsl:template>
	</xsl:stylesheet>
	STDOUT

define srcml <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION">
	
	<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="REVISION" language="C++" filename="sub/a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
	<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>

	</unit>
	STDOUT

xmlcheck "$srcml"
createfile sub/a.cpp.xml "$srcml"
createfile identity.xsl "$identity_xslt"

# --xslt=identity.xsl
srcml2src --xslt=identity.xsl sub/a.cpp.xml
checkv2 "$srcml"

srcml2src --xslt=identity.xsl < sub/a.cpp.xml
checkv2 "$srcml"

srcml2src --xslt=identity.xsl sub/a.cpp.xml -o sub/b.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

srcml2src --xslt=identity.xsl -o sub/b.cpp.xml sub/a.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

srcml2src --xslt=identity.xsl -o sub/b.cpp.xml < sub/a.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

# --xslt identity.xsl
srcml2src --xslt identity.xsl sub/a.cpp.xml
checkv2 "$srcml"

srcml2src --xslt identity.xsl < sub/a.cpp.xml
checkv2 "$srcml"

srcml2src --xslt identity.xsl sub/a.cpp.xml -o sub/b.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

srcml2src --xslt identity.xsl -o sub/b.cpp.xml sub/a.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

srcml2src --xslt identity.xsl -o sub/b.cpp.xml < sub/a.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

# --xslt "identity.xsl"
srcml2src --xslt "identity.xsl" sub/a.cpp.xml
checkv2 "$srcml"

srcml2src --xslt "identity.xsl" < sub/a.cpp.xml
checkv2 "$srcml"

srcml2src --xslt "identity.xsl" sub/a.cpp.xml -o sub/b.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

srcml2src --xslt "identity.xsl" -o sub/b.cpp.xml sub/a.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

srcml2src --xslt "identity.xsl" -o sub/b.cpp.xml < sub/a.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

# --xslt="identity.xsl"
srcml2src --xslt="identity.xsl" sub/a.cpp.xml
checkv2 "$srcml"

srcml2src --xslt="identity.xsl" < sub/a.cpp.xml
checkv2 "$srcml"

srcml2src --xslt="identity.xsl" sub/a.cpp.xml -o sub/b.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

srcml2src --xslt="identity.xsl" -o sub/b.cpp.xml sub/a.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"

srcml2src --xslt="identity.xsl" -o sub/b.cpp.xml < sub/a.cpp.xml
checkv2 sub/b.cpp.xml "$srcml"
