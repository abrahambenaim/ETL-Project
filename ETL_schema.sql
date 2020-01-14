-- most granular table
CREATE TABLE MDC_RE_data
(
    index int UNIQUE
    PRIMARY KEY,
    zip_code VARCHAR NOT NULL,
    home_value varchar NOT NULL,
    rent_value varchar NOT NULL
);

    CREATE TABLE avgincome_perzip
    (
        zip VARCHAR PRIMARY KEY,
        avg_income VARCHAR NOT NULL
    );

    CREATE TABLE top30_disparity
    (
        emp_no int NOT NULL,
        dept_no VARCHAR NOT NULL,
        from_date VARCHAR NOT NULL,
        to_date VARCHAR NOT NULL,
        FOREIGN KEY(dept_no) REFERENCES Departments(dept_no),
        FOREIGN KEY(emp_no) REFERENCES Employees(emp_no)
    );

    CREATE TABLE restaurants_df
    (
        index int UNIQUE
        PRIMARY KEY,
    name VARCHAR, 
    location VARCHAR,
    city VARCHAR,
    zipcode VARCHAR, 
    rating VARCHAR,
    price VARCHAR
    );

        CREATE TABLE Salaries
        (
            emp_no int NOT NULL,
            salary int NOT NULL,
            from_date VARCHAR NOT NULL,
            to_date VARCHAR NOT NULL,
            FOREIGN KEY(emp_no) REFERENCES Employees(emp_no)
        );

        CREATE TABLE Titles
        (
            emp_no int NOT NULL,
            title varchar NOT NULL,
            from_date VARCHAR NOT NULL,
            to_date VARCHAR NOT NULL,
            FOREIGN KEY(emp_no) REFERENCES Employees(emp_no)
        );