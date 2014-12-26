#!/usr/bin/python
#
# clitest.py
#
# Michael L. Collard
# collard@cs.kent.edu

from testclialpha import *
from defaults import *

limit = 0
if len(sys.argv) > 1:
        globals()["limit"] = int(sys.argv[1])

# test
##
# empty default
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++'], "", srcml)

# test
##
# empty with debug
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:err="http://www.sdml.info/srcML/srcerr" language="C++"/>
"""
checkallforms(src2srcml, option.DEBUG_FLAG_SHORT, option.DEBUG_FLAG, "", "", srcml)

# test
##
# language flag
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

checkallforms(src2srcml, option.LANGUAGE_FLAG_SHORT, option.LANGUAGE_FLAG, "C++", "", srcml)


# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C"/>
"""
checkallforms(src2srcml, option.LANGUAGE_FLAG_SHORT, option.LANGUAGE_FLAG, "C", "", srcml)


# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" language="Java"/>
"""
checkallforms(src2srcml, option.LANGUAGE_FLAG_SHORT, option.LANGUAGE_FLAG, "Java", "", srcml)

# test
##
# filename flag
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="foo"/>
"""
checkallforms(src2srcml, option.FILENAME_FLAG_SHORT, option.FILENAME_FLAG, "foo", "", srcml)

# test
# filenames are not expanded if specified (unlike when extracted from name)
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="bar/foo"/>
"""
checkallforms(src2srcml, option.FILENAME_FLAG_SHORT, option.FILENAME_FLAG, "bar/foo", "", srcml)

# test
# filename and directory specified
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="bar" filename="foo"/>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.FILENAME_FLAG_SHORT, "foo", option.DIRECTORY_FLAG_SHORT, "bar"], "", srcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="bar" filename="foo"/>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.DIRECTORY_FLAG_SHORT, "bar", option.FILENAME_FLAG_SHORT, "foo"], "", srcml)

# test
##
# directory flag
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="bar"/>
"""
checkallforms(src2srcml, option.DIRECTORY_FLAG_SHORT, option.DIRECTORY_FLAG, "bar", "", srcml)


# test
##
# version flag
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" version="1.0"/>
"""
checkallforms(src2srcml, option.SRCVERSION_FLAG_SHORT, option.SRCVERSION_FLAG, "1.0", "", srcml)

# test
##
# xml encoding flag
srcml = """<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""
checkallforms(src2srcml, option.ENCODING_FLAG_SHORT, option.ENCODING_FLAG, "ISO-8859-1", "", srcml)

# test
##
# create testing files
if not os.path.exists("sub"):
        os.system("mkdir sub")

sfile1 = """
a;
"""

sxmlfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++'], sfile1, sxmlfile1)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "-", "-o", "sub/a.cpp.xml"], sfile1, "")


# test
sfile2 = """
b;
"""

sxmlfile2 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++'], sfile2, sxmlfile2)

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "-", "-o", "sub/b.cpp.xml"], sfile2, "")

# test
nestedfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

</unit>
"""

nestedfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/b.cpp" hash="aecf18b52d520ab280119febd8ff6c803135ddfc">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

nestedfilesrc = xml_declaration + """
<src:unit xmlns:src="http://www.sdml.info/srcML/src">

<src:unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<src:expr_stmt><src:expr><src:name>a</src:name></src:expr>;</src:expr_stmt>
</src:unit>

<src:unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/b.cpp">
<src:expr_stmt><src:expr><src:name>b</src:name></src:expr>;</src:expr_stmt>
</src:unit>

</src:unit>
"""

if not os.path.exists("sub"):
        os.mkdir("sub")

f = open("sub/a.cpp", "w")
f.write("\na;\n")
f.close()

f = open("sub/b.cpp", "w")
f.write("\nb;\n")
f.close()

check([src2srcml, "sub/a.cpp", "sub/b.cpp", "-o", "-"], "", nestedfile)

check([src2srcml, option.COMPOUND_FLAG, "sub/a.cpp", "-o", "-"], "", nestedfile1)

filelist = """
sub/a.cpp
# fff
sub/b.cpp
"""

f = open('filelistab', 'w')
f.write("\nsub/a.cpp\nsub/b.cpp\n\n")
f.close()

check([src2srcml, option.FILELIST_FLAG, "filelistab"], "", nestedfile)


# test
####
# srcml2src

src = """
a;
"""

srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(srcml)
f.close()

check([srcml2src], srcml, src)
check([srcml2src, 'sub/a.cpp.xml'], "", src)

srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="bar" filename="foo" version="1.2"/>
"""

checkallforms(srcml2src, "", option.LANGUAGE_DISPLAY_FLAG, "", srcml, "C++\n")
checkallforms(srcml2src, "", option.DIRECTORY_DISPLAY_FLAG, "", srcml, "bar\n")
checkallforms(srcml2src, "", option.FILENAME_DISPLAY_FLAG, "", srcml, "foo\n")
checkallforms(srcml2src, "", option.SRCVERSION_DISPLAY_FLAG, "", srcml, "1.2\n")
checkallforms(srcml2src, "", option.ENCODING_DISPLAY_FLAG, "", srcml, default_srcml2src_encoding + "\n")

srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="" dir="" filename="" version=""/>
"""

checkallforms(srcml2src, "", option.LANGUAGE_DISPLAY_FLAG, "", srcml, "\n")
checkallforms(srcml2src, "", option.DIRECTORY_DISPLAY_FLAG, "", srcml, "\n")
checkallforms(srcml2src, "", option.FILENAME_DISPLAY_FLAG, "", srcml, "\n")
checkallforms(srcml2src, "", option.SRCVERSION_DISPLAY_FLAG, "", srcml, "\n")

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp"/>
"""

checkallforms(srcml2src, "", option.LANGUAGE_DISPLAY_FLAG, "", srcml, "")
checkallforms(srcml2src, "", option.DIRECTORY_DISPLAY_FLAG, "", srcml, "")
checkallforms(srcml2src, "", option.FILENAME_DISPLAY_FLAG, "", srcml, "")
checkallforms(srcml2src, "", option.SRCVERSION_DISPLAY_FLAG, "", srcml, "")

check([srcml2src, option.NESTED_FLAG], srcml, "0\n")
check([srcml2src, option.NESTED_FLAG], nestedfile, "2\n")

check([srcml2src, option.NESTED_FLAG], nestedfilesrc, "2\n")

checkallforms(srcml2src, option.UNIT_FLAG_SHORT, option.UNIT_FLAG, "1", nestedfile, sfile1)
check([srcml2src, option.UNIT_FLAG, "1", "-"], nestedfile, sfile1)

checkallforms(srcml2src, option.UNIT_FLAG_SHORT, option.UNIT_FLAG, "2", nestedfile, sfile2)
check([srcml2src, option.UNIT_FLAG, "2"], nestedfile, sfile2)

# test
sxmlfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

nestedfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="b.cpp">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", "-"], nestedfile, sxmlfile1)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1"], nestedfile, sxmlfile1)

sxmlfile2 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="b.cpp">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>
"""
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", "-"], nestedfile, sxmlfile2)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2"], nestedfile, sxmlfile2)

# test
if platform.system() != "Windows" :
        os.system("rm -f sub/a.cpp")
else :
        os.system("del sub\\a.cpp")

#remove
if platform.system() != "Windows" and sys.platform != 'cygwin' :
        checkNoOutput([srcml2src, option.TO_DIR_FLAG + '=.'], sxmlfile1)

        validate(open("sub/a.cpp", "r").read(), sfile1)

#remove
if platform.system() != "Windows" and sys.platform != 'cygwin' :
        os.system("rm -f sub/a.cpp sub/b.cpp;")
else :
        os.system("del sub\\a.cpp sub\\b.cpp")

if platform.system() != "Windows" and sys.platform != 'cygwin' :
        checkNoOutput([srcml2src, option.TO_DIR_FLAG + '=.'], nestedfile)

        validate(open("sub/a.cpp", "r").read(), sfile1)
        validate(open("sub/b.cpp", "r").read(), sfile2)

#os.system("rm -f sub/a.cpp sub/b.cpp")

#checkNoOutput([srcml2src, option.TO_DIR_FLAG_SHORT, '.'], nestedfile)

#validate(open("sub/a.cpp", "r").read(), sfile1)
#validate(open("sub/b.cpp", "r").read(), sfile2)

# srcml2src extract nested unit
nestedfileextra = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C" dir="sub" filename="a.cpp" mytag="foo">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="Java" dir="sub" filename="b.cpp" mytag="foo">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

sxmlfile1extra = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C" dir="sub" filename="a.cpp" mytag="foo">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", "-"], nestedfileextra, sxmlfile1extra)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1"], nestedfileextra, sxmlfile1extra)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.FILENAME_DISPLAY_FLAG], nestedfileextra, "a.cpp\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.FILENAME_DISPLAY_FLAG], nestedfileextra, "b.cpp\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.DIRECTORY_DISPLAY_FLAG], nestedfileextra, "sub\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.DIRECTORY_DISPLAY_FLAG], nestedfileextra, "sub\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.LANGUAGE_DISPLAY_FLAG], nestedfileextra, "C\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.LANGUAGE_DISPLAY_FLAG], nestedfileextra, "Java\n")

# test
# srcml2src extract nested unit
nestedfileextra = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:lc="http://www.sdml.info/srcML/linecol" language="C++">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C" dir="sub" filename="a.cpp" mytag="foo">
<expr_stmt lc:line="1"><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="Java" dir="sub" filename="b.cpp" mytag="foo">
<expr_stmt lc:line="1"><expr><name>b</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="c.cpp" mytag="foo">
<expr_stmt lc:line="1"><expr><name>c</name></expr>;</expr_stmt>
</unit>

</unit>
"""

sxmlfile1extra = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lc="http://www.sdml.info/srcML/linecol" language="C" dir="sub" filename="a.cpp" mytag="foo">
<expr_stmt lc:line="1"><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

sxmlfile2extra = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lc="http://www.sdml.info/srcML/linecol" language="Java" dir="sub" filename="b.cpp" mytag="foo">
<expr_stmt lc:line="1"><expr><name>b</name></expr>;</expr_stmt>
</unit>
"""

sxmlfile3extra = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lc="http://www.sdml.info/srcML/linecol" language="C++" dir="sub" filename="c.cpp" mytag="foo">
<expr_stmt lc:line="1"><expr><name>c</name></expr>;</expr_stmt>
</unit>
"""

check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", "-"], nestedfileextra, sxmlfile1extra)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1"], nestedfileextra, sxmlfile1extra)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", "-"], nestedfileextra, sxmlfile2extra)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2"], nestedfileextra, sxmlfile2extra)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "3", "-"], nestedfileextra, sxmlfile3extra)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "3"], nestedfileextra, sxmlfile3extra)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.FILENAME_DISPLAY_FLAG], nestedfileextra, "a.cpp\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.FILENAME_DISPLAY_FLAG], nestedfileextra, "b.cpp\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.DIRECTORY_DISPLAY_FLAG], nestedfileextra, "sub\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.DIRECTORY_DISPLAY_FLAG], nestedfileextra, "sub\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.LANGUAGE_DISPLAY_FLAG], nestedfileextra, "C\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.LANGUAGE_DISPLAY_FLAG], nestedfileextra, "Java\n")

##
# src2srcml error return

# invalid input filename
#validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "foobar"], None), status.STATUS_INPUTFILE_PROBLEM)

# invalid input filename (repeat in output)
#validate(getreturn([src2srcml, "sub/a.cpp", "-o", "sub/a.cpp"], None), status.STATUS_INPUTFILE_PROBLEM)

# unknown option
#validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--strip", "foobar"], None), status.STATUS_UNKNOWN_OPTION)

# unknown encoding

# test
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.SRC_ENCODING_FLAG + "=" + bad_encoding, "foobar"], None), status.STATUS_UNKNOWN_ENCODING)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.ENCODING_FLAG + "=" + bad_encoding, "foobar"], None), status.STATUS_UNKNOWN_ENCODING)
        
# missing value
validate(getreturn([src2srcml, option.LANGUAGE_FLAG, bad_language, "foobar"], None), status.STATUS_INVALID_LANGUAGE)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG], None), status.STATUS_LANGUAGE_MISSING)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.FILENAME_FLAG], ""), status.STATUS_FILENAME_MISSING)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.DIRECTORY_FLAG], ""), status.STATUS_DIRECTORY_MISSING)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.SRCVERSION_FLAG], ""), status.STATUS_VERSION_MISSING)

# source encoding not given
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.SRC_ENCODING_FLAG], ""), status.STATUS_SRCENCODING_MISSING)

validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.ENCODING_FLAG], ""), status.STATUS_XMLENCODING_MISSING)

# test
##
# srcml2src error return

# invalid input filename
if sys.platform != 'cygwin' :
        validate(getreturn([srcml2src, "foobar"], None), status.STATUS_INPUTFILE_PROBLEM)

# unknown option
validate(getreturn([srcml2src, "--strip", "foobar"], None), status.STATUS_UNKNOWN_OPTION)

# unknown encoding
validate(getreturn([srcml2src, option.SRC_ENCODING_FLAG + "=" + bad_encoding], ""), status.STATUS_UNKNOWN_ENCODING)
validate(getreturn([srcml2src, option.SRC_ENCODING_FLAG], ""), status.STATUS_SRCENCODING_MISSING)
        
# source encoding not given

# unit option selected but no value
validate(getreturn([srcml2src, option.UNIT_FLAG], ""), status.STATUS_UNIT_MISSING)

# unit value too large

missing_unit = "3";
if sys.platform != 'cygwin' :
        validate(getreturn([srcml2src, option.UNIT_FLAG, missing_unit], nestedfile), status.STATUS_UNIT_INVALID)
        validate(getreturn([srcml2src, option.UNIT_FLAG, missing_unit, option.XML_FLAG], nestedfile), status.STATUS_UNIT_INVALID)
        validate(getreturn([srcml2src, option.UNIT_FLAG, missing_unit, option.FILENAME_DISPLAY_FLAG], nestedfile), status.STATUS_UNIT_INVALID)
        validate(getreturn([srcml2src, option.UNIT_FLAG, missing_unit, option.DIRECTORY_DISPLAY_FLAG], nestedfile), status.STATUS_UNIT_INVALID)
        validate(getreturn([srcml2src, option.UNIT_FLAG, missing_unit, option.SRCVERSION_DISPLAY_FLAG], nestedfile), status.STATUS_UNIT_INVALID)

# invalid combinations
validate(getreturn([srcml2src, option.XML_FLAG, option.SRC_ENCODING_FLAG, "UTF-8", "foobar"], None), status.STATUS_INVALID_OPTION_COMBINATION)

print "HELLO"

# test
##
# cpp markup else

cpp_src = """
#if A
break;
#else
return;
#endif
"""

cpp_marked_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><name>A</name></expr></cpp:if>
<break>break;</break>
<cpp:else>#<cpp:directive>else</cpp:directive></cpp:else>
<return>return;</return>
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++'], cpp_src, cpp_marked_srcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_MARKUP_ELSE_FLAG], cpp_src, cpp_marked_srcml)


cpp_textonly_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><name>A</name></expr></cpp:if>
<break>break;</break>
<cpp:else>#<cpp:directive>else</cpp:directive></cpp:else>
return;
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_TEXTONLY_ELSE_FLAG], cpp_src, cpp_textonly_srcml)

validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_MARKUP_ELSE_FLAG, option.CPP_TEXTONLY_ELSE_FLAG, "foobar"], None), status.STATUS_INVALID_OPTION_COMBINATION)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_TEXTONLY_ELSE_FLAG, option.CPP_MARKUP_ELSE_FLAG, "foobar"], None), status.STATUS_INVALID_OPTION_COMBINATION)

# test
##
# cpp markup if0

cpp_if0 = """
#if 0
break;
#endif
"""

cpp_textonly_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><literal type="number">0</literal></expr></cpp:if>
break;
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++'], cpp_if0, cpp_textonly_srcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_TEXTONLY_IF0_FLAG], cpp_if0, cpp_textonly_srcml)

cpp_marked_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><literal type="number">0</literal></expr></cpp:if>
<break>break;</break>
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_MARKUP_IF0_FLAG], cpp_if0, cpp_marked_srcml)

validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_MARKUP_IF0_FLAG, option.CPP_TEXTONLY_IF0_FLAG, "foobar"], None), status.STATUS_INVALID_OPTION_COMBINATION)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_TEXTONLY_IF0_FLAG, option.CPP_MARKUP_IF0_FLAG, "foobar"], None), status.STATUS_INVALID_OPTION_COMBINATION)

# test
##
# xmlns options

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

# separate
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--xmlns=http://www.sdml.info/srcML/src"], "", srcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--xmlns:cpp=http://www.sdml.info/srcML/cpp"], "", srcml)

# multiple
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp"], "", srcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:err="http://www.sdml.info/srcML/srcerr" language="C++"/>
"""

# separate
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", "--xmlns:err=http://www.sdml.info/srcML/srcerr"], "", srcml)

# multiple
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp"], "", srcml)

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:err=http://www.sdml.info/srcML/srcerr"], "", srcml)

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--debug", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", "--xmlns:err=http://www.sdml.info/srcML/srcerr"], "", srcml)

# test
srcml = xml_declaration + """
<src:unit xmlns:src="http://www.sdml.info/srcML/src" xmlns="http://www.sdml.info/srcML/cpp" language="C++"/>
"""
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--xmlns:src=http://www.sdml.info/srcML/src", "--xmlns=http://www.sdml.info/srcML/cpp"], "", srcml)

##
# prefix extraction
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp"/>
"""

checkallforms(srcml2src, option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.sdml.info/srcML/src", srcml, """
""")

checkallforms(srcml2src, option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.sdml.info/srcML/cpp", srcml, """cpp
""")

checkallforms(srcml2src, option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.sdml.info/srcML/literal", srcml, "")

checkallforms(srcml2src, option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.cs.uakron.edu/~collard/foo", srcml, "")

# test
srcml = xml_declaration + """
<unit xmlns:cpp="http://www.sdml.info/srcML/src" xmlns="http://www.sdml.info/srcML/cpp"/>
"""

checkallforms(srcml2src, option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.sdml.info/srcML/src", srcml, """cpp""")

checkallforms(srcml2src, option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.sdml.info/srcML/cpp", srcml, """""")

# test
##
# no xml declaration
srcml = """<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.NO_XML_DECLARATION_FLAG], "", srcml)

# test
##
# no namespace declaration
srcml = xml_declaration + """
<unit language="C++"/>
"""

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.NO_NAMESPACE_DECLARATION_FLAG], "", srcml)

# test
##
# check missingfile
srcml = "srcml: Unable to open file foo.c\n"

checkError([src2srcml, 'foo.c'], "", srcml)

# test
srcml = "srcml: Unable to open file abc.c\n"

checkError([src2srcml, 'abc.c'], "", srcml)

# test
srcml = "srcml: Unable to open file ../src/foo.c\n"

checkError([src2srcml, '../src/foo.c'], "", srcml)

# test
##
# check correct language based on file extension

xmltag = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
opentag = '<unit '
namespaceone = 'xmlns="http://www.sdml.info/srcML/src" '
namespacetwo = 'xmlns:cpp="http://www.sdml.info/srcML/cpp" '
fileopen = 'filename="emptysrc/'
fileclose = '"'
endtag = '/>\n'

# check c file extensions
language = 'language="C" '

check([src2srcml, 'emptysrc/empty.c'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.c' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.h'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.h' + fileclose + endtag)

check([src2srcml, 'emptysrc/empty.c.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.c.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.h.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.h.gz' + fileclose + endtag)

# check c++ file extensions
language = 'language="C++" '

check([src2srcml, 'emptysrc/empty.cpp'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.cpp' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.cc'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.cc' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.cxx'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.cxx' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.c++'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.c++' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.hpp'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.hpp' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.hh'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.hh' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.hxx'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.hxx' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.h++'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.h++' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.tcc'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.tcc' + fileclose + endtag)

check([src2srcml, 'emptysrc/empty.cpp.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.cpp.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.cc.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.cc.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.cxx.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.cxx.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.c++.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.c++.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.hpp.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.hpp.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.hh.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.hh.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.hxx.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.hxx.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.h++.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.h++.gz' + fileclose + endtag)
check([src2srcml, 'emptysrc/empty.tcc.gz'], "", xmltag + opentag + namespaceone + namespacetwo + language  + fileopen + 'empty.tcc.gz' + fileclose + endtag)

# check java file extension
language = 'language="Java" '

check([src2srcml, 'emptysrc/empty.java'], "", xmltag + opentag + namespaceone + language  + fileopen + 'empty.java' + fileclose + endtag)

check([src2srcml, 'emptysrc/empty.java.gz'], "", xmltag + opentag + namespaceone + language  + fileopen + 'empty.java.gz' + fileclose + endtag)

# check aspectj file extension
language = 'language="AspectJ" '

check([src2srcml, 'emptysrc/empty.aj'], "", xmltag + opentag + namespaceone + language  + fileopen + 'empty.aj' + fileclose + endtag)

check([src2srcml, 'emptysrc/empty.aj.gz'], "", xmltag + opentag + namespaceone + language  + fileopen + 'empty.aj.gz' + fileclose + endtag)

# test
##
# Test output options

# src2srcml
sfile = """
a;
"""

sxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

fxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

f = open('sub/a.cpp', 'w')
f.write(sfile)
f.close()

check([src2srcml, 'sub/a.cpp', '--output', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fxmlfile)
check([src2srcml, 'sub/a.cpp', '--output=sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fxmlfile)
check([src2srcml, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fxmlfile)

if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-', '-o', 'sub/a.cpp.xml'], sfile, "")
        validate(open('sub/a.cpp.xml', 'r').read(), sxmlfile)
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-o', 'sub/a.cpp.xml'], sfile, "")
        validate(open('sub/a.cpp.xml', 'r').read(), sxmlfile)

# non-windows
if platform.system() != "Windows" :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-', '--output', '/dev/stdout'], sfile, sxmlfile)
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-', '--output=/dev/stdout'], sfile, sxmlfile)
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-', '-o', '/dev/stdout'], sfile, sxmlfile)

# test
# srcml2src

check([srcml2src, 'sub/a.cpp.xml', '--output', 'sub/a.cpp'], "", "")
validate(open('sub/a.cpp', 'r').read(), sfile)
check([srcml2src, 'sub/a.cpp.xml', '--output=sub/a.cpp'], "", "")
validate(open('sub/a.cpp', 'r').read(), sfile)
check([srcml2src, 'sub/a.cpp.xml', '-o', 'sub/a.cpp'], "", "")
validate(open('sub/a.cpp', 'r').read(), sfile)

check([srcml2src, '-', '-o', 'sub/a.cpp'], sxmlfile, "")
validate(open('sub/a.cpp', 'r').read(), sfile)
check([srcml2src, '-o', 'sub/a.cpp'], sxmlfile, "")
validate(open('sub/a.cpp', 'r').read(), sfile)


# non-windows
if platform.system() != "Windows" :
        check([srcml2src, '-', '--output', '/dev/stdout'], sxmlfile, sfile)
        check([srcml2src, '-', '--output=/dev/stdout'], sxmlfile, sfile)
        check([srcml2src, '-', '-o', '/dev/stdout'], sxmlfile, sfile)

# test
##
# Test src2srcml options with files

sfile1 = ""

sfile2 = """
b;
"""

f = open('sub/a.cpp', 'w')
f.write(sfile1)
f.close()

# test
##
# empty with debug
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:err="http://www.sdml.info/srcML/srcerr" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:err="http://www.sdml.info/srcML/srcerr" language="C++" filename="sub/a.cpp"/>
"""
checkallformsfile(src2srcml, 'sub/a.cpp', option.DEBUG_FLAG_SHORT, option.DEBUG_FLAG, "", "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.DEBUG_FLAG_SHORT, '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.DEBUG_FLAG_SHORT, 'sub/a.cpp','-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
##
# language flag
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp"/>
"""
checkallformsfile(src2srcml, 'sub/a.cpp', option.LANGUAGE_FLAG_SHORT, option.LANGUAGE_FLAG, "C++", "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', 'sub/a.cpp','-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C" filename="sub/a.cpp"/>
"""
checkallformsfile(src2srcml, 'sub/a.cpp', option.LANGUAGE_FLAG_SHORT, option.LANGUAGE_FLAG, "C", "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C', '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C', 'sub/a.cpp','-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" language="Java"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" language="Java" filename="sub/a.cpp"/>
"""
checkallformsfile(src2srcml, 'sub/a.cpp', option.LANGUAGE_FLAG_SHORT, option.LANGUAGE_FLAG, "Java", "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'Java', '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'Java', 'sub/a.cpp','-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
##
# filename flag
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="foo.cpp"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="foo.cpp"/>
"""
checkallformsfile(src2srcml, 'sub/a.cpp', option.FILENAME_FLAG_SHORT, option.FILENAME_FLAG, "foo.cpp", "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.FILENAME_FLAG_SHORT, 'foo.cpp', '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.FILENAME_FLAG_SHORT, 'foo.cpp', 'sub/a.cpp','-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
##
# directory flag
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="bar"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="bar" filename="sub/a.cpp"/>
"""
checkallformsfile(src2srcml, 'sub/a.cpp', option.DIRECTORY_FLAG_SHORT, option.DIRECTORY_FLAG, "bar", "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.DIRECTORY_FLAG_SHORT, 'bar', '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.DIRECTORY_FLAG_SHORT, 'bar', 'sub/a.cpp','-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
##
# version flag
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" version="1.0"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp" version="1.0"/>
"""
checkallformsfile(src2srcml, 'sub/a.cpp', option.SRCVERSION_FLAG_SHORT, option.SRCVERSION_FLAG, "1.0", "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.SRCVERSION_FLAG_SHORT, '1.0', '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.SRCVERSION_FLAG_SHORT, '1.0', 'sub/a.cpp','-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

##
# xml encoding flag
# test
srcml = """<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

fsrcml = """<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp"/>
"""
checkallformsfile(src2srcml, 'sub/a.cpp', option.ENCODING_FLAG_SHORT, option.ENCODING_FLAG, "ISO-8859-1", "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.ENCODING_FLAG_SHORT, 'ISO-8859-1', '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.ENCODING_FLAG_SHORT, 'ISO-8859-1', 'sub/a.cpp','-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

##
# text encoding flag
# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp"/>
"""
checkallforms(src2srcml, option.SRC_ENCODING_FLAG_SHORT, option.SRC_ENCODING_FLAG, "ISO-8859-1", sfile1, srcml)
checkallformsfile(src2srcml, 'sub/a.cpp', option.SRC_ENCODING_FLAG_SHORT, option.SRC_ENCODING_FLAG, "ISO-8859-1", "", fsrcml)
check([src2srcml, option.SRC_ENCODING_FLAG, "ISO-8859-1", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.SRC_ENCODING_FLAG, "ISO-8859-1", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.SRC_ENCODING_FLAG, "ISO-8859-1", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# nested 

sfile1 = """
a;
"""

sfile2 = """
b;
"""


nestedfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

</unit>
"""

nestedfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/b.cpp" hash="aecf18b52d520ab280119febd8ff6c803135ddfc">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

nestedfilesrc = xml_declaration + """
<src:unit xmlns:src="http://www.sdml.info/srcML/src">

<src:unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
<src:expr_stmt><src:expr><src:name>a</src:name></src:expr>;</src:expr_stmt>
</src:unit>

<src:unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/b.cpp" hash="aecf18b52d520ab280119febd8ff6c803135ddfc">
<src:expr_stmt><src:expr><src:name>b</src:name></src:expr>;</src:expr_stmt>
</src:unit>

</src:unit>
"""

f = open('sub/a.cpp', 'w')
f.write(sfile1)
f.close()

f = open('sub/b.cpp', 'w')
f.write(sfile2)
f.close()

check([src2srcml, option.COMPOUND_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml').read(), nestedfile1)
check([src2srcml, 'sub/a.cpp', 'sub/b.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml').read(), nestedfile)
check([src2srcml, '--xmlns:src=http://www.sdml.info/srcML/src', 'sub/a.cpp', 'sub/b.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml').read(), nestedfilesrc)

# files from
nestedfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/b.cpp" hash="aecf18b52d520ab280119febd8ff6c803135ddfc">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

filelist = """
sub/a.cpp
# fff
sub/b.cpp
"""

f = open('filelistab', 'w')
f.write("\nsub/a.cpp\nsub/b.cpp\n\n")
f.close()

check([src2srcml, option.FILELIST_FLAG, "filelistab", '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), nestedfile)

##
# xmlns options

sfile1 = ""

sfile2 = """
b;
"""

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp"/>
"""

f = open('sub/a.cpp', 'w')
f.write(sfile1)
f.close()

# separate
check([src2srcml, "--xmlns=http://www.sdml.info/srcML/src", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--xmlns=http://www.sdml.info/srcML/src", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, "--xmlns=http://www.sdml.info/srcML/src", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)
check([src2srcml, "--xmlns:cpp=http://www.sdml.info/srcML/cpp", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--xmlns:cpp=http://www.sdml.info/srcML/cpp", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, "--xmlns:cpp=http://www.sdml.info/srcML/cpp", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# multiple
check([src2srcml, "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:err="http://www.sdml.info/srcML/srcerr" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:err="http://www.sdml.info/srcML/srcerr" language="C++" filename="sub/a.cpp"/>
"""

# separate
check([src2srcml, "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", "--xmlns:err=http://www.sdml.info/srcML/srcerr", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", "--xmlns:err=http://www.sdml.info/srcML/srcerr", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", "--xmlns:err=http://www.sdml.info/srcML/srcerr", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# multiple
check([src2srcml, "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

check([src2srcml, "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:err=http://www.sdml.info/srcML/srcerr", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:err=http://www.sdml.info/srcML/srcerr", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, "--debug", "--xmlns=http://www.sdml.info/srcML/src", "--xmlns:err=http://www.sdml.info/srcML/srcerr", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

check([src2srcml, "--debug", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", "--xmlns:err=http://www.sdml.info/srcML/srcerr", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--debug", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", "--xmlns:err=http://www.sdml.info/srcML/srcerr", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, "--debug", "--xmlns:cpp=http://www.sdml.info/srcML/cpp", "--xmlns:err=http://www.sdml.info/srcML/srcerr", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<src:unit xmlns:src="http://www.sdml.info/srcML/src" xmlns="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

fsrcml = xml_declaration + """
<src:unit xmlns:src="http://www.sdml.info/srcML/src" xmlns="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp"/>
"""
check([src2srcml, "--xmlns:src=http://www.sdml.info/srcML/src", "--xmlns=http://www.sdml.info/srcML/cpp", 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', "--xmlns:src=http://www.sdml.info/srcML/src", "--xmlns=http://www.sdml.info/srcML/cpp", '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, "--xmlns:src=http://www.sdml.info/srcML/src", "--xmlns=http://www.sdml.info/srcML/cpp", 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

##
# no xml declaration
# test
srcml = """<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

fsrcml = """<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp"/>
"""

check([src2srcml, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.NO_XML_DECLARATION_FLAG, '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

##
# no namespace declaration
# test
srcml = xml_declaration + """
<unit language="C++"/>
"""

fsrcml = xml_declaration + """
<unit language="C++" filename="sub/a.cpp"/>
"""

check([src2srcml, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp'], "", fsrcml)
check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.NO_NAMESPACE_DECLARATION_FLAG, '-o', 'sub/a.cpp.xml'], sfile1, "")
validate(open('sub/a.cpp.xml', 'r').read(), srcml)
check([src2srcml, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

##
# cpp markup else

cpp_src = """
#if A
break;
#else
return;
#endif
"""

cpp_marked_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><name>A</name></expr></cpp:if>
<break>break;</break>
<cpp:else>#<cpp:directive>else</cpp:directive></cpp:else>
<return>return;</return>
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""

fcpp_marked_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><name>A</name></expr></cpp:if>
<break>break;</break>
<cpp:else>#<cpp:directive>else</cpp:directive></cpp:else>
<return>return;</return>
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""

f = open('sub/a.cpp', 'w')
f.write(cpp_src)
f.close()

check([src2srcml, 'sub/a.cpp'], "", fcpp_marked_srcml)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-o', 'sub/a.cpp.xml'], cpp_src, "")
        validate(open('sub/a.cpp.xml', 'r').read(), cpp_marked_srcml)
check([src2srcml, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fcpp_marked_srcml)

check([src2srcml, option.CPP_MARKUP_ELSE_FLAG, 'sub/a.cpp'], "", fcpp_marked_srcml)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_MARKUP_ELSE_FLAG, '-o', 'sub/a.cpp.xml'], cpp_src, "")
        validate(open('sub/a.cpp.xml', 'r').read(), cpp_marked_srcml)
check([src2srcml, option.CPP_MARKUP_ELSE_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fcpp_marked_srcml)

cpp_textonly_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><name>A</name></expr></cpp:if>
<break>break;</break>
<cpp:else>#<cpp:directive>else</cpp:directive></cpp:else>
return;
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""

fcpp_textonly_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><name>A</name></expr></cpp:if>
<break>break;</break>
<cpp:else>#<cpp:directive>else</cpp:directive></cpp:else>
return;
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""

check([src2srcml, option.CPP_TEXTONLY_ELSE_FLAG, 'sub/a.cpp'], "", fcpp_textonly_srcml)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_TEXTONLY_ELSE_FLAG, '-o', 'sub/a.cpp.xml'], cpp_src, "")
        validate(open('sub/a.cpp.xml', 'r').read(), cpp_textonly_srcml)
check([src2srcml, option.CPP_TEXTONLY_ELSE_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fcpp_textonly_srcml)

##
# cpp markup if0

cpp_if0 = """
#if 0
break;
#endif
"""

cpp_textonly_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><literal type="number">0</literal></expr></cpp:if>
break;
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""

fcpp_textonly_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><literal type="number">0</literal></expr></cpp:if>
break;
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""

f = open('sub/a.cpp', 'w')
f.write(cpp_if0)
f.close()

check([src2srcml, 'sub/a.cpp'], "", fcpp_textonly_srcml)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-o', 'sub/a.cpp.xml'], cpp_if0, "")
        validate(open('sub/a.cpp.xml', 'r').read(), cpp_textonly_srcml)
check([src2srcml, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fcpp_textonly_srcml)

check([src2srcml, option.CPP_TEXTONLY_IF0_FLAG, 'sub/a.cpp'], "", fcpp_textonly_srcml)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_TEXTONLY_IF0_FLAG, '-o', 'sub/a.cpp.xml'], cpp_if0, "")
        validate(open('sub/a.cpp.xml', 'r').read(), cpp_textonly_srcml)
check([src2srcml, option.CPP_TEXTONLY_IF0_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fcpp_textonly_srcml)

cpp_marked_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><literal type="number">0</literal></expr></cpp:if>
<break>break;</break>
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""

fcpp_marked_srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<cpp:if>#<cpp:directive>if</cpp:directive> <expr><literal type="number">0</literal></expr></cpp:if>
<break>break;</break>
<cpp:endif>#<cpp:directive>endif</cpp:directive></cpp:endif>
</unit>
"""

check([src2srcml, option.CPP_MARKUP_IF0_FLAG, 'sub/a.cpp'], "", fcpp_marked_srcml)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.CPP_MARKUP_IF0_FLAG, '-o', 'sub/a.cpp.xml'], cpp_if0, "")
        validate(open('sub/a.cpp.xml', 'r').read(), cpp_marked_srcml)
check([src2srcml, option.CPP_MARKUP_IF0_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml', 'r').read(), fcpp_marked_srcml)

##
# Test srcml2src options with files

sxmlfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp" version="1.2">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

nestedfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

</unit>
"""

nestedfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/b.cpp">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

nestedfilesrc = xml_declaration + """
<src:unit xmlns:src="http://www.sdml.info/srcML/src">

<src:unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<src:expr_stmt><src:expr><src:name>a</src:name></src:expr>;</src:expr_stmt>
</src:unit>

<src:unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/b.cpp">
<src:expr_stmt><src:expr><src:name>b</src:name></src:expr>;</src:expr_stmt>
</src:unit>

</src:unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(sxmlfile1)
f.close()
# check metadata options
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.LANGUAGE_DISPLAY_FLAG, option.LANGUAGE_DISPLAY_FLAG, "", "", "C++\n")
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.DIRECTORY_DISPLAY_FLAG, option.DIRECTORY_DISPLAY_FLAG, "", "", "sub\n")
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.FILENAME_DISPLAY_FLAG, option.FILENAME_DISPLAY_FLAG, "", "", "a.cpp\n")
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.SRCVERSION_DISPLAY_FLAG, option.SRCVERSION_DISPLAY_FLAG, "", "", "1.2\n")
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.ENCODING_DISPLAY_FLAG, option.ENCODING_DISPLAY_FLAG, "", "", default_srcml2src_encoding + "\n")

check([srcml2src, option.NESTED_FLAG, 'sub/a.cpp.xml'], "", "1\n")

f = open('sub/a.cpp.xml', 'w')
f.write(nestedfile1)
f.close()
check([srcml2src, option.NESTED_FLAG, 'sub/a.cpp.xml'], "", "1\n")

f = open('sub/a.cpp.xml', 'w')
f.write(nestedfile)
f.close()
check([srcml2src, option.NESTED_FLAG, 'sub/a.cpp.xml'], "", "2\n")

f = open('sub/a.cpp.xml', 'w')
f.write(nestedfilesrc)
f.close()
check([srcml2src, option.NESTED_FLAG, 'sub/a.cpp.xml'], "", "2\n")

# check unit option

sfile1 = """
a;
"""

sfile2 = """
b;
"""

sxmlfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

sxmlfile2 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="b.cpp">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>
"""

nestedfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="b.cpp">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(nestedfile)
f.close()

checkallformsfile(srcml2src, 'sub/a.cpp.xml', "-U", option.UNIT_FLAG, "1", "", sfile1)
if sys.platform != 'cygwin' :
        check([srcml2src, option.UNIT_FLAG, "1", '-o', "sub/a.cpp"], nestedfile, "")
        validate(open('sub/a.cpp', 'r').read(), sfile1)
check([srcml2src, option.UNIT_FLAG, "1", 'sub/a.cpp.xml', '-o', "sub/a.cpp"], "", "")
validate(open('sub/a.cpp', 'r').read(), sfile1)

checkallformsfile(srcml2src, 'sub/a.cpp.xml', "-U", option.UNIT_FLAG, "2", "", sfile2)
if sys.platform != 'cygwin' :
        check([srcml2src, option.UNIT_FLAG, "2", '-o', "sub/b.cpp"], nestedfile, "")
        validate(open('sub/b.cpp', 'r').read(), sfile2)
check([srcml2src, option.UNIT_FLAG, "2", 'sub/a.cpp.xml', '-o', "sub/b.cpp"], "", "")
validate(open('sub/b.cpp', 'r').read(), sfile2)

# check xml and unit option

check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", 'sub/a.cpp.xml'], "", sxmlfile1)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", '-o', 'sub/b.cpp.xml'], nestedfile, "")
        validate(open('sub/b.cpp.xml', 'r').read(), sxmlfile1)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", 'sub/a.cpp.xml', '-o', "sub/b.cpp.xml"], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), sxmlfile1)

check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", 'sub/a.cpp.xml'], "", sxmlfile2)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", '-o', 'sub/b.cpp.xml'], nestedfile, "")
        validate(open('sub/b.cpp.xml', 'r').read(), sxmlfile2)
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", 'sub/a.cpp.xml', '-o', "sub/b.cpp.xml"], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), sxmlfile2)

# check metadata options with xml and unit

nestedfileextra = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp" mytag="foo">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="Java" dir="emptysrc" filename="empty.java" mytag="foo">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(nestedfileextra)
f.close()

check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.LANGUAGE_DISPLAY_FLAG, 'sub/a.cpp.xml'], "", "C++\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.DIRECTORY_DISPLAY_FLAG, 'sub/a.cpp.xml'], "", "sub\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "1", option.FILENAME_DISPLAY_FLAG, 'sub/a.cpp.xml'], "", "a.cpp\n")

check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.LANGUAGE_DISPLAY_FLAG, 'sub/a.cpp.xml'], "", "Java\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.DIRECTORY_DISPLAY_FLAG, 'sub/a.cpp.xml'], "", "emptysrc\n")
check([srcml2src, option.XML_FLAG, option.UNIT_FLAG, "2", option.FILENAME_DISPLAY_FLAG, 'sub/a.cpp.xml'], "", "empty.java\n")

# prefix extraction

sxmlfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(sxmlfile1)
f.close()
execute([src2srcml, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "")
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.sdml.info/srcML/src", "", """
""")

checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.sdml.info/srcML/cpp", "", """cpp
""")

checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.sdml.info/srcML/literal", "", "")

checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.NAMESPACE_FLAG_SHORT, option.NAMESPACE_FLAG, "http://www.cs.uakron.edu/~collard/foo", "", "")

##
# text encoding flag

sfile1 = """
a;
"""

sxmlfile1 = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

f = open('sub/a.cpp', 'w')
f.write(sfile1)
f.close()
checkallforms(srcml2src, "", option.SRC_ENCODING_FLAG, "ISO-8859-1", sxmlfile1, sfile1)
checkallformsfile(srcml2src, 'sub/a.cpp.xml', "", option.SRC_ENCODING_FLAG, "ISO-8859-1", "", sfile1)
check([srcml2src, option.SRC_ENCODING_FLAG, "ISO-8859-1", 'sub/a.cpp.xml'], "", sfile1)
if sys.platform != 'cygwin' :
        check([srcml2src, option.SRC_ENCODING_FLAG, "ISO-8859-1", '-o', 'sub/a.cpp'], sxmlfile1, "")
        validate(open('sub/a.cpp', 'r').read(), sfile1)
check([srcml2src, option.SRC_ENCODING_FLAG, "ISO-8859-1", 'sub/a.cpp.xml', '-o', 'sub/a.cpp'], "", "")
validate(open('sub/a.cpp', 'r').read(), sfile1)

##
# test compression tool

sfile = """
a;
"""

sxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

fxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

# src2srcml
if platform.system() != "Windows" :

        f = open('sub/a.cpp', 'w')
        f.write(sfile)
        f.close()
        check([src2srcml, option.COMPRESSED_FLAG_SHORT, 'sub/a.cpp', '-o', 'sub/a.cpp.xml.gz'], "", "")
        check(['gunzip', '-c', 'sub/a.cpp.xml.gz'], "", fxmlfile)
        check([src2srcml, option.COMPRESSED_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml.gz'], "", "")
        check(['gunzip', '-c', 'sub/a.cpp.xml.gz'], "", fxmlfile)
        if sys.platform != 'cygwin' :
                check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.COMPRESSED_FLAG_SHORT, '-o', 'sub/a.cpp.xml.gz'], sfile, "")
                check(['gunzip', '-c', 'sub/a.cpp.xml.gz'], "", sxmlfile)


# srcml2src

if platform.system() != "Windows" :

        f = open('sub/a.cpp.xml', 'w')
        f.write(fxmlfile)
        f.close()
        check([srcml2src, option.COMPRESSED_FLAG_SHORT, 'sub/a.cpp.xml', '-o', 'sub/a.cpp.gz'], "", "")
        check(['gunzip', '-c', 'sub/a.cpp.gz'], "", sfile)
        check([srcml2src, option.COMPRESSED_FLAG, 'sub/a.cpp.xml', '-o', 'sub/a.cpp.gz'], "", "")
        check(['gunzip', '-c', 'sub/a.cpp.gz'], "", sfile)
        if sys.platform != 'cygwin' :
                check([srcml2src, option.COMPRESSED_FLAG_SHORT, '-o', 'sub/a.cpp.gz'], fxmlfile, "")
                check(['gunzip', '-c', 'sub/a.cpp.gz'], "", sfile)

# test input file is gzipped

sfile = """
a;
"""

sxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

fxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp.gz">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

if platform.system() != "Windows" :

        f = open('sub/a.cpp.gz', 'r')
        gzipped = f.read()
        f.close()

        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++'], gzipped, sxmlfile)
        check([src2srcml, 'sub/a.cpp.gz'], "", fxmlfile)
        if sys.platform != 'cygwin' :
                check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', '-o', 'sub/a.cpp.xml'], gzipped, "")
                validate(open('sub/a.cpp.xml', 'r').read(), sxmlfile)
        check([src2srcml, 'sub/a.cpp.gz', '-o', 'sub/a.cpp.xml'], "", "")
        validate(open('sub/a.cpp.xml', 'r').read(), fxmlfile)
        
        f = open('sub/a.cpp.xml.gz', 'r')
        gzipped = f.read()
        f.close()

        check([srcml2src], gzipped, sfile)
        check([srcml2src, 'sub/a.cpp.xml.gz'], "", sfile)
        if sys.platform != 'cygwin' :
                check([srcml2src, '-o', 'sub/a.cpp'], gzipped, "")
                validate(open('sub/a.cpp', 'r').read(), sfile)
        check([srcml2src, 'sub/a.cpp.xml.gz', '-o', 'sub/a.cpp'], "", "")
        validate(open('sub/a.cpp', 'r').read(), sfile)

##
# src2srcml Markup Extensions
sfile = ""

f = open('sub/a.cpp', 'w')
f.write(sfile)
f.close()

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lit="http://www.sdml.info/srcML/literal" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lit="http://www.sdml.info/srcML/literal" language="C++" filename="sub/a.cpp"/>
"""

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG], sfile, srcml)
##check([src2srcml, option.LITERAL_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.LITERAL_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:op="http://www.sdml.info/srcML/operator" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:op="http://www.sdml.info/srcML/operator" language="C++" filename="sub/a.cpp"/>
"""

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG], sfile, srcml)
#check([src2srcml, option.OPERATOR_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.OPERATOR_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:type="http://www.sdml.info/srcML/modifier" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:type="http://www.sdml.info/srcML/modifier" language="C++" filename="sub/a.cpp"/>
"""

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG], sfile, srcml)
#check([src2srcml, option.MODIFIER_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.MODIFIER_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lit="http://www.sdml.info/srcML/literal" xmlns:op="http://www.sdml.info/srcML/operator" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lit="http://www.sdml.info/srcML/literal" xmlns:op="http://www.sdml.info/srcML/operator" language="C++" filename="sub/a.cpp"/>
"""

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, option.OPERATOR_FLAG], sfile, srcml)
##check([src2srcml, option.LITERAL_FLAG, option.OPERATOR_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, option.OPERATOR_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.LITERAL_FLAG, option.OPERATOR_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, option.LITERAL_FLAG], sfile, srcml)
##check([src2srcml, option.OPERATOR_FLAG, option.LITERAL_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, option.LITERAL_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.OPERATOR_FLAG, option.LITERAL_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lit="http://www.sdml.info/srcML/literal" xmlns:type="http://www.sdml.info/srcML/modifier" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lit="http://www.sdml.info/srcML/literal" xmlns:type="http://www.sdml.info/srcML/modifier" language="C++" filename="sub/a.cpp"/>
"""

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, option.MODIFIER_FLAG], sfile, srcml)
##check([src2srcml, option.LITERAL_FLAG, option.MODIFIER_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, option.MODIFIER_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.LITERAL_FLAG, option.MODIFIER_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, option.LITERAL_FLAG], sfile, srcml)
##check([src2srcml, option.MODIFIER_FLAG, option.LITERAL_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, option.LITERAL_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.MODIFIER_FLAG, option.LITERAL_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:op="http://www.sdml.info/srcML/operator" xmlns:type="http://www.sdml.info/srcML/modifier" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:op="http://www.sdml.info/srcML/operator" xmlns:type="http://www.sdml.info/srcML/modifier" language="C++" filename="sub/a.cpp"/>
"""

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, option.MODIFIER_FLAG], sfile, srcml)
#check([src2srcml, option.OPERATOR_FLAG, option.MODIFIER_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, option.MODIFIER_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.OPERATOR_FLAG, option.MODIFIER_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, option.OPERATOR_FLAG], sfile, srcml)
#check([src2srcml, option.MODIFIER_FLAG, option.OPERATOR_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, option.OPERATOR_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.MODIFIER_FLAG, option.OPERATOR_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lit="http://www.sdml.info/srcML/literal" xmlns:op="http://www.sdml.info/srcML/operator" xmlns:type="http://www.sdml.info/srcML/modifier" language="C++"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:lit="http://www.sdml.info/srcML/literal" xmlns:op="http://www.sdml.info/srcML/operator" xmlns:type="http://www.sdml.info/srcML/modifier" language="C++" filename="sub/a.cpp"/>
"""

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, option.OPERATOR_FLAG, option.MODIFIER_FLAG], sfile, srcml)
##check([src2srcml, option.LITERAL_FLAG, option.OPERATOR_FLAG, option.MODIFIER_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, option.OPERATOR_FLAG, option.MODIFIER_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.LITERAL_FLAG, option.OPERATOR_FLAG, option.MODIFIER_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, option.MODIFIER_FLAG, option.OPERATOR_FLAG], sfile, srcml)
##check([src2srcml, option.LITERAL_FLAG, option.MODIFIER_FLAG, option.OPERATOR_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.LITERAL_FLAG, option.MODIFIER_FLAG, option.OPERATOR_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.LITERAL_FLAG, option.MODIFIER_FLAG, option.OPERATOR_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, option.LITERAL_FLAG, option.MODIFIER_FLAG], sfile, srcml)
##check([src2srcml, option.OPERATOR_FLAG, option.LITERAL_FLAG, option.MODIFIER_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, option.LITERAL_FLAG, option.MODIFIER_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.OPERATOR_FLAG, option.LITERAL_FLAG, option.MODIFIER_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, option.MODIFIER_FLAG, option.LITERAL_FLAG], sfile, srcml)
##check([src2srcml, option.OPERATOR_FLAG, option.MODIFIER_FLAG, option.LITERAL_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.OPERATOR_FLAG, option.MODIFIER_FLAG, option.LITERAL_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.OPERATOR_FLAG, option.MODIFIER_FLAG, option.LITERAL_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, option.LITERAL_FLAG, option.OPERATOR_FLAG], sfile, srcml)
##check([src2srcml, option.MODIFIER_FLAG, option.LITERAL_FLAG, option.OPERATOR_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, option.LITERAL_FLAG, option.OPERATOR_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.MODIFIER_FLAG, option.LITERAL_FLAG, option.OPERATOR_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, option.OPERATOR_FLAG, option.LITERAL_FLAG], sfile, srcml)
##check([src2srcml, option.MODIFIER_FLAG, option.OPERATOR_FLAG, option.LITERAL_FLAG, 'sub/a.cpp'], "", fsrcml)
#if sys.platform != 'cygwin' :
#        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.MODIFIER_FLAG, option.OPERATOR_FLAG, option.LITERAL_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#        validate(open('sub/a.cpp.xml', 'r').read(), srcml)
#check([src2srcml, option.MODIFIER_FLAG, option.OPERATOR_FLAG, option.LITERAL_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsrcml)

# test
##
# srcml2src info and longinfo

info = """xmlns="http://www.sdml.info/srcML/src"
xmlns:cpp="http://www.sdml.info/srcML/cpp"
encoding="UTF-8"
language="C++"
directory="sub"
filename="a.cpp"
"""

longinfo = """xmlns="http://www.sdml.info/srcML/src"
xmlns:cpp="http://www.sdml.info/srcML/cpp"
encoding="UTF-8"
language="C++"
directory="sub"
filename="a.cpp"
units="1"
"""

longinfonested = """xmlns="http://www.sdml.info/srcML/src"
encoding="UTF-8"
units="2"
"""

sxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

nestedfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="b.cpp">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(sxmlfile1)
f.close()
checkallforms(srcml2src, option.INFO_FLAG_SHORT, option.INFO_FLAG, "", sxmlfile, info)
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.INFO_FLAG_SHORT, option.INFO_FLAG, "", "", info)
checkallforms(srcml2src, option.LONG_INFO_FLAG_SHORT, option.LONG_INFO_FLAG, "", sxmlfile, longinfo)
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.LONG_INFO_FLAG_SHORT, option.LONG_INFO_FLAG, "", "", longinfo)

f = open('sub/a.cpp.xml', 'w')
f.write(nestedfile)
f.close()
checkallforms(srcml2src, option.LONG_INFO_FLAG_SHORT, option.LONG_INFO_FLAG, "", nestedfile, longinfonested)
checkallformsfile(srcml2src, 'sub/a.cpp.xml', option.LONG_INFO_FLAG_SHORT, option.LONG_INFO_FLAG, "", "", longinfonested)

# test
##
# test extract all command

sfile1 = """
a;
"""

sfile2 = """
b;
"""

# test
srcml = xml_declaration + """ 
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

nestedfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="b.cpp">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(srcml)
f.close()

if platform.system() != "Windows" :
        os.system("rm -f sub/a.cpp")
else :
        os.system("del sub\\a.cpp")

#remove
if platform.system() != "Windows" and sys.platform != 'cygwin':
        checkNoOutput([srcml2src, option.TO_DIR_FLAG + '=.', 'sub/a.cpp.xml'], srcml)

        validate(open("sub/a.cpp", "r").read(), sfile1)

f = open('sub/a.cpp.xml', 'w')
f.write(nestedfile)
f.close()

if platform.system() != "Windows" :
        os.system("rm -f sub/a.cpp sub/b.cpp")
else :
        os.system("del sub\\a.cpp sub\\b.cpp")

#remove
if platform.system() != "Windows" and sys.platform != 'cygwin':
        checkNoOutput([srcml2src, option.TO_DIR_FLAG + '=.', 'sub/a.cpp.xml'], "")
        validate(open('sub/a.cpp', 'r').read(), sfile1)
        validate(open('sub/b.cpp', 'r').read(), sfile2)

#os.system("rm -f sub/a.cpp sub/b.cpp")

        checkNoOutput([srcml2src, option.TO_DIR_FLAG_SHORT, '.', 'sub/a.cpp.xml'], "")
#validate(open('sub/a.cpp', 'r').read(), sfile1)
#validate(open('sub/b.cpp', 'r').read(), sfile2)

# test
##
# xml flag

srcml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(srcml)
f.close()

check([srcml2src, option.XML_FLAG], srcml, srcml)
check([srcml2src, option.XML_FLAG, 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XML_FLAG, '-o', 'sub/a.cpp.xml'], srcml, "")
        validate(open('sub/a.cpp.xml').read(), srcml)
check([srcml2src, option.XML_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcml)

# test
##
# no xml declaration srcml2src
srcml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

srcmlout = """<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(srcml)
f.close()

check([srcml2src, option.XML_FLAG, option.NO_XML_DECLARATION_FLAG], srcml, srcmlout)
check([srcml2src, option.XML_FLAG, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XML_FLAG, option.NO_XML_DECLARATION_FLAG, '-o', 'sub/a.cpp.xml'], srcml, "")
        validate(open('sub/a.cpp.xml').read(), srcmlout)
check([srcml2src, option.XML_FLAG, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

check([srcml2src, option.NO_XML_DECLARATION_FLAG, option.XML_FLAG], srcml, srcmlout)
check([srcml2src, option.NO_XML_DECLARATION_FLAG, option.XML_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.NO_XML_DECLARATION_FLAG, option.XML_FLAG, '-o', 'sub/a.cpp.xml'], srcml, "")
        validate(open('sub/a.cpp.xml').read(), srcmlout)
check([srcml2src, option.NO_XML_DECLARATION_FLAG, option.XML_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

check([srcml2src, option.NO_XML_DECLARATION_FLAG], srcml, srcmlout)
check([srcml2src, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.NO_XML_DECLARATION_FLAG, '-o', 'sub/a.cpp.xml'], srcml, "")
        validate(open('sub/a.cpp.xml').read(), srcmlout)
check([srcml2src, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

# test
srcml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
</unit>
"""

srcmlout = """<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(srcml)
f.close()

check([srcml2src, option.XML_FLAG, option.NO_XML_DECLARATION_FLAG], srcml, srcmlout)
check([srcml2src, option.XML_FLAG, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XML_FLAG, option.NO_XML_DECLARATION_FLAG, '-o', 'sub/a.cpp.xml'], srcml, "")
        validate(open('sub/a.cpp.xml').read(), srcmlout)
check([srcml2src, option.XML_FLAG, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

check([srcml2src, option.NO_XML_DECLARATION_FLAG, option.XML_FLAG], srcml, srcmlout)
check([srcml2src, option.NO_XML_DECLARATION_FLAG, option.XML_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.NO_XML_DECLARATION_FLAG, option.XML_FLAG, '-o', 'sub/a.cpp.xml'], srcml, "")
        validate(open('sub/a.cpp.xml').read(), srcmlout)
check([srcml2src, option.NO_XML_DECLARATION_FLAG, option.XML_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

check([srcml2src, option.NO_XML_DECLARATION_FLAG], srcml, srcmlout)
check([srcml2src, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.NO_XML_DECLARATION_FLAG, '-o', 'sub/a.cpp.xml'], srcml, "")
        validate(open('sub/a.cpp.xml').read(), srcmlout)
check([srcml2src, option.NO_XML_DECLARATION_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

# test
##
# no namespace declaration

srcml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

srcmlout = xml_declaration + """
<unit language="C++"/>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(srcml)
f.close()

check([srcml2src, option.XML_FLAG, option.NO_NAMESPACE_DECLARATION_FLAG], srcml, srcmlout)
check([srcml2src, option.XML_FLAG, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XML_FLAG, option.NO_NAMESPACE_DECLARATION_FLAG, '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml').read(), srcmlout)
check([srcml2src, option.XML_FLAG, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, option.XML_FLAG], srcml, srcmlout)
check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, option.XML_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, option.XML_FLAG, '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml').read(), srcmlout)
check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, option.XML_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG], srcml, srcmlout)
check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml').read(), srcmlout)
check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

# test
srcml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
</unit>
"""

srcmlout = xml_declaration + """
<unit language="C++">
</unit>
"""

f = open('sub/a.cpp.xml', 'w')
f.write(srcml)
f.close()

check([srcml2src, option.XML_FLAG, option.NO_NAMESPACE_DECLARATION_FLAG], srcml, srcmlout)
check([srcml2src, option.XML_FLAG, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XML_FLAG, option.NO_NAMESPACE_DECLARATION_FLAG, '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml').read(), srcmlout)
check([srcml2src, option.XML_FLAG, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, option.XML_FLAG], srcml, srcmlout)
check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, option.XML_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, option.XML_FLAG, '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml').read(), srcmlout)
check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, option.XML_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG], srcml, srcmlout)
check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp.xml'], "", srcmlout)
if sys.platform != 'cygwin' :
        check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml').read(), srcmlout)
check([srcml2src, option.NO_NAMESPACE_DECLARATION_FLAG, 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml').read(), srcmlout)

# test
##
# Help and version


# src2srcml
if platform.system() != "Windows" :

        globals()["test_count"] += 1
        globals()["test_line"] = os.path.basename(src2srcml) + ' ' + option.HELP_FLAG
        print test_count, os.path.basename(src2srcml) + ' ' + option.HELP_FLAG
        line = execute([src2srcml, option.HELP_FLAG], "")
        execute(['grep', 'Report bugs'], line)

        globals()["test_count"] += 1
        globals()["test_line"] = os.path.basename(src2srcml) + ' ' + option.VERSION_FLAG
        print test_count, os.path.basename(src2srcml) + ' ' + option.VERSION_FLAG
        line = execute([src2srcml, option.VERSION_FLAG], "")
        execute(['grep', 'Copyright'], line)

# srcML2src
if platform.system() != "Windows" :

        globals()["test_count"] += 1
        globals()["test_line"] = os.path.basename(srcml2src) + ' ' + option.HELP_FLAG
        print test_count, os.path.basename(srcml2src) + ' ' + option.HELP_FLAG
        line = execute([srcml2src, option.HELP_FLAG], "")
        execute(['grep', 'Report bugs'], line)

        globals()["test_count"] += 1
        globals()["test_line"] = os.path.basename(srcml2src) + ' ' + option.VERSION_FLAG
        print test_count, os.path.basename(srcml2src) + ' ' + option.VERSION_FLAG
        line = execute([srcml2src, option.VERSION_FLAG], "")
        execute(['grep', 'Copyright'], line)

# test
##
# Test order of metadata option order

srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" dir="sub" filename="a.cpp" version="1.0"/>
"""

options = [option.LANGUAGE_FLAG_SHORT, option.DIRECTORY_FLAG_SHORT, option.FILENAME_FLAG_SHORT, option.SRCVERSION_FLAG_SHORT, option.ENCODING_FLAG_SHORT,
           option.LANGUAGE_FLAG_SHORT, option.DIRECTORY_FLAG_SHORT, option.FILENAME_FLAG_SHORT, option.SRCVERSION_FLAG_SHORT, option.ENCODING_FLAG_SHORT]

values = ['language="C++"\n', 'directory="sub"\n', 'filename="a.cpp"\n', 'src-version="1.0"\n', 'encoding="UTF-8"\n',
          'language="C++"\n', 'directory="sub"\n', 'filename="a.cpp"\n', 'src-version="1.0"\n', 'encoding="UTF-8"\n']

index = 0
check([srcml2src, options[index] + options[index + 1][1] + options[index + 2][1] + options[index + 3][1] + options[index + 4][1]], srcml, values[index] + values[index + 1] + values[index + 2] + values[index + 3] + values[index + 4])

index += 1
check([srcml2src, options[index] + options[index + 1][1] + options[index + 2][1] + options[index + 3][1] + options[index + 4][1]], srcml, values[index] + values[index + 1] + values[index + 2] + values[index + 3] + values[index + 4])

index += 1
check([srcml2src, options[index] + options[index + 1][1] + options[index + 2][1] + options[index + 3][1] + options[index + 4][1]], srcml, values[index] + values[index + 1] + values[index + 2] + values[index + 3] + values[index + 4])

index += 1
check([srcml2src, options[index] + options[index + 1][1] + options[index + 2][1] + options[index + 3][1] + options[index + 4][1]], srcml, values[index] + values[index + 1] + values[index + 2] + values[index + 3] + values[index + 4])

index += 1
check([srcml2src, options[index] + options[index + 1][1] + options[index + 2][1] + options[index + 3][1] + options[index + 4][1]], srcml, values[index] + values[index + 1] + values[index + 2] + values[index + 3] + values[index + 4])

# test
##
# Testing for verbose

sfile = """
a;
"""

sxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

srcencoding = """
Source Encoding: """ + default_src2srcml_encoding

xmlencoding = """
XML Encoding: """ + default_srcml2src_encoding

f = open('sub/a.cpp', 'w')
f.write(sfile)
f.close

f = open('sub/a.cpp.xml', 'w')
f.write(sxmlfile)
f.close()
 
# src2srcml
if platform.system() != "Windows" and sys.platform != 'cygwin' :

        globals()["test_count"] += 1
        globals()["test_line"] = os.path.basename(src2srcml) + ' ' + option.VERBOSE_FLAG
        print test_count, os.path.basename(src2srcml) + ' ' + option.VERBOSE_FLAG
        line = execute([src2srcml, option.VERBOSE_FLAG, option.LANGUAGE_FLAG_SHORT, 'C++'], sfile)
        execute(['grep', srcencoding + xmlencoding], line)

        globals()["test_count"] += 1
        globals()["test_line"] = os.path.basename(src2srcml) + ' ' + option.VERBOSE_FLAG + ' sub/a.cpp'
        print test_count, os.path.basename(src2srcml) + ' ' + option.VERBOSE_FLAG + ' sub/a.cpp'
        line = execute([src2srcml, option.VERBOSE_FLAG, 'sub/a.cpp'], "")
        execute(['grep', srcencoding + xmlencoding], line)

# srcml2src
if platform.system() != "Windows" and sys.platform != 'cygwin' :

        globals()["test_count"] += 1
        globals()["test_line"] = os.path.basename(srcml2src) + ' ' + option.VERBOSE_FLAG
        print test_count, os.path.basename(srcml2src) + ' ' + option.VERBOSE_FLAG
        line = execute([srcml2src, option.VERBOSE_FLAG], sxmlfile)
        execute(['grep', xmlencoding + srcencoding], line)

        globals()["test_count"] += 1
        globals()["test_line"] = os.path.basename(srcml2src) + ' ' + option.VERBOSE_FLAG + ' sub/a.cpp.xml'
        print test_count, os.path.basename(srcml2src) + ' ' + option.VERBOSE_FLAG + ' sub/a.cpp.xml'
        line = execute([srcml2src, option.VERBOSE_FLAG, 'sub/a.cpp.xml'], "")
        execute(['grep', xmlencoding + srcencoding], line)

# test
##
# src2srcml expression option

sfile ="""
a
"""

sxmlfile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr><name>a</name></expr>
</unit>
"""

fsxmlfile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<expr><name>a</name></expr>
</unit>
"""

file = open('sub/a.cpp', 'w')
file.write(sfile)
file.close()

#checkallforms(src2srcml, option.EXPRESSION_MODE_FLAG_SHORT, option.EXPRESSION_MODE_FLAG, "", sfile, sxmlfile)
#checkallformsfile(src2srcml, 'sub/a.cpp', option.EXPRESSION_MODE_FLAG_SHORT, option.EXPRESSION_MODE_FLAG, "", "", fsxmlfile)
#check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.EXPRESSION_MODE_FLAG, '-o', 'sub/a.cpp.xml'], sfile, "")
#validate(open('sub/a.cpp.xml', 'r').read(), sxmlfile)
#check([src2srcml, option.EXPRESSION_MODE_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
#validate(open('sub/a.cpp.xml', 'r').read(), fsxmlfile)

##
# Test Query and Transformation Options

# xpath

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

xpath_error = """srcml2src: Start tag expected, '<' not found in '-'
"""

xpath = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>

</unit>
"""

xpath_empty = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src"/>
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

if sys.platform != 'cygwin' :
        checkError([srcml2src, option.XPATH_FLAG + '=/src:unit'], "", xpath_error)
        validate(getreturn([srcml2src, option.XPATH_FLAG + '=/src:unit'], ""), 2)

check([srcml2src, option.XPATH_FLAG + '=/src:unit'], srcml, xpath)
check([srcml2src, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml'], "", xpath)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=/src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath)
check([srcml2src, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=//src:unit'], srcml, xpath)
check([srcml2src, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml'], "", xpath)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=//src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath)
check([srcml2src, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=src:unit'], srcml, xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:unit', 'sub/a.cpp.xml'], "", xpath_empty)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

# test
# xpath apply root

srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

xpath_error = """srcml2src: Start tag expected, '<' not found in '-'
"""

xpath = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>

</unit>
"""

xpath_empty = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src"/>
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

if sys.platform != 'cygwin' :
        checkError([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit'], "", xpath_error)
        validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit'], ""), 2)

check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit'], srcml, xpath)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml'], "", xpath)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath)

validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:unit'], srcml, xpath)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml'], "", xpath)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath)

validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=src:unit'], srcml, xpath_empty)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=src:unit', 'sub/a.cpp.xml'], "", xpath_empty)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)

validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

# test
srcml_nested = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"><expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

xpath_nested = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"><expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>

</unit>
"""

xpath_nested_recursive = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"><expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"><expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

xpath_single_expr_stmt = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" item="1"><expr_stmt><expr><name>a</name></expr>;</expr_stmt></unit>

</unit>
"""

xpath_nested_expr_stmt = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" item="1"><expr_stmt><expr><name>a</name></expr>;</expr_stmt></unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" item="2"><expr_stmt><expr><name>b</name></expr>;</expr_stmt></unit>

</unit>
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml_nested)
file.close()

check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit'], srcml_nested, xpath_nested)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml'], "", xpath_nested)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit', '-o', 'sub/b.cpp.xml'], srcml_nested, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_nested)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_nested)

check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:unit'], srcml_nested, xpath_nested_recursive)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml'], "", xpath_nested_recursive)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:unit', '-o', 'sub/b.cpp.xml'], srcml_nested, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_nested_recursive)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_nested_recursive)

check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit/src:unit[1]/src:expr_stmt'], srcml_nested, xpath_single_expr_stmt)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit/src:unit[1]/src:expr_stmt', 'sub/a.cpp.xml'], "", xpath_single_expr_stmt)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit/src:unit[1]/src:expr_stmt', '-o', 'sub/b.cpp.xml'], srcml_nested, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_single_expr_stmt)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=/src:unit/src:unit[1]/src:expr_stmt', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_single_expr_stmt)

check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:expr_stmt'], srcml_nested, xpath_nested_expr_stmt)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:expr_stmt', 'sub/a.cpp.xml'], "", xpath_nested_expr_stmt)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:expr_stmt', '-o', 'sub/b.cpp.xml'], srcml_nested, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_nested_expr_stmt)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XPATH_FLAG + '=//src:expr_stmt', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_nested_expr_stmt)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

xpath = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" item="1"><name>a</name></unit>

</unit>
"""

xpath_empty = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src"/>
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

check([srcml2src, option.XPATH_FLAG + '=/src:unit/src:expr_stmt/src:expr/src:name'], srcml, xpath)
check([srcml2src, option.XPATH_FLAG + '=/src:unit/src:expr_stmt/src:expr/src:name', 'sub/a.cpp.xml'], "", xpath)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=/src:unit/src:expr_stmt/src:expr/src:name', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath)
check([srcml2src, option.XPATH_FLAG + '=/src:unit/src:expr_stmt/src:expr/src:name', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=//src:name'], srcml, xpath)
check([srcml2src, option.XPATH_FLAG + '=//src:name', 'sub/a.cpp.xml'], "", xpath)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=//src:name', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath)
check([srcml2src, option.XPATH_FLAG + '=//src:name', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=src:name'], srcml, xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:name', 'sub/a.cpp.xml'], "", xpath_empty)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=src:name', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:name', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:foo="http://www.cs.uakron.edu/~collard/foo">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/src" xmlns:bar="http://www.cs.uakron.edu/~collard/bar" language="Java">
<cpp:expr_stmt><cpp:expr><cpp:name>b</cpp:name></cpp:expr>;</cpp:expr_stmt>
</unit>

</unit>
"""

xpath = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:foo="http://www.cs.uakron.edu/~collard/foo">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" item="1"><name>a</name></unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/src" xmlns:bar="http://www.cs.uakron.edu/~collard/bar" language="Java" item="1"><cpp:name>b</cpp:name></unit>

</unit>
"""

xpath_empty = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:foo="http://www.cs.uakron.edu/~collard/foo"/>
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

check([srcml2src, option.XPATH_FLAG + '=/src:unit/src:expr_stmt/src:expr/src:name'], srcml, xpath)
check([srcml2src, option.XPATH_FLAG + '=/src:unit/src:expr_stmt/src:expr/src:name', 'sub/a.cpp.xml'], "", xpath)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=/src:unit/src:expr_stmt/src:expr/src:name', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath)
check([srcml2src, option.XPATH_FLAG + '=/src:unit/src:expr_stmt/src:expr/src:name', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=//src:name'], srcml, xpath)
check([srcml2src, option.XPATH_FLAG + '=//src:name', 'sub/a.cpp.xml'], "", xpath)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=//src:name', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath)
check([srcml2src, option.XPATH_FLAG + '=//src:name', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=src:name'], srcml, xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:name', 'sub/a.cpp.xml'], "", xpath_empty)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=src:name', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:name', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:foo="http://www.cs.uakron.edu/~collard/foo">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<foo:a/>
</unit>

<unit xmlns:bar="http://www.cs.uakron.edu/~collard/bar" language="Java">
<bar:b/>
</unit>

</unit>
"""

xpath_empty = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:foo="http://www.cs.uakron.edu/~collard/foo"/>
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

check([srcml2src, option.XPATH_FLAG + '=/src:unit'], srcml, srcml)
check([srcml2src, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=/src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=//src:unit'], srcml, srcml)
check([srcml2src, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=//src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=src:unit'], srcml, xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:unit', 'sub/a.cpp.xml'], "", xpath_empty)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:foo="http://www.cs.uakron.edu/~collard/foo">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++">
<foo:a/>
</unit>

<unit xmlns:bar="http://www.cs.uakron.edu/~collard/foo" language="Java">
<foo:a/><bar:b/>
</unit>

</unit>
"""

xpath_empty = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:foo="http://www.cs.uakron.edu/~collard/foo"/>
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

check([srcml2src, option.XPATH_FLAG + '=/src:unit'], srcml, srcml)
check([srcml2src, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=/src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.XPATH_FLAG + '=/src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=//src:unit'], srcml, srcml)
check([srcml2src, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=//src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.XPATH_FLAG + '=//src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

check([srcml2src, option.XPATH_FLAG + '=src:unit'], srcml, xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:unit', 'sub/a.cpp.xml'], "", xpath_empty)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XPATH_FLAG + '=src:unit', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)
check([srcml2src, option.XPATH_FLAG + '=src:unit', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xpath_empty)

validate(getreturn([srcml2src, option.XPATH_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XPATH_FLAG + '='], srcml), status.STATUS_ERROR)

# xslt and param

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

xslt_error = """srcml2src: Start tag expected, '<' not found in '-'
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

# xslt

if sys.platform != 'cygwin' :
        checkError([srcml2src, option.XSLT_FLAG + '=copy.xsl'], "", xslt_error)
        validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl'], ""), 2)

check([srcml2src, option.XSLT_FLAG + '=copy.xsl'], srcml, srcml)
check([srcml2src, option.XSLT_FLAG + '=copy.xsl', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XSLT_FLAG + '=copy.xsl', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.XSLT_FLAG + '=copy.xsl', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

validate(getreturn([srcml2src, option.XSLT_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XSLT_FLAG + '='], srcml), status.STATUS_ERROR)

# xslt apply root

if sys.platform != 'cygwin' :
        checkError([srcml2src, option.APPLY_ROOT_FLAG, option.XSLT_FLAG + '=copy.xsl'], "", xslt_error)
        validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XSLT_FLAG + '=copy.xsl'], ""), 2)

check([srcml2src, option.APPLY_ROOT_FLAG, option.XSLT_FLAG + '=copy.xsl'], srcml, srcml)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XSLT_FLAG + '=copy.xsl', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.XSLT_FLAG + '=copy.xsl', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.APPLY_ROOT_FLAG, option.XSLT_FLAG + '=copy.xsl', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XSLT_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.XSLT_FLAG + '='], srcml), status.STATUS_ERROR)

# param

check([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.PARAM_FLAG, 'NAME=VALUE'], srcml, srcml)
check([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.PARAM_FLAG, 'NAME=VALUE', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.PARAM_FLAG, 'NAME=VALUE', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.PARAM_FLAG, 'NAME=VALUE', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.PARAM_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.PARAM_FLAG, "NAME"], srcml), status.STATUS_ERROR)

xslt = """a
"""

check([srcml2src, option.XSLT_FLAG + '=param.xsl', option.PARAM_FLAG, 'name="a"'], srcml, xslt)
check([srcml2src, option.XSLT_FLAG + '=param.xsl', option.PARAM_FLAG, 'name="a"', 'sub/a.cpp.xml'], "", xslt)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XSLT_FLAG + '=param.xsl', option.PARAM_FLAG, 'name="a"', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xslt)
check([srcml2src, option.XSLT_FLAG + '=param.xsl', option.PARAM_FLAG, 'name="a"', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xslt)

validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.PARAM_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.PARAM_FLAG, "name"], srcml), status.STATUS_ERROR)

# stringparam

check([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.STRING_PARAM_FLAG, 'NAME=VALUE'], srcml, srcml)
check([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.STRING_PARAM_FLAG, 'NAME=VALUE', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.STRING_PARAM_FLAG, 'NAME=VALUE', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.STRING_PARAM_FLAG, 'NAME=VALUE', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.STRING_PARAM_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.STRING_PARAM_FLAG, "NAME"], srcml), status.STATUS_ERROR)

xslt = """a
"""

check([srcml2src, option.XSLT_FLAG + '=param.xsl', option.STRING_PARAM_FLAG, 'name=a'], srcml, xslt)
check([srcml2src, option.XSLT_FLAG + '=param.xsl', option.STRING_PARAM_FLAG, 'name=a', 'sub/a.cpp.xml'], "", xslt)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XSLT_FLAG + '=param.xsl', option.STRING_PARAM_FLAG, 'name=a', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xslt)
check([srcml2src, option.XSLT_FLAG + '=param.xsl', option.STRING_PARAM_FLAG, 'name=a', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xslt)

validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.STRING_PARAM_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XSLT_FLAG + '=copy.xsl', option.STRING_PARAM_FLAG, "name"], srcml), status.STATUS_ERROR)

# test
# src:archive
# empty test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" filename="a.cpp" language="C++"/>
"""

xslt = """a.cpp
C++
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

check([srcml2src, option.XSLT_FLAG + '=archive.xsl'], srcml, xslt)
check([srcml2src, option.XSLT_FLAG + '=archive.xsl', 'sub/a.cpp.xml'], "", xslt)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XSLT_FLAG + '=archive.xsl', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xslt)
check([srcml2src, option.XSLT_FLAG + '=archive.xsl', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xslt)

validate(getreturn([srcml2src, option.XSLT_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XSLT_FLAG + '='], srcml), status.STATUS_ERROR)

# test
# single file test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" filename="a.cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

xslt = """a.cpp
C++
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

check([srcml2src, option.XSLT_FLAG + '=archive.xsl'], srcml, xslt)
check([srcml2src, option.XSLT_FLAG + '=archive.xsl', 'sub/a.cpp.xml'], "", xslt)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XSLT_FLAG + '=archive.xsl', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xslt)
check([srcml2src, option.XSLT_FLAG + '=archive.xsl', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xslt)

validate(getreturn([srcml2src, option.XSLT_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XSLT_FLAG + '='], srcml), status.STATUS_ERROR)

# archive test

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" filename="a.cpp" language="C++">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit filename="b.cpp" language="Java">
<expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

xslt = ""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

check([srcml2src, option.XSLT_FLAG + '=archive.xsl'], srcml, xslt)
check([srcml2src, option.XSLT_FLAG + '=archive.xsl', 'sub/a.cpp.xml'], "", xslt)
if sys.platform != 'cygwin' :
        check([srcml2src, option.XSLT_FLAG + '=archive.xsl', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), xslt)
check([srcml2src, option.XSLT_FLAG + '=archive.xsl', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), xslt)

validate(getreturn([srcml2src, option.XSLT_FLAG], srcml), status.STATUS_ERROR)
validate(getreturn([srcml2src, option.XSLT_FLAG + '='], srcml), status.STATUS_ERROR)

# relaxng

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++"/>
"""

relaxng_error = """srcml2src: Start tag expected, '<' not found in '-'
"""

file = open('sub/a.cpp.xml', 'w')
file.write(srcml)
file.close()

if sys.platform != 'cygwin' :
        checkError([srcml2src, option.RELAXNG_FLAG + '=schema.rng'], "", relaxng_error)
        validate(getreturn([srcml2src, option.RELAXNG_FLAG + '=schema.rng'], ""), 2)

check([srcml2src, option.RELAXNG_FLAG + '=schema.rng'], srcml, srcml)
check([srcml2src, option.RELAXNG_FLAG + '=schema.rng', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.RELAXNG_FLAG + '=schema.rng', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.RELAXNG_FLAG + '=schema.rng', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

# TODO really make sure this is ok to return ok when no schema supplied.
validate(getreturn([srcml2src, option.RELAXNG_FLAG], srcml), status.STATUS_SUCCESS)
if sys.platform != 'cygwin' :
        validate(getreturn([srcml2src, option.RELAXNG_FLAG + '='], srcml), status.STATUS_SUCCESS)

# relaxng apply root

if sys.platform != 'cygwin' :
        checkError([srcml2src, option.APPLY_ROOT_FLAG, option.RELAXNG_FLAG + '=schema.rng'], "", relaxng_error)
        validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.RELAXNG_FLAG + '=schema.rng'], ""), 2)

check([srcml2src, option.APPLY_ROOT_FLAG, option.RELAXNG_FLAG + '=schema.rng'], srcml, srcml)
check([srcml2src, option.APPLY_ROOT_FLAG, option.RELAXNG_FLAG + '=schema.rng', 'sub/a.cpp.xml'], "", srcml)
if sys.platform != 'cygwin' :
        check([srcml2src, option.APPLY_ROOT_FLAG, option.RELAXNG_FLAG + '=schema.rng', '-o', 'sub/b.cpp.xml'], srcml, "")
        validate(open('sub/b.cpp.xml', 'r').read(), srcml)
check([srcml2src, option.APPLY_ROOT_FLAG, option.RELAXNG_FLAG + '=schema.rng', 'sub/a.cpp.xml', '-o', 'sub/b.cpp.xml'], "", "")
validate(open('sub/b.cpp.xml', 'r').read(), srcml)

# TODO really make sure this is ok to return ok when no schema supplied.
validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.RELAXNG_FLAG], srcml), status.STATUS_SUCCESS)
if sys.platform != 'cygwin' :
        validate(getreturn([srcml2src, option.APPLY_ROOT_FLAG, option.RELAXNG_FLAG + '='], srcml), status.STATUS_SUCCESS)

# position

sxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:pos="http://www.sdml.info/srcML/position" language="C++" pos:tabs="8"/>
"""

fsxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:pos="http://www.sdml.info/srcML/position" language="C++" filename="sub/a.cpp" pos:tabs="8"/>
"""

f = open('sub/a.cpp', 'w')
f.write("")
f.close()

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.POSITION_FLAG], "", sxmlfile)
check([src2srcml, option.POSITION_FLAG, 'sub/a.cpp'], "", fsxmlfile)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.POSITION_FLAG, '-o', 'sub/a.cpp.xml'], "", "")
        validate(open('sub/a.cpp.xml').read(), sxmlfile)
check([src2srcml, option.POSITION_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml').read(), fsxmlfile)

# tabs

sxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:pos="http://www.sdml.info/srcML/position" language="C++" pos:tabs="4"/>
"""

fsxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:pos="http://www.sdml.info/srcML/position" language="C++" filename="sub/a.cpp" pos:tabs="4"/>
"""

f = open('sub/a.cpp', 'w')
f.write("")
f.close()

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.TABS_FLAG, '4'], "", sxmlfile)
check([src2srcml, option.TABS_FLAG, '4', 'sub/a.cpp'], "", fsxmlfile)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.TABS_FLAG, '4', '-o', 'sub/a.cpp.xml'], "", "")
        validate(open('sub/a.cpp.xml').read(), sxmlfile)
check([src2srcml, option.TABS_FLAG, '4', 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml').read(), fsxmlfile)

validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.TABS_FLAG], ""), status.STATUS_ERROR)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.TABS_FLAG, 'a'], ""), status.STATUS_UNIT_INVALID)

# position and tabs

sxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:pos="http://www.sdml.info/srcML/position" language="C++" pos:tabs="2"/>
"""

fsxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" xmlns:pos="http://www.sdml.info/srcML/position" language="C++" filename="sub/a.cpp" pos:tabs="2"/>
"""

f = open('sub/a.cpp', 'w')
f.write("")
f.close()

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.POSITION_FLAG, option.TABS_FLAG, '2'], "", sxmlfile)
check([src2srcml, option.POSITION_FLAG, option.TABS_FLAG, '2', 'sub/a.cpp'], "", fsxmlfile)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.POSITION_FLAG, option.TABS_FLAG, '2', '-o', 'sub/a.cpp.xml'], "", "")
        validate(open('sub/a.cpp.xml').read(), sxmlfile)
check([src2srcml, option.POSITION_FLAG, option.TABS_FLAG, '2', 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml').read(), fsxmlfile)

validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.POSITION_FLAG, option.TABS_FLAG], ""), status.STATUS_ERROR)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.POSITION_FLAG, option.TABS_FLAG, 'a'], ""), status.STATUS_UNIT_INVALID)

check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.TABS_FLAG, '2', option.POSITION_FLAG], "", sxmlfile)
check([src2srcml, option.TABS_FLAG, '2', option.POSITION_FLAG, 'sub/a.cpp'], "", fsxmlfile)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.TABS_FLAG, '2', option.POSITION_FLAG, '-o', 'sub/a.cpp.xml'], "", "")
        validate(open('sub/a.cpp.xml').read(), sxmlfile)
check([src2srcml, option.TABS_FLAG, '2', option.POSITION_FLAG, 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
validate(open('sub/a.cpp.xml').read(), fsxmlfile)

validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.TABS_FLAG, option.POSITION_FLAG], ""), status.STATUS_UNIT_INVALID)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.TABS_FLAG, 'a', option.POSITION_FLAG], ""), status.STATUS_UNIT_INVALID)

# register language

fsxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" language="Java" filename="sub/a.cpp"/>
"""

f = open('sub/a.cpp', 'w')
f.write("")
f.close()

check([src2srcml, option.REGISTER_EXT_FLAG, 'cpp=Java', 'sub/a.cpp'], "", fsxmlfile)
check([src2srcml, option.REGISTER_EXT_FLAG + '=cpp=Java', 'sub/a.cpp'], "", fsxmlfile)
if sys.platform != 'cygwin' :
        check([src2srcml, option.REGISTER_EXT_FLAG, 'cpp=Java', 'sub/a.cpp', '-o', 'sub/a.cpp.xml'], "", "")
        validate(open('sub/a.cpp.xml').read(), fsxmlfile)

validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.REGISTER_EXT_FLAG], ""), status.STATUS_ERROR)
validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.REGISTER_EXT_FLAG, "cpp=Jawa"], ""), status.STATUS_ERROR)

fsxmlfile = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" language="Java" filename="sub/a.xml"/>
"""

if platform.system() != "Windows":
        os.system("touch sub/a.xml")
else :
        os.system("copy emptysrc\\empty.cpp sub\\a.xml")

check([src2srcml, option.REGISTER_EXT_FLAG, 'xml=Java', 'sub/a.xml'], "", fsxmlfile)
check([src2srcml, option.REGISTER_EXT_FLAG + '=xml=Java', 'sub/a.xml'], "", fsxmlfile)
if sys.platform != 'cygwin' :
        check([src2srcml, option.REGISTER_EXT_FLAG, 'xml=Java', 'sub/a.xml', '-o', 'sub/a.cpp.xml'], "", "")
        validate(open('sub/a.cpp.xml').read(), fsxmlfile)

validate(getreturn([src2srcml, option.LANGUAGE_FLAG_SHORT, 'C++', option.REGISTER_EXT_FLAG, "xml=Jawa"], ""), status.STATUS_ERROR)

##
# directory input

# test
srcmlstart = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">
"""

aj = """
<unit language="AspectJ" filename="dir/file.aj">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

c = """
<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C" filename="dir/file.c">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

cpp = """
<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="dir/file.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

java = """
<unit language="Java" filename="dir/file.java">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

# test
srcmlend = """
</unit>
"""

if platform.system() != "Windows" :
	dir = execute(['ls', 'dir'], "").split("\n")
else :
	dir = os.listdir('dir')

# test
srcml = srcmlstart

for file in dir :
        if file == 'file.aj' :
                srcml += aj
        if file == 'file.c' :
                srcml += c
        if file == 'file.cpp' :
                srcml += cpp
        if file == 'file.java' :
                srcml += java

# test
srcml += srcmlend

if platform.system() == "Windows" or sys.platform == 'cygwin' :
        srcml = string.replace(srcml, "dir/", "dir\\")

check([src2srcml, 'dir'], "", srcml)
check([src2srcml, 'dir', '-o', 'dir/dir.xml'], "", "")
validate(open('dir/dir.xml', 'r').read(), srcml)

if platform.system() != "Windows" and sys.platform != 'cygwin' :
        execute(['tar', 'czf', 'dir/foo.tar', 'dir/file.c'], "")

        check([src2srcml, 'dir'], "", srcml)
        check([src2srcml, 'dir', '-o', 'dir/dir.xml'], "", "")
        validate(open('dir/dir.xml', 'r').read(), srcml)

        execute(['rm', 'dir/foo.tar'], "")

#
# nested files

src = """
a;
"""

# test
srcmlstart = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">
"""

cpp = """
<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

cppempty = """
<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/a.cpp"/>
"""

java = """
<unit language="Java" filename="sub/a.java">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

javaempty = """
<unit language="Java" filename="sub/a.java"/>
"""

# test
srcmlend = """
</unit>
"""

if platform.system() != "Windows" :
        os.system('rm sub/a.cpp; touch sub/a.cpp')
else :
        os.system("del sub\\a.cpp")
        os.system("copy emptysrc\\empty.cpp sub\\a.cpp")

f = open('sub/a.java', 'w')
f.write(src)
f.close()

check([src2srcml, 'sub/a.cpp', 'sub/a.java'], '', srcmlstart + cppempty + java + srcmlend)
check([src2srcml, 'sub/a.cpp', 'sub/a.java', '-o', 'sub/all.xml'], '', '')
validate(open('sub/all.xml', 'r').read(), srcmlstart + cppempty + java + srcmlend)

check([src2srcml, 'sub/a.java', 'sub/a.cpp'], '', srcmlstart + java + cppempty + srcmlend)
check([src2srcml, 'sub/a.java', 'sub/a.cpp', '-o', 'sub/all.xml'], '', '')
validate(open('sub/all.xml', 'r').read(), srcmlstart + java + cppempty + srcmlend)

if platform.system() != "Windows" :
        os.system('rm sub/a.java; touch sub/a.java')
else :
        os.system("del sub\\a.java")
        os.system("copy emptysrc\\empty.java sub\\a.java")

f = open('sub/a.cpp', 'w')
f.write(src)
f.close()

check([src2srcml, 'sub/a.cpp', 'sub/a.java'], '', srcmlstart + cpp + javaempty + srcmlend)
check([src2srcml, 'sub/a.cpp', 'sub/a.java', '-o', 'sub/all.xml'], '', '')
validate(open('sub/all.xml', 'r').read(), srcmlstart + cpp + javaempty + srcmlend)

check([src2srcml, 'sub/a.java', 'sub/a.cpp'], '', srcmlstart + javaempty + cpp + srcmlend)
check([src2srcml, 'sub/a.java', 'sub/a.cpp', '-o', 'sub/all.xml'], '', '')
validate(open('sub/all.xml', 'r').read(), srcmlstart + javaempty + cpp + srcmlend)

cpp = """
<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="sub/b.cpp">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

if platform.system() != "Windows" :
        os.system('rm sub/a.cpp; touch sub/a.cpp')
else :
        os.system("del sub\\a.cpp")
        os.system("copy emptysrc\\empty.cpp sub\\a.cpp")

f = open('sub/b.cpp', 'w')
f.write(src)
f.close()

check([src2srcml, 'sub/a.cpp', 'sub/b.cpp'], '', srcmlstart + cppempty + cpp + srcmlend)
check([src2srcml, 'sub/a.cpp', 'sub/b.cpp', '-o', 'sub/all.xml'], '', '')
validate(open('sub/all.xml', 'r').read(), srcmlstart + cppempty + cpp + srcmlend)

check([src2srcml, 'sub/b.cpp', 'sub/a.cpp'], '', srcmlstart + cpp + cppempty + srcmlend)
check([src2srcml, 'sub/b.cpp', 'sub/a.cpp', '-o', 'sub/all.xml'], '', '')
validate(open('sub/all.xml', 'r').read(), srcmlstart + cpp + cppempty + srcmlend)

java = """
<unit language="Java" filename="sub/b.java">
<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

if platform.system() != "Windows" :
        os.system('rm sub/a.java; touch sub/a.java')
else :
        os.system("del sub\\a.java")
        os.system("copy emptysrc\\empty.java sub\\a.java")

f = open('sub/b.java', 'w')
f.write(src)
f.close()

check([src2srcml, 'sub/a.java', 'sub/b.java'], '', srcmlstart + javaempty + java + srcmlend)
check([src2srcml, 'sub/a.java', 'sub/b.java', '-o', 'sub/all.xml'], '', '')
validate(open('sub/all.xml', 'r').read(), srcmlstart + javaempty + java + srcmlend)

check([src2srcml, 'sub/b.java', 'sub/a.java'], '', srcmlstart + java + javaempty + srcmlend)
check([src2srcml, 'sub/b.java', 'sub/a.java', '-o', 'sub/all.xml'], '', '')
validate(open('sub/all.xml', 'r').read(), srcmlstart + java + javaempty + srcmlend)

# xml error test
info_single = """xmlns="http://www.sdml.info/srcML/src"
xmlns:cpp="http://www.sdml.info/srcML/cpp"
encoding="UTF-8"
language="C++"
"""

info_archive = """xmlns="http://www.sdml.info/srcML/src"
encoding="UTF-8"
"""
# ok
check([srcml2src, option.INFO_FLAG, 'xml_error/illformed.xml'], '' ,info_single)
check([srcml2src, option.INFO_FLAG, 'xml_error/illformedarchive.xml'], '', info_archive)

xml_error = """srcml2src: expected '>' in 'xml_error/illformed.xml'
"""

xml_archive_error = """srcml2src: Extra content at the end of the document in 'xml_error/illformedarchive.xml'
"""

# bad
checkError([srcml2src, 'xml_error/illformed.xml'], '', xml_error)
checkError([srcml2src, option.NESTED_FLAG, 'xml_error/illformedarchive.xml'], '', xml_archive_error)

# escaped xml test

extract_option_xpath_simple ="concat('&lt;', string(//src:decl[string(src:name)='TO_DIR_FLAG']/src:name), '&gt;')"

extract_option_xpath = "concat('&lt;&#33;ENTITY ', string(//src:decl[substring(src:name, string-length(src:name) - 4)='_FLAG']/src:name), ' \"--', substring(string(//src:decl[substring(src:name, string-length(src:name) - 4)='_FLAG']/src:init/src:expr), 2, string-length(string(//src:decl[substring(src:name, string-length(src:name) - 4)='_FLAG']/src:init/src:expr)) - 2), '\"&gt;')"

extract_option_xpath_output_simple = """<TO_DIR_FLAG>
"""

extract_option_xpath_output = """<!ENTITY TO_DIR_FLAG "--to-dir">
"""

extract_options_output = """<!ENTITY TO_DIR_FLAG "--to-dir">
<!ENTITY TO_DIR_FLAG_SHORT '-a'>
<!ENTITY UNIT_FLAG "--unit">
<!ENTITY UNIT_FLAG_SHORT '-U'>
<!ENTITY XML_FLAG "--xml">
<!ENTITY XML_FLAG_SHORT '-X'>
<!ENTITY INFO_FLAG "--info">
<!ENTITY INFO_FLAG_SHORT '-i'>
<!ENTITY LONG_INFO_FLAG "--longinfo">
<!ENTITY LONG_INFO_FLAG_SHORT '-L'>
<!ENTITY NAMESPACE_FLAG "--prefix">
<!ENTITY NAMESPACE_FLAG_SHORT '-p'>
<!ENTITY OMIT_FLAG "--omit">
<!ENTITY OMIT_FLAG_SHORT '-O'>
<!ENTITY XPATH_FLAG "--xpath">
<!ENTITY XSLT_FLAG "--xslt">
<!ENTITY PARAM_FLAG "--xpathparam">
<!ENTITY STRING_PARAM_FLAG "--param">
<!ENTITY APPLY_ROOT_FLAG "--apply-root">
<!ENTITY RELAXNG_FLAG "--relaxng">
<!ENTITY CONTEXT_FLAG "--context">
<!ENTITY LIST_FLAG "--list">
<!ENTITY REGISTER_EXTENSION_FLAG "--register-ext">
<!ENTITY REGISTER_EXTENSION_FILE_FLAG "--register-ext-file">
<!ENTITY REGISTER_EXTENSION_FUNCTION_FLAG "--register-xpath-func">
<!ENTITY REGISTER_EXTENSION_FUNCTION_FILE_FLAG "--register-xpath-func-file">
<!ENTITY EOL_FLAG "--eol">
"""

check([srcml2src, option.XPATH_FLAG, extract_option_xpath_simple, 'extract_options/extract_options_test.cpp.xml'], '', extract_option_xpath_output_simple)
check([srcml2src, option.XPATH_FLAG, extract_option_xpath, 'extract_options/extract_options_test.cpp.xml'], '', extract_option_xpath_output)
check([srcml2src, option.XSLT_FLAG, 'extract_options/extract_options.xsl', 'extract_options/extract_options_test.cpp.xml'], '', extract_options_output)

# UTF-8 BOM

src_no_bom = """a;
"""
src_bom = """\xef\xbb\xbfa;
"""

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

check([src2srcml, option.LANGUAGE_FLAG, 'C'], src_no_bom, srcml)
check([src2srcml, option.LANGUAGE_FLAG, 'C'], src_bom, srcml)

# xpath various return types

# attribute

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="a.cpp"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>
"""

# test
srcml_nested = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="a.cpp"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="b.cpp"><expr_stmt><expr><name>b</name></expr>;</expr_stmt>
</unit>

</unit>
"""

xpath_attribute = "//src:unit/@filename"

xpath_attribute_string = "string(//src:unit/@filename)"

xpath_attribute_output = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="a.cpp" item="1">a.cpp</unit>

</unit>
"""

xpath_attribute_string_output = """a.cpp
"""

xpath_attribute_nested_output = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="a.cpp" item="1">a.cpp</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="b.cpp" item="1">b.cpp</unit>

</unit>
"""

xpath_attribute_string_nested_output = """a.cpp
b.cpp
"""

check([srcml2src, option.XPATH_FLAG, xpath_attribute], srcml, xpath_attribute_output)
check([srcml2src, option.XPATH_FLAG, xpath_attribute_string], srcml, xpath_attribute_string_output)

check([srcml2src, option.XPATH_FLAG, xpath_attribute], srcml_nested, xpath_attribute_nested_output)
check([srcml2src, option.XPATH_FLAG, xpath_attribute_string], srcml_nested, xpath_attribute_string_nested_output)

# comment

# test
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="a.cpp"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
<!-- Comment -->
</unit>
"""

# test
srcml_nested = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="a.cpp"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
<!-- Comment One -->
</unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="b.cpp"><expr_stmt><expr><name>b</name></expr>;</expr_stmt>
<!-- Comment Two -->
</unit>

</unit>
"""

xpath_comment = "//comment()"

xpath_comment_string = "string(//comment())"

xpath_comment_output = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="a.cpp" item="1"><!-- Comment --></unit>

</unit>
"""

xpath_comment_string_output = """ Comment 
"""

xpath_comment_nested_output = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src">

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="a.cpp" item="1"><!-- Comment One --></unit>

<unit xmlns:cpp="http://www.sdml.info/srcML/cpp" language="C++" filename="b.cpp" item="1"><!-- Comment Two --></unit>

</unit>
"""

xpath_comment_string_nested_output = """ Comment One 
 Comment Two 
"""

check([srcml2src, option.XPATH_FLAG, xpath_comment], srcml, xpath_comment_output)
check([srcml2src, option.XPATH_FLAG, xpath_comment_string], srcml, xpath_comment_string_output)

check([srcml2src, option.XPATH_FLAG, xpath_comment], srcml_nested, xpath_comment_nested_output)
check([srcml2src, option.XPATH_FLAG, xpath_comment_string], srcml_nested, xpath_comment_string_nested_output)

# check srcml2src diff option

f = open('diff/diff.cpp.xml', 'r')
srcdiff = f.read()
f.close()

f = open('diff/a.cpp', 'r')
src_old = f.read()
f.close()

f = open('diff/a.cpp.xml', 'r')
# test
srcml_old = f.read()
f.close()

f = open('diff/b.cpp', 'r')
src_new = f.read()
f.close()

f = open('diff/b.cpp.xml', 'r')
# test
srcml_new = f.read()
f.close()

if False :
        check([srcml2src, option.DIFF_FLAG_LONG, '1'], srcdiff, src_old)
        check([srcml2src, option.DIFF_FLAG_LONG, '1', 'diff/diff.cpp.xml'], '', src_old)
        check([srcml2src, option.DIFF_FLAG_LONG, '2'], srcdiff, src_new)
        check([srcml2src, option.DIFF_FLAG_LONG, '2', 'diff/diff.cpp.xml'], '', src_new)
        
        check([srcml2src, option.DIFF_FLAG_LONG, '1', '-o', 'diff/old.cpp'], srcdiff, '')
        validate(open('diff/old.cpp', 'r').read(), src_old)
        check([srcml2src, option.DIFF_FLAG_LONG, '1', 'diff/diff.cpp.xml', '-o', 'diff/old.cpp'], '', '')
        validate(open('diff/old.cpp', 'r').read(), src_old)
        check([srcml2src, option.DIFF_FLAG_LONG, '2', '-o', 'diff/new.cpp'], srcdiff, '')
        validate(open('diff/new.cpp', 'r').read(), src_new)
        check([srcml2src, option.DIFF_FLAG_LONG, '2', 'diff/diff.cpp.xml', '-o', 'diff/new.cpp'], '', '')
        validate(open('diff/new.cpp', 'r').read(), src_new)

        check([srcml2src, option.XML_FLAG, option.DIFF_FLAG_LONG, '1', 'diff/diff.cpp.xml'], '', srcml_old)
        check([srcml2src, option.XML_FLAG, option.DIFF_FLAG_LONG, '2', 'diff/diff.cpp.xml'], '', srcml_new)

        check([srcml2src, option.XML_FLAG, option.DIFF_FLAG_LONG, '1', '-o', 'diff/old.cpp.xml'], srcdiff, '')
        validate(open('diff/old.cpp.xml', 'r').read(), srcml_old)
        check([srcml2src, option.XML_FLAG, option.DIFF_FLAG_LONG, '1', 'diff/diff.cpp.xml', '-o', 'diff/old.cpp.xml'], '', '')
        validate(open('diff/old.cpp.xml', 'r').read(), srcml_old)
        check([srcml2src, option.XML_FLAG, option.DIFF_FLAG_LONG, '2', '-o', 'diff/new.cpp.xml'], srcdiff, '')
        validate(open('diff/new.cpp.xml', 'r').read(), srcml_new)
        check([srcml2src, option.XML_FLAG, option.DIFF_FLAG_LONG, '2', 'diff/diff.cpp.xml', '-o', 'diff/new.cpp.xml'], '', '')
        validate(open('diff/new.cpp.xml', 'r').read(), srcml_new)

# cpp option

sfile1 = ""


f = open('sub/a.java', 'w')
f.write(sfile1)
f.close()

# test
##
# empty with debug
srcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="Java"/>
"""

fsrcml = xml_declaration + """
<unit xmlns="http://www.sdml.info/srcML/src" xmlns:cpp="http://www.sdml.info/srcML/cpp" language="Java" filename="sub/a.java"/>
"""
checkallformsfile(src2srcml, 'sub/a.java', option.CPP_FLAG, option.CPP_FLAG, "", "", fsrcml)
if sys.platform != 'cygwin' :
        check([src2srcml, option.LANGUAGE_FLAG_SHORT, 'Java', option.CPP_FLAG, '-o', 'sub/a.java.xml'], sfile1, "")
        validate(open('sub/a.java.xml', 'r').read(), srcml)
check([src2srcml, option.CPP_FLAG, 'sub/a.java','-o', 'sub/a.java.xml'], "", "")
validate(open('sub/a.java.xml', 'r').read(), fsrcml)

# test
# footer
print
print "Error count:\t\t", error_count, "\t", error_list
print "EOL Error count:\t", eol_error_count, "\t", eol_error_list
print "Exception count:\t", exception_count
print

for i in range(len(error_list)) :
        print str(error_list[i]) + "\t" + error_lines[i]
print
print src2srcmlversion()
print srcml2srcversion()

cli_file = open("srcMLcliTestReport.txt", "w")
cli_file.write("Error count:\t\t" +  str(error_count) + "\t" + str(error_list) + "\n")
cli_file.write("EOL Error count:\t" +  str(eol_error_count) + "\t" + str(eol_error_list) + "\n")
cli_file.write("Exception count:\t" +  str(exception_count) + "\n")
cli_file.close()

exit