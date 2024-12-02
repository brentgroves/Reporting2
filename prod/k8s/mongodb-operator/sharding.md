https://stackoverflow.com/questions/74687480/does-mongodb-community-operator-supports-sharding-architecture

Does mongodb community operator supports sharding architecture? If no what are the alternate open source operator options which supports the sharding setup

0


The accepted answer is totally wrong. The community operator doesn't support sharded cluster. Their GitHub clearly states this:

"The Community Operator does not support creation of sharded clusters yet. Please feel free to contribute to the codebase for features like this." Apr 2022

https://github.com/mongodb/mongodb-kubernetes-operator/issues/947#issuecomment-1102320381
https://github.com/mongodb/mongodb-kubernetes-operator/issues/231

The design of the Enterprise and Community Operators is quite different - they share some code, but not the code which deploys MongoDB instances (the Enterprise Operator relies on Ops or Cloud Manager).

As a result, sharded cluster support in this Operator will need to be new code - whether it's written by a community member or the MongoDB Kubernetes team.

We would accept Community PRs to add Sharding support, as long as they had the right amount of testing so that we could support the feature. No forking needed - that's what OSS is all about.
0


It does. The main features in Enterprise Edition which are not available in Community Edition are these:

In-Memory Storage Engine
Auditing
Kerberos Authentication
LDAP Proxy Authentication and LDAP Authorization
Encryption at Rest
See https://www.mongodb.com/docs/manual/administration/upgrade-community-to-enterprise/

There are a few more functions in Enterprise, but they are minor.

https://www.mongodb.com/docs/manual/administration/upgrade-community-to-enterprise/