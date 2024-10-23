USE BreastCancer;
-- Taking Backup 
BACKUP DATABASE BreastCancer
TO DISK = 'E:\Projects\breastcancer.bak';

-- Presenting Data
SELECT * 
FROM BRCA;

-- Checking datatypes

SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'BRCA';

-- Checking null values and blanks in Numeric columns

SELECT *
FROM BRCA
WHERE ISNUMERIC(Protein3) = 0;
SELECT count(Protein1)
FROM BRCA
WHERE Protein1 IS NULL;
/*
It seems that Null Values is represents as blanks which destroys the process of converting the column to its actual type
and it seems that this rows is not valuble as all fields in it is also blanks 
They are the same in the other proteins
We will replace these blanks with nulls
*/ 

-- Changing blanks to nulls 
Update BRCA
SET Protein1 = NULL 
WHERE ISNUMERIC(Protein1) = 0;
Update BRCA
SET Protein2 = NULL 
WHERE ISNUMERIC(Protein2) = 0;
Update BRCA
SET Protein3 = NULL 
WHERE ISNUMERIC(Protein3) = 0;
Update BRCA
SET Protein4 = NULL 
WHERE ISNUMERIC(Protein4) = 0;
-- Converting (Protein 1 , 2 , 3 and 4) Columns into Numeric columns 
Begin TRANSACTION;
ALTER TABLE BRCA 
ALTER COLUMN Protein1 Decimal(10,3);
ALTER TABLE BRCA 
ALTER COLUMN Protein2 Decimal(10,3);
ALTER TABLE BRCA 
ALTER COLUMN Protein3 Decimal(10,3);
ALTER TABLE BRCA 
ALTER COLUMN Protein4 Decimal(10,3);
COMMIT;
-- Converting Date columns into the datatype date 
Begin TRANSACTION;
ALTER TABLE BRCA 
ALTER COLUMN Date_of_Surgery DATE;
ALTER TABLE BRCA 
ALTER COLUMN Date_of_Last_Visit DATE;
COMMIT;
-- Converting Age Column into Integer 
ALTER TABLE BRCA 
ALTER COLUMN Age INT;
-- Grouping Tumour stages
SELECT COUNT(*),Tumour_Stage
FROM BRCA
GROUP BY Tumour_Stage;
-- Creating new column representing tumor stages as numbers and convert blanks to nulls
ALTER TABLE BRCA
ADD Tumor_Stage_Numeric INT;
UPDATE BRCA
SET Tumor_Stage_Numeric = CASE Tumour_Stage 
WHEN 'I' THEN 1
WHEN 'II' THEN 2 
WHEN 'III' THEN 3
ELSE NULL
END
FROM BRCA;
-- Dealing with Blanks and strange values in Date columns
DELETE FROM BRCA
WHERE DATEPART(YEAR,Date_of_Last_Visit) = 1900 AND DATEPART(YEAR,Date_of_Surgery) = 1900;

-- Replacing Blanks in Patient status with "Unknow"
UPDATE BRCA
SET Patient_Status = 'Unknown'
WHERE Patient_Status = '';
-- Checking if there are any other blanks or Null values 
SELECT *
FROM BRCA
WHERE [Surgery_type] = '';
-- Adding column Year_of_Surgery extracted from the Date_of_Surgery Column 
ALTER TABLE BRCA
ADD Year_of_Surgery INT;
UPDATE BRCA
SET Year_of_Surgery = DATEPART(Year,Date_of_Surgery);