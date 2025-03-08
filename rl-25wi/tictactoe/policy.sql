DROP TABLE IF EXISTS policy;

CREATE TABLE policy (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  state INTEGER UNIQUE NOT NULL,
  index0 REAL,
  index1 REAL,
  index2 REAL,
  index3 REAL,
  index4 REAL,
  index5 REAL,
  index6 REAL,
  index7 REAL,
  index8 REAL
);
