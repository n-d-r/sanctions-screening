#===============================================================================
# Setup
#===============================================================================

import re
import sqlite3

from ss_variables import area_codes, countries, name_part_types, detail_types
from ss_functions import ns
from ss_constants import (DB_NAME, DB_TABLE_INDIVIDUALS, DB_TABLE_ENTITIES, 
                          DB_TABLE_VESSELS, DB_TABLE_AIRCRAFT, DB_TABLE_FEATURES,
                          DB_TABLE_FEATURES_TO_PARTIES)

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
        party_fixedref, profile_id,       identity_id,
        alias_fixedref, name_id,          first,
        middle,         last,             nickname,
        maiden,         patronymic,       matronymic,
        full_name,      full_name_sorted
      )
      VALUES(
        "{party_fixedref}", "{profile_id}",       "{identity_id}",
        "{alias_fixedref}", "{name_id}",          "{first}",
        "{middle}",         "{last}",             "{nickname}",
        "{maiden}",         "{patronymic}",       "{matronymic}",
        "{full_name}",      "{full_name_sorted}"
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

  @staticmethod
  def format_entity_command(to_submit):
    return """
      INSERT INTO {tbl}(
        party_fixedref,     profile_id, identity_id,
        alias_fixedref,     name_id,    entity_name,
        entity_name_sorted
      )
      VALUES(
        "{party_fixedref}",    "{profile_id}", "{identity_id}",
        "{alias_fixedref}",    "{name_id}",    "{entity_name}",
        "{entity_name_sorted}"
      );
    """.format(tbl=to_submit['tbl'],
               party_fixedref=to_submit['fixedref'],
               profile_id=to_submit['profile_id'],
               identity_id=to_submit['identity_id'],
               alias_fixedref=to_submit['AliasFixedRef'],
               name_id=to_submit['DocumentedNameID'],
               entity_name=to_submit['Entity Name'],
               entity_name_sorted=to_submit['entity_name_sorted'])

  @staticmethod
  def format_vessel_command(to_submit):
    return """
      INSERT INTO {tbl}(
        party_fixedref,     profile_id, identity_id,
        alias_fixedref,     name_id,    vessel_name,
        vessel_name_sorted
      )
      VALUES(
        "{party_fixedref}",    "{profile_id}", "{identity_id}",
        "{alias_fixedref}",    "{name_id}",    "{vessel_name}",
        "{vessel_name_sorted}"
      );
    """.format(tbl=to_submit['tbl'],
               party_fixedref=to_submit['fixedref'],
               profile_id=to_submit['profile_id'],
               identity_id=to_submit['identity_id'],
               alias_fixedref=to_submit['AliasFixedRef'],
               name_id=to_submit['DocumentedNameID'],
               vessel_name=to_submit['Vessel Name'],
               vessel_name_sorted=to_submit['vessel_name_sorted'])

  @staticmethod
  def format_aircraft_command(to_submit):
    return """
      INSERT INTO {tbl}(
        party_fixedref,     profile_id, identity_id,
        alias_fixedref,     name_id,    aircraft_name,
        aircraft_name_sorted
      )
      VALUES(
        "{party_fixedref}",    "{profile_id}", "{identity_id}",
        "{alias_fixedref}",    "{name_id}",    "{aircraft_name}",
        "{aircraft_name_sorted}"
      );
    """.format(tbl=to_submit['tbl'],
               party_fixedref=to_submit['fixedref'],
               profile_id=to_submit['profile_id'],
               identity_id=to_submit['identity_id'],
               alias_fixedref=to_submit['AliasFixedRef'],
               name_id=to_submit['DocumentedNameID'],
               aircraft_name=to_submit['Aircraft Name'],
               aircraft_name_sorted=to_submit['aircraft_name_sorted'])

  @staticmethod
  def format_feature_command(to_submit):
    return """
      INSERT INTO {tbl}(
        feature_id,      detail_type,   location_id,
        start_date_from, start_date_to, end_date_from,
        end_date_to
      )
      VALUES(
        "{feature_id}",      "{detail_type}",   "{location_id}",
        "{start_date_from}", "{start_date_to}", "{end_date_from}",
        "{end_date_to}"
      );
    """.format(tbl=to_submit['tbl'],
               feature_id=to_submit['feature_id'],
               detail_type=to_submit['detail_type'],
               location_id=to_submit['location_id'],
               start_date_from=to_submit['start_date_from'],
               start_date_to=to_submit['start_date_to'],
               end_date_from=to_submit['end_date_from'],
               end_date_to=to_submit['end_date_to'])

  @staticmethod
  def format_feature_to_parties_command(to_submit):
    return """
      INSERT INTO {tbl}(identity_ref, feature_id)
      VALUES("{identity_ref}", "{feature_id}");
    """.format(tbl=to_submit['tbl_ftp'],
               identity_ref=to_submit['identity_ref'],
               feature_id=to_submit['feature_id'])


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
    commands = []
    for name in self.names:
      to_submit = {}
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
    commands = []
    for name in self.names:
      to_submit = {'fixedref': self.fixedref}
      to_submit['profile_id'] = self.profile_id
      to_submit['identity_id'] = self.identity_id
      to_submit['AliasFixedRef'] = name['AliasFixedRef']
      to_submit['DocumentedNameID'] = name['DocumentedNameID']
      to_submit['Entity Name'] = name['Entity Name']
      to_submit['entity_name_sorted'] = ' '.join(
        sorted([n.lower() for n in name['Entity Name'].split(' ')])
      ).strip()
      to_submit['tbl'] = tbl      
      commands.append(CommandFormatter.format_entity_command(to_submit))
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for command in commands:
      cursor.execute(command)
    connection.commit()
    connection.close()

  def _commit_vessel(self, db, tbl):
    commands = []
    for name in self.names:
      to_submit = {'fixedref': self.fixedref}
      to_submit['profile_id'] = self.profile_id
      to_submit['identity_id'] = self.identity_id
      to_submit['AliasFixedRef'] = name['AliasFixedRef']
      to_submit['DocumentedNameID'] = name['DocumentedNameID']
      to_submit['Vessel Name'] = name['Vessel Name']
      to_submit['vessel_name_sorted'] = ' '.join(
        sorted([n.lower() for n in name['Vessel Name'].split(' ')])
      ).strip()
      to_submit['tbl'] = tbl
      commands.append(CommandFormatter.format_vessel_command(to_submit))
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for command in commands:
      cursor.execute(command)
    connection.commit()
    connection.close()

  def _commit_aircraft(self, db, tbl):
    commands = []
    for name in self.names:
      to_submit = {'fixedref': self.fixedref}
      to_submit['profile_id'] = self.profile_id
      to_submit['identity_id'] = self.identity_id
      to_submit['AliasFixedRef'] = name['AliasFixedRef']
      to_submit['DocumentedNameID'] = name['DocumentedNameID']
      to_submit['Aircraft Name'] = name['Aircraft Name']
      to_submit['aircraft_name_sorted'] = ' '.join(
        sorted([n.lower() for n in name['Aircraft Name'].split(' ')])
      ).strip()
      to_submit['tbl'] = tbl      
      commands.append(CommandFormatter.format_aircraft_command(to_submit))
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for command in commands:
      cursor.execute(command)
    connection.commit()
    connection.close()

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


class Feature(object):

  def __init__(self, feature_id):
    self.feature_id      = feature_id
    self.detail_type     = ''
    self.location_id     = ''
    self.start_date_from = ''
    self.start_date_to   = ''
    self.end_date_from   = ''
    self.end_date_to     = ''
 
  def _process_date(self, date):
    year = date.find(ns('Year')).text
    month = date.find(ns('Month')).text
    day = date.find(ns('Day')).text
    if len(month) == 1:
      month = '0' + month
    if len(day) == 1:
      day = '0' + day
    return '{year}-{month}-{day}'.format(year=year, month=month, day=day)

  def _process_range(self, rng):
    range_from = rng.find(ns('From'))
    range_from = self._process_date(range_from)
    range_to = rng.find(ns('To'))
    range_to = self._process_date(range_to)
    return (range_from, range_to)

  def _process_date_period(self, dateperiod):
    start = dateperiod.find(ns('Start'))
    start_date_from, start_date_to = self._process_range(start)
    self.start_date_from = start_date_from
    self.start_date_to = start_date_to

    end = dateperiod.find(ns('End'))
    end_date_from, end_date_to = self._process_range(end)
    self.end_date_from = end_date_from
    self.end_date_to = end_date_to

  def _process_feature_version(self, ftr_version, detail_type_id_lookup=detail_types):
    for child in ftr_version.getchildren():
      tag = child.tag.split('}')[-1]
      if tag == 'DatePeriod':
        self._process_date_period(child)
      elif tag == 'VersionDetail':
        self.detail_type = detail_type_id_lookup[child.attrib['DetailTypeID']]
      elif tag == 'VersionLocation':
        self.location_id = child.attrib['LocationID']
      else:
        pass

  def process_element(self, elem):
    # there should always only be one FeatureVersion per Feature
    ftr_version = elem.find(ns('FeatureVersion'))
    self._process_feature_version(ftr_version[0])

    # there should also always only be one IdentityReference per Feature
    identity_ref = elem.find(ns('IdentityReference'))
    self.identity_ref = identity_ref.attrib['IdentityID']

  def commit(self, db=DB_NAME, tbl_feaures=DB_TABLE_FEATURES,
             tbl_features_to_parties=DB_TABLE_FEATURES_TO_PARTIES):
    to_submit = vars(self)
    to_submit['tbl'] = tbl_feaures
    to_submit['tbl_ftp'] = tbl_features_to_parties
    commands = [
      CommandFormatter.format_feature_command(to_submit),
      CommandFormatter.format_feature_to_parties_command(to_submit)
    ]
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for command in commands:
      cursor.execute(command)
    connection.commit()
    connection.close()


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