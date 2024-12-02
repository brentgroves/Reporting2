#!/usr/bin/bash
sudo mkdir -p /etc/lastpass
sudo chmod 777 /etc/lastpass
pushd .
cd /etc/lastpass
# Plex ODBC
echo "mg.odbcalbion" > ./username
echo "Mob3xalbion" > ./password
# Azure SQL Server
echo "mgadmin" > ./username2
echo "WeDontSharePasswords1!" > ./password2
# MySql Server
echo "root" > ./username3
echo "password" > ./password3
# Plex Edon SOAP Web Service
echo "MGEdonReportsws@plex.com" > ./username4
echo "9f45e3d-67ed-" > ./password4
echo "MGAlabamaReportsws@plex.com" > ./username5
echo "957f15d-813d-" > ./password5
# Plex Albion SOAP Web Service
echo "MGAlbionReportsws@plex.com" > ./username6
echo "697fd42-084c-" > ./password6
# Plex Avilla SOAP Web Service
echo "MGAvillaReportsws@plex.com" > ./username7
echo "56e1f6c-7323-" > ./password7
# Plex FP SOAP Web Service
echo "MGAFPReportsws@plex.com" > ./username8
echo "c65a4d9-641f-" > ./password8
# Plex TechCenter SOAP Web Service
echo "MGTechReportws@plex.com" > ./username9
echo "90e3351-952f-" > ./password9
# Plex SouthField SOAP Web Service
echo "MGSouthReportWs@plex.com" > ./username10
echo "cfdf135-564a-" > ./password10
# MongoDB 
echo "adminuser" > ./username11
echo "password123" > ./password11

# User Name: BuscheAlbionWs2@plex.com 
# Password: 6afff48-ba19- 
# UserName: BuscheAvillaKorsws@plex.com 
# Password: 5b11b45-f59f- 
# User Name: BuscheFranklinKorsWs@plex.com 
# Password: 0a1da8b-71e 
# UserName: BuscFruitportKorsWs@plex.com 
# Password: ef4606b-adb1- 

# Misc deployment parameters
echo "%MYSQL_HOST%" > ./MYSQL_HOST
echo "%MYSQL_PORT%" > ./MYSQL_PORT
echo "%AZURE_DW%" > ./AZURE_DW
echo "%MONGO_HOST%" > ./MONGO_HOST
echo "%MONGO_PORT%" > ./MONGO_PORT
echo "%MONGO_DB%" > ./MONGO_DB

pushd -1

