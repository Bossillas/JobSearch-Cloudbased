DROP USER IF EXISTS "jobsearch-read-only";
DROP USER IF EXISTS "jobsearch-read-write";

CREATE USER "jobsearch-read-only" IDENTIFIED BY "abc123!!";
CREATE USER "jobsearch-read-write" IDENTIFIED BY "def456!!";

GRANT SELECT, SHOW VIEW ON jobsearch.*
    TO "jobsearch-read-only";
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER ON jobsearch.*
    TO "jobsearch-read-write";

FLUSH PRIVILEGES;
