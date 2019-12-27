/**
 * @file sax2_srcsax_handler.cpp
 *
 * @copyright Copyright (C) 2013-2019 srcML, LLC. (www.srcML.org)
 *
 * This file is part of the srcML SAX2 Framework.
 *
 * The srcML SAX2 Framework is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * The srcML SAX2 Framework is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 *  You should have received a copy of the GNU General Public License
 * along with the srcML SAX2 Framework; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include <sax2_srcsax_handler.hpp>
#include <srcmlns.hpp>
#include <string>
#include <algorithm>
#include <cstring>

#include <libxml/parser.h>
#include <libxml/parserInternals.h>
#include <libxml/tree.h>

#ifdef SRCSAX_DEBUG
    #define BASE_DEBUG fprintf(stderr, "BASE:  %s %s %d |%.*s| at pos %ld\n", __FILE__,  __FUNCTION__, __LINE__, 3, state->base, state->base - state->prevbase); 
    #define SRCML_DEBUG(title, ch, len) fprintf(stderr, "%s:  %s %s %d |%.*s|\n", title, __FILE__,  __FUNCTION__, __LINE__, (int)len, ch); 
    #define SRCSAX_DEBUG_BASE(title,m) fprintf(stderr, "%s: %s %s %d %s BASE: pos %ld |%.*s| \n", title, __FILE__, __FUNCTION__, __LINE__, m, state->base - state->prevbase, 3, state->base);
    #define SRCSAX_DEBUG_START(m) SRCSAX_DEBUG_BASE("BEGIN",m)
    #define SRCSAX_DEBUG_END(m)   SRCSAX_DEBUG_BASE("END  ",m)
    #define SRCSAX_DEBUG_START_CHARS(ch,len) SRCML_DEBUG("BEGIN",ch,len);
    #define SRCSAX_DEBUG_END_CHARS(ch,len)   SRCML_DEBUG("END  ",ch,len);
#else
    #define BASE_DEBUG
    #define SRCML_DEBUG(title, ch, len)
    #define SRCSAX_DEBUG(title,m) 
    #define SRCSAX_DEBUG_START(m)
    #define SRCSAX_DEBUG_END(m)
    #define SRCSAX_DEBUG_START_CHARS(ch,len)
    #define SRCSAX_DEBUG_END_CHARS(ch,len)
#endif

// libxml2 places elements into a dictionary
// once initialized, can compare pointers instead of strings
static const xmlChar* UNIT_ENTRY = nullptr;
static const xmlChar* MACRO_LIST_ENTRY = nullptr;
static const xmlChar* ESCAPE_ENTRY = nullptr;

/**
 * factory
 *
 * Create SAX handler.
 */
xmlSAXHandler srcsax_sax2_factory() {

    xmlSAXHandler sax;
    memset(&sax, 0, sizeof(sax));

    sax.initialized    = XML_SAX2_MAGIC;

    sax.startDocument = &start_document;
    sax.endDocument = &end_document;

    sax.startElementNs = &start_root;
    sax.endElementNs = &end_element;

    sax.characters = sax.ignorableWhitespace = &characters_unit;

    sax.comment = &comment;
    sax.cdataBlock = &cdata_block;
    sax.processingInstruction = &processing_instruction;

    return sax;
}

// updates the state being used to extract XML directly from the context
// necessary because as libxml buffers are full, data is moved
static void update_ctx(void* ctx) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    if (state->prevconsumed != ctxt->input->consumed) {
        state->base -= ctxt->input->consumed - state->prevconsumed;
    }
    state->prevconsumed = ctxt->input->consumed;

    if (state->prevbase != ctxt->input->base) {
        state->base += ctxt->input->base - state->prevbase;
    }
    state->prevbase = ctxt->input->base;
}

// unit and root delayed-start processing
static int reparse_root(void* ctx) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return 0;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return 0;

    // Basically, reparse the root start tag, collected when first parsed
    xmlSAXHandler roottagsax;
    memset(&roottagsax, 0, sizeof(roottagsax));
    roottagsax.initialized    = XML_SAX2_MAGIC;
    xmlSetStructuredErrorFunc(ctx, [](void * userData, 
                     xmlErrorPtr /* error */) {

        auto ctxt = (xmlParserCtxtPtr) userData;
        if (ctxt == nullptr)
            return;
        auto state = (sax2_srcsax_handler*) ctxt->_private;
        if (state == nullptr)
            return;
    });

    roottagsax.startElementNs = [](void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI,
                     int nb_namespaces, const xmlChar** namespaces,
                     int nb_attributes, int /* nb_defaulted */, const xmlChar** attributes) {

        auto ctxt = (xmlParserCtxtPtr) ctx;
        if (ctxt == nullptr)
            return;
        auto state = (sax2_srcsax_handler*) ctxt->_private;
        if (state == nullptr)
            return;

        // call the upper-level start_root
        state->context->handler->start_root(state->context, (const char*) localname, 
                            (const char*) prefix, (const char*) URI,
                            nb_namespaces, namespaces, nb_attributes, attributes);

        // call the upper-level start_unit for non-archives
        if (!state->context->is_archive)
            state->context->handler->start_unit(state->context, (const char*) localname, 
                    (const char*) prefix, (const char*) URI, nb_namespaces, namespaces, nb_attributes, attributes);
    };

    xmlParserCtxtPtr context = xmlCreateMemoryParserCtxt(state->rootstarttag.c_str(), (int) state->rootstarttag.size());
    auto save_private = context->_private;
    context->_private = state;
    auto save_sax = context->sax;
    context->sax = &roottagsax;

    state->rootcalled = true;

    int status = xmlParseDocument(context);

    context->_private = save_private;
    context->sax = save_sax;
    xmlFreeParserCtxt(context);

    return status;
}

/**
 * start_document
 * @param ctx an xmlParserCtxtPtr
 *
 * SAX handler function for start of document.
 * Immediately calls supplied handlers function.
 */
void start_document(void* ctx) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    // initialize internal sax buffer char*'s and counts
    state->base = ctxt->input->cur;
    state->prevconsumed = ctxt->input->consumed;
    state->prevbase = ctxt->input->base;

    SRCSAX_DEBUG_START("");

    // save for dictionary lookup of common elements
    UNIT_ENTRY       = xmlDictLookup(ctxt->dict, (const xmlChar*) "unit", (int) strlen("unit"));
    MACRO_LIST_ENTRY = xmlDictLookup(ctxt->dict, (const xmlChar*) "macro-list", (int) strlen("macro-list"));
    ESCAPE_ENTRY     = xmlDictLookup(ctxt->dict, (const xmlChar*) "escape", (int) strlen("escape"));

    // save the encoding from the input
    state->context->encoding = "UTF-8";
    if (ctxt->encoding && ctxt->encoding[0] != '\0')
        state->context->encoding = (const char *)ctxt->encoding;
    else if (ctxt->input)
        state->context->encoding = (const char *)ctxt->input->encoding;

    // process any upper layer start document handling
    state->context->handler->start_document(state->context);




    SRCSAX_DEBUG_END("");
}

/**
 * end_document
 * @param ctx an xmlParserCtxtPtr
 *
 * SAX handler function for end of document.
 * Calls end_root if needed then
 * immediately calls supplied handlers function.
 */
void end_document(void* ctx) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    update_ctx(ctx);

    SRCSAX_DEBUG_START("");

    // handle libxml errors
    const char* errmsg = 0;
    switch (ctxt->errNo) {
    case XML_ERR_DOCUMENT_END:
        errmsg = "Extra content at the end of the document";
        break;
    default:
        break;
    };

    if (errmsg) {
//        fprintf(stderr, "srcml: %s\n", errmsg);
    }

    // never found any content, so end the root
//    if (state->mode != END_ROOT && state->mode != START)
//        end_root(ctx, state->root.localname, state->root.prefix, state->root.URI);

    // process any upper layer end document handling
    state->context->handler->end_document(state->context);

    SRCSAX_DEBUG_END("");
}

/**
 * start_root
 * @param ctx an xmlParserCtxtPtr
 * @param localname the name of the element tag
 * @param prefix the tag prefix
 * @param URI the namespace of tag
 * @param nb_namespaces number of namespaces definitions
 * @param namespaces the defined namespaces
 * @param nb_attributes the number of attributes on the tag
 * @param nb_defaulted the number of defaulted attributes
 * @param attributes list of attribute name value pairs (localname/prefix/URI/value/end)
 *
 * SAX handler function for start of root element.
 * Caches root info and immediately calls supplied handlers function.
 */
void start_root(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI,
               int nb_namespaces, const xmlChar** namespaces,
               int nb_attributes, int /* nb_defaulted */, const xmlChar** attributes) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    update_ctx(ctx);

    SRCSAX_DEBUG_START(localname);

    state->mode = ROOT;

    // wait to call upper-level callbacks until we know whether this is an archive or not
    // this is done in first_start_element()

/*
    for (auto citr : state->meta_tags) {

        state->context->handler->meta_tag(state->context, (const char*) citr.localname, (const char*) citr.prefix, (const char*) citr.URI,
                                                          citr.nb_namespaces, citr.namespaces.data(),
                                                          citr.nb_attributes, citr.attributes.data());
    }
*/
    // save the root start tag because we are going to parse it again to generate proper start_root() and start_unit()
    // calls after we know whether this is an archive or not
    state->rootstarttag.reserve(ctxt->input->cur - state->base + 2);
    state->rootstarttag.assign((const char*) state->base, ctxt->input->cur - state->base);
    state->rootstarttag.append("/>");

    // record namespace string in an extensible list so we can add the per unit
    if (state->collect_unit_body) {

        // precalculate length
        int ns_length = nb_namespaces * 2;
        int size = 0;
        for (int i = 0; i < ns_length; i += 2) {

            // state->rootnsstr += "xmlns";
            size += 5;
            if (namespaces[i]) {
                // state->rootnsstr += ":";
                // state->rootnsstr += (const char*) namespaces[i];
                size += 1 + (int) strlen((const char*) namespaces[i]);
            }
            // state->rootnsstr += "=\"";
            // state->rootnsstr += (const char*) namespaces[i + 1];
            // state->rootnsstr += "\" ";
            size += 2 + (int) strlen((const char*) namespaces[i + 1]) + 2;
        }

        state->rootnsstr.reserve(size);

        for (int i = 0; i < ns_length; i += 2) {

            state->rootnsstr += "xmlns";
            if (namespaces[i]) {
                state->rootnsstr += ":";
                state->rootnsstr += (const char*) namespaces[i];
            }
            state->rootnsstr += "=\"";
            state->rootnsstr += (const char*) namespaces[i + 1];
            state->rootnsstr += "\" ";
        }
    }

    SRCML_DEBUG("UNIT", state->unitsrcml.c_str(), state->unitsrcml.size());

    SRCSAX_DEBUG_END(localname);

    // for empty units we need to call the upper-level handling
    // and not delay it
    bool isempty = ctxt->input->cur[0] == '/';
    if (isempty)
        state->context->is_archive = false;

    // call the upper-level start_root when an empty element
    if (isempty) {
        state->rootcalled = true;
        state->context->handler->start_root(state->context, (const char*) localname, 
                            (const char*) prefix, (const char*) URI,
                            nb_namespaces, namespaces, nb_attributes, attributes);
    }

    // assume this is not a solo unit, but delay calling the upper levels until we are sure
    state->callupper = false;
    start_unit(ctx, localname, prefix, URI, nb_namespaces, namespaces, nb_attributes, 0, attributes);
    state->callupper = true;
    state->mode = ROOT;

    // call the upper-level start_unit for non-archives
    if (isempty && !state->context->is_archive) {
        state->context->handler->start_unit(state->context, (const char*) localname, 
                (const char*) prefix, (const char*) URI, nb_namespaces, namespaces, nb_attributes, attributes);
    }

    // handle nested units
    ctxt->sax->startElementNs = &first_start_element;
}

/**
 * first_start_element
 * @param ctx an xmlParserCtxtPtr
 * @param localname the name of the element tag
 * @param prefix the tag prefix
 * @param URI the namespace of tag
 * @param nb_namespaces number of namespaces definitions
 * @param namespaces the defined namespaces
 * @param nb_attributes the number of attributes on the tag
 * @param nb_defaulted the number of defaulted attributes
 * @param attributes list of attribute name value pairs (localname/prefix/URI/value/end)
 *
 * SAX handler function for start of first element after root
 * Detects archive and acts accordingly.
 */
void first_start_element(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI,
                         int nb_namespaces, const xmlChar** namespaces,
                         int nb_attributes, int /* nb_defaulted */, const xmlChar** attributes) {


    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    SRCSAX_DEBUG_START(localname);

    // if macros are found, then must return, process first
    // but stay in first_start_element, since this can be between root unit and nested unit
    if (localname == MACRO_LIST_ENTRY) {

        state->context->handler->meta_tag(state->context, (const char*) localname, (const char*) prefix, (const char*) URI,
                                          nb_namespaces, namespaces, nb_attributes, attributes);
        return;
    }

    // archive when the first element after the root is <unit>
    state->context->is_archive = (localname == UNIT_ENTRY);

    // turn off first_start_element() handling
    ctxt->sax->startElementNs = &start_element;

    SRCSAX_DEBUG_END(localname);

    // call the delayed upper-level callbacks for starting a root and a unit
    // waited because we did not know yet if this was an archive
    // Basically, reparse the root start tag, collected when first parsed
    reparse_root(ctx);

    // decide if this start element is for a unit (archive), or just a regular element (solo unit)
    if (state->context->is_archive) {
        
        // restart unit count due to call of start_unit() in start_root() when we assumed a solo unit
        state->unit_count = 0;

        state->loc = 0;

        // unit starts for real, discarding previous start_unit() in start_root()
        start_unit(ctx, localname, prefix, URI, nb_namespaces, namespaces, nb_attributes, 0, attributes);

    } else {

        // pass on the parameters to the regular start element
        start_element(ctx, localname, prefix, URI, nb_namespaces, namespaces, nb_attributes, 0, attributes);
    }
    state->mode = UNIT;
}

/**
 * start_unit
 * @param ctx an xmlParserCtxtPtr
 * @param localname the name of the element tag
 * @param prefix the tag prefix
 * @param URI the namespace of tag
 * @param nb_namespaces number of namespaces definitions
 * @param namespaces the defined namespaces
 * @param nb_attributes the number of attributes on the tag
 * @param nb_defaulted the number of defaulted attributes
 * @param attributes list of attribute name value pairs (localname/prefix/URI/value/end)
 *
 * SAX handler function for start of an unit.
 * Immediately calls supplied handlers function.
 */
void start_unit(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI,
               int nb_namespaces, const xmlChar** namespaces,
               int nb_attributes, int /* nb_defaulted */, const xmlChar** attributes) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    // collect cpp prefix
    for (int i = 0; i < nb_namespaces; ++i) {

        if (std::string((const char*) namespaces[i * 2 + 1]) == SRCML_CPP_NS_URI) {
            state->cpp_prefix = namespaces[i * 2] ? "" : (const char*) namespaces[i * 2];
        }
    }

    update_ctx(ctx);

    SRCSAX_DEBUG_START(localname);

    state->mode = UNIT;

    state->unit_count += 1;

    if (true || state->collect_unit_body) {

        // find end of unit tag name, e.g., end of "<unit" or "<src:unit"
        int pos = (int) (1 + strlen((const char*) localname) + (prefix ? strlen((const char*) prefix) + 1 : 0) + 1);

        if (pos >= 0) {
            // merge the namespaces from the root into this one
            state->unitsrcml.reserve(ctxt->input->cur - state->base + 1 + (state->context->is_archive ? state->rootnsstr.size() : 0));
            state->unitsrcml.assign((const char*) state->base, pos);
            state->insert_begin = (int) state->unitsrcml.size();
            if (state->context->is_archive) {
                state->unitsrcml.append(state->rootnsstr);
                state->insert_end = (int) state->unitsrcml.size();
            }

            state->unitsrcml.append((const char*) state->base + pos, ctxt->input->cur - state->base + 1 - pos);

            if (!state->context->is_archive) {
                std::string& s = state->unitsrcml;
                auto pos = s.find("xmlns");
                auto firstquote = s.find("\"", pos + 1);
                auto secondquote = s.find("\"", firstquote + 1);
                state->insert_end = (int) secondquote + 2;
            }
        }

        SRCML_DEBUG("UNIT", state->unitsrcml.c_str(), state->unitsrcml.size());

        // where the content begins, past the start unit tag
        state->content_begin = (int) state->unitsrcml.size();
    }

    // update position
    state->base = ctxt->input->cur + 1;

    // upper-level start unit handling
    // note: In order to nop this, it is set to 0 sometimes, so have to check
    if (state->callupper)
        state->context->handler->start_unit(state->context, (const char *)localname, (const char *)prefix, (const char *)URI,
                                            nb_namespaces, namespaces,
                                            nb_attributes, attributes);

    // assuming not collecting the unit body
    ctxt->sax->startElementNs = 0;
    ctxt->sax->ignorableWhitespace = ctxt->sax->characters = 0;
    ctxt->sax->comment = 0;
    ctxt->sax->cdataBlock = 0;
    ctxt->sax->processingInstruction = 0;

    if (!state->collect_unit_body)
        return;

    // next start tag will be for a non-unit element
    ctxt->sax->startElementNs = &start_element;
    ctxt->sax->ignorableWhitespace = ctxt->sax->characters = &characters_unit;
    ctxt->sax->comment = &comment;
    ctxt->sax->cdataBlock = &cdata_block;
    ctxt->sax->processingInstruction = &processing_instruction;

    // start to collect source
    state->unitsrc.clear();

    SRCSAX_DEBUG_END(localname);
}

/**
 * end_unit
 * @param ctx an xmlParserCtxtPtr
 * @param localname the name of the element tag
 * @param prefix the tag prefix
 * @param URI the namespace of tag
 *
 * SAX handler function for end of a unit
 */
void end_unit(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    SRCSAX_DEBUG_START(localname);

    SRCML_DEBUG("UNIT", state->unitsrcml.c_str(), state->unitsrcml.size());

    state->mode = END_UNIT;

    state->context->handler->end_unit(state->context, (const char *)localname, (const char *)prefix, (const char *)URI);

    ctxt->sax->startElementNs = &start_unit;

    if (true || state->collect_unit_body)
        ctxt->sax->ignorableWhitespace = ctxt->sax->characters = &characters_root;

    SRCSAX_DEBUG_END(localname);
}

/**
 * end_root
 * @param ctx an xmlParserCtxtPtr
 * @param localname the name of the element tag
 * @param prefix the tag prefix
 * @param URI the namespace of tag
 *
 * SAX handler function for end of a unit
 */
void end_root(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    SRCSAX_DEBUG_START(localname);

    if (!state->rootcalled) {

        // call the delayed upper-level callbacks for starting a root and a unit
        // waited because we did not know yet if this was an archive
        // Basically, reparse the root start tag, collected when first parsed
        reparse_root(ctx);

        state->context->handler->end_unit(state->context, (const char *)localname, (const char *)prefix, (const char *)URI);
    }

    state->context->handler->end_root(state->context, (const char *)localname, (const char *)prefix, (const char *)URI);

    SRCSAX_DEBUG_END(localname);
}

/**
 * start_element
 * @param ctx an xmlParserCtxtPtr
 * @param localname the name of the element tag
 * @param prefix the tag prefix
 * @param URI the namespace of tag
 * @param nb_namespaces number of namespaces definitions
 * @param namespaces the defined namespaces
 * @param nb_attributes the number of attributes on the tag
 * @param nb_defaulted the number of defaulted attributes
 * @param attributes list of attribute name value pairs (localname/prefix/URI/value/end)
 *
 * SAX handler function for start of an element.
 * Immediately calls supplied handlers function.
 */
void start_element(void* ctx, const xmlChar* localname, const xmlChar* /* prefix */, const xmlChar* /* URI */,
                    int /* nb_namespaces */, const xmlChar** /* namespaces */,
                    int /* nb_attributes */, int /* nb_defaulted */, const xmlChar** attributes) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    update_ctx(ctx);

    SRCSAX_DEBUG_START(localname);

    if (state->collect_unit_body) {

        // end previous start element
        if (state->base[0] == '>') {
            state->unitsrcml.append(1, '>');
            state->base += 1;
        }

        auto srcmllen = ctxt->input->cur - state->base;
        if (srcmllen < 0) {
//            fprintf(stderr, "srcml: Internal error");
            return;
        }

        SRCML_DEBUG("BASE", (const char*) state->base, srcmllen);

        state->unitsrcml.append((const char*) state->base, srcmllen);

        SRCML_DEBUG("UNIT", state->unitsrcml.c_str(), state->unitsrcml.size());

        // Special element <escape char="0x0c"/> used to embed non-XML characters
        // extract the value of the char attribute and add to the src (text)
        if (localname == ESCAPE_ENTRY) {

            std::string svalue((const char *)attributes[0 * 5 + 3], attributes[0 * 5 + 4] - attributes[0 * 5 + 3]);

            char value = (int)strtol(svalue.c_str(), NULL, 0);

            state->unitsrc.append(1, value);
        }
    }
    state->base = ctxt->input->cur;

    SRCSAX_DEBUG_END(localname);
}

/**
 * end_element
 * @param ctx an xmlParserCtxtPtr
 * @param localname the name of the element tag
 * @param prefix the tag prefix
 * @param URI the namespace of tag
 *
 * SAX handler function for end of an element.
 * Detects end of unit and calls correct functions
 * for either end_root end_unit or end_element.
 */
void end_element(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)  
        return;
    
    update_ctx(ctx);

    SRCSAX_DEBUG_START(localname);

    // collect end element tag
    if (state->collect_unit_body) {

        auto srcmllen = ctxt->input->cur - state->base;
        if (srcmllen < 0) {
            fprintf(stderr, "srcml: Internal error");
            return;
        }

        state->content_end = (int) state->unitsrcml.size() + 1;
        state->unitsrcml.append((const char*) state->base, srcmllen);

        SRCML_DEBUG("UNIT", state->unitsrcml.c_str(), state->unitsrcml.size());
    }

    state->base = ctxt->input->cur;

    SRCSAX_DEBUG_END(localname);

    // plain end element
    if (localname != UNIT_ENTRY) {
        return;
    }

    // At this point, we have the end of a unit

    if (ctxt->nameNr == 2 || !state->context->is_archive) {

        end_unit(ctx, localname, prefix, URI);
    }
 
    if (ctxt->nameNr == 1) {

        state->mode = END_ROOT;

        end_root(ctx, localname, prefix, URI);
    }
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"

/**
 * characters_root
 * @param ctx an xmlParserCtxtPtr
 * @param ch the characers
 * @param len number of characters
 *
 * SAX handler function for character handling at the root level.
 * Immediately calls supplied handlers function.
 */
void characters_root(void* ctx, const xmlChar* ch, int len) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    update_ctx(ctx);

    SRCSAX_DEBUG_START_CHARS(ch, len);

    // skip over
    state->base = ctxt->input->cur;

    SRCSAX_DEBUG_END_CHARS(ch, len);
}

#pragma GCC diagnostic pop

/**
 * characters_unit
 * @param ctx an xmlParserCtxtPtr
 * @param ch the characers
 * @param len number of characters
 *
 * SAX handler function for character handling within a unit.
 * Immediately calls supplied handlers function.
 */
void characters_unit(void* ctx, const xmlChar* ch, int len) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    update_ctx(ctx);

    SRCSAX_DEBUG_START_CHARS(ch, len);

    BASE_DEBUG;

    if (!state->collect_unit_body)
        return;

    state->unitsrc.append((const char*) ch, len);

    state->loc += (int) std::count((const char*) ch, (const char*) ch + len, '\n');

    update_ctx(ctx);

    // end previous start element
    if (state->base[0] == '>') {
        state->unitsrcml.append(1, '>');
        state->base += 1;
    }

    // libxml2 handles things in the background differently for whitespace and escaped characters
    // using a different buffer. For POS (Plain Old Strings), it uses the original buffer
    if (state->base == ctxt->input->cur) {

        // plain old strings
        state->unitsrcml.append((const char*) ch, len);

        // libxml2 passes ctxt->input->cur as ch, so then must increment to len
        state->base = ctxt->input->cur + len;

    } else {

        // whitespace and escaped characters
        state->unitsrcml.append((const char*) state->base, ctxt->input->cur - state->base);
        state->base = ctxt->input->cur;
    }

    SRCML_DEBUG("UNIT", state->unitsrcml.c_str(), state->unitsrcml.size());

    BASE_DEBUG

    SRCSAX_DEBUG_END_CHARS(ch, len);
}

/**
 * comment
 * @param ctx an xmlParserCtxtPtr
 * @param value the comment content
 *
 * A comment has been parsed.
 * Immediately calls supplied handlers function.
 */
void comment(void* ctx, const xmlChar* /* value */) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    update_ctx(ctx);

    SRCSAX_DEBUG_START("");

    if (state->collect_unit_body) {

        state->unitsrcml.append((const char*) state->base, ctxt->input->cur - state->base);

        state->base = ctxt->input->cur;
    }

    SRCSAX_DEBUG_END("");
}

/**
 * cdata_block
 * @param ctx an xmlParserCtxtPtr
 * @param value the pcdata content
 * @param len the block length
 *
 * Called when a pcdata block has been parsed.
 * Immediately calls supplied handlers function.
 */
void cdata_block(void* ctx, const xmlChar* value, int len) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    update_ctx(ctx);

    SRCSAX_DEBUG_START("");

    // append CDATA
    if (state->collect_unit_body) {

        // xml can get raw
        state->unitsrcml.append((const char*) state->base, ctxt->input->cur - state->base);

        // CDATA is character data
        state->unitsrc.append((const char*) value, len);

        state->base = ctxt->input->cur;
    }

    SRCSAX_DEBUG_END("");
}

/**
 * processing_instruction
 * @param ctx an xmlParserCtxtPtr
 * @param target the processing instruction target.
 * @param data the processing instruction data.
 *
 * Called when a processing instruction has been parsed.
 * Immediately calls supplied handlers function.
 */
void processing_instruction(void* ctx, const xmlChar* /* target */, const xmlChar* /* data */) {

    auto ctxt = (xmlParserCtxtPtr) ctx;
    if (ctxt == nullptr)
        return;
    auto state = (sax2_srcsax_handler*) ctxt->_private;
    if (state == nullptr)
        return;

    update_ctx(ctx);

    SRCSAX_DEBUG_START("");

    if (state->collect_unit_body) {

        state->unitsrcml.append((const char*) state->base, ctxt->input->cur - state->base);

        state->base = ctxt->input->cur;
    }

    SRCSAX_DEBUG_END("");
}
