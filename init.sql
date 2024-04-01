CREATE DATABASE IF NOT EXISTS poc;
USE poc;
CREATE TABLE poc_test (
    own_ID INT AUTO_INCREMENT PRIMARY KEY,
    trigger_method TEXT,
    test_platform VARCHAR(1000),
    software_version VARCHAR(1000),
    record VARCHAR(1000),
    title VARCHAR(3000),
    author VARCHAR(1000),
    code_language VARCHAR(1000),
    reference VARCHAR(3000),
    time DATE,
    tag VARCHAR(10),
    CVE_ID VARCHAR(1000),
    bugid VARCHAR(1000),
    source VARCHAR(1000),
    other_information LONGTEXT
);
