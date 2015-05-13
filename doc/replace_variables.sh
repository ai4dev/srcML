#!/bin/bash

# list of all global variables and what they should be replaced with
REPLACEMENTS="LANGUAGE_FLAG_SHORT,l
LANGUAGE_FLAG_LONG,language
DIRECTORY_FLAG_SHORT,d
DIRECTORY_FLAG_LONG,directory
FILENAME_FLAG_SHORT,f
FILENAME_FLAG_LONG,filename
SRCVERSION_FLAG_SHORT,s
SRCVERSION_FLAG_LONG,src-version
TEXT_FLAG_SHORT,t
TEXT_FLAG_LONG,text
SRC_ENCODING_FLAG_LONG,src-encoding
HASH_FLAG_LONG,hash
XML_ENCODING_FLAG_SHORT,x
XML_ENCODING_FLAG_LONG,xml-encoding
LONG_INFO_FLAG_SHORT,L
LONG_INFO_FLAG_LONG,longinfo
INFO_FLAG_SHORT,i
INFO_FLAG_LONG,info
PREFIX_FLAG_SHORT,p
PREFIX_FLAG_LONG,prefix
LINE_ENDING_FLAG_LONG,output-src-eol
LIST_FLAG_LONG,list
UPDATE_FLAG_LONG,update
OUTPUT_FLAG_SHORT,o
OUTPUT_FLAG_LONG,output
OUTPUT_XML_FLAG_SHORT,X
OUTPUT_XML_FLAG_LONG,output-xml
OUTPUT_SRC_FLAG_SHORT,S
OUTPUT_SRC_FLAG_LONG,output-src
OUTPUT_FORMAT_FLAG_LONG,output-format
TO_DIR_FLAG_LONG,to-dir
UNIT_OPTION_LONG,unit
UNIT_OPTION_SHORT,U
ARCHIVE_FLAG_SHORT,r
ARCHIVE_FLAG_LONG,archive
NO_XML_DECL_LONG,no-xml-declaration
NO_NAMESPACE_DECL_LONG,no-namespace-decl
INTERACTIVE_FLAG_SHORT,c
INTERACTIVE_FLAG_LONG,interactive
FILES_FROM_LONG,files-from
DEBUG_FLAG_SHORT,g
DEBUG_FLAG_LONG,debug
SRCML_ERR_NS_PREFIX_DEFAULT,err
SRCML_CPP_NS_PREFIX_DEFAULT,cpp
SRCML_EXT_POSITION_NS_PREFIX_DEFAULT,pos
SRCML_ERR_NS_URI,http:\/\/www.sdml.info\/srcML\/srcerr
SRCML_SRC_NS_URI,http:\/\/www.sdml.info\/srcML\/src
SRCML_CPP_NS_URI,http:\/\/www.sdml.info\/srcML\/cpp
SRCML_EXT_POSITION_NS_URI,http:\/\/www.sdml.info\/srcML\/position
POSITION_FLAG_LONG,position
XMLNS_FLAG,xmlns
VERBOSE_FLAG_SHORT,v
VERBOSE_FLAG_LONG,verbose
REGISTER_EXTENSION_FLAG_LONG,register-ext
LITERAL_FLAG,idk
MAX_THREADS_FLAG_LONG,max-threads
IN_ORDER_FLAG_LONG,in-order
EXTERNAL_LONG,external
TABS_FLAG,tabs
TIMESTAMP_FLAG_LONG,timestamp
CPP_FLAG_LONG,cpp
CPP_MARKUP_IF0_FLAG_LONG,cpp-markup-if0
CPP_NO_MARKUP_ELSE_FLAG_LONG,cpp-no-markup-else
XML_PROCESSING_FLAG_LONG,xml-processing
APPLY_ROOT_FLAG_LONG,apply-root
RELAXNG_OPTION_LONG,relaxng
XPATH_OPTION_LONG,xpath
XPATH_PARAM_LONG,xpathparam
XSLT_LONG,xslt
ATTRIBUTE_LONG,attribute
ELEMENT_LONG,element
STATUS_SUCCESS,0
STATUS_ERROR,idk
STATUS_INPUTFILE_PROBLEM,idk
STATUS_UNKNOWN_OPTION,idk
STATUS_UNKNOWN_ENCODING,idk
STATUS_INVALID_LANGUAGE,idk
STATUS_INVALID_OPTION_COMBINATION,idk
STATUS_TERMINATED,idk
QUIET_FLAG_SHORT,q
QUIET_FLAG_LONG,quiet
VERSION_FLAG_LONG,version
VERSION_FLAG_SHORT,V
HELP_FLAG_SHORT,h
HELP_FLAG_LONG,help
PRETTY_FLAG_LONG,pretty"

INPUT=$1
OUTPUT=$2
rm "$OUTPUT"
cp "$INPUT" "$OUTPUT"

# replace each expression from the list
while IFS=',' read -r target replacement; do
	sed -i -e "s/$target/$replacement/g" $OUTPUT
done < <(echo "$REPLACEMENTS")