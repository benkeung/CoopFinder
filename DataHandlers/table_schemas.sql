CREATE TABLE if not exists placepro(
    id INTEGER PRIMARY KEY,
    posting_tile TEXT,
    company_name TEXT,
    url TEXT NULL,
    location TEXT NULL,
    deadline TEXT,
    job_description TEXT,
    contains_keyword BOOLEAN,
    in_calendar BOOLEAN)
