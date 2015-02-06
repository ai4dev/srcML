#!/bin/bash

# test framework
source $(dirname "$0")/framework_test.sh

# test
##
# empty with debug
define output <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" revision="0.8.0" language="Java"/>
	STDOUT

define foutput <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" revision="0.8.0" language="Java" filename="sub/a.java"/>
	STDOUT

createfile sub/a.java ""

src2srcml --cpp sub/a.java

check 3<<< "$foutput"

echo -n "" | src2srcml -l Java --cpp -o sub/a.java.xml

check sub/a.java.xml 3<<< "$output"

src2srcml --cpp sub/a.java -o sub/a.java.xml

check sub/a.java.xml 3<<< "$foutput"