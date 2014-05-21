/**
 * @file srcml.cpp
 *
 * @copyright Copyright (C) 2014 SDML (www.srcML.org)
 *
 * This file is part of the srcml command-line client.
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
 * along with the srcml command-line client; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <srcml.h>
#include <srcml_cli.hpp>
#include <srcml_options.hpp>
#include <create_srcml.hpp>
#include <decompress_srcml.hpp>
#include <compress_srcml.hpp>
#include <create_src.hpp>
#include <transform_srcml.hpp>
#include <srcml_display_metadata.hpp>
#include <srcml_execute.hpp>
#include <isxml.hpp>

#include <archive.h>
#include <iostream>

bool request_create_srcml          (const srcml_request_t&, const srcml_input_t&, const srcml_output_dest&);
bool request_transform_srcml       (const srcml_request_t&, const srcml_input_t&, const srcml_output_dest&);
bool request_display_metadata      (const srcml_request_t&, const srcml_input_t&, const srcml_output_dest&);
bool request_additional_compression(const srcml_request_t&, const srcml_input_t&, const srcml_output_dest&);
bool request_create_src            (const srcml_request_t&, const srcml_input_t&, const srcml_output_dest&);

int main(int argc, char * argv[]) {

    // parse the command line
    srcml_request_t srcml_request = parseCLI(argc, argv);

    // version
    if (srcml_request.command & SRCML_COMMAND_VERSION) {
        std::cout <<  srcml_version_string() << "\n";
        std::cout << "srcml Version Number " << srcml_version_number() << "\n";
        std::cout << "libarchive Version " << ARCHIVE_VERSION_NUMBER << "\n";
        return 0;
    }

    // setup global access to options
    SRCMLOptions::set(srcml_request.command);

    // convert the list of input filenames to input sources
    srcml_input_t input_sources(srcml_request.input.begin(), srcml_request.input.end());

    // standard input handled as FILE* to determine if srcML or src
    if (srcml_request.stdindex) {

        srcml_input_src* pstdin = &input_sources[*srcml_request.stdindex];

        // FILE* becomes part of stdin input source
        pstdin->fileptr = fdopen(STDIN_FILENO, "r");
        pstdin->fd = boost::none;

        // determine if the input is srcML or src
        pstdin->state = isxml(*(pstdin->fileptr)) ? SRCML : SRC;

        // language is required when standard input is used for source
        if ((pstdin->state == SRC) && !srcml_request.att_language) {
            std::cerr << "Using stdin requires a declared language\n";
            exit(1);
        }
    }

    // output destination
    srcml_output_dest destination(srcml_request.output_filename ? *srcml_request.output_filename : "");

    // determine what processing needs to occur by setting up an internal pipeline
    processing_steps_t pipeline;

    // src->srcml
    if (request_create_srcml(srcml_request, input_sources, destination)) {

        pipeline.push_back(create_srcml);
    }

    // XPath, XSLT, and RelaxNG processing
    if (request_transform_srcml(srcml_request, input_sources, destination)) {

        pipeline.push_back(transform_srcml);
    }

    // metadata output
    if (request_display_metadata(srcml_request, input_sources, destination)) {

        pipeline.push_back(srcml_display_metadata);
    }
    
    // srcml->src
    if (request_create_src(srcml_request, input_sources, destination)) {

        pipeline.push_back(create_src);
    }

    // additional output compression
    if (request_additional_compression(srcml_request, input_sources, destination)) {

#if ARCHIVE_VERSION_NUMBER > 3001002
        pipeline.push_back(compress_srcml);
#else
        std::cerr << "Unsupported output compression\n";
        exit(1);
#endif
    }

    // should always have something to do
    assert(!pipeline.empty());

    // execute the pipeline
    srcml_execute(srcml_request, pipeline, input_sources, destination);

    srcml_cleanup_globals();

    return 0;
}

bool request_create_srcml(const srcml_request_t& /* srcml_request */, 
                          const srcml_input_t& input_sources,
                          const srcml_output_dest& destination) {

    return std::find_if(input_sources.begin(), input_sources.end(), is_src) != input_sources.end() ||
        (input_sources.size() > 1 && destination.state == SRCML);
}

bool request_transform_srcml(const srcml_request_t& srcml_request,
                             const srcml_input_t& /* input_sources */,
                             const srcml_output_dest& /* destination */) {

    return !srcml_request.transformations.empty();
}

bool request_display_metadata(const srcml_request_t& srcml_request,
                              const srcml_input_t& /* input_sources */,
                              const srcml_output_dest& /* destination */) {

    return (srcml_request.command & SRCML_COMMAND_INSRCML) || srcml_request.unit > 0;
}

bool request_additional_compression(const srcml_request_t& /* srcml_request */,
                                    const srcml_input_t& /* input_sources */,
                                    const srcml_output_dest& destination) {

    return (destination.compressions.size() > 1) ||
        (destination.compressions.size() == 1 && destination.compressions.front() != ".gz");
}

bool request_create_src(const srcml_request_t& srcml_request,
                        const srcml_input_t& input_sources,
                        const srcml_output_dest& destination) {

    return destination.state != SRCML && !request_display_metadata(srcml_request, input_sources, destination);
}
