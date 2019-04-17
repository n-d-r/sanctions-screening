DROP TABLE IF EXISTS individuals;
DROP TABLE IF EXISTS entities;
DROP TABLE IF EXISTS vessels;
DROP TABLE IF EXISTS aircraft;

CREATE TABLE individuals(
  party_fixedref   TEXT,
  profile_id       TEXT,
  identity_id      TEXT,
  alias_fixedref   TEXT,
  name_id          TEXT,
  first            TEXT,
  middle           TEXT,
  last             TEXT,
  nickname         TEXT,
  maiden           TEXT,
  patronymic       TEXT,
  matronymic       TEXT,
  full_name        TEXT,
  full_name_sorted TEXT,
  PRIMARY KEY(party_fixedref, profile_id, identity_id, alias_fixedref, name_id)
);

CREATE TABLE entities(
  party_fixedref     TEXT,
  profile_id         TEXT,
  identity_id        TEXT,
  alias_fixedref     TEXT,
  name_id            TEXT,
  entity_name        TEXT,
  entity_name_sorted TEXT,
  PRIMARY KEY(party_fixedref, profile_id, identity_id, alias_fixedref, name_id)
);

CREATE TABLE vessels(
  party_fixedref     TEXT,
  profile_id         TEXT,
  identity_id        TEXT,
  alias_fixedref     TEXT,
  name_id            TEXT,
  vessel_name        TEXT,
  vessel_name_sorted TEXT,
  PRIMARY KEY(party_fixedref, profile_id, identity_id, alias_fixedref, name_id)  
);

CREATE TABLE aircraft(
  party_fixedref       TEXT,
  profile_id           TEXT,
  identity_id          TEXT,
  alias_fixedref       TEXT,
  name_id              TEXT,
  aircraft_name        TEXT,
  aircraft_name_sorted TEXT,
  PRIMARY KEY(party_fixedref, profile_id, identity_id, alias_fixedref, name_id)  
);