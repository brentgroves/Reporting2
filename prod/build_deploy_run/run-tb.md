# run tb

## Reporting2

Tested the Reporing2 repo on 12/05/24. Removed references to mysql because I was unable to connect to mysql on reports31.

## Reason for TB

/*
Accounting_account: accounting_account_DW_Import  

This is used to determine the current accounts needed in the account_period_balance table. It has
additional fields such as the category account and sub category account that are no longer supported by
Plex. I believe the Multi-Level in the Plex Multi-Level report has to do with an account that used the
category and sub-category account.  Not supporting the category and sub-category account linkage is
the reason Southfield's Plex Multi-Level report does not show many of the accounts.

-- select count(*)
-- select*
from accounting_v_account_e  a
join accounting_v_category_type act -- This is the value used by the new method of configuring plex accounts.
on a.category_type=act.category_type  -- 36,636
-- Category numbers linked to an account by the a category_account record will no longer be supported by Plex
left outer join accounting_v_category_account_e ca  --
on a.plexus_customer_no=ca.plexus_customer_no
and a.account_no=ca.account_no
left outer join accounting_v_category_e c  --
on ca.plexus_customer_no=c.plexus_customer_no
and ca.category_no=c.category_no
left outer join accounting_v_category_type t -- This is the value used by the old method of configuring plex accounts.
on c.category_type=t.category_type
-- sub category numbers linked to an account by the sub category_account record will no longer be supported by Plex
left outer JOIN accounting_v_sub_category_account_e AS sca
--JOIN accounting_v_Sub_Category_Account_e AS SCA -- 4,204 for 123681
ON a.plexus_customer_no = sca.plexus_customer_no
and a.account_no = sca.account_no
left outer join accounting_v_sub_category_e sc  --
on sca.plexus_customer_no=sc.plexus_customer_no
and sca.sub_category_no=sc.sub_category_no
left outer join accounting_v_category_e c2  --
on sc.plexus_customer_no=c2.plexus_customer_no
and sc.category_no=c2.category_no
left outer join accounting_v_category_type t2 -- This is another value used by the old method of configuring plex accounts.
on c2.category_type=t2.category_type
left outer join account_balance_start b
on a.plexus_customer_no = b.pcn
and a.account_key=b.account_key

AccountingYearCategoryType:
It is used to keep track of if an account is classified as an expense or revenue for each year.
This is needed in YTD calculations which checks if an account  
is a revenue/expense to determine whether to reset YTD values to 0 for every year.

*/

## Remove TB dependancy

Did this on Dec 2nd in Reporting2 repo because I was no longer able to ping google.com from the Avilla K8s. I told them I was going to get rid of this cluster and try to recreate one on the linamar vlan.

## Linamar change notes

From Alb-utl1, 10.1.1.1 Download the TRIALBALANCE report from plex and import it into the DW
Run Power BI report from Alb-utl4.

## Idea

/*

* Try to find any new accounts by comparing Plex.account_period_balance to Plex.accounting_account_year_category_type
* after the AccountingYearCategoryType.sh script and before the AccountPeriodBalanceRecreatePeriodRange.sh script
 */

select top 10 b.pcn,b.account_no, c.pcn,c.[year],c.account_no
from Plex.accounting_account_year_category_type c
left outer join Plex.account_period_balance b
on c.pcn = b.pcn
and c.account_no = b.account_no
where c.pcn = 123681 -- 23,063
and c.[year] = 2024
order by b.pcn

## Issue

Timeout issue with the "AccountActivitySummaryGetOpenPeriodRange"
SOAP web service script.
20240507
open-period range was 202403 to 202405. It worked on 202403 and 202404 but failed on 202405 the active period. I shutdown all apps on my dev system and ran again with no error. There maybe an issue when more than 2 Plex SOAP web services are called one after another. Or there maybe some issue with running the scripts while memory resources are low.
Had this issue again on 20241004. I ran TrialBalance-test.sh with VS Code open and all the scripts uncommented and it ran until the "AccountActivitySummaryGetOpenPeriodRange" script and then it failed. I then commented out all the scripts which ran successfully the first time and ran TrialBalance-test.sh again and it completed without any issues.

## **Format of file name**

## Note call to web service did not work until I stopped the MSSQL Server docker container

"Heather Luttrell" <Heather.Luttrell@Linamar.com>
TB-202311_to_202411_on_12-16_DM_HL
TB-202310_to_202410_on_11-11_DM_HL
TB-202310_to_202410_on_11-05_DM_HL
TB-202310_to_202410_on_11-04_DM_HL
TB-202309_to_202409_on_10-04_DM_HL
TB-202308_to_202408_on_09-06_DM
TB-202307_to_202407_on_08-08_DM
TB-202306_to_202406_on_07-07_DM_HL
TB-202305_to_202405_on_06-07_DM
TB-202304_to_202404_on_05-08_DM
TB-202304_to_202404_on_05-07_DM
TB-202303_to_202403_on_04-05_DM
TB-202302_to_202402_on_03-08_DM
TB-202301_to_202401_on_02-09_DM
TB-202301_to_202401_on_02-08B_DM
TB-202301_to_202401_on_02-08_DM
TB-202212_to_202312_on_01-09_DM
TB-202212_to_202312_on_01-03_DM_LR
TB-202211_to_202311_on_12-12_DM_LR_JS
TB-202211_to_202311_on_12-08_DM_LR_JS
TB-202210_to_202310_on_11-21_DM_GP_LR
TB-202210_to_202310_on_11-20_DM_GP_LR
TB-202210_to_202310_on_11-13_DM_GP_LR
TB-202210_to_202310_on_11-07_DM_GP
TB-202209_to_202309_on_10-24_DM_GP

TB-202209_to_202309_on_10-18_DM_GP

TB-202209_to_202309_on_10-17_DM
TB-202209_to_202309_on_10-17_GP

TB-202209_to_202309_on_10-10_DM
TB-202209_to_202309_on_10-10_GP

## install lastpass in k8s and on dev system

```bash
pushd .. 
cd ~/src/Reporting2/prod/k8s/secrets/lastpass
./print-etc-lastpass.sh
mysql_host=$1
mysql_port=$2
mongo_host=$3
mongo_port=$4
mongo_db=$5
azure_dw=$6
./sed-lastpass-yaml.sh reports31 30031 reports32 30332 reports 1
ssh to cluster
kubectl apply -f lastpass.yaml
on dev system update local passwords in /etc/lastpass
./sed-lastpass-sh.sh reports31 30031 reports32 30332 reports 1
ls /etc/lastpass
ssh to dev system
./lastpass.sh
```

## initailize the scripts for prod or dev

```bash
pushd . 
cd ~/src/Reporting2/prod/volume
mysql_host=$2
mysql_port=$3
azure_dw=$4
mongo_host=$5
mongo_port=$6
mongo_db=$7

# if debugging the python script then
./sed-volume.sh dev reports31 30031 1 reports32 30332 reports
# if running the TrialBalance.sh or TrialBalance-test.sh script manually then:  
./sed-volume.sh prod reports31 30031 1 reports32 30332 reports
```

## run trial balance scripts

```bash
pushd .
cd ~/src/Reporting2/prod/volume/PipeLine

"Heather Luttrell" <Heather.Luttrell@Linamar.com>
"Dan Martin" <dan.martin@linamar.com>
TB-202311_to_202411_on_12-05_DM_HL
TB-202310_to_202410_on_11-11_DM_HL
TB-202310_to_202410_on_11-05_DM_HL
TB-202310_to_202410_on_11-05_DM_HL
TB-202310_to_202410_on_11-04_DM_HL
TB-202309_to_202409_on_10-04_DM_HL
TB-202308_to_202408_on_09-06_DM
TB-202407_to_202407_on_08-08_DM
TB-202307_to_202407_on_08-08_DM
TB-202306_to_202406_on_07-07_DM_HL
TB-202305_to_202405_on_06-07_DM
TB-202304_to_202404_on_05-08_DM
TB-202304_to_202404_on_05-07_DM
TB-202303_to_202403_on_04-05_DM
TB-202302_to_202402_on_03-08_DM
TB-202301_to_202401_on_02-12_DM
TB-202301_to_202401_on_02-09_DM
TB-202301_to_202401_on_02-08B_DM
TB-202212_to_202312_on_01-18_BG // to test bug fix
TB-202212_to_202312_on_01-09b_DM // This was after a bug fix and ran sprocs manually
TB-202212_to_202312_on_01-04_DM_LR
TB-202212_to_202312_on_01-03_DM_LR
TB-202211_to_202311_on_12-12_DM_LR_JS
TB-202211_to_202311_on_12-08_DM_LR_JS // time: 15:00, period 202311 was not closed
TB-202210_to_202310_on_11-21_DM_GP_LR
TB-202210_to_202310_on_11-20_DM_GP_LR
TB-202210_to_202310_on_11-13_DM_GP_LR
TB-202210_to_202310_on_11-07_DM_GP
TB-202209_to_202309_on_10-24_DM_GP

TB-202209_to_202309_on_10-18_DM_GP

conda activate reports
```

## How to Install a Virtual Environment using Venv (USE CONDA TEST ONLY)

Virtualenv is a tool to set up your Python environments. Since Python 3.3, a subset of it has been integrated into the standard library under the venv module. You can install venv to your host Python by running this command in your terminal:

pip install virtualenv
To use venv in your project, in your terminal, create a new project folder, cd to the project folder in your terminal, and run the following command:

```bash
# add env/ folder to gitignore
conda deactivate
pushd .
cd ~/src/Reporting2/prod/volume/PipeLine
# python3.8 -m venv env if multiple versions of python are installed using deadsnakes ppa
python3 -m venv env
source env/bin/activate
pip install pyodbc
```

```bash
# usage ./TrialBalance-test.sh "TB" "<bgroves@buschegroup.com>" "202201" "202301" 0 "once"

# If start_period_update = 1 the AccountingStartPeriodUpdate script will run

./TrialBalance-test.sh "TB" "bgroves@buschegroup.com" "202311" "202411" 0 "once"
```

## run dbeaver

open azure_account_period_balance_validate.sql and mysql_trial_balace_validation.sql
follow steps

```bash
/*

* Detected an error on 03/09/2023:
* no_update = 1 but there were no 2023-01 balance records at all.
* The daily scripts were not running during this period.
* Until the scripts are running again run the TrialBalance pipeline
* with start_period_update = 0 so all the balance records will be
* pulled from Plex everytime.
 */
TB-202311_to_202411_on_12-05_DM_HL
TB-202306_to_202406_on_07-07_DM_HL
TB-202211_to_202311_on_12-12_DM_LR_JS
TB-202211_to_202311_on_12-08_DM_LR_JS
TB-202207_to_202307_on_08-24_DM
TB-202207_to_202307_on_08-24_GP
TB-202203_to_202303_on_04-11_DM
TB-202203_to_202303_on_04-11_GP
export report_name=$1
export email=$2
export start_period=$3
export end_period=$4
export start_period_update=$5
export frequency=$5
./TrialBalance-test.sh TB <bgroves@buschegroup.com> 202203 202303 0 once
```

## Update MySQL Trialbalance table with Plex CSV

Still working on this CsvToTrialBalanceMultiLevel script. Delete and inserts are working so next pass start_period and end_period to shell script. Copy Trial_Balance to ~/src/Reporting directory for now.
It looks like it inserts the records ok now I need to delete the periods in the table before inserting the new records.

## From Alb-utl Download the TRIALBALANCE report from plex and import it into the DW

goto azure_account_period_balance_validate.sql
/*

* Decide which TB periods to pull by  
* each period has 2 records. ordinal 1 is the most recent
* goto Main Compare: section and locate the last period to have any differences
* and import all periods after and including that one for both balance and activity_summary records.
* TB-202211_to_202311_on_12-12_DM_LR_JS pull just 202311
* TB-202211_to_202311_on_12-08_DM_LR_JS
* TB-202210_to_202310_on_11-13_DM_GP_LR
* TB-202210_to_202310_on_11-07_DM_GP
* TB-202209_to_202309_on_10-17_DM found 1 diff between 202210 and 202308 from the trial_balance_multi_level so i imported 202308 again
* TB-202209_to_202309_on_10-10_DM found no diff between 202210 and 202308 from the trial_balance_multi_level so did not import 202308 again
* TB-202208_to_202308_on_09-18_DM found no diff between 202209 and 202307 from the trial_balance_multi_level so did not import 202307 again
* TB-202208_to_202308_on_09-13_DM found no diff between 202208 and 202307 from the trial_balance_multi_level so did not import 202307 again
* TB-202208_to_202308_on_09-11_DM found no diff between 202208 and 202307 from the trial_balance_multi_level so did not import 202307 again
* TB-202207_to_202307_on_08-24_DM found no diff between 202207 and 202307 from the trial_balance_multi_level so did not import 202307 again
* TB-202207_to_202307_on_08-09_DM found no diff between 202207 and 202306 so just need to import 202307
* TB-202206_to_202306_on_07-11_DM found no diff between 202206 and 202305 so just need to import 202306
* TB-202205_to_202305_on_06-13_DM dan made minor adjustments to 202305
* TB-202205_to_202305_on_06-09_DM found no diff between 202205 and 202304 so just need to import 202305
* 05-09-2023: diff found in 202303 between trial_balance_multi-level and accounting_period_balance
* 04-11-2023: diff found in 202303 between trial_balance_multi-level and accounting_period_balance
* TB-202203_to_202303_on_04-11_DM
* TB-202203_to_202303_on_04-11_GP
* 03-09-2023: Pulled 202302 to 202303 since there where no updates on 202301 since 2023-02-27
* 03-02-2023: Pulled 202212 to 202301
 */

Thank you Father for the peace that you have given me in troubles, pain, and sorrow!

## run TB report

Run TB report, trial_balance.rdl, from any Windows machine with the Power BI report builder installed - alb-utl4. Use YYYYMM format for period range parameters.

go to **[credentials](../../../secrets/namespaces/default/credentials.yaml)**
and use username2/password2 to authenticate.

**Format of file name**
TB-202311_to_202411_on_12-05_DM_HL
TB-202310_to_202410_on_11-11_DM_HL

TB-202310_to_202410_on_11-05_DM_HL

TB-202310_to_202410_on_11-04_DM_HL
TB-202309_to_202409_on_10-04_DM_HL

TB-202308_to_202408_on_09-06_DM

TB-202306_to_202406_on_07-07_DM_HL

TB-202301_to_202401_on_02-12_DM
TB-202301_to_202401_on_02-09_DM
TB-202301_to_202401_on_02-08B_DM
TB-202301_to_202401_on_02-08_DM
TB-202212_to_202312_on_01-03_DM_LR
TB-202211_to_202311_on_12-12_DM_LR_JS
TB-202211_to_202311_on_12-08_DM_LR_JS
TB-202210_to_202310_on_11-20_DM_GP_LR
TB-202210_to_202310_on_11-13_LR_DM_GP
TB-202210_to_202310_on_11-07_DM_GP
TB-202209_to_202309_on_10-24_DM_GP

TB-202209_to_202309_on_10-18_DM_GP
TB-202209_to_202309_on_10-17_DM

Hi Dan,
Are you expecting to see any changes between this TB and the one I sent you on the 13th? I'm asking because I didn't see any changes between the two but that does not mean there could not have been updates it only means there were no updates that show up in the Plex version of the TB.  So, if the changes happened on accounts that are not displayed in the Plex version of the TB then there could still be changes between this TB and the one I sent on the 13th.
