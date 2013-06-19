from ctypes import *
# language constants
LANGUAGE_NONE = ("", 64)
LANGUAGE_C = ("C", 1)
LANGUAGE_CS = ("C#", 32)
LANGUAGE_CXX = ("C++", 2)
LANGUAGE_CXX_11 = ("C++11", 4)
LANGUAGE_JAVA = ("Java", 8)
LANGUAGE_ASPECTJ = ("AspectJ", 16)
LANGUAGE_CSHARP = ("C#", 32)

# parsing options
OPTION_DEBUG           = 1 << 0

OPTION_NESTED          = 1 << 1
OPTION_LITERAL         = 1 << 2
OPTION_CPP_MARKUP_ELSE = 1 << 22
OPTION_XPATH_TOTAL     = OPTION_CPP_MARKUP_ELSE
OPTION_CPP_MARKUP_IF0  = 1 << 23
OPTION_EXPRESSION      = 1 << 25
OPTION_CPP             = 1 << 28
OPTION_OPERATOR        = 1 << 16
OPTION_MODIFIER        = 1 << 17

# default uri
URI_TYPE = c_char_p * 8
URI_PREFIX = URI_TYPE("", "cpp", "err", "lit", "op", "type", "pos", None )
