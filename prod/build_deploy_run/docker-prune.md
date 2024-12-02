<!-- https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes -->
# remove all images associated with a label
docker rmi $(docker images brentgroves/jupyterhub -q)

# clean up system 
provides a single command that will clean up any resources — images, containers, volumes, and networks — that are dangling (not tagged or associated with a container):
docker system prune

To additionally remove any stopped containers and all unused images (not just dangling images), add the -a flag to the command:

docker system prune -a

Remove dangling images
Docker images consist of multiple layers. Dangling images are layers that have no relationship to any tagged images. They no longer serve a purpose and consume disk space. They can be located by adding the filter flag -f with a value of dangling=true to the docker images command. When you’re sure you want to delete them, you can use the docker image prune command:

Note: If you build an image without tagging it, the image will appear on the list of dangling images because it has no association with a tagged image. You can avoid this situation by providing a tag when you build, and you can retroactively tag an image with the docker tag command.

List:
docker images -f dangling=true
Remove:

docker image prune

# Removing images according to a pattern
You can find all the images that match a pattern using a combination of docker images and grep. Once you’re satisfied, you can delete them by using awk to pass the IDs to docker rmi. Note that these utilities are not supplied by Docker and are not necessarily available on all systems:

List:
docker images -a |  grep "pattern"
Remove:

docker images -a | grep "pattern" | awk '{print $3}' | xargs docker rmi

# Remove all images
All the Docker images on a system can be listed by adding -a to the docker images command. Once you’re sure you want to delete them all, you can add the -q flag to pass the image ID to docker rmi:

List:

docker images -a
Remove:

docker rmi $(docker images -a -q)

# remove docker container
docker container ls
docker container rm --force 3fd46398ff65

# remove docker image
docker image ls
docker rmi 3f49118314d0  

# build docker image
docker build --tag brentgroves/reporting:3 .
docker build --tag brentgroves/reporting:3 --build-arg CACHEBUST=$(date +%s) .
