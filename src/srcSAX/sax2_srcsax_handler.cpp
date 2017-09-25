/**
 *  @file sax2_srcsax_handler.cpp
 *
 * @copyright Copyright (C) 2013-2014 srcML, LLC. (www.srcML.org)
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
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <sax2_srcsax_handler.hpp>
#include <string>

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

    sax.startElementNs = &start_root_first;
    sax.endElementNs = &end_element;

    sax.characters = &characters_start;
    sax.ignorableWhitespace = &characters_start;

    sax.comment = &comment;
    sax.cdataBlock = &cdata_block;
    sax.processingInstruction = &processing_instruction;

    return sax;
}

static const xmlChar* UNIT_ENTRY = nullptr;
static const xmlChar* MACRO_LIST_ENTRY = nullptr;

static void update_ctx(void* ctx) {

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

#if 0
    fprintf(stderr, "DEBUG:  %s %s %d ctxt->input->consumed: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  ctxt->input->consumed);
    fprintf(stderr, "DEBUG:  %s %s %d state->prevconsumed: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  state->prevconsumed);
    fprintf(stderr, "DEBUG:  %s %s %d ctxt->input->base: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  ctxt->input->base);
    fprintf(stderr, "DEBUG:  %s %s %d state->prevbase: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  state->prevbase);
    fprintf(stderr, "DEBUG:  %s %s %d state->base: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  state->base);
    fprintf(stderr, "DEBUG:  %s %s %d ctxt->input->cur: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  ctxt->input->cur);
    fprintf(stderr, "DEBUG:  %s %s %d ctxt->input->cur - state->base: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  ctxt->input->cur - state->base);
#endif
    if (state->prevconsumed != ctxt->input->consumed) {
        state->base -= ctxt->input->consumed - state->prevconsumed;
//        fprintf(stderr, "DEBUG:  %s %s %d state->base: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  state->base);
    }
    state->prevconsumed = ctxt->input->consumed;

    if (state->prevbase != ctxt->input->base) {
//        fprintf(stderr, "DEBUG:  %s %s %d state->base: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  state->base);
        state->base += ctxt->input->base - state->prevbase;
    }
    state->prevbase = ctxt->input->base;
}

/**
 * start_document
 * @param ctx an xmlParserCtxtPtr
 *
 * SAX handler function for start of document.
 * Immediately calls supplied handlers function.
 */
void start_document(void* ctx) {

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    // setup dictionary lookup for common elements
    UNIT_ENTRY = xmlDictLookup(ctxt->dict, (const xmlChar*) "unit", 4);
    MACRO_LIST_ENTRY = xmlDictLookup(ctxt->dict, (const xmlChar*) "macro_list", strlen("macro_list"));

    state->base = ctxt->input->cur;
    state->prevconsumed = ctxt->input->consumed;
    state->prevbase = ctxt->input->base;

/*
    if (state->context->handler->characters_unit)
        state->process = COLLECT_SRC;

    if (state->context->handler->start_element)
        state->process = COLLECT_SRCML;
*/
    if (state->context->handler->start_document)
        state->context->handler->start_document(state->context);

    // get encoding from the input
    state->context->encoding = "UTF-8";
    if (ctxt->encoding && ctxt->encoding[0] != '\0')
        state->context->encoding = (const char *)ctxt->encoding;
    else if (ctxt->input)
        state->context->encoding = (const char *)ctxt->input->encoding;

    if (state->context->terminate)
        return;

    if (state->create_dom) {
        xmlSAX2StartDocument(ctxt);
    }

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif
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

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

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

    if (state->context->terminate)
        return;

    // never found any content, so end the root
    if (state->mode != END_ROOT && state->mode != START)
        end_root(ctx, state->root.localname, state->root.prefix, state->root.URI);

    if (state->context->terminate)
        return;

    if (state->context->handler->end_document)
        state->context->handler->end_document(state->context);

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif
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
void start_root_first(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI,
               int nb_namespaces, const xmlChar** namespaces,
               int nb_attributes, int nb_defaulted, const xmlChar** attributes) {

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    // cache the root data because we don't know if we are in an archive or not
    state->root = std::move(srcml_element(state->context, localname, prefix, URI,
                                                nb_namespaces, namespaces,
                                                nb_attributes, nb_defaulted, attributes));

    state->mode = ROOT;

    // handle nested units
    ctxt->sax->startElementNs = &start_element_start;

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif
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

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    // have to call this here because we need to first know if we are in an archive
    if (state->context->handler->start_root)
        state->context->handler->start_root(state->context, (const char*) localname, (const char*) prefix, (const char*) URI,
                                                            nb_namespaces, namespaces, 
                                                            nb_attributes, attributes);

    if (state->context->terminate)
        return;

    for (auto citr : state->meta_tags) {

        state->context->handler->meta_tag(state->context, (const char*) citr.localname, (const char*) citr.prefix, (const char*) citr.URI,
                                                          citr.nb_namespaces, citr.namespaces.data(),
                                                          citr.nb_attributes, citr.attributes.data());
        if (state->context->terminate)
            return;
    }

    // record namespaces in an extensible list so we can add the per unit
    if (state->create_dom) {
        int ns_length = nb_namespaces * 2;
        for (int i = 0; i < ns_length; i += 2) {

            state->data.push_back(namespaces[i]);
            state->data.push_back(namespaces[i + 1]);
        }
        state->rootsize = state->data.size();
    }

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif
}
/**
 * start_element_start
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
void start_element_start(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI,
                         int nb_namespaces, const xmlChar** namespaces,
                         int nb_attributes, int nb_defaulted, const xmlChar** attributes) {

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    // if macros are found, then must return, but first save them if necessary
    if (localname == MACRO_LIST_ENTRY) {

        if (state->context->handler->meta_tag)
            state->meta_tags.emplace_back(srcml_element(state->context, localname, prefix, URI,
                                                     nb_namespaces, namespaces,
                                                     nb_attributes, nb_defaulted, attributes));
        return;
    }

    if (state->context->terminate)
        return;

    state->context->is_archive = state->is_archive = (localname == UNIT_ENTRY);

    // have to call this here because we need to first know if we are in an archive
    start_root(ctx, state->root.localname, state->root.prefix, state->root.URI,
                    state->root.nb_namespaces, state->root.namespaces.data(),
                    state->root.nb_attributes, 0, state->root.attributes.data());

    if (!state->is_archive) {

        state->mode = UNIT;

        state->endfirstelement = ctxt->input->cur;

        start_unit(ctx, state->root.localname, state->root.prefix, state->root.URI,
                        state->root.nb_namespaces, state->root.namespaces.data(),
                        state->root.nb_attributes, 0, state->root.attributes.data());

        characters_unit(ctx, (const xmlChar*) state->characters.c_str(), (int)state->characters.size());
      //  state->characters.clear();

        start_element(ctx, localname, prefix, URI, nb_namespaces, namespaces, nb_attributes, 0, attributes);

    } else {
        
        characters_root(ctx, (const xmlChar*) state->characters.c_str(), (int)state->characters.size());
//        state->characters.clear();

        state->mode = UNIT;

        start_unit(ctx, localname, prefix, URI, nb_namespaces, namespaces, nb_attributes, 0, attributes);
    }

    if (state->context->terminate)
        return;

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif
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

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    update_ctx(ctx);

    state->unitsrcml = "";
    if (state->endfirstelement) {
        state->unitsrcml.append((const char*) state->base, state->endfirstelement - state->base);
        state->base = state->endfirstelement;
        state->endfirstelement = 0;
    } else {
        state->unitsrcml.append((const char*) state->base, ctxt->input->cur - state->base + 1);
        state->base = ctxt->input->cur + 1;
    }

    if (state->context->terminate)
        return;

    ++state->unit_count;
//fprintf(stderr, "COUNT:  %s %s %d state->unit_count: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  state->unit_count);

  //  state->mode = UNIT;

    if (state->context->handler->start_unit)
        state->context->handler->start_unit(state->context, (const char *)localname, (const char *)prefix, (const char *)URI,
                                            nb_namespaces, namespaces,
                                            nb_attributes, attributes);

    // next start tag will be for a non-unit element
    if (ctxt->sax->startElementNs)
        ctxt->sax->startElementNs = &start_element;

    // characters are for the unit
    if (state->collect_src || state->collect_srcml)
        ctxt->sax->ignorableWhitespace = ctxt->sax->characters = &characters_unit;

    state->unitstr.clear();

//    state->unitsrcml.clear();


    if (state->create_dom) {

        // remove per-unit namespaces
        state->data.resize(state->rootsize);

        // combine namespaces from root and local to this unit (if an archive)
        for (int i = 0; i < nb_namespaces; ++i) {

            // make sure not already in
            bool found = false;
            for (unsigned int j = 0; j < state->data.size() / 2; ++j) {
                if (xmlStrEqual(state->data[j * 2], namespaces[i * 2])) {
                    found = true;
                    break;
                }
            }
            if (found)
                continue;

            state->data.push_back(namespaces[i * 2]);
            state->data.push_back(namespaces[i * 2 + 1]);
        }

        xmlSAX2StartElementNs(ctxt, localname, prefix, URI,
                                    (int)(state->data.size() / 2), &(state->data[0]),
                                    nb_attributes, 0, attributes);
    }

    if (state->create_dom) {
        ctxt->sax->characters = xmlSAX2Characters;
        ctxt->sax->ignorableWhitespace = xmlSAX2Characters;
        ctxt->sax->comment = xmlSAX2Comment;
        ctxt->sax->cdataBlock = xmlSAX2CDataBlock;
    }

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif
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

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    state->mode = END_UNIT;

    if (state->create_dom) {
        xmlSAX2EndElementNs(ctxt, localname, prefix, URI);
        xmlSAX2EndDocument(ctxt);
    }

    if (state->context->handler->end_unit)
        state->context->handler->end_unit(state->context, (const char *)localname, (const char *)prefix, (const char *)URI);

    if (ctxt->sax->startElementNs)
        ctxt->sax->startElementNs = &start_unit;

    if (state->collect_src || state->collect_srcml)
        ctxt->sax->ignorableWhitespace = ctxt->sax->characters = &characters_root;

    // free up the document that has this particular unit
    xmlNodePtr aroot = ctxt->myDoc->children;
    xmlUnlinkNode(ctxt->myDoc->children);
    xmlFreeNodeList(aroot);
    ctxt->myDoc->children = 0;
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

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    state->base = ctxt->input->cur;

    if (state->context->handler->end_root)
        state->context->handler->end_root(state->context, (const char *)localname, (const char *)prefix, (const char *)URI);
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
void start_element(void* ctx, const xmlChar* localname, const xmlChar* prefix, const xmlChar* URI,
                    int nb_namespaces, const xmlChar** namespaces,
                    int nb_attributes, int /* nb_defaulted */, const xmlChar** attributes) {

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    update_ctx(ctx);

    auto srcmllen = ctxt->input->cur + 1 - state->base;
    if (srcmllen < 0) {
        fprintf(stderr, "DEBUG:  %s %s %d \n", __FILE__,  __FUNCTION__, __LINE__);
        exit(1);
    }

    state->unitsrcml.append((const char*) state->base, srcmllen);
    state->base = ctxt->input->cur + 1;

    if (state->context->terminate)
        return;

    if (state->create_dom)
        xmlSAX2StartElementNs(ctxt, localname, prefix, URI, nb_namespaces, namespaces, nb_attributes, 0, attributes);

    if (false && state->context->handler->start_element)
        state->context->handler->start_element(state->context, (const char *)localname, (const char *)prefix, (const char *)URI,
                                               nb_namespaces, namespaces, nb_attributes, attributes);

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif
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

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;  

    update_ctx(ctx);

    auto srcmllen = ctxt->input->cur - state->base;
    if (srcmllen < 0) {
        fprintf(stderr, "DEBUG:  %s %s %d \n", __FILE__,  __FUNCTION__, __LINE__);
        exit(1);
    }

    state->unitsrcml.append((const char*) state->base, srcmllen);
    state->base = ctxt->input->cur;

    if (localname == MACRO_LIST_ENTRY)
        return;

    // plain end element
    if (localname != UNIT_ENTRY) {
        if (state->create_dom)
            xmlSAX2EndElementNs(ctxt, localname, prefix, URI);

        if (false && state->context->handler->end_element)
            state->context->handler->end_element(state->context, (const char *)localname, (const char *)prefix, (const char *)URI);

        return;
    }

    // the root is the only element so we never got this started
    if (state->mode == ROOT) {

        state->context->is_archive = state->is_archive = false;

        start_root(ctx, state->root.localname, state->root.prefix, state->root.URI,
                        state->root.nb_namespaces, state->root.namespaces.data(),
                        state->root.nb_attributes, 0, state->root.attributes.data());

        start_unit(ctx, state->root.localname, state->root.prefix, state->root.URI,
                        state->root.nb_namespaces, state->root.namespaces.data(),
                        state->root.nb_attributes, 0, state->root.attributes.data());

        characters_unit(ctx, (const xmlChar*) state->characters.c_str(), (int)state->characters.size());
      //  state->characters.clear();
    }

    if (ctxt->nameNr == 2 || !state->is_archive) {

        end_unit(ctx, localname, prefix, URI);
    }

    if (ctxt->nameNr == 1) {

        state->mode = END_ROOT;

        end_root(ctx, localname, prefix, URI);
    }

    if (state->context->terminate)
        return;

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, (const char *)localname);
#endif
}

/**
 * characters_start
 * @param ctx an xmlParserCtxtPtr
 * @param ch the characers
 * @param len number of characters
 *
 * SAX handler function for character handling before we
 * know if we have an archive or not.
 * Immediately calls supplied handlers function.
 */
void characters_start(void* ctx, const xmlChar* ch, int len) {

#ifdef SRCSAX_DEBUG
    std::string chars;
    chars.append((const char *)ch, len);
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, chars.c_str());
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

 //   state->base = ctxt->input->cur;

    // cache the characters since we don't know if in unit or outer archive
    // note that characters() could be called more than once for a particular sequence of characters, so append
    state->characters.append((const char *)ch, len);

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, chars.c_str());
#endif
}

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

#ifdef SRCSAX_DEBUG
    std::string chars;
    chars.append((const char *)ch, len);
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, chars.c_str());
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    state->base = ctxt->input->cur;

    if (state->context->terminate)
        return;

    if (false && state->context->handler->characters_root)
        state->context->handler->characters_root(state->context, (const char *)ch, len);

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, chars.c_str());
#endif
}

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

#ifdef SRCSAX_DEBUG
    std::string chars;
    chars.append((const char *)ch, len);
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, chars.c_str());
    fprintf(stderr, "DEBUG:  %s %s %d len: %zd\n", __FILE__,  __FUNCTION__, __LINE__,  len);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    update_ctx(ctx);

    if (ctxt->input->cur - state->base == 0) {
        state->unitsrcml.append((const char*) ctxt->input->cur, len);
        state->base = ctxt->input->cur + len;
    } else {
        state->unitsrcml.append((const char*) state->base, ctxt->input->cur - state->base);
        state->base = ctxt->input->cur;
    }

    if (state->context->terminate)
        return;

    if (false && len > 0 && state->context->handler->characters_unit)
        state->context->handler->characters_unit(state->context, (const char *)ch, len);

    if (!state->collect_src && !state->collect_srcml)
        return;

    state->unitstr.append((const char*) ch, len);

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d '%s'\n", __FILE__, __FUNCTION__, __LINE__, chars.c_str());
#endif
}

/**
 * comment
 * @param ctx an xmlParserCtxtPtr
 * @param value the comment content
 *
 * A comment has been parsed.
 * Immediately calls supplied handlers function.
 */
void comment(void* ctx, const xmlChar* value) {

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    if (state->context->terminate)
        return;

    if (state->context->handler->comment)
        state->context->handler->comment(state->context, (const char *)value);

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif
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

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    if (state->context->terminate)
        return;

    if (state->context->handler->cdata_block)
        state->context->handler->cdata_block(state->context, (const char *)value, len);

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif
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
void processing_instruction(void* ctx, const xmlChar* target, const xmlChar* data) {

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif

    if (ctx == nullptr)
        return;

    auto ctxt = (xmlParserCtxtPtr) ctx;
    auto state = (sax2_srcsax_handler*) ctxt->_private;

    if (state->context->terminate)
        return;

    if (state->context->handler->processing_instruction)
        state->context->handler->processing_instruction(state->context, (const char *)target, (const char *)data);

#ifdef SRCSAX_DEBUG
    fprintf(stderr, "HERE: %s %s %d\n", __FILE__, __FUNCTION__, __LINE__);
#endif
}
