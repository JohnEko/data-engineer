ALTER TABLE
   `de-projects-373304.gasprice_dataset.weekly-gasoline` ADD COLUMN
IF NOT EXISTS Main_gasprices STRING;
CREATE OR REPLACE TABLE
    `de-projects-373304.gasprices_data.weekly-gasoline` AS
SELECT
   IFNULL(Main_gasprices, 
   'Gasprice') AS Main_gasprices,  
   Fiscal_Year,
   Fiscal_Week,
   Current_Year_Production,
   Previous_Year_Production,
   Difference_From_Same_Week_Last_Year,
   Current_Year_Cumulative_Production,
   Cumulative_Difference
FROM
  `de-projects-373304.gasprice_dataset.weekly-gasoline`;




