# login to the node to install mysql 
ssh brent@reports31
# make the database and backup directory
mkdir -p ~/backups/mysql
sudo chmod -R 777 ~/backups

# ftp a current dw backup onto the node
lftp brent@reports-avi
or
lftp brent@moto

mirror -c /home/brent/backups/mysql /home/brent/backups/mysql
mirror -c server/source_dir client/target_dir
exit

# configure mysql client from host node
mysql_config_editor print --all
setw synchronize-panes on
setw synchronize-panes off
mysql_config_editor set --login-path=client --host=reports41 --port=30011 --user=root --password 

# backup all databases
mysqldump -u root -p -h reports31 --port=30031 --column-statistics=0 --add-drop-table --routines --all-databases > /home/brent/backups/mysql/$(/bin/date +\%Y-\%m-\%d-\%R:\%S).sql.bak

# restore datbases from a backup
note: port 30034 for test of mayastor only
mysql -u root -p -h reports31 --port=30034 < ~/backups/mysql/2023-02-03-13:54:31.sql.bak
