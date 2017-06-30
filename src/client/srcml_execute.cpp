/**
 * @file srcml_execute.cpp
 *
 * @copyright Copyright (C) 2014 srcML, LLC. (www.srcML.org)
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

#include <srcml_execute.hpp>
#include <boost/foreach.hpp>

#if defined(_MSC_BUILD) || defined(__MINGW32__)
#include <io.h>
#include <fcntl.h>
#include <windows.h>
#endif

#include <thread>
#include <list>

void join(std::thread& t)
{
    t.join();
}

void srcml_execute(const srcml_request_t& srcml_request,
                   std::list<process_srcml>& pipeline,
                   const srcml_input_t& input_sources,
                   const srcml_output_dest& destination) {

    // create a thread for each step, creating pipes between adjoining steps
    std::list<std::thread> pipethreads;
    int fds[2] = { -1, -1 };
    BOOST_FOREACH(process_srcml command, pipeline) {

        // special handling for first and last steps
        bool first = command == pipeline.front();
        bool last  = command == pipeline.back();

        // pipe between each step
        int prevoutfd = fds[0];
        fds[0] = fds[1] = -1;
        if (pipeline.size() > 1 && !last) {
#if !defined(_MSC_BUILD) && !defined(__MINGW32__)
            pipe(fds);
#else
            HANDLE read_pipe;
            HANDLE write_pipe;
            CreatePipe(&read_pipe,&write_pipe, NULL, 0);

            fds[1] = _open_osfhandle((intptr_t)write_pipe, 0);
            fds[0] = _open_osfhandle((intptr_t)read_pipe, _O_RDONLY);
#endif
        }

        /* run this step in the sequence */
        pipethreads.push_back(std::thread(
            command,
            srcml_request,
            /* first process_srcml uses input_source, rest input from previous output pipe */
            first ? input_sources : srcml_input_t(1, srcml_input_src("stdin://-", prevoutfd)),
            /* last process_srcml uses destination, rest output to pipe */                
            last  ? destination   : srcml_output_dest("-", fds[1])
        ));
    }

    // wait on all threads
    std::for_each(pipethreads.begin(), pipethreads.end(), join);
}
