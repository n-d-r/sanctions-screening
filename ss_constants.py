#===============================================================================
# Constants
#===============================================================================

DB_NAME = 'sanctions.db'
DB_TABLE_INDIVIDUALS = 'individuals'
DB_TABLE_ENTITIES = 'entities'
DB_TABLE_VESSELS = 'vessels'
DB_TABLE_AIRCRAFT = 'aircraft'
DB_TABLE_FEATURES = 'features'
DB_TABLE_FEATURES_TO_PARTIES = 'features_to_parties'
XMLNS = 'http://www.un.org/sanctions/1.0'
TAGS_TO_IGNORE = [
  'Sanctions',
  'DateOfIssue',
  'ReferenceValueSets',
  'AliasTypeValues',
  'AreaCodeValues',
  'AreaCodeTypeValues',
  'AreaCodeType',
  'CalendarTypeValues',
  'CalendarType',
  'CountryValues',
  'CountryRelevanceValues',
  'CountryRelevance',
  'DecisionMakingBodyValues',
  'DecisionMakingBody',
  'DetailReferenceValues',
  'DetailTypeValues',
  'DocNameStatusValues',
  'DocNameStatus',
  'EntryEventTypeValues',
  'EntryEventType',
  'EntryLinkTypeValues',
  'ExRefTypeValues',
  'FeatureTypeValues',
  'FeatureTypeGroupValues',
  'IDRegDocDateTypeValues',
  'IDRegDocTypeValues',
  'IdentityFeatureLinkTypeValues',
  'IdentityFeatureLinkType',
  'LegalBasisValues',
  'LegalBasisTypeValues',
  'LegalBasisType',
  'ListValues',
  'LocPartTypeValues',
  'LocPartValueStatusValues',
  'LocPartValueTypeValues',
  'NamePartTypeValues',
  'OrganisationValues',
  'Organisation',
  'PartySubTypeValues',
  'PartyTypeValues',
  'RelationQualityValues',
  'RelationTypeValues',
  'ReliabilityValues',
  'SanctionsProgramValues',
  'ScriptValues',
  'ScriptStatusValues',
  'SubsidiaryBodyValues',
  'SubsidiaryBody',
  'SupInfoTypeValues',
  'TargetTypeValues',
  'ValidityValues',
  'Locations'
]