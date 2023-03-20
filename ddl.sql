DROP DATABASE IF EXISTS courseregistrar;
CREATE DATABASE courseregistrar;
USE courseregistrar;

CREATE TABLE students(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    uniq_id VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE courses(

    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    moniker VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    department VARCHAR(20) NOT NULL
);

CREATE TABLE prerequisites(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    course VARCHAR(20) NOT NULL,
    prereq VARCHAR(20) NOT NULL,
    min_grade INTEGER NOT NULL,
    FOREIGN KEY(course) REFERENCES courses(moniker),
    FOREIGN KEY(prereq) REFERENCES courses(moniker),
    CHECK(min_grade >=0 AND min_grade <= 100)
);

CREATE TABLE student_course(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    student VARCHAR(20) NOT NULL,
    course VARCHAR(20) NOT NULL,
    year INTEGER,
    grade INTEGER,
    FOREIGN KEY (student) REFERENCES students(uniq_id),
    FOREIGN KEY (course) REFERENCES courses(moniker),
    UNIQUE (student, course, year),
    CHECK (grade >= 0 AND grade <=100)
);

DROP TRIGGER IF EXISTS before_student_course_insert;
CREATE TRIGGER before_student_course_insert
    BEFORE INSERT
    ON student_course
    FOR EACH ROW
BEGIN
    -- create temp tables to hold prereqs and unmet prereqs
    DROP TEMPORARY TABLE IF EXISTS temp_prereqs;
    DROP TEMPORARY TABLE IF EXISTS unmet_prereqs;
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_prereqs
    (
        prereq VARCHAR(10) REFERENCES courses(moniker),
        min_grade INTEGER

    );

    CREATE TEMPORARY TABLE IF NOT EXISTS unmet_prereqs
    (
        prereq VARCHAR(10) REFERENCES courses(moniker)

    );
--     check if course has prereqs. if yes, insert into first temp table
    INSERT INTO temp_prereqs(prereq, min_grade)
    SELECT prereq, min_grade
    FROM prerequisites as p
    WHERE p.course = NEW.course;
    -- NEW: new record attempting to insert

    -- check if student met the prerequisites. and insert them in temp table
    INSERT INTO unmet_prereqs(prereq)
    SELECT prereq
    FROM temp_prereqs as tp
    WHERE tp.prereq NOT IN (
            SELECT sc.course
            FROM student_course sc
            WHERE sc.student=NEW.student AND
            sc.grade > tp.min_grade
    );

    -- check unmet prerequisites
    if (exists(SELECT 1 FROM unmet_prereqs)>0) THEN
        SET @message = CONCAT('Student ', NEW.student , ' cannot take course ', NEW.course , ' because did not meet all the prerequisites.');
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = @message;
    end if;

end;


CREATE TABLE IF NOT EXISTS letter_grade
(
    grade INTEGER NOT NULL,
    letter VARCHAR(10) NOT NULL,
    check (grade >=0 and grade <= 100)
);




















