DROP TABLE IF EXISTS boards;

CREATE TABLE boards(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  index0 integer NOT NULL,
  index1 integer NOT NULL,
  index2 integer NOT NULL,
  index3 integer NOT NULL,
  index4 integer NOT NULL,
  index5 integer NOT NULL,
  index6 integer NOT NULL,
  index7 integer NOT NULL,
  index8 integer NOT NULL,
  match TEXT NOT NULL REFERENCES matches(id)
);
