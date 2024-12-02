https://learnk8s.io/templating-yaml-with-code
https://www.densify.com/kubernetes-tools/kustomize


Using templates with search and replace
A better strategy is to have a placeholder and replace it with the real value before the YAML is submitted to the cluster.

Search and replace.

If you're familiar with bash, you can implement search and replace with few lines of sed.

Your Pod should contain a placeholder like this:

pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: test-container
    image: k8s.gcr.io/busybox
    env:
    - name: ENV
      value: %ENV_NAME%
And you could run the following command to replace the value of the environment on the fly.

bash
sed s/%ENV_NAME%/$production/g \
 pod_template.yaml > pod_production.yaml

%REPORTS_SERVICE%
 reports11-service
sed s/%SERVICE_NAME%/reports11-service/g \
 reports-deploy.yaml > sed/chg1.yaml
sed s/%APP%/reports11/g \
 sed/chg1.yaml > sed/chg2.yaml
sed s/%VER%/1/g \
 sed/chg2.yaml > reports1/reports11-deploy.yaml
