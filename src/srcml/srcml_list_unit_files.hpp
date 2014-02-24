/*
  srcml_list_unit_files.cpp

  Copyright (C) 2014  SDML (www.srcML.org)

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
  srcml_list_unit_files.cpp function for listing all unit files contained in a srcml archive
*/

#ifndef SRCML_LIST_UNIT_FILES_HPP
#define SRCML_LIST_UNIT_FILES_HPP

#include <string>
#include <vector>

void srcml_list_unit_files(const std::vector<std::string>& pos_args);
void srcml_list_unit_files(const std::string& srcml_input);

#endif