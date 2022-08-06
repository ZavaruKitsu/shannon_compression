###################################
# Practice configuration file #
###################################

# AZAR ARCHIVE STRUCTURE:
#
# MAGIC_HEADER
# DATA_LENGTH
# LETTER[]
# MAGIC_SEPARATOR
# CODE[]
# MAGIC_SEPARATOR
# DATA

# ZavaruKitsu ARchive
ARCHIVE_EXTENSION = 'azar'

#
# Encoding options
#
ENCODING = 'utf-8'
BYTE_ORDER = 'little'

#
# File structure options
#
MAGIC_HEADER = 'azAR'.encode(ENCODING)
MAGIC_SEPARATOR = 'RAza'.encode(ENCODING)
SYMBOL_SEPARATOR = '\0'.encode(ENCODING)

INT_LENGTH = 4
SYMBOL_LENGTH = 4

CALLBACK_STEP = 80
