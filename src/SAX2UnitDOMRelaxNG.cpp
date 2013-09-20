/*
  SAX2UnitDOMRelaxNG.cpp

  Copyright (C) 2010  SDML (www.srcML.org)

  This file is part of the srcML Toolkit.

  The srcML Toolkit is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  The srcML Toolkit is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with the srcML Toolkit; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


*/

#include "SAX2TextWriter.hpp"
#include "SAX2UnitDOMRelaxNG.hpp"
#include "SAX2Utilities.hpp"
#include "srcmlns.hpp"

#include <cstring>
#include "Options.hpp"
#include "srcmlns.hpp"

#include "srcexfun.hpp"
#include <cassert>

#include <libxml/SAX2.h>

#define SIZEPLUSLITERAL(s) sizeof(s) - 1, s

SAX2UnitDOMRelaxNG::SAX2UnitDOMRelaxNG(const char* a_context_element, const char* a_fxslt[], const char* a_ofilename, int options, int fd)
  : SAX2UnitDOM(a_context_element, a_ofilename, options, fd), fxslt(a_fxslt) {
}

xmlSAXHandler SAX2UnitDOMRelaxNG::factory() {

  xmlSAXHandler sax = { 0 };

  sax.initialized    = XML_SAX2_MAGIC;

  sax.startDocument  = &SAX2UnitDOM::startDocument;
  sax.endDocument    = &SAX2UnitDOMRelaxNG::endDocument;
  sax.startElementNs = &SAX2UnitDOM::startElementNsRoot;
  sax.endElementNs   = &SAX2UnitDOMRelaxNG::endElementNs;
  sax.characters     = xmlSAX2Characters;
  sax.ignorableWhitespace = xmlSAX2Characters;
  sax.comment        = xmlSAX2Comment;
  sax.processingInstruction = xmlSAX2ProcessingInstruction;

  return sax;
}

// end unit element and current file/buffer (started by startElementNs
void SAX2UnitDOMRelaxNG::endElementNs(void *ctx, const xmlChar *localname, const xmlChar *prefix, const xmlChar *URI) {

  xmlParserCtxtPtr ctxt = (xmlParserCtxtPtr) ctx;
  SAX2UnitDOMRelaxNG* pstate = (SAX2UnitDOMRelaxNG*) ctxt->_private;

  // DOM building end element
  xmlSAX2EndElementNs(ctx, localname, prefix, URI);

  // only handle unit elements
  if (strcmp((const char*) localname, "unit") != 0)
    return;

  // validate
  int n = xmlRelaxNGValidateDoc(pstate->rngptr, ctxt->myDoc);

  // output if it validates
 if (n == 0) {

    // if in per-unit mode and this is the first result found
    if (pstate->isnested && !pstate->found && !isoption(pstate->options, OPTION_XSLT_ALL)) {
      xmlOutputBufferWrite(pstate->buf, pstate->rootbuf->use, (const char*) pstate->rootbuf->content);
      xmlBufferFree(pstate->rootbuf);
      xmlOutputBufferWrite(pstate->buf, SIZEPLUSLITERAL(">\n\n"));
      pstate->found = true;
    }

    xmlNodeDumpOutput(pstate->buf, ctxt->myDoc, ctxt->node, 0, 0, 0);
    xmlOutputBufferWrite(pstate->buf, 2, "\n\n");
 }

  SAX2UnitDOM::endElementNs(ctx, localname, prefix, URI);
}

// end document
void SAX2UnitDOMRelaxNG::endDocument(void *ctx) {

  xmlParserCtxtPtr ctxt = (xmlParserCtxtPtr) ctx;

  SAX2UnitDOMRelaxNG* pstate = (SAX2UnitDOMRelaxNG*) ctxt->_private;

  xmlSAX2EndDocument(ctx);

  // root unit end tag
  if (pstate->isnested && !isoption(pstate->options, OPTION_XSLT_ALL))
      xmlOutputBufferWriteString(pstate->buf, pstate->found ? "</unit>\n" : "/>\n");

  // standard end document
  SAX2UnitDOM::endDocument(ctx);
}
