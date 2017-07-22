/**
 * @file write_queue.hpp
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

#ifndef WRITE_QUEUE_HPP
#define WRITE_QUEUE_HPP

#include <srcml.h>
#include <parse_request.hpp>
#include <ctpl_stl.h>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <queue>
#include <deque>
#include <thread>

struct WriteOrder {
    bool operator()(ParseRequest* r1, ParseRequest* r2) {
        return r1->position > r2->position;
    }
};

class WriteQueue {

public:
    WriteQueue(std::function<void(ParseRequest*)> writearg, bool ordered = true);

    /* writes out the current srcml */
    void schedule(ParseRequest* pvalue);

    void eos(ParseRequest* pvalue);

    void wait();

    static void process();

public:
    static std::function<void(ParseRequest*)> write;
    static bool ordered;
    std::thread* pwrite_thread;
    std::atomic<int> maxposition;
    static std::priority_queue<ParseRequest*, std::deque<ParseRequest*>, WriteOrder> q;
    static std::mutex gmutex;
    static std::condition_variable cv;
    static std::condition_variable cv2;
};

#endif
