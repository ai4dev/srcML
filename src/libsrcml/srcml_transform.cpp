/**
 * @file srcml_transform.cpp
 *
 * @copyright Copyright (C) 2013-2014 SDML (www.srcML.org)
 *
 * The srcML Toolkit is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * The srcML Toolkit is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with the srcML Toolkit; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <srcml_macros.hpp>

#include <srcml.h>
#include <srcml_types.hpp>
#include <srcml_sax2_utilities.hpp>

#include <stdio.h>

#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#ifndef _MSC_BUILD
#include <unistd.h>
#else
#include <io.h>
#endif

#include <libxml/parser.h>
#include <libxml/xmlIO.h>

xpath_arguments null_arguments;


/**
 * srcml_append_transform_xpath
 * @param archive a srcml archive
 * @param xpath_string an XPath expression
 *
 * Append the XPath expression to the list
 * of transformation/queries.  As of yet no way to specify context
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_xpath(srcml_archive* archive, const char* xpath_string) {

    if(archive == NULL || xpath_string == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    // FIXME: Temporary fix for xpath_string being munched (by temporary filename)
    // This struct needs to use std::string
    struct xpath_arguments arguments = { strdup(xpath_string), 0, 0, 0, 0, 0, 0, 0 };

    transform tran = { SRCML_XPATH, std::vector<const char *>(1, (const char *)0), arguments, 0 };
    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_xpath_attribute
 * @param archive a srcml archive
 * @param xpath_string an XPath expression
 * @param prefix the attribute prefix
 * @param namespace_uri the attribute namespace
 * @param attr_name the attribute name
 * @param attr_value the attribute value
 *
 * Append the XPath expression to the list
 * of transformation/queries.  As of yet no way to specify context.
 * Instead of outputting the results each in a separte unit tag.  Output the complete
 * archive marking the xpath results with a user provided attribute.
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_xpath_attribute (struct srcml_archive* archive, const char* xpath_string,
                                                            const char* prefix, const char* namespace_uri,
                                                            const char* attr_name, const char* attr_value) {

    if(archive == NULL || xpath_string == 0 || attr_name == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    struct xpath_arguments arguments = { xpath_string, 0, 0, 0, prefix, namespace_uri, attr_name, attr_value };

    transform tran = { SRCML_XPATH, std::vector<const char *>(1, (const char *)0), arguments, 0 };
    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;
}

/**
 * srcml_append_transform_xpath_element
 * @param archive a srcml archive
 * @param xpath_string an XPath expression
 * @param prefix the element prefix
 * @param namespace_uri the element namespace
 * @param element the element name
 *
 * Append the XPath expression to the list
 * of transformation/queries.  As of yet no way to specify context.
 * Instead of outputting the results each in a separte unit tag.  Output the complete
 * archive marking the xpath results with a user provided element.
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_xpath_element (struct srcml_archive* archive, const char* xpath_string,
                                                            const char* prefix, const char* namespace_uri,
                                                            const char* element,
                                                            const char* attr_prefix, const char* attr_namespace_uri,
                                                            const char* attr_name, const char* attr_value) {

    if(archive == NULL || xpath_string == 0 || element == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    struct xpath_arguments arguments = { xpath_string, prefix, namespace_uri, element, attr_prefix, attr_namespace_uri, attr_name, attr_value };

    transform tran = { SRCML_XPATH, std::vector<const char *>(1, (const char *)0), arguments, 0 };
    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;
}

/**
 * srcml_append_transform_xslt_filename
 * @param archive a srcml_archive
 * @param xslt_filename an XSLT program filename path
 *
 * Append the XSLT program filename path to the list
 * of transformation/queries.  As of yet no way to specify parameters or context
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_xslt_filename(srcml_archive* archive, const char* xslt_filename) {

    if(archive == NULL || xslt_filename == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    xmlDocPtr doc = xmlReadFile(xslt_filename, 0, 0);

    transform tran = { SRCML_XSLT, std::vector<const char *>(1, (const char *)0), null_arguments, doc };

    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_xslt_memory
 * @param archive a srcml_archive
 * @param xslt_buffer a buffer holding an XSLT
 * @param size the size of the passed buffer
*
 * Append the XSLT program in the buffer to the list
 * of transformation/queries.  As of yet no way to specify parameters or context
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_xslt_memory(srcml_archive* archive, const char* xslt_buffer, size_t size) {

    if(archive == NULL || xslt_buffer == 0 || size == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    xmlDocPtr doc = xmlReadMemory(xslt_buffer, (int)size, 0, 0, 0);

    transform tran = { SRCML_XSLT, std::vector<const char *>(1, (const char *)0), null_arguments, doc };

    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_xslt_FILE
 * @param archive a srcml_archive
 * @param xslt_file a FILE containing an XSLT program
 *
 * Append the XSLT program in FILE to the list
 * of transformation/queries.  As of yet no way to specify parameters or context
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_xslt_FILE(srcml_archive* archive, FILE* xslt_file) {

    if(archive == NULL || xslt_file == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    xmlRegisterDefaultInputCallbacks();
    xmlDocPtr doc = xmlReadIO(xmlFileRead, 0, xslt_file, 0, 0, 0);

    transform tran = { SRCML_XSLT, std::vector<const char *>(1, (const char *)0), null_arguments, doc };

    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_xslt_fd
 * @param archive a srcml_archive
 * @param xslt_fd a file descriptor containing an XSLT program
 *
 * Append the XSLT program in fd to the list
 * of transformation/queries.  As of yet no way to specify parameters or context
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_xslt_fd(srcml_archive* archive, int xslt_fd) {

    if(archive == NULL || xslt_fd < 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    xmlDocPtr doc = xmlReadFd(xslt_fd, 0, 0, 0);

    transform tran = { SRCML_XSLT, std::vector<const char *>(1, (const char *)0), null_arguments, doc };

    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_relaxng_filename
 * @param archive a srcml archive
 * @param relaxng_filename a RelaxNG schema filename path
 *
 * Append the RelaxNG schema filename path to the list
 * of transformation/queries.
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_relaxng_filename(srcml_archive* archive, const char* relaxng_filename) {

    if(archive == NULL || relaxng_filename == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    xmlDocPtr doc = xmlReadFile(relaxng_filename, 0, 0);

    transform tran = { SRCML_RELAXNG, std::vector<const char *>(1, (const char *)0), null_arguments, doc };

    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_relaxng_memory
 * @param archive a srcml archive
 * @param relaxng_buffer a buffer holding a RelaxNG schema
 * @param size the size of the passed buffer
 *
 * Append the RelaxNG schema in the buffer to the list
 * of transformation/queries.
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_relaxng_memory(srcml_archive* archive, const char* relaxng_buffer, size_t size) {

    if(archive == NULL || relaxng_buffer == 0 || size == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    xmlDocPtr doc = xmlReadMemory(relaxng_buffer, (int)size, 0, 0, 0);

    transform tran = { SRCML_RELAXNG, std::vector<const char *>(1, (const char *)0), null_arguments, doc };

    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_relaxng_FILE
 * @param archive a srcml archive
 * @param relaxng_file a FILE containing aRelaxNG schema
 *
 * Append the RelaxNG schema in FILE to the list
 * of transformation/queries.
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_relaxng_FILE(srcml_archive* archive, FILE* relaxng_file) {

    if(archive == NULL || relaxng_file == 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    xmlRegisterDefaultInputCallbacks();
    xmlDocPtr doc = xmlReadIO(xmlFileRead, 0, relaxng_file, 0, 0, 0);

    transform tran = { SRCML_RELAXNG, std::vector<const char *>(1, (const char *)0), null_arguments, doc };

    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_relaxng_fd
 * @param archive a srcml archive
 * @param relaxng_fd a file descriptor containing a RelaxNG schema
 *
 * Append the RelaxNG schema in fd to the list
 * of transformation/queries.
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_append_transform_relaxng_fd(srcml_archive* archive, int relaxng_fd) {

    if(archive == NULL || relaxng_fd < 0) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;

    xmlDocPtr doc = xmlReadFd(relaxng_fd, 0, 0, 0);

    transform tran = { SRCML_RELAXNG, std::vector<const char *>(1, (const char *)0), null_arguments, doc };

    archive->transformations.push_back(tran);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_param
 * @param archive a srcml archive
 * @param xpath_param_name name of a parameter
 * @param xpath_param_value value of the named parameter
 *
 * Append the parameter to the last transformation.
 *
 * @returns Returns SRCML_STATUS_OK on success and a status errors code on failure.
 */
int srcml_append_transform_param(srcml_archive* archive, const char* xpath_param_name, const char* xpath_param_value) {

    if(archive == NULL || xpath_param_name == NULL || xpath_param_value == NULL) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;
    if(archive->transformations.size() == 0) return SRCML_STATUS_NO_TRANSFORMATION;

    archive->transformations.back().xsl_parameters.pop_back();
    archive->transformations.back().xsl_parameters.push_back(xpath_param_name);
    archive->transformations.back().xsl_parameters.push_back(strdup(xpath_param_value));
    archive->transformations.back().xsl_parameters.push_back(0);

    return SRCML_STATUS_OK;

}

/**
 * srcml_append_transform_stringparam
 * @param archive a srcml archive
 * @param xpath_param_name name of a parameter
 * @param xpath_param_value value of the named parameter will be wrapped in "
 *
 * Append the parameter to the last transformation with the value wrapped in ".
 *
 * @returns Returns SRCML_STATUS_OK on success and a status errors code on failure.
 */
int srcml_append_transform_stringparam(srcml_archive* archive, const char* xpath_param_name, const char* xpath_param_value) {

    if(archive == NULL || xpath_param_name == NULL || xpath_param_value == NULL) return SRCML_STATUS_INVALID_ARGUMENT;
    if(archive->type != SRCML_ARCHIVE_READ && archive->type != SRCML_ARCHIVE_RW) return SRCML_STATUS_INVALID_IO_OPERATION;
    if(archive->transformations.size() == 0) return SRCML_STATUS_NO_TRANSFORMATION;

    archive->transformations.back().xsl_parameters.pop_back();
    archive->transformations.back().xsl_parameters.push_back(xpath_param_name);

    size_t xpath_param_value_length = strlen(xpath_param_value);
    char * string_value = new char[xpath_param_value_length + 3];
    string_value[0] = '"';
    strncpy(string_value + 1, xpath_param_value, xpath_param_value_length);
    string_value[xpath_param_value_length + 1] = '"';
    string_value[xpath_param_value_length + 2] = 0;

    archive->transformations.back().xsl_parameters.push_back(string_value);
    archive->transformations.back().xsl_parameters.push_back(0);

    return SRCML_STATUS_OK;

}

/**
 * srcml_clear_transforms
 * @param archive an archive
 *
 * Remove all transformations from archive.
 *
 * @returns SRCML_STATUS_OK on success and SRCML_STATUS_INVALID_ARGUMENT on failure.
 */
int srcml_clear_transforms(srcml_archive * archive) {

    if(archive == NULL) return SRCML_STATUS_INVALID_ARGUMENT;

    for(std::vector<transform>::iterator itr = archive->transformations.begin(); itr != archive->transformations.end(); ++itr) {

        for(std::vector<const char *>::size_type pos = 1; pos < itr->xsl_parameters.size(); pos += 2)
            delete itr->xsl_parameters[pos];

        if(itr->type == SRCML_XSLT || itr->type == SRCML_RELAXNG)
            xmlFreeDoc(itr->doc);

    }

    archive->transformations.clear();

    return SRCML_STATUS_OK;

}

/**
 * srcml_apply_transforms
 * @param iarchive an input srcml archive
 * @param oarchive and output srcml archive
 *
 * Apply appended transformations inorder added and consecutively.
 * Intermediate results are stored in a temporary file.
 * Transformations are cleared.
 *
 * @returns Returns SRCML_STATUS_OK on success and a status error codes on failure.
 */
int srcml_apply_transforms(srcml_archive* iarchive, srcml_archive* oarchive) {

    if(iarchive == NULL || oarchive == NULL) return SRCML_STATUS_INVALID_ARGUMENT;
    if((iarchive->type != SRCML_ARCHIVE_READ && iarchive->type != SRCML_ARCHIVE_RW)
        || (oarchive->type != SRCML_ARCHIVE_WRITE && oarchive->type != SRCML_ARCHIVE_RW)) return SRCML_STATUS_INVALID_IO_OPERATION;

    static const char * transform_filename_template = "srcml_transform_XXXXXXXX";

    const char * last_transform_filename = 0;
    for(std::vector<transform>::size_type i = 0; i < iarchive->transformations.size(); ++i) {

        char * transform_filename = STRDUP(transform_filename_template);
        if(!transform_filename) {

            if(last_transform_filename) UNLINK(last_transform_filename);
            free((void *)last_transform_filename);
            return SRCML_STATUS_ERROR;

        }

#if defined(__GNUG__) && !defined(__MINGW32__)
        int transform_fd = mkstemp(transform_filename);
#else
        MKTEMP(transform_filename);
        int transform_fd = OPEN(transform_filename, O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
#endif

        xmlParserInputBufferPtr pinput = 0;
        if(i == 0) pinput = iarchive->input;
        else pinput = xmlParserInputBufferCreateFilename(last_transform_filename, xmlParseCharEncoding(0));

        if(pinput == NULL) {

            CLOSE(transform_fd);
            free((void *)transform_filename);
            return SRCML_STATUS_INVALID_INPUT;

        }
        int error = 0;
        try {

            switch(iarchive->transformations.at(i).type) {

            case SRCML_XPATH: {

                error = srcml_xpath(pinput, "src:unit",
                                    iarchive->transformations.at(i).arguments.str,
                                    iarchive->transformations.at(i).arguments.prefix, iarchive->transformations.at(i).arguments.uri,
                                    iarchive->transformations.at(i).arguments.element,
                                    iarchive->transformations.at(i).arguments.attr_prefix, iarchive->transformations.at(i).arguments.attr_uri,
                                    iarchive->transformations.at(i).arguments.attr_name, iarchive->transformations.at(i).arguments.attr_value,
                                    transform_fd, oarchive->options);
                break;
            }

            case SRCML_XSLT: {

                error = srcml_xslt(pinput, "src:unit",
                                   iarchive->transformations.at(i).doc,
                                   &iarchive->transformations.at(i).xsl_parameters.front(), 0, transform_fd, oarchive->options);
                break;
            }

            case SRCML_RELAXNG: {

                error = srcml_relaxng(pinput,
                                      iarchive->transformations.at(i).doc,
                                      transform_fd, oarchive->options);
                break;
            }

            default : break;

            }

        } catch(...) {

            CLOSE(transform_fd);
            if(i != 0) xmlFreeParserInputBuffer(pinput);
            if(last_transform_filename)  UNLINK(last_transform_filename);
            free((void *)last_transform_filename);

            return SRCML_STATUS_INVALID_INPUT;
        }

        if(i != 0) xmlFreeParserInputBuffer(pinput);
        if(last_transform_filename) UNLINK(last_transform_filename);
        free((void *)last_transform_filename);
        last_transform_filename = transform_filename;
        if(error != SRCML_STATUS_OK) {
            if(last_transform_filename) UNLINK(last_transform_filename);
            free((void *)last_transform_filename);
            return error;
        }

    }

    srcml_archive * tmp_archive = srcml_create_archive();

    srcml_read_open_filename(tmp_archive, last_transform_filename);
    tmp_archive->prefixes.swap(oarchive->prefixes);
    tmp_archive->namespaces.swap(oarchive->namespaces);
 
    /** @todo ask if should rely on user to have correct to bit-or these */
    srcml_archive_set_options(oarchive, srcml_archive_get_options(tmp_archive));

    srcml_unit * unit;
    while((unit = srcml_read_unit(tmp_archive))) {

        srcml_write_unit(oarchive, unit);
        srcml_free_unit(unit);

    }

    srcml_close_archive(tmp_archive);
    srcml_free_archive(tmp_archive);
    if(last_transform_filename) UNLINK(last_transform_filename);
    free((void *)last_transform_filename);

    srcml_clear_transforms(iarchive);

    return SRCML_STATUS_OK;

}
