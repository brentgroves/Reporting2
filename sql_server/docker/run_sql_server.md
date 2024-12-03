# SQL Server in Docker

## references

<https://www.youtube.com/watch?v=fFpDf5si_Hw>
<https://hub.docker.com/_/microsoft-mssql-server>

## How to use this Image

Start a mssql-server instance for SQL Server 2022, which is now generally available (GA). These images are based on Ubuntu 20.04 and is fully supported for production workload.

Start a mssql-server instance for SQL Server 2022, which is now generally available (GA). These images are based on Ubuntu 20.04 and is fully supported for production workload.

**[Pull and connect](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&preserve-view=true&tabs=cli&pivots=cs1-bash)**

```bash
docker pull mcr.microsoft.com/mssql/server:2022-latest

docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=~/src/secrets/namespaces/default/credentials.yaml' \
   -p 1433:1433 --name sql1 --hostname sql1 \
   -d \
   mcr.microsoft.com/mssql/server:2022-latest
```

## Connect to SQL Server

The following steps use the SQL Server command-line tool, sqlcmd utility, inside the container to connect to SQL Server.

Use the docker exec -it command to start an interactive bash shell inside your running container. In the following example, sql1 is name specified by the --name parameter when you created the container.

```Bash
docker exec -it sql1 "bash"
# Once inside the container, connect locally with sqlcmd, using its full path.
sudo /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "~/src/secrets/namespaces/default/credentials.yaml"
# Create a new database
# The following steps create a new database named TestDB.
# From the sqlcmd command prompt, paste the following Transact-SQL command to create a test database:
CREATE DATABASE TestDB;
# On the next line, write a query to return the name of all of the databases on your server:
SELECT Name from sys.databases;
# The previous two commands weren't run immediately. Type GO on a new line to run the previous commands:
GO
Name                                                                                                                            
--------------------------------------------------------------------------------------------------------------------------------
master                                                                                                                          
tempdb                                                                                                                          
model                                                                                                                           
msdb                                                                                                                            
TestDB                                                                                                                          

(5 rows affected)
CREATE TABLE Inventory (id INT, name NVARCHAR(50), quantity INT);
INSERT INTO Inventory VALUES (1, 'banana', 150); INSERT INTO Inventory VALUES (2, 'orange', 154);
```

<!-- https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&preserve-view=true&tabs=cli&pivots=cs1-bash -->