# Neural search demo Cloud deployment

## Requirements

- kubectl 1.29.2
- aws-cli 2.15.21
- istioctl 1.22.0
- terraform 1.7.5
- k9s ( Optional )

### AWS IAM user permsission required

To create an EKS module using Terraform, the AWS user needs the following IAM policies:

>|this permissions are not recommended for a production environment

- AmazonEC2FullAccess: Allows full access to Amazon EC2.
- AmazonRoute53FullAccess: Allows full access to Amazon Route 53.
- AmazonS3FullAccess: Allows full access to Amazon S3.
- IAMFullAccess: Allows full access to IAM.
- AmazonVPCFullAccess: Allows full access to Amazon VPC.
- AWSCloudFormationFullAccess: Allows full access to AWS CloudFormation.
- AmazonEKSFullAccess: Allows full access to Amazon EKS.
- AmazonEKSClusterPolicy: Allows EKS Cluster related operations.
- AmazonEKSServicePolicy: Allows EKS Service related operations.
- CloudWatchLogsFullAccess
- AmazonSSMFullAccess
- AWSKeyManagementServicePowerUser
- Custom Policy (eks:*)

For Congnito add

- AmazonCognitoPowerUser


## EKS Cluster creation

From Terraform folder

```
terraform init
terraform plan -target module.aws_k8s
```

Create EKS Cluster

> terraform apply -target module.aws_k8s

Run Export from output

> export KUBERNETES_MASTER=qdrant-demo

Update Kube Config

> aws eks update-kubeconfig --region us-east-1 --name $KUBERNETES_MASTER

Install Istio with istioctl

```
istioctl install -y --set meshConfig.accessLogFile=/dev/stdout
```

Install Qdrant DB and Nueral Search

```
kubectl create namespace qdrant-services
kubectl label namespace qdrant-services istio-injection=enabled
helm install qdrant-demo ../charts/qdrant_demo -n qdrant-services
helm install qdrant ../charts/qdrant/ -n qdrant-services --set replicaCount 3
```

Get Load Balancer URL
> kubectl get svc -n istio-system

Check the application accessing EXTERNAL-IP


Deploy Obervability Addons

```
cd ../charts; ./install_addons.sh; cd ../terraform;
```

Access Dashboards

```
kubectl port-forward svc/kiali 20001:20001 -n istio-system
kubectl port-forward svc/prometheus 9090:9090 -n istio-system
kubectl port-forward svc/grafana 3000:3000 -n istio-system
kubectl port-forward svc/jaeger 16686:16686 -n istio-system
```

Access the application with port-forward

```
kubectl port-forward svc/qdrant-demo 8000:80 -n qdrant-services
```

Access qdrant with port-foward
```
kubectl port-forward svc/qdrant 6333:6333 -n qdrant-services
kubectl port-forward svc/qdrant 6334:6334 -n qdrant-services
```


Access qdrant-demo app to upload data

> kubectl exec --stdin --tty svc/qdrant-demo -n qdrant-services -- /bin/bash

Inside the pod or local using port-forward, both 6333 and 6334

```
wget https://storage.googleapis.com/generall-shared-data/startups_demo.json -P data/
python -m qdrant-demo.init_collection_startups
```
