### Question 1: What is count of records for the 2022 Green Taxi Data?

**840,402**

```console
SELECT COUNT(*) FROM `de-zoomcamp.trips_dataset.trips_green_2022_external`;
// 840,402
SELECT COUNT(*) FROM `de-zoomcamp.trips_dataset.trips_green_2022_materialized`;
// 840,402
```

### Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

**0 MB for the External Table and 6.41MB for the Materialized Table**

```console
SELECT COUNT (DISTINCT PULocationID) FROM `de-zoomcamp.trips_dataset.trips_green_2022_external`;
// 0 B
SELECT COUNT (DISTINCT PULocationID) FROM `de-zoomcamp.trips_dataset.trips_green_2022_materialized`;
// 6.41 MB
```

### Question 3:
How many records have a fare_amount of 0?

**1,622**

```console
SELECT COUNT(*) FROM `de-zoomcamp.trips_dataset.trips_green_2022_external` WHERE fare_amount = 0;
// 1,622
SELECT COUNT(*) FROM `de-zoomcamp.trips_dataset.trips_green_2022_materialized` WHERE fare_amount = 0;
// 1,622
```

### Question 4:
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime?

**Partition by lpep_pickup_datetime Cluster on PUlocationID**

```console
CREATE TABLE `de-zoomcamp.trips_dataset.trips_green_2022_partitioned` 
PARTITION BY DATE (lpep_pickup_datetime) 
CLUSTER BY PULocationID 
AS 
SELECT * FROM `de-zoomcamp.trips_dataset.trips_green_2022_external`;
```

### Question 5:

Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

Choose the answer which most closely matches.
Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.

**12.82 MB for non-partitioned table and 1.12 MB for the partitioned table**

```console
SELECT DISTINCT(PULocationID) FROM `de-zoomcamp.trips_dataset.trips_green_2022_materialized` WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
// 12.82 MB

SELECT DISTINCT(PULocationID) FROM `de-zoomcamp.trips_dataset.trips_green_2022_partitioned` WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
// 1.12 MB
```

### Question 6:
Where is the data stored in the External Table you created?

**GCP Bucket**

### Question 7:
It is best practice in Big Query to always cluster your data:

**False**

### (Bonus: Not worth points) Question 8:
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
```console
SELECT COUNT(*) FROM `de-zoomcamp.trips_dataset.trips_green_2022_materialized`;
// 0 B
```
'SELECT *' in BigQuery makes it challenging to accurately estimate the number of rows that need to be fetched.
