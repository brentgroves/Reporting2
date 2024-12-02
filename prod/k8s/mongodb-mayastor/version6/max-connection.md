kubectl run -it mongo-shell --image=mongo:6.0.3 --rm -- /bin/bash
mongosh mongo.mongo.svc.cluster.local


https://github.com/docker-library/mongo/issues/575

   The server generated these startup warnings when booting
   2023-02-13T18:32:41.436+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2023-02-13T18:32:41.996+00:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   2023-02-13T18:32:41.997+00:00: vm.max_map_count is too low
