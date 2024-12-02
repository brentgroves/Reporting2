# build docker image for reports-volume-init
-Thank you Father for helping me today!
pushd ~/src/Reporting/prod

# do this only once so that you can debug on local machine.
# ftp a current dw backup onto the node
# I don't think we need to do this anymore
lftp brent@reports31
mirror -c /etc/db-user-pass /home/brent/db-user-pass
exit
sudo cp -r /home/brent/db-user-pass /etc/db-user-pass
rm -rf /home/brent/db-user-pass

# update source files for build and node info
pushd ~/src/Reporting/prod/volume
./sed-volume.sh dev reports31 30031 0 reports31 30331 reports

ver=$1
./build-reports-volume-init.sh 1
docker build --tag brentgroves/reports-volume-init:1 --build-arg CACHEBUST=$(date +%s) .

# start a container in the background
docker run --name reports-volume-init -d brentgroves/reports-volume-init:1
docker container ls -a

# Next, execute an interactive bash shell on the container.
docker exec -it reports-volume-init bash

# push to docker hub
docker login brentgroves Jesuslives1!
docker push brentgroves/reports-volume-init:1







