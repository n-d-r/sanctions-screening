#===============================================================================
# Setup
#===============================================================================

from ss_constants import XMLNS

#===============================================================================
# Functions
#===============================================================================

def ns(tag, xmlns='http://www.un.org/sanctions/1.0'):
  return '{{{xmlns}}}{tag}'.format(xmlns=xmlns, tag=tag)