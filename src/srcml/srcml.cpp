/*
  srcml.cpp

  Copyright (C) 2013  SDML (www.srcML.org)

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

/*
  The srcml program to transform to/from the srcML format, plus provides a variety of
  querying and transformation features.

  Replaces the src2srcml and srcml2src of the original srcML toolkit.
*/

#include <srcml.h>
#include <srcmlCLI.hpp>
#include <thread_queue.hpp>

#include <archive.h>
#include <archive_entry.h>
//#include <curl/curl.h>
#include <pthread.h>

#include <iostream>
#include <string>

struct ParseRequest {
    ParseRequest() : buffer(0) {}

    void swap(ParseRequest& other) {

        filename.swap(other.filename);
        buffer.swap(other.buffer);
    }

    // empty ParseRequests indicate termination
    bool empty() const {
        return filename.empty() && buffer.empty();
    }

    std::string filename;
    std::vector<char> buffer;
};

ParseRequest NullParseRequest;

bool checkLocalFile(const std::string& pos_arg) {
  FILE * local;
  if(pos_arg.find("http:") == std::string::npos){
    local = fopen(pos_arg.c_str(),"r");
    if (local == NULL) {
      std::cerr << "File " << pos_arg << " not found.\n";
      return false;
    }
    fclose(local);
  }
  return true;
}

bool convenienceCheck(const std::string& filename) {
  archive * arch = archive_read_new();
  archive_entry * arch_entry = archive_entry_new();

  archive_read_support_format_7zip(arch);
  archive_read_support_format_ar(arch);
  archive_read_support_format_cab(arch);
  archive_read_support_format_cpio(arch);
  archive_read_support_format_gnutar(arch);
  archive_read_support_format_iso9660(arch);
  archive_read_support_format_lha(arch);
  archive_read_support_format_mtree(arch);
  archive_read_support_format_rar(arch);
  archive_read_support_format_tar(arch);
  archive_read_support_format_xar(arch);
  archive_read_support_format_zip(arch);
  archive_read_support_format_raw(arch);

  archive_read_support_filter_all(arch);

  if(archive_read_open_filename(arch, filename.c_str(), 16384) == ARCHIVE_OK) {
    if(archive_read_next_header(arch, &arch_entry) == ARCHIVE_OK) {
      if(archive_filter_code(arch,0) == ARCHIVE_FILTER_NONE &&
        archive_format(arch) == ARCHIVE_FORMAT_RAW){
        archive_read_finish(arch);
        return true;
      }
    }
  }
  archive_read_finish(arch);
  return false;
}

int main(int argc, char * argv[]) {
  
  srcml_request_t srcml_request = srcmlCLI::parseCLI(argc, argv);

  // CHECK FOR INVALID GLOBAL FLAGS
  if (srcml_request.encoding != "" && srcml_check_encoding(srcml_request.encoding.c_str()) == 0) {
    std::cerr << "Invalid Encoding.\n";
    return 1; //ERROR CODE TBD
  }

  if (srcml_request.language != "" && srcml_check_language(srcml_request.language.c_str()) == 0) {
    std::cerr << "Invalid Language.\n";
    return 1; //ERROR CODE TBD
  }

  if (srcml_request.tabs <= 0) {
    std::cerr << "Invalid Tab Stop.\n";
    return 1; //ERROR CODE TBD
  }
  
  // SET GLOBAL OPTIONS
  if (srcml_request.encoding != "") {
    srcml_set_encoding(srcml_request.encoding.c_str());
  }
  if (srcml_request.filename != "") {
    srcml_set_filename(srcml_request.filename.c_str());
  }
  //TODO: THIS NEEDS A FLAG TOO AS "" CAN BE A VALID DIRECTORY
  if (srcml_request.directory != "") {
    srcml_set_directory(srcml_request.directory.c_str());
  }
  if (srcml_request.src_versions != "") {
    srcml_set_version(srcml_request.src_versions.c_str());
  }
  if (srcml_request.markup_options != 0) {
    srcml_set_all_options(srcml_request.markup_options);
  }
  
  if (srcml_request.language != "") {
    srcml_set_language(srcml_request.language.c_str());  
  }
  else {
    srcml_set_language(SRCML_LANGUAGE_NONE);  
  }

  srcml_set_tabstop(srcml_request.tabs);

  for(int i = 0; i < srcml_request.register_ext.size(); ++i) {
    int pos = srcml_request.register_ext[i].find('=');
    srcml_register_file_extension(srcml_request.register_ext[i].substr(0,pos).c_str(),
          srcml_request.register_ext[i].substr(pos+1).c_str());
  }

  for(int i = 0; i < srcml_request.xmlns_prefix.size(); ++i) {
    int pos = srcml_request.xmlns_prefix[i].find('=');
    srcml_register_namespace(srcml_request.xmlns_prefix[i].substr(0,pos).c_str(),
           srcml_request.xmlns_prefix[i].substr(pos+1).c_str());
  }

  /* 
    MIGHT USE THIS LATER:
    CHECK TO SEE WHAT VERSION OF LIBARCHIVE IS RUNNING
    SWITCH ON FEATURES (LIBARCHIVE FOR DIRECTORY, ETC.)
    #if ARCHIVE_VERSION_NUMBER < 3000000
      //YOU HAVE V2 OR LOWER
    #else
      //YOU HAVE V3 OR HIGHER
    #endif
  */

  ThreadQueue<ParseRequest, 10> queue;
  
  if (srcml_request.positional_args.empty()) {
    std::cerr << "No input files found.\n";
    return 0;
  }
  
  for (int i = 0; i < srcml_request.positional_args.size(); ++i) {
    if (!checkLocalFile(srcml_request.positional_args[i]))
      return 1;
  } 

  if (srcml_request.positional_args.size() == 1) {
    if(convenienceCheck(srcml_request.positional_args[0])) {
      srcml(srcml_request.positional_args[0].c_str(), srcml_request.output.c_str());
      return 0;
    }
  }
  
  // libsrcML Setup
  srcml_archive * srcml_arch = srcml_create_archive();
  srcml_write_open_filename(srcml_arch, srcml_request.output.c_str());

  for (int i = 0; i < srcml_request.positional_args.size(); ++i) {
    
    // libArchive Setup
    archive * arch = archive_read_new();
    archive_entry * arch_entry = archive_entry_new();

    archive_read_support_format_7zip(arch);
    archive_read_support_format_ar(arch);
    archive_read_support_format_cab(arch);
    archive_read_support_format_cpio(arch);
    archive_read_support_format_empty(arch);
    archive_read_support_format_gnutar(arch);
    archive_read_support_format_iso9660(arch);
    archive_read_support_format_lha(arch);
    archive_read_support_format_mtree(arch);
    archive_read_support_format_rar(arch);
    archive_read_support_format_raw(arch);
    archive_read_support_format_tar(arch);
    archive_read_support_format_xar(arch);
    archive_read_support_format_zip(arch);

    archive_read_support_filter_all(arch);

    if(archive_read_open_filename(arch, srcml_request.positional_args[i].c_str(), 16384) == ARCHIVE_OK) {
      const void* buffer;
      const char* cptr;
      size_t size;
      int64_t offset;

      while (archive_read_next_header(arch, &arch_entry) == ARCHIVE_OK) { 
        srcml_unit * unit = srcml_create_unit(srcml_arch);
        std::string filename = archive_entry_pathname(arch_entry);

        /* 
          The header path for a standard file is just "data".
          That needs to be swapped out with the actual file name from the 
          CLI arg.
        */
        if (filename.compare("data") != 0) {
          srcml_unit_set_filename(unit, filename.c_str());
          srcml_unit_set_language(unit, srcml_archive_check_extension(srcml_arch, filename.c_str()));
        }
        else {
          srcml_unit_set_filename(unit, srcml_request.positional_args[i].c_str()); 
          srcml_unit_set_language(unit, srcml_archive_check_extension(srcml_arch, srcml_request.positional_args[i].c_str()));
        }
        
        while (true) {
          int readStatus = archive_read_data_block(arch, &buffer, &size, &offset);
          cptr = (char*)buffer;
          
          if (readStatus != ARCHIVE_OK) {
            break;
          }
          
          srcml_parse_unit_memory(unit, cptr, size);
          srcml_write_unit(srcml_arch, unit);
        }
      }
    }
    else {
      std::cerr << "Unable to open archive\n";
      return 1;
    }
    archive_read_finish(arch);
  }

  srcml_close_archive(srcml_arch);
  srcml_free_archive(srcml_arch);

  return 0;
}