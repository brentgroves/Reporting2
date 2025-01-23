# Test TB from Azure SQL DB 

- update dsn
- run tb from mi
- run tb from repsys1
- cmp rowcounts of mi and repsys1
- create repsys1.Plex.account_period_balance_mi
- cp mi.account_period_balance to repsys1.Plex.account_period_balance_mi
-  cmp repsys1.Plex.account_period_balance_mi with repsys1.Plex.account_period_balance


## update lastpass for mi

```bash
pushd .. 
cd ~/src/Reporting2/prod/k8s/secrets/lastpass
./print-etc-lastpass.sh
# on dev system update local passwords in /etc/lastpass
./sed-lastpass-sh.sh reports31 30031 reports32 30332 reports 1
ls /etc/lastpass
# ssh to dev system
./lastpass_mi.sh
./print-etc-lastpass.sh

```

## run tb

## update lastpass for repsys1

```bash
pushd .. 
cd ~/src/Reporting2/prod/k8s/secrets/lastpass
./print-etc-lastpass.sh
# on dev system update local passwords in /etc/lastpass
./sed-lastpass-sh.sh reports31 30031 reports32 30332 reports 1
ls /etc/lastpass
# ssh to dev system
./lastpass_repsys1.sh
./print-etc-lastpass.sh

```
