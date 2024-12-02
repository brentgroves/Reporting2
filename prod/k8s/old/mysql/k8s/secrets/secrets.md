# create primary tls secret for 'microk8s.local'
microk8s kubectl create -n default secret tls tls-credential --key=/tmp/microk8s.local.key --cert=/tmp/microk8s.local.crt


https://kubernetes.io/docs/concepts/configuration/secret/
# shows both tls secrets
microk8s kubectl get secrets --namespace default
microk8s kubectl describe secrets/tls-credential

Secrets
A Secret is an object that contains a small amount of sensitive data such as a password, a token, or a key. Such information might otherwise be put in a Pod specification or in a container image. Using a Secret means that you don't need to include confidential data in your application code.

Because Secrets can be created independently of the Pods that use them, there is less risk of the Secret (and its data) being exposed during the workflow of creating, viewing, and editing Pods. Kubernetes, and applications that run in your cluster, can also take additional precautions with Secrets, such as avoiding writing secret data to nonvolatile storage.

Secrets are similar to ConfigMaps but are specifically intended to hold confidential data.

Caution:
Kubernetes Secrets are, by default, stored unencrypted in the API server's underlying data store (etcd). Anyone with API access can retrieve or modify a Secret, and so can anyone with access to etcd. Additionally, anyone who is authorized to create a Pod in a namespace can use that access to read any Secret in that namespace; this includes indirect access such as the ability to create a Deployment.

In order to safely use Secrets, take at least the following steps:

Enable Encryption at Rest for Secrets.
Enable or configure RBAC rules that restrict reading and writing the Secret. Be aware that secrets can be obtained implicitly by anyone with the permission to create a Pod.
Where appropriate, also use mechanisms such as RBAC to limit which principals are allowed to create new Secrets or replace existing ones.

Creating a Secret
There are several options to create a Secret:

create Secret using kubectl command
create Secret from config file
create Secret using kustomize
Constraints on Secret names and data
The name of a Secret object must be a valid DNS subdomain name.

You can specify the data and/or the stringData field when creating a configuration file for a Secret. The data and the stringData fields are optional. The values for all keys in the data field have to be base64-encoded strings. If the conversion to base64 string is not desirable, you can choose to specify the stringData field instead, which accepts arbitrary strings as values.

The keys of data and stringData must consist of alphanumeric characters, -, _ or .. All key-value pairs in the stringData field are internally merged into the data field. If a key appears in both the data and the stringData field, the value specified in the stringData field takes precedence.

Size limit
Individual secrets are limited to 1MiB in size. This is to discourage creation of very large secrets that could exhaust the API server and kubelet memory. However, creation of many smaller secrets could also exhaust memory. You can use a resource quota to limit the number of Secrets (or other resources) in a namespace.

Editing a Secret
You can edit an existing Secret using kubectl:

kubectl edit secrets mysecret

This opens your default editor and allows you to update the base64 encoded Secret values in the data field; for example:

# Please edit the object below. Lines beginning with a '#' will be ignored,
# and an empty file will abort the edit. If an error occurs while saving this file, it will be
# reopened with the relevant failures.
#
apiVersion: v1
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
kind: Secret
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: { ... }
  creationTimestamp: 2020-01-22T18:41:56Z
  name: mysecret
  namespace: default
  resourceVersion: "164619"
  uid: cfee02d6-c137-11e5-8d73-42010af00002
type: Opaque
That example manifest defines a Secret with two keys in the data field: username and password. The values are Base64 strings in the manifest; however, when you use the Secret with a Pod then the kubelet provides the decoded data to the Pod and its containers.

You can package many keys and values into one Secret, or use many Secrets, whichever is convenient.

Using a Secret
Secrets can be mounted as data volumes or exposed as environment variables to be used by a container in a Pod. Secrets can also be used by other parts of the system, without being directly exposed to the Pod. For example, Secrets can hold credentials that other parts of the system should use to interact with external systems on your behalf.

Secret volume sources are validated to ensure that the specified object reference actually points to an object of type Secret. Therefore, a Secret needs to be created before any Pods that depend on it.

If the Secret cannot be fetched (perhaps because it does not exist, or due to a temporary lack of connection to the API server) the kubelet periodically retries running that Pod. The kubelet also reports an Event for that Pod, including details of the problem fetching the Secret.

Optional Secrets
When you define a container environment variable based on a Secret, you can mark it as optional. The default is for the Secret to be required.

None of a Pod's containers will start until all non-optional Secrets are available.

If a Pod references a specific key in a Secret and that Secret does exist, but is missing the named key, the Pod fails during startup.

Using Secrets as files from a Pod
If you want to access data from a Secret in a Pod, one way to do that is to have Kubernetes make the value of that Secret be available as a file inside the filesystem of one or more of the Pod's containers.

To configure that, you:

Create a secret or use an existing one. Multiple Pods can reference the same secret.
Modify your Pod definition to add a volume under .spec.volumes[]. Name the volume anything, and have a .spec.volumes[].secret.secretName field equal to the name of the Secret object.
Add a .spec.containers[].volumeMounts[] to each container that needs the secret. Specify .spec.containers[].volumeMounts[].readOnly = true and .spec.containers[].volumeMounts[].mountPath to an unused directory name where you would like the secrets to appear.
Modify your image or command line so that the program looks for files in that directory. Each key in the secret data map becomes the filename under mountPath.
This is an example of a Pod that mounts a Secret named mysecret in a volume:

apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
      readOnly: true
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      optional: false # default setting; "mysecret" must exist
Each Secret you want to use needs to be referred to in .spec.volumes.

If there are multiple containers in the Pod, then each container needs its own volumeMounts block, but only one .spec.volumes is needed per Secret.

Consuming Secret values from volumes
Inside the container that mounts a secret volume, the secret keys appear as files. The secret values are base64 decoded and stored inside these files.

This is the result of commands executed inside the container from the example above:

ls /etc/foo/
The output is similar to:

username
password
cat /etc/foo/username
The output is similar to:

admin
cat /etc/foo/password
The output is similar to:

1f2d1e2e67df
The program in a container is responsible for reading the secret data from these files, as needed.

Mounted Secrets are updated automatically
When a volume contains data from a Secret, and that Secret is updated, Kubernetes tracks this and updates the data in the volume, using an eventually-consistent approach.

Note: A container using a Secret as a subPath volume mount does not receive automated Secret updates.
The kubelet keeps a cache of the current keys and values for the Secrets that are used in volumes for pods on that node. You can configure the way that the kubelet detects changes from the cached values. The configMapAndSecretChangeDetectionStrategy field in the kubelet configuration controls which strategy the kubelet uses. The default strategy is Watch.

Updates to Secrets can be either propagated by an API watch mechanism (the default), based on a cache with a defined time-to-live, or polled from the cluster API server on each kubelet synchronisation loop.

As a result, the total delay from the moment when the Secret is updated to the moment when new keys are projected to the Pod can be as long as the kubelet sync period + cache propagation delay, where the cache propagation delay depends on the chosen cache type (following the same order listed in the previous paragraph, these are: watch propagation delay, the configured cache TTL, or zero for direct polling).

Using Secrets as environment variables
To use a Secret in an environment variable in a Pod:

Create a Secret (or use an existing one). Multiple Pods can reference the same Secret.
Modify your Pod definition in each container that you wish to consume the value of a secret key to add an environment variable for each secret key you wish to consume. The environment variable that consumes the secret key should populate the secret's name and key in env[].valueFrom.secretKeyRef.
Modify your image and/or command line so that the program looks for values in the specified environment variables.
This is an example of a Pod that uses a Secret via environment variables:

apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: mycontainer
    image: redis
    env:
      - name: SECRET_USERNAME
        valueFrom:
          secretKeyRef:
            name: mysecret
            key: username
            optional: false # same as default; "mysecret" must exist
                            # and include a key named "username"
      - name: SECRET_PASSWORD
        valueFrom:
          secretKeyRef:
            name: mysecret
            key: password
            optional: false # same as default; "mysecret" must exist
                            # and include a key named "password"
  restartPolicy: Never