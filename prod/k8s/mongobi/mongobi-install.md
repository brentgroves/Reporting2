Plan:
created statefulset deployment and a loadbalancer using existing dockerfile.
Deploy to azure following the steps of mongodb-aks.
Update dockerfile to point to dns entry instead of Azure IP
Think about changing mongobi from storing everything in memory to a pv or something else.
Think about deploying ETL scripts to Azure AKS.

