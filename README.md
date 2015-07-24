# TECTONIQ

Modeling territorial knowledge from Web data about natural and cultural heritage

There are basically two approaches defined here. 

Solution 1
==========

Solution1 is based on a MongoDB database with added functionalities and improvements on information retrieval. For example indexing is done based on tfidf calculations. 


All the data given in all the xml files were passed to store in one collection in the mongodb database. 

doc_id: {descriptors} --> This follows the metadata model described in the metadatamodel.png


Solution 2
==========

The second solution is based on a domain ontology for textile industry. The ontology is defined in the tectoniq.owl file. Crawler.py is for data population and this is written only for image described xml files and only one image description is populated as a sample.  

Python interpreter
------------------
Crawler.py -> Python 2.7 
View.py -> Python 3.4

Run the View.py file and open it using the URL http://127.0.0.1:5000/result. 

Data Lake Implementation using Hadoop
=====================================

Implementing a Data Lake is one of the prominent solutions for organizing and storing patrimonial data. Data Lake implementation initialy was introduced with Hadoop. Therefore, as a trial I started deploying a Hadoop cluster on Amazon cloud(EC2-Ubuntu Servers). But it is always better to use physical servers. I used four virtual servers altogether, one being the master node and three slave nodes. To install Hadoop you can simply follow this tutorial: 

https://dzone.com/articles/how-set-multi-node-hadoop

SSH has to be configured properly so that the master node can communicate with its slave nodes. 

It is done only up to this point and the next step is to store our data in the cluster.

