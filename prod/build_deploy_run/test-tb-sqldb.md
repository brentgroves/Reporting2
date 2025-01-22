# Test TB from Azure SQL DB 

- run tb from mi
- run tb from repsys1
- cmp rowcounts of mi and repsys1
- create repsys1.Plex.account_period_balance_mi
- cp mi.account_period_balance to repsys1.Plex.account_period_balance_mi
-  cmp repsys1.Plex.account_period_balance_mi with repsys1.Plex.account_period_balance
