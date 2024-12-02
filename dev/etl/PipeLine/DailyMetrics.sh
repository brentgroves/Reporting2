#!/bin/bash
# python debug1.py
# ./debug2.sh
pipeline="TrialBalance"
export em=""
export emline=""
export dm=""
export line=""
export tm=""
export result=0
export wsusername=""
export wspassword=""

export pcn=""
export pcn_list="123681,300758"

export username=$(</etc/foo/username)
export password=$(</etc/foo/password)
export username2=$(</etc/foo/username2)
export password2=$(</etc/foo/password2)
export username3=$(</etc/foo/username3)
export password3=$(</etc/foo/password3)
export username4=$(</etc/foo/username4)
export password4=$(</etc/foo/password4)
export username5=$(</etc/foo/username5)
export password5=$(</etc/foo/password5)
export username6=$(</etc/foo/username6)
export password6=$(</etc/foo/password6)
export username7=$(</etc/foo/username7)
export password7=$(</etc/foo/password7)
export username8=$(</etc/foo/username8)
export password8=$(</etc/foo/password8)
export username9=$(</etc/foo/username9)
export password9=$(</etc/foo/password9)

# username:mg.odbcalbion, Plex odbc connection
# username2:mgadmin, Azure DW
# username3: mysql, root 
# Plex soap webservice section
# username4: MGEdonReportsws@plex.com, 306766/Edon,
# username5: MGAlabamaReportsws@plex.com, 300757/Alabama
# username6: MGAlbionReportsws@plex.com, 300758/Albion
# username7:MGAvillaReportsws@plex.com, 310507/Avilla
# username8:MGAFPReportsws@plex.com,295932/FruitPort
# username9:MGTechReportws@plex.com


# export em="none"
# export emline="none"
# export dm="none"
# export line="none"
# export tm="none"
# export result=0 

# printf "TrialBalance path= $PATH." | mail -s "Trial Balance Path" bgroves@buschegroup.com

# set pcn
pcn=300758
wsusername=$username6
wspassword=$password6

script="DailyShiftReportGet"
cd ../DailyShiftReportGet
source DailyShiftReportGet.sh 
# echo "AccountingYearCategoryType result=$result"

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=310507
wsusername=$username7
wspassword=$password7

if [[ $result -eq 0 ]]
then # if/then branch
  script="DailyShiftReportGet"
  cd ../DailyShiftReportGet
  source DailyShiftReportGet.sh 
fi

# set variables
em=""
emline=""
dm=""
line=""
tm=""

pcn=300757
wsusername=$username5
wspassword=$password5

if [[ $result -eq 0 ]]
then # if/then branch
  script="DailyShiftReportGet"
  cd ../DailyShiftReportGet
  source DailyShiftReportGet.sh 
fi

# set variables
em=""
emline=""
dm=""
line=""
tm=""

pcn=306766
wsusername=$username4
wspassword=$password4

if [[ $result -eq 0 ]]
then # if/then branch
  script="DailyShiftReportGet"
  cd ../DailyShiftReportGet
  source DailyShiftReportGet.sh 
fi

# set variables
em=""
emline=""
dm=""
line=""
tm=""

pcn=295932
wsusername=$username8
wspassword=$password8

if [[ $result -eq 0 ]]
then # if/then branch
  script="DailyShiftReportGet"
  cd ../DailyShiftReportGet
  source DailyShiftReportGet.sh 
fi

if [[ $result -ne 0 ]]
then # if/then branch
  printf "Pipeline terminated at $script\n"
  printf "Pipeline terminated on $script script." | mail -s "MCP Pipeline Failure" bgroves@buschegroup.com

fi
