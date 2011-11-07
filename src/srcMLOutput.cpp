/*
  srcMLOutput.cpp

  Copyright (C) 2003-2011  SDML (www.sdml.info)

  This file is part of the srcML translator.

  The srcML translator is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  The srcML translator is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with the srcML translator; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

  Output of the XML format based on srcMLParser
*/

#include "srcMLOutput.hpp"
#include "srcMLToken.hpp"
#include "project.hpp"
#include "srcmlns.hpp"
#include <boost/preprocessor/iteration/local.hpp>

#include "srcMLOutputPR.hpp"

#include <cstring>
#include <sstream>

#define ELEMENT_MAP_CALL_NAME element_name
#define ELEMENT_MAP_FIRST_TYPE int
#define ELEMENT_MAP_SECOND_TYPE const char*
#define ELEMENT_MAP_DEFAULT(s) template <ELEMENT_MAP_FIRST_TYPE n> inline ELEMENT_MAP_SECOND_TYPE \
  ELEMENT_MAP_CALL_NAME() { s }

#define ELEMENT_MAP_CALL(t) ELEMENT_MAP_CALL_NAME <srcMLParserTokenTypes::t>()
#define ELEMENT_MAP(t, s) template <> inline ELEMENT_MAP_SECOND_TYPE ELEMENT_MAP_CALL(t) { return s; }

// map the token types to specific strings
namespace {

  // base member
  ELEMENT_MAP_DEFAULT(return "";)

  // map tokens to strings
  // order matters if referring to previous definition
  ELEMENT_MAP(SUNIT, "unit")
  ELEMENT_MAP(COMMENT_START, "comment")
  ELEMENT_MAP(COMMENT_END, ELEMENT_MAP_CALL(COMMENT_START))
  ELEMENT_MAP(LINECOMMENT_START, ELEMENT_MAP_CALL(COMMENT_START))
  ELEMENT_MAP(LINECOMMENT_END, ELEMENT_MAP_CALL(COMMENT_START))
  ELEMENT_MAP(JAVADOC_COMMENT_START, ELEMENT_MAP_CALL(COMMENT_START))

  // No op
  ELEMENT_MAP(SNOP, "")

  // literal values
  ELEMENT_MAP(SSTRING,  "literal")
  ELEMENT_MAP(SCHAR,    "literal")
  ELEMENT_MAP(SLITERAL, "literal")
  ELEMENT_MAP(SBOOLEAN, "literal")

  // operators
  ELEMENT_MAP(SOPERATOR, "operator")

  // type modifier
  ELEMENT_MAP(SMODIFIER, "modifier")

  // sub-statement elements
  ELEMENT_MAP(SNAME, "name")
  ELEMENT_MAP(SONAME, "")
  ELEMENT_MAP(SCNAME, "name")
  ELEMENT_MAP(STYPE, "type")
  ELEMENT_MAP(SCONDITION, "condition")
  ELEMENT_MAP(SBLOCK, "block")
  ELEMENT_MAP(SINDEX, "index")

  ELEMENT_MAP(SEXPRESSION_STATEMENT, "expr_stmt")
  ELEMENT_MAP(SEXPRESSION, "expr")

  ELEMENT_MAP(SDECLARATION_STATEMENT, "decl_stmt")
  ELEMENT_MAP(SDECLARATION, "decl")
  ELEMENT_MAP(SDECLARATION_INITIALIZATION, "init")

  ELEMENT_MAP(SBREAK_STATEMENT, "break")
  ELEMENT_MAP(SCONTINUE_STATEMENT, "continue")
  ELEMENT_MAP(SGOTO_STATEMENT, "goto")
  ELEMENT_MAP(SLABEL_STATEMENT, "label")

  ELEMENT_MAP(STYPEDEF, "typedef")
  ELEMENT_MAP(SASM, "asm")
  ELEMENT_MAP(SMACRO_CALL, "macro")
  ELEMENT_MAP(SENUM, "enum")

  ELEMENT_MAP(SIF_STATEMENT, "if")
  ELEMENT_MAP(STHEN, "then")
  ELEMENT_MAP(SELSE, "else")

  ELEMENT_MAP(SWHILE_STATEMENT, "while")
  ELEMENT_MAP(SDO_STATEMENT, "do")

  ELEMENT_MAP(SSWITCH, "switch")
  ELEMENT_MAP(SCASE, "case")
  ELEMENT_MAP(SDEFAULT, "default")

  ELEMENT_MAP(SFOR_STATEMENT, "for")
  ELEMENT_MAP(SFOR_GROUP, "")
  ELEMENT_MAP(SFOR_INITIALIZATION, "init")
  ELEMENT_MAP(SFOR_CONDITION, ELEMENT_MAP_CALL(SCONDITION))
  ELEMENT_MAP(SFOR_INCREMENT, "incr")

  // functions
  ELEMENT_MAP(SFUNCTION_DEFINITION,  "function")
  ELEMENT_MAP(SFUNCTION_DECLARATION, "function_decl")
  ELEMENT_MAP(SFUNCTION_SPECIFIER,   "specifier")
  ELEMENT_MAP(SRETURN_STATEMENT,     "return")
  ELEMENT_MAP(SFUNCTION_CALL,        "call")
  ELEMENT_MAP(SPARAMETER_LIST,       "parameter_list")
  ELEMENT_MAP(SPARAMETER,            "param")
  ELEMENT_MAP(SARGUMENT_LIST,        "argument_list")
  ELEMENT_MAP(SARGUMENT,             "argument")

  // struct, union
  ELEMENT_MAP(SSTRUCT, "struct")
  ELEMENT_MAP(SSTRUCT_DECLARATION,   "struct_decl")
  ELEMENT_MAP(SUNION, "union")
  ELEMENT_MAP(SUNION_DECLARATION,    "union_decl")

  // class
  ELEMENT_MAP(SCLASS,                   "class")
  ELEMENT_MAP(SCLASS_DECLARATION,       "class_decl")
  ELEMENT_MAP(SPUBLIC_ACCESS,           "public")
  ELEMENT_MAP(SPUBLIC_ACCESS_DEFAULT,   "public")
  ELEMENT_MAP(SPRIVATE_ACCESS,          "private")
  ELEMENT_MAP(SPRIVATE_ACCESS_DEFAULT, "private")
  ELEMENT_MAP(SPROTECTED_ACCESS,        "protected")

  ELEMENT_MAP(SMEMBER_INITIALIZATION_LIST, "member_list")
  ELEMENT_MAP(SCONSTRUCTOR_DEFINITION, "constructor")
  ELEMENT_MAP(SCONSTRUCTOR_DECLARATION, "constructor_decl")
  ELEMENT_MAP(SDESTRUCTOR_DEFINITION,   "destructor")
  ELEMENT_MAP(SDESTRUCTOR_DECLARATION, "destructor_decl")
  ELEMENT_MAP(SDERIVATION_LIST,         "super")
  ELEMENT_MAP(SFRIEND,                  "friend")
  ELEMENT_MAP(SCLASS_SPECIFIER,         "specifier")

  // extern definition
  ELEMENT_MAP(SEXTERN, "extern")

  // namespaces
  ELEMENT_MAP(SNAMESPACE, "namespace")
  ELEMENT_MAP(SUSING_DIRECTIVE, "using")

  // exception handling
  ELEMENT_MAP(STRY_BLOCK,       "try")
  ELEMENT_MAP(SCATCH_BLOCK,     "catch")
  ELEMENT_MAP(STHROW_STATEMENT, "throw")
  ELEMENT_MAP(STHROW_SPECIFIER, "throw")
  ELEMENT_MAP(STHROW_SPECIFIER_JAVA, "throws")

  // template
  ELEMENT_MAP(STEMPLATE, "template")
  ELEMENT_MAP(STEMPLATE_ARGUMENT,       ELEMENT_MAP_CALL(SARGUMENT))
  ELEMENT_MAP(STEMPLATE_ARGUMENT_LIST,  ELEMENT_MAP_CALL(SARGUMENT_LIST))
  ELEMENT_MAP(STEMPLATE_PARAMETER,      ELEMENT_MAP_CALL(SPARAMETER))
  ELEMENT_MAP(STEMPLATE_PARAMETER_LIST, ELEMENT_MAP_CALL(SPARAMETER_LIST))
  ELEMENT_MAP(SREQUIRES, "requires")
  ELEMENT_MAP(SCLAUSE, "constraint")

  // cpp
  ELEMENT_MAP(SCPP_DIRECTIVE, "directive")
  ELEMENT_MAP(SCPP_FILENAME,  "file")
  ELEMENT_MAP(SCPP_INCLUDE,   "include")
  ELEMENT_MAP(SCPP_DEFINE,    "define")
  ELEMENT_MAP(SCPP_UNDEF,     "undef")
  ELEMENT_MAP(SCPP_LINE,      "line")
  ELEMENT_MAP(SCPP_IF,        "if")
  ELEMENT_MAP(SCPP_IFDEF,     "ifdef")
  ELEMENT_MAP(SCPP_IFNDEF,    "ifndef")
  ELEMENT_MAP(SCPP_ELSE,      "else")
  ELEMENT_MAP(SCPP_ELIF,      "elif")
  ELEMENT_MAP(SCPP_ENDIF,     "endif")
  ELEMENT_MAP(SCPP_THEN,      "then")
  ELEMENT_MAP(SCPP_PRAGMA,    "pragma")
  ELEMENT_MAP(SCPP_ERROR,     "error")

  ELEMENT_MAP(SMARKER,        "marker")
  ELEMENT_MAP(SERROR_PARSE,   "parse")
  ELEMENT_MAP(SERROR_MODE,    "mode")

  // Java elements
  ELEMENT_MAP(SEXTENDS,       "extends")
  ELEMENT_MAP(SIMPLEMENTS,    "implements")
  ELEMENT_MAP(SIMPORT,        "import")
  ELEMENT_MAP(SPACKAGE,       "package")
  ELEMENT_MAP(SINTERFACE,     "class")

  // special characters
  ELEMENT_MAP(CONTROL_CHAR,   "escape")

  //
  ELEMENT_MAP(SEMPTY,         "empty_stmt")

  // C++0x elements
  ELEMENT_MAP(SCONCEPT,       "concept")
  ELEMENT_MAP(SCONCEPTMAP,    "concept_map")
};

enum { SRCML_SRC_NS_URI_POS,
       SRCML_CPP_NS_URI_POS,
       SRCML_ERR_NS_URI_POS,
       SRCML_EXT_LITERAL_NS_URI_POS,
       SRCML_EXT_OPERATOR_NS_URI_POS,
       SRCML_EXT_MODIFIER_NS_URI_POS,
       SRCML_EXT_POSITION_NS_URI_POS,
};

#undef ELEMENT_MAP_CALL_NAME
#undef ELEMENT_MAP_SECOND_TYPE

#define ELEMENT_MAP_CALL_NAME element_prefix
#define ELEMENT_MAP_FIRST_TYPE int
#define ELEMENT_MAP_SECOND_TYPE int
#define ELEMENT_MAP_DEFAULT(s) template <ELEMENT_MAP_FIRST_TYPE n> inline ELEMENT_MAP_SECOND_TYPE \
  ELEMENT_MAP_CALL_NAME() { s }

#define ELEMENT_MAP_CALL(t) ELEMENT_MAP_CALL_NAME <srcMLParserTokenTypes::t>()
#define ELEMENT_MAP(t, s) template <> inline ELEMENT_MAP_SECOND_TYPE ELEMENT_MAP_CALL(t) { return s; }

namespace {

  // default is the srcML namespace
  ELEMENT_MAP_DEFAULT(return SRCML_SRC_NS_URI_POS;)

  // cpp namespace
  #define BOOST_PP_LOCAL_MACRO(n) template<> inline int element_prefix<n>() { return SRCML_CPP_NS_URI_POS; }
  //  #define BOOST_PP_LOCAL_MACRO(n) ELEMENT_MAP(n, SRCML_CPP_NS_URI_POS),
  #define BOOST_PP_LOCAL_LIMITS (TOKEN_SCPP_DIRECTIVE, TOKEN_SCPP_ENDIF)
  #include BOOST_PP_LOCAL_ITERATE()
  #undef BOOST_PP_LOCAL_MACRO
  #undef BOOST_PP_LOCAL_LIMITS

  // literal namespace
  ELEMENT_MAP(SSTRING,   SRCML_EXT_LITERAL_NS_URI_POS)
  ELEMENT_MAP(SCHAR,     SRCML_EXT_LITERAL_NS_URI_POS)
  ELEMENT_MAP(SLITERAL,  SRCML_EXT_LITERAL_NS_URI_POS)
  ELEMENT_MAP(SBOOLEAN,  SRCML_EXT_LITERAL_NS_URI_POS)

  // operator namespace
  ELEMENT_MAP(SOPERATOR, SRCML_EXT_OPERATOR_NS_URI_POS)

  // modifier namespace
  ELEMENT_MAP(SMODIFIER, SRCML_EXT_MODIFIER_NS_URI_POS)
};

// check if encoding is supported
bool srcMLOutput::checkEncoding(const char* encoding) {

  return xmlFindCharEncodingHandler(encoding) != 0;
}

//xmlBufferPtr output_buffer = 0;

srcMLOutput::srcMLOutput(TokenStream* ints,
			 const char* filename,
			 const char* language,
			 const char* xml_enc,
			 OPTION_TYPE& op,
			 const char* curi[],
			 int ts,
                         xmlBuffer* output_buffer
			 )
  : input(ints), xout(0), srcml_filename(filename), unit_language(language), unit_dir(0), unit_filename(0),
    unit_version(0), options(op), xml_encoding(xml_enc), num2prefix(curi), openelementcount(0), curline(0),
    curcolumn(0), tabsize(ts), depth(0)
{
  // open the output text writer stream
  // "-" filename is standard output
  if (output_buffer == 0)
    xout = xmlNewTextWriterFilename(srcml_filename, isoption(OPTION_COMPRESSED));
  else
    xout = xmlNewTextWriterMemory(output_buffer, isoption(OPTION_COMPRESSED));
  if (!xout) {
    fprintf(stderr, "src2srcml: " "Unable to open output file %s\n", srcml_filename);
    exit(2);
  }

  if (isoption(OPTION_POSITION)) {

    // setup the line attribute name
    std::ostringstream out;
    out << num2prefix[SRCML_EXT_POSITION_NS_URI_POS] << ':' << "line";
    lineAttribute = out.str();

    std::ostringstream out2;
    out2 << num2prefix[SRCML_EXT_POSITION_NS_URI_POS] << ':' << "column";
    columnAttribute = out2.str();
  }

  // issue the xml declaration, but only if we want to
  if (!isoption(OPTION_XMLDECL))
    xmlTextWriterStartDocument(xout, XML_VERSION, xml_encoding, XML_DECLARATION_STANDALONE);
}

srcMLOutput::~srcMLOutput() {

  close();
}

void srcMLOutput::close() {

  if (xout) {
    xmlTextWriterEndDocument(xout);
    xmlFreeTextWriter(xout);
    xout = 0;
  }
}

void srcMLOutput::setTokenStream(TokenStream& ints) {

  input = &ints;
}

void srcMLOutput::consume(const char* language, const char* directory, const char* filename, const char* version) {

  // store attributes so that first occurrence of unit element will be correct
  unit_dir = directory;
  unit_filename = filename;
  unit_version = version;
  unit_language = language;

  // consume all input until EOF
  while (consume_next() != antlr::Token::EOF_TYPE) {

    // in interactive mode flush after each token is discovered
    if (isoption(OPTION_INTERACTIVE))
      xmlTextWriterFlush(xout);
  }
}

bool srcMLOutput::isoption(int flag) const {
  return (flag & options) > 0;
}

int srcMLOutput::consume_next() {

  const antlr::RefToken& token = input->nextToken();

  outputToken(token);

  return token->getType();
}

const char* srcMLOutput::token2name(const antlr::RefToken& token) const {

  return type2name(token->getType());
}

const char* srcMLOutput::type2name(int token_type) const {

  static std::string name;

  const char* tagname = ElementNames[token_type];

  // no element name
  if (tagname[0] == '\0')
    return "";

  // non-default namespace name
  const char* prefix = num2prefix[(int)ElementPrefix[token_type]];
  if (prefix[0] != '\0') {
     name = prefix;
     name += ':';
     name.append(tagname);
     return name.c_str();
  }

  // default namespace name
  return tagname;
}

void srcMLOutput::srcMLTextWriterStartElement(xmlTextWriter* xout, const xmlChar* s) {

  xmlTextWriterStartElement(xout, s);
  ++openelementcount;
}

void srcMLOutput::srcMLTextWriterEndElement(xmlTextWriter* xout) {

  xmlTextWriterEndElement(xout);
  --openelementcount;
}

// output text
void srcMLOutput::processText(const std::string& str) {

  xmlTextWriterWriteRawLen(xout, BAD_CAST (unsigned char*) str.data(), str.size());
}

void srcMLOutput::processText(const char* s, int size) {

  xmlTextWriterWriteRawLen(xout, BAD_CAST (unsigned char*) s, size);
}

const char* srcMLOutput::lineAttributeValue(const antlr::RefToken& token) {

  static char out[21];
  snprintf(out, 20, "%d", token->getLine());

  return out;
}

const char* srcMLOutput::columnAttributeValue(const antlr::RefToken& token) {

  static char out[21];
  snprintf(out, 20, "%d", token->getColumn());

  return out;
}

void srcMLOutput::processText(const antlr::RefToken& token) {

  if (isoption(OPTION_POSITION)) {

    xmlTextWriterWriteAttribute(xout, BAD_CAST lineAttribute.c_str(), BAD_CAST lineAttributeValue(token));

    xmlTextWriterWriteAttribute(xout, BAD_CAST columnAttribute.c_str(), BAD_CAST columnAttributeValue(token));
  }

  xmlTextWriterWriteRawLen(xout, BAD_CAST (unsigned char*) token->getText().data(), token->getText().size());
}

void srcMLOutput::processEscape(const antlr::RefToken& token) {

  const char* s = token2name(token);

  srcMLTextWriterStartElement(xout, BAD_CAST s);

  int n = token->getText()[0];

  static char out[20 + 2 + 1];
  snprintf(out, 22, "0x%x", n);

  xmlTextWriterWriteAttribute(xout, BAD_CAST "char", BAD_CAST out);

  srcMLTextWriterEndElement(xout);
}

void srcMLOutput::startUnit(const char* language, const char* dir, const char* filename, const char* version, bool outer) {

  // start of main tag
  srcMLTextWriterStartElement(xout, BAD_CAST type2name(SUNIT));

  // outer units have namespaces
  if (/* outer && */ !isoption(OPTION_NAMESPACEDECL)) {

    // figure out which namespaces are needed
    char const * const ns[] = {

      // main srcML namespace declaration always used
      (depth == 0) ? SRCML_SRC_NS_URI : 0,

      // main cpp namespace declaration
      isoption(OPTION_CPP) && (isoption(OPTION_NESTED) == !outer) ? SRCML_CPP_NS_URI : 0,

      // optional debugging xml namespace
      (depth == 0) && isoption(OPTION_DEBUG)    ? SRCML_ERR_NS_URI : 0,

      // optional literal xml namespace
      (depth == 0) && isoption(OPTION_LITERAL)  ? SRCML_EXT_LITERAL_NS_URI : 0,

      // optional operator xml namespace
      (depth == 0) && isoption(OPTION_OPERATOR) ? SRCML_EXT_OPERATOR_NS_URI : 0,

      // optional modifier xml namespace
      (depth == 0) && isoption(OPTION_MODIFIER) ? SRCML_EXT_MODIFIER_NS_URI : 0,

      // optional position xml namespace
      (depth == 0) && isoption(OPTION_POSITION) ? SRCML_EXT_POSITION_NS_URI : 0,
    };

    // output the namespaces
    for (unsigned int i = 0; i < sizeof(ns) / sizeof(ns[0]); ++i) {
      if (!ns[i])
	continue;

      std::string prefix = "xmlns";
      if (num2prefix[i][0] != '\0') {
	prefix += ':';
	prefix += num2prefix[i];
      }

      xmlTextWriterWriteAttribute(xout, BAD_CAST prefix.c_str(), BAD_CAST ns[i]);
    }
  }

  // setting up for tabs, even if not used
  std::ostringstream stabs;
  std::string tabattribute;
  if (isoption(OPTION_POSITION)) {
    stabs << tabsize;
    tabattribute = num2prefix[SRCML_EXT_POSITION_NS_URI_POS];
    tabattribute.append(":");
    tabattribute.append("tabs");
  }

  // list of attributes
  const char* const attrs[][2] = {

    // language attribute
    { UNIT_ATTRIBUTE_LANGUAGE, language },

    // directory attribute
    { UNIT_ATTRIBUTE_DIRECTORY, dir },

    // filename attribute
    { UNIT_ATTRIBUTE_FILENAME, filename },

    // version attribute
    { UNIT_ATTRIBUTE_VERSION, version },

    // position tab setting
    { tabattribute.c_str(), isoption(OPTION_POSITION) ? stabs.str().c_str() : 0 },
  };

  // output attributes
  for (unsigned int i = 0; i < sizeof(attrs) / sizeof(attrs[0]); ++i) {
    if (!attrs[i][1])
      continue;

    xmlTextWriterWriteAttribute(xout, BAD_CAST attrs[i][0], BAD_CAST attrs[i][1]);
  }

  // leave space for nested unit
  if (outer && isoption(OPTION_NESTED))
    processText("\n\n", 2);

  ++depth;
}

void srcMLOutput::processUnit(const antlr::RefToken& token) {

  if (isstart(token)) {

    // keep track of number of open elements
    openelementcount = 0;

    startUnit(unit_language, unit_dir, unit_filename, unit_version, !isoption(OPTION_NESTED));

  } else {

    // end anything still open, including the unit
    while (openelementcount)
      srcMLTextWriterEndElement(xout);

    // leave a blank line before next nested unit even the last one
    if (isoption(OPTION_NESTED))
      processText("\n\n", 2);
  }
}

void srcMLOutput::processAccess(const antlr::RefToken& token) {
  static const char* type_default = "default";

  if (!isstart(token)) {
    processToken(token);
    return;
  }

  // start the element
  srcMLTextWriterStartElement(xout, BAD_CAST token2name(token));

  xmlTextWriterWriteAttribute(xout, BAD_CAST "type", BAD_CAST type_default);

  // end the element right away if empty
  if (isempty(token)) {
    srcMLTextWriterEndElement(xout);
  }
}

void srcMLOutput::processToken(const antlr::RefToken& token) {

  const char* s = token2name(token);

  if (s[0] == 0)
    return;

  if (isstart(token) || isempty(token)) {
    srcMLTextWriterStartElement(xout, BAD_CAST s);
  }

  if (!isstart(token) || isempty(token)) {
    srcMLTextWriterEndElement(xout);
  }
}

void srcMLOutput::processJavadocCommentStart(const antlr::RefToken& token) {
  static const char* JAVADOC_COMMENT_ATTR = "javadoc";

  const char* s = token2name(token);

  srcMLTextWriterStartElement(xout, BAD_CAST s);

  xmlTextWriterWriteAttribute(xout, BAD_CAST "type", BAD_CAST JAVADOC_COMMENT_ATTR);

  processText(token);
}

void srcMLOutput::processBlockCommentStart(const antlr::RefToken& token) {
  static const char* BLOCK_COMMENT_ATTR = "block";

  const char* s = token2name(token);

  srcMLTextWriterStartElement(xout, BAD_CAST s);

  xmlTextWriterWriteAttribute(xout, BAD_CAST "type", BAD_CAST BLOCK_COMMENT_ATTR);

  processText(token);
}

void srcMLOutput::processLineCommentStart(const antlr::RefToken& token) {
  static const char* const LINE_COMMENT_ATTR = "line";

  const char* s = token2name(token);

  srcMLTextWriterStartElement(xout, BAD_CAST s);

  xmlTextWriterWriteAttribute(xout, BAD_CAST "type", BAD_CAST LINE_COMMENT_ATTR);

  processText(token);
}

void srcMLOutput::processEndLineToken(const antlr::RefToken& token) {

  int size = token->getText().size();

  if (size > 1)
    processText(token);

  srcMLTextWriterEndElement(xout);

  if (size == 1)
    processText(token);
}

void srcMLOutput::processEndBlockToken(const antlr::RefToken& token) {

  processText(token);

  srcMLTextWriterEndElement(xout);
}

void srcMLOutput::processOptional(const antlr::RefToken& token, const char* attr_name, const char* attr_value) {

  const char* s = token2name(token);

  if (isstart(token)) {
    srcMLTextWriterStartElement(xout, BAD_CAST s);
    xmlTextWriterWriteAttribute(xout, BAD_CAST attr_name, BAD_CAST attr_value);
  } else {
    srcMLTextWriterEndElement(xout);
  }
}

void srcMLOutput::processString(const antlr::RefToken& token) {

  processOptional(token, "type", "string");
}

void srcMLOutput::processChar(const antlr::RefToken& token) {

  processOptional(token, "type", "char");
}

void srcMLOutput::processLiteral(const antlr::RefToken& token) {

  processOptional(token, "type", "number");
}

void srcMLOutput::processBoolean(const antlr::RefToken& token) {

  processOptional(token, "type", "boolean");
}

#if DEBUG
void srcMLOutput::processMarker(const antlr::RefToken& token) {

  const char* s = token2name(token);

  if (s[0] == 0)
    return;

  srcMLTextWriterStartElement(xout, BAD_CAST s);

  xmlTextWriterWriteAttribute(xout, BAD_CAST "location", BAD_CAST token->getText().c_str());

  srcMLTextWriterEndElement(xout);
}
#endif

void srcMLOutput::processInterface(const antlr::RefToken& token) {

  processOptional(token, "type", "interface");
}

inline void srcMLOutput::outputToken(const antlr::RefToken& token) {

  // use the array of pointers to methods to call the correct output routine
  ((*this).*(num2process[(int)process_table[token->getType()]]))(token);
}

// element names array
const char* const srcMLOutput::ElementNames[] = {

  // fill the array in order of token numbers
  #define BOOST_PP_LOCAL_MACRO(n)   element_name<n>(),
  #define BOOST_PP_LOCAL_LIMITS     (0, TOKEN_END_ELEMENT_TOKEN - 1)
  #include BOOST_PP_LOCAL_ITERATE()
  #undef BOOST_PP_LOCAL_MACRO
  #undef BOOST_PP_LOCAL_LIMITS
};

// element prefix number
const char srcMLOutput::ElementPrefix[] = {

  // fill the array with the prefixes
  #define BOOST_PP_LOCAL_MACRO(n)   element_prefix<n>(),
  #define BOOST_PP_LOCAL_LIMITS     (0, TOKEN_END_ELEMENT_TOKEN - 1)
  #include BOOST_PP_LOCAL_ITERATE()
  #undef BOOST_PP_LOCAL_MACRO
  #undef BOOST_PP_LOCAL_LIMITS
};
