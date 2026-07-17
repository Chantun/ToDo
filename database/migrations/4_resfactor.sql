ALTER TABLE note
DROP COLUMN date;

ALTER TABLE note
RENAME COLUMN title TO content;

DROP TABLE subnote;
