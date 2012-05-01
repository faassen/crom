import sys, types

if sys.version_info[0] < 3: #pragma NO COVER
    CLASS_TYPES = (type, types.ClassType)  
else: #pragma NO COVER
    CLASS_TYPES = (type,)
