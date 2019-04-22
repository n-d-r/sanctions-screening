#===============================================================================
# Setup
#===============================================================================

import xml.etree.cElementTree as cET

from ss_variables import *
from ss_constants import *
from ss_functions import *
from ss_parsing_classes import DistinctParty, Location, Feature, CommandFormatter

#===============================================================================
# Parsing lists - Specially Designated Nationals List (SDN List)
#===============================================================================

if __name__ == '__main__':

  sdn = cET.iterparse('sdn_list.xml', events=('end',))

  for event, elem in sdn:
   
    if elem.tag==ns('AliasType'):
      alias_types[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('AreaCode'):
      area_codes[elem.attrib['ID']] = {
        'CountryID': elem.attrib['CountryID'],
        'Description': elem.attrib['Description'],
        'Text': elem.text
      }
      elem.clear()

    elif elem.tag==ns('Country'):
      if 'ISO2' in elem.attrib.keys():
        countries[elem.attrib['ID']] = {
          'ISO2': elem.attrib['ISO2'],
          'Text': elem.text
        }
      else:
        countries[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('DetailReference'):
      detail_references[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('DetailType'):
      detail_types[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('FeatureType'):
      feature_types[elem.attrib['ID']] = {
        'FeatureTypeGroupID': elem.attrib['FeatureTypeGroupID'],
        'Text': elem.text
      }
      elem.clear()

    elif elem.tag==ns('IDRegDocType'):
      id_reg_doc_types[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('LegalBasis'):
      legal_bases[elem.attrib['ID']] = {
        'LegalBasisShortRef': elem.attrib['LegalBasisShortRef'],
        'LegalBasisTypeID': elem.attrib['LegalBasisTypeID'],
        'SanctionsProgramID': elem.attrib['SanctionsProgramID'],
        'Text': elem.text
      }
      elem.clear()

    elif elem.tag==ns('List'):
      lists[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('LocPartType'):
      loc_part_types[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('NamePartType'):
      name_part_types[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('PartySubType'):
      party_sub_types[elem.attrib['ID']] = {
        'PartyTypeID': elem.attrib['PartyTypeID'],
        'Text': elem.text
      }
      elem.clear()

    elif elem.tag==ns('PartyType'):
      party_types[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('RelationQuality'):
      relation_quality[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('RelationType'):
      relation_types[elem.attrib['ID']] = {
        'Symmetrical': elem.attrib['Symmetrical'],
        'Text': elem.text
      }
      elem.clear()

    elif elem.tag==ns('Reliability'):
      reliability[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('SanctionsProgram'):
      sanctions_programs[elem.attrib['ID']] = {
        'SubsidiaryBodyID': elem.attrib['SubsidiaryBodyID'],
        'Text': elem.text
      }
      elem.clear()

    elif elem.tag==ns('SanctionsType'):
      sanctions_types[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    elif elem.tag==ns('Script'):
      scripts[elem.attrib['ID']] = {
        'ScriptCode': elem.attrib['ScriptCode'],
        'Text': elem.text
      }
      elem.clear()

    elif elem.tag==ns('Validity'):
      validity_values[elem.attrib['ID']] = {'Text': elem.text}
      elem.clear()

    # elif elem.tag==ns('Location'):
    #   location = Location(elem.attrib['ID'])
    #   location.set_area_code(elem.findall(ns('LocationAreaCode')))
    #   location.set_country(elem.findall(ns('LocationCountry')))
    #   location.set_location_parts(elem.findall(ns('LocationPart')))
    #   location.commit()
    #   elem.clear()

    elif elem.tag==ns('DistinctParty'):
      distinct_party = DistinctParty(elem.attrib['FixedRef'])
      distinct_party.process_element(elem)
      distinct_party.commit()
      elem.clear()

    elif elem.tag==ns('Feature'):
      ftr = Feature(elem.attrib['ID'])
      ftr.process_element(elem)
      ftr.commit()
      elem.clear()

    elif elem.tag.split('}')[-1] in TAGS_TO_IGNORE:
      elem.clear()

    # else:
    #   print('[!] found unknown tag: {}'.format(elem.tag.split('}')[-1]))