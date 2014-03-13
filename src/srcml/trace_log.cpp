/**
 * @file trace_log.cpp
 *
 * @copyright @copyright Copyright (C) 2014 SDML (www.srcML.org)
 *
 * This file is part of the srcML Toolkit.
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

#include <trace_log.hpp>

TraceLog::TraceLog(std::ostream& out, int options)
        : out(out), count(0), overallcount(0) {

        enabled = options & SRCML_COMMAND_VERBOSE;
    }

TraceLog& operator<<(TraceLog& tlog, char c) {

    if (!tlog.enabled)
        return tlog;

    if (c != '-')
        ++tlog.count;

    tlog.out << std::setw(5) << tlog.count;

    return tlog;
}

TraceLog& operator<<(TraceLog& tlog, const std::string& s) {

    if (!tlog.enabled)
        return tlog;

    tlog.out << s << '\n';

    return tlog;
}