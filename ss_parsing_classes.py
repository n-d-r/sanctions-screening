#===============================================================================
# Setup
#===============================================================================

import re
import sqlite3

from ss_variables import area_codes, countries, name_part_types
from ss_functions import ns
from ss_constants import DB_NAME, DB_TABLE_INDIVIDUALS, DB_TABLE_ENTITIES, DB_TABLE_VESSELS, DB_TABLE_AIRCRAFT

#===============================================================================
# Classes
#===============================================================================

class CommandFormatter(object):

  def __init__(self):
    pass

  @staticmethod
  def format_individual_command(to_submit):
    return """
      INSERT INTO {tbl}(
        party_fixedref,
        profile_id,
        identity_id,
        alias_fixedref,
        name_id,
        first,
        middle,
        last,
        nickname,
        maiden,
        patronymic,
        matronymic,
        full_name,
        full_name_sorted
      )
      VALUES(
        "{party_fixedref}",
        "{profile_id}",
        "{identity_id}",
        "{alias_fixedref}",
        "{name_id}",
        "{first}",
        "{middle}",
        "{last}",
        "{nickname}",
        "{maiden}",
        "{patronymic}",
        "{matronymic}",
        "{full_name}",
        "{full_name_sorted}"
      );
    """.format(tbl=to_submit['tbl'],
               party_fixedref=to_submit['fixedref'],
               profile_id=to_submit['profile_id'],
               identity_id=to_submit['identity_id'],
               alias_fixedref=to_submit['AliasFixedRef'],
               name_id=to_submit['DocumentedNameID'],
               first=to_submit['First Name'],
               middle=to_submit['Middle Name'],
               last=to_submit['Last Name'],
               nickname=to_submit['Nickname'],
               maiden=to_submit['Maiden Name'],
               patronymic=to_submit['Patronymic'],
               matronymic=to_submit['Matronymic'],
               full_name=to_submit['full_name'],
               full_name_sorted=to_submit['full_name_sorted'])


class DistinctParty(object):

  def __init__(self, fixedref):
    self.fixedref = fixedref

  def _sanitize(self, string):
    return ''.join([char for char in string if char not in '"/\\\''])

  def _process_name_part_groups(self, identity, 
                                name_part_type_lookup=name_part_types):
    name_part_groups = identity.find(ns('NamePartGroups'))
    master_name_part_groups = {}
    for group in name_part_groups.findall(ns('MasterNamePartGroup')):
      name_part_group = group.find(ns('NamePartGroup'))
      master_name_part_groups[name_part_group.attrib['ID']] = (
        name_part_type_lookup[name_part_group.attrib['NamePartTypeID']]['Text']
      )
    self.name_part_type_lookup = master_name_part_groups

  def _process_aliases(self, identity):
    self.names = []
    aliases = identity.findall(ns('Alias'))
    for alias in aliases:
      documented_names = alias.findall(ns('DocumentedName'))
      for name in documented_names:
        new_name = {
          'DocumentedNameID': name.attrib['ID'],
          'AliasFixedRef': alias.attrib['FixedRef'],
          'AliasTypeID': alias.attrib['AliasTypeID']
        }
        name_parts = name.findall(ns('DocumentedNamePart'))
        for part in name_parts:
          name_part_value = part.find(ns('NamePartValue'))
          name_part_type = (
            self.name_part_type_lookup[name_part_value.attrib['NamePartGroupID']]
          )
          new_name[name_part_type] = self._sanitize(name_part_value.text.strip())
        self.names.append(new_name)

  def _determine_party_type(self):
    if 'Vessel Name' in self.name_part_type_lookup.values():
      self.party_type = 'Vessel'
    elif 'Entity Name' in self.name_part_type_lookup.values():
      self.party_type = 'Entity'
    elif 'Aircraft Name' in self.name_part_type_lookup.values():
      self.party_type = 'Aircraft'
    else:
      self.party_type = 'Individual'

  def process_element(self, elem):
    profile = elem.findall(ns('Profile'))
    # should always be one profile per distinct party, as per specification
    if len(profile) > 1:
      raise Exception(
        '[!] found more than one Profile: {fixedref}'
        .format(self.fixedref)
      )
    self.profile_id = profile[0].attrib['ID']

    # should always be one identity per profile, as per specification
    identity = profile[0].findall(ns('Identity'))
    if len(identity) > 1:
      raise Exception(
        '[!] found more than one Identity: {fixedref}'
        .format(self.fixedref)
      )
    self.identity_id = identity[0].attrib['ID']

    self._process_name_part_groups(identity[0])
    self._process_aliases(identity[0])
    self._determine_party_type()

  def _commit_individual(self, db, tbl):
    to_submit = {}
    commands = []
    for name in self.names:
      for name_part in [
        'First Name', 'Middle Name', 'Last Name', 'Nickname',
        'Maiden Name', 'Patronymic', 'Matronymic'
      ]:
        if name_part in name.keys():
          to_submit[name_part] = name[name_part]
        else:
          to_submit[name_part] = ''
      full_name = ' '.join([
        to_submit['First Name'],
        to_submit['Middle Name'],
        to_submit['Last Name'],
        to_submit['Nickname'],
        to_submit['Maiden Name'],
        to_submit['Patronymic'],
        to_submit['Matronymic']
      ])
      to_submit['full_name'] = re.sub(' {2,}', ' ', full_name).strip()
      to_submit['full_name_sorted'] = ' '.join(
        sorted([n.lower() for n in full_name.split(' ')])
      ).strip()
      to_submit['tbl'] = tbl
      to_submit['fixedref'] = self.fixedref
      to_submit['profile_id'] = self.profile_id
      to_submit['identity_id'] = self.identity_id
      to_submit['AliasFixedRef'] = name['AliasFixedRef']
      to_submit['DocumentedNameID'] = name['DocumentedNameID']
      commands.append(CommandFormatter.format_individual_command(to_submit))
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for command in commands:
      cursor.execute(command)
    connection.commit()
    connection.close()

  def _commit_entity(self, db, tbl):
    pass

  def _commit_vessel(self, db, tbl):
    pass

  def _commit_aircraft(self, db, tbl):
    pass

  def commit(self, db=DB_NAME, 
             tbl_individuals=DB_TABLE_INDIVIDUALS,
             tbl_entities=DB_TABLE_ENTITIES, 
             tbl_vessels=DB_TABLE_VESSELS,
             tbl_aircraft=DB_TABLE_AIRCRAFT):
    if self.party_type == 'Individual':
      self._commit_individual(db, tbl_individuals)
    elif self.party_type == 'Entity':
      self._commit_entity(db, tbl_entities)
    elif self.party_type == 'Vessel':
      self._commit_vessel(db, tbl_vessels)
    elif self.party_type == 'Aircraft':
      self._commit_aircraft(db, tbl_aircraft)


class Location(object):

  def __init__(self, id):
    self.id = id 

  def set_area_code(self, area_code, area_code_lookup=area_codes):
    if len(area_code) > 1:
      raise Exception(
        '[!] found more than one AreaCode: {id}'
        .format(id=self.id)
      )
    elif len(area_code) == 0:
      self.area_code = None
    else:
      self.area_code = area_code_lookup[area_code[0].attrib['AreaCodeID']]

  def set_country(self, country, country_lookup=countries):
    if len(country) > 1:
      raise Exception(
        '[!] found more than one Country: {id}'
        .format(id=self.id)
      )
    elif len(country) == 0:
      self.country = None
    else:
      self.country = country_lookup[country[0].attrib['CountryID']]

  def set_location_parts(self, location_parts):
    values_list = []
    for loc_part in location_parts:
      loc_part_values = loc_part.findall(ns('LocationPartValue'))
      if len(loc_part_values) > 1:
        for loc_part_value in loc_part_values:
          if loc_part_value.attrib['Primary'] == 'true': # fix this; parse all instead, not just primary
            values = loc_part_value.findall(ns('Value'))
            break
      else:
        values = loc_part_values[0].findall(ns('Value'))
      if len(values) > 1:
        raise Exception(
          '[!] found more than one LocationPartValue value: {id}'
          .format(id=self.id)
        )
      values_list.append(values[0].text.strip())
    self.location_parts = ' '.join(values_list)

  def commit(self, db):
    # to do
    pass