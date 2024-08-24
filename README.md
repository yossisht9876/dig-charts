# DevOps Home Assignment - Dig Security

## Overview

task containes 6 main folders:
* .github/workflow: 

    contain the ci-cd yaml file:
    
    Build each container service - with the DOCKERFILE

    Deploy each image to the private registry - DOCKER-HUB

    Update the K8s cluster with new containers services - EKS or any other 

* application:

    contain the backend\frontend code with the dockerfile used to containerize the app services

* charts:

    contain an umbrella chart that made up of 3 helm charts:
    backend
    frontend
    postgresql

* ci-cd:
  
    contain the github action yaml file - build/push/deploy

* terraform:

    contains few basic tf files to deploy the all infrastructure:


    eks folder : 

    eks.tf - will create the eks cluster 

    helm folder:

    helm.tf - another option that will deploy the helm charts using terraform

    plan output:  (full output can be found in the terraform repo - tf-plan.txt)

  eks:
  
  ![image](https://github.com/user-attachments/assets/a39005af-7a09-4a86-b558-b8d30a79d5f8)

  helm:
  
  ![image](https://github.com/user-attachments/assets/4bb770b7-77cb-4137-94ab-deef053960dc)


  

* private-docker-registry

  create a private-docker-registry with pvc to ensure the the images will 

  persist after restart

* Usage:

There are few options to deploy the stack:

1. using terraform:

   run the terraform stack to create the eks cluster and deploy the helm 

   charts using terraform to the created eks cluster

2. using github action

   run the ci-cd github action that build the image ,

   then push it and last deploy the helm charts to the eks cluster.


3. manualy

* build / push the images:

   `docker build -t <tagname>`

   `docker push <tagname>`
* update the charts with the iamge tag and deploy using helm:

   `helm install dig . -n dig`

![image](https://github.com/user-attachments/assets/41050135-34ef-40fd-af4f-93f16c4bfaa4)

using port-forward when the container is running :

![תמונה](https://github.com/user-attachments/assets/e4580ebe-5c5a-409f-92fb-aac1e1271a47)



* monitoring:

    for monitoring option solution Prometheus + grafana can be used:
    
    1 . ajest the code in order to expose the metrics
       
    for example i added prometheus_client in order to expose the metrics to the /metrics path
    
    ![תמונה](https://github.com/user-attachments/assets/fd2398a7-9388-4563-a8de-41fd9b6b4322)
    
    then from localhost/port/metrics

![תמונה](https://github.com/user-attachments/assets/e3e141a2-a12d-405b-850d-e6b873743329)


the next set is to deploy the Prometheus stack

1. Install Prometheus and Grafana

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Create a monitoring namespace
kubectl create namespace monitoring

# Install Prometheus
helm install prometheus prometheus-community/prometheus --namespace monitoring

# Install Grafana
helm install grafana grafana/grafana --namespace monitoring

then create a ServiceMonitor for your service to scarp it every X time:

`apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backend-service-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: backend
  endpoints:
  - port: http
    interval: 30s
    path: /metrics`

add target to promethus and create a relevent dashboard on grafana





