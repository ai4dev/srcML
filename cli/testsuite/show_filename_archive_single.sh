#!/bin/bash

# test framework
source $(dirname "$0")/framework_test.sh

# test get directory
define archive <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.sdml.info/srcML/src" revision="0.8.0" filename="a.cpp.tar">

	<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" revision="0.8.0" language="C++" filename="a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
	<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>

	</unit>
	STDOUT

createfile sub/archive.cpp.xml "$archive"

# TODO: bug #1109
srcml --show-filename sub/archive.cpp.xml
check 3<<< "a.cpp.tar"

srcml --show-filename < sub/archive.cpp.xml
check 3<<< "a.cpp.tar"

# empty
define empty <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.sdml.info/srcML/src" revision="0.8.0" filename=""/>
	STDOUT

createfile sub/archive.cpp.xml "$empty"

srcml --show-filename sub/archive.cpp.xml
check 3<<< ""

srcml --show-filename < sub/archive.cpp.xml
check 3<<< ""

# none
define none <<- 'STDIN'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.sdml.info/srcML/src" revision="0.8.0"/>
	STDIN

createfile sub/archive.cpp.xml "$none"

srcml --show-filename sub/archive.cpp.xml
check_null

srcml --show-filename < sub/archive.cpp.xml
check_null

