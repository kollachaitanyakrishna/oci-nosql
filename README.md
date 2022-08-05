# How to optimize the cost of the oracle nosql cloud tables?
NoSQL is used to store JSON document, columnar and key-value database models, delivering predictable single digit millisecond response times with data replication for high availability.

Let us look at a use case with estimated cost and further steps to reduce the cost.

Use Case: using Kubernetes (OKE), Store the cost data from the cost management section in Oracle CLoud (OCI) as “billing_raw” in nosql cloud table and process it further from hourly data to daily data in to another table “billing_processed”. 

Sample Cost Calculation:
NoSQL billing cost is calculated based on storage size, reads & writes allocation. 
| Table Name | No. of Reads. | No. of writes |	Database size	| Cost |
| ---------- | ------------- | ------------- | --------------- | ---- |
|billing_raw	|1000	|1000	|10gb|	$132.46
|billing_processed	|500	|500	|5gb	|$66.23

This cost may vary, please check Cost Estimator - [link](https://www.oracle.com/in/cloud/costestimator.html) for latest rates

As per the use case this process will take ~10 mins to complete this requirement with daily cron job in OKE. 

By implementing the best practices, the cost can be further reduced.

In a 24hrs of day, compute power is required during the job execution time. It does not require any reads and writes in idle. 

Manually it is not possible to allocate before the start of process and reduce after the process. Oracle NoSQL SDK supports to set the read and write using the API.

# Flow:
start -> Increase read & writes -> Process Job -> Reduce Reads & writes -> Stop 

# References
Try with Local installation of NoSQL link

