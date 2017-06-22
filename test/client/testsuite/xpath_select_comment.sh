#!/bin/bash

# test framework
source $(dirname "$0")/framework_test.sh

# test
define input <<- 'INPUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION">

	<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="REVISION" language="C++" filename="a.cpp"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	<!-- Comment Two -->
	</unit>

	<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="REVISION" language="C++" filename="b.cpp"><expr_stmt><expr><name>b</name></expr>;</expr_stmt>
	<!-- Comment Two -->
	</unit>

	</unit>
	INPUT

define output <<- 'OUTPUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION">

	<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="REVISION" language="C++" filename="a.cpp" item="1"><!-- Comment Two --></unit>

	<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="REVISION" language="C++" filename="b.cpp" item="1"><!-- Comment Two --></unit>

	</unit>
	OUTPUT

xmlcheck "$input"
xmlcheck "$output"

createfile sub/archive.xml "$input"

srcml --xpath "//comment()" <<< "$input"
checkv2 "$output"

srcml sub/archive.xml --xpath "//comment()"
checkv2 "$output"

srcml --xpath "//comment()" sub/archive.xml
checkv2 "$output"

srcml sub/archive.xml --xpath "//comment()" -o sub/a.xml
checkv2 sub/a.xml "$output"

srcml --xpath "//comment()" sub/archive.xml -o sub/a.xml
checkv2 sub/a.xml "$output"

srcml sub/archive.xml -o sub/a.xml --xpath "//comment()"
checkv2 sub/a.xml "$output"

srcml --xpath "//comment()" -o sub/a.xml sub/archive.xml
checkv2 sub/a.xml "$output"

srcml -o sub/a.xml sub/archive.xml --xpath "//comment()"
checkv2 sub/a.xml "$output"

srcml -o sub/a.xml --xpath "//comment()" sub/archive.xml
checkv2 sub/a.xml "$output"
