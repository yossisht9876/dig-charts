postgres secrets

in case that we dont use vault/ssm or any other secret store 

kubectl create secret generic postgres-secret --from-literal=username=digroot --from-literal=password=rootxxxTTAGgh
