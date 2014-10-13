
This docker image has 
latest ubuntu
spark 1.1.0
oracle jdk7
python2.7
scala 2.10.4(ubuntu's default 2.9 didn't work)
spark-cassandra-connector 1.1.0
cassandra 2.0.10 (2.1 didn't work)
cassandra java driver 2.1.0(2.1.1 didn't work)


# How to use it:
There's a shell script called spark-cass which calls spark-shell with the appropriate jar files for adding
```
host# docker run -t -i spark-cass-image
root@docker# ./spark-cass
... # lots of spark startup messages
scala>   import com.datastax.spark.connector._;
# scala tab-completion can't complete sc.cassandraTable() so you have to type it in directly.
scala>   val table = sc.cassandraTable("testkeyspace","trigram");
scala>   table.count

# or us SchemaRDD
scala>   import org.apache.spark.sql.cassandra.CassandraSQLContext;
scala>   val cc = new CassandraSQLContext(sc)
scala>   val rdd: SchemaRDD = cc.sql("SELECT * from testkeyspace.trigram WHERE ...")
```

#Trigram scala project:
see README in trigram on building a scala project to access cassandra tables

More info:
The docker cmd starts up the cassandra service. Spark uses a local cluster connected to a local cassandra cluster via 127.0.0.1

It creates a script /root/spark-cass which is just spark-shell but passes in the appropriate jars 

I'm no expert in any of these packages, so improvements can be made. I built this so I could 
jump into testing, not as an example of best practices.

eg: sbt assembly builds an uber jar with all dependencies, this is slow but reduces dependency issues.
Instead of spark-cass, there's probably a way to use environment variables directly instead of a separate script which calls spark-shell with jar files. Whether that's better is up for debate.



