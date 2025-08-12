#!/bin/bash

# Step 1: Scale to 3 replicas
kubectl scale deployment django-app --replicas=3

# Step 2: Verify pods
kubectl get pods -o wide

# Step 3: Load testing
wrk -t4 -c100 -d30s http://django-service/

# Step 4: Resource usage
kubectl top pods
