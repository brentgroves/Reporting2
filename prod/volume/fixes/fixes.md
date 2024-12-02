# https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues
ubuntu uses /run/systemd/resolve/resolv.conf but k8s uses /etc/resolv.conf to resolve dns names
