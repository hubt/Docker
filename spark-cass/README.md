
This docker image has 
latest ubuntu
spark 1.1.0
oracle jdk7
python2.7
scala 2.10.4(ubuntu's default 2.9 didn't work)
spark-cassandra-connector 1.1.0
cassandra 2.0.10 (2.1 didn't work)
cassandra java driver 2.1.0(2.1.1 didn't work)

How to use it:
docker run -t -i spark-cass
./spark-cass
scala>   import com.datastax.spark.connector._;
# scala tab-completion can't complete sc.cassandraTable() so you have to type it in directly.
scala>   val table = sc.cassandraTable("testkeyspace","trigram");
scala>   table.count

# or us SchemaRDD
scala>   import org.apache.spark.sql.cassandra.CassandraSQLContext;
scala>   val cc = new CassandraSQLContext(sc)
scala>   val rdd: SchemaRDD = cc.sql("SELECT * from testkeyspace.trigram WHERE ...")

Trigram scala project:
see README in trigram on building a scala project to access cassandra tables

More info:
The docker cmd starts up the cassandra service

It creates a script /root/spark-cass which is just spark-shell but passes in the appropriate jars 

I'm no expert in any of these packages, so improvements are welcome. I built this so I could 
jump into testing, not as an example of best practices.

eg: sbt assembly builds an uber jar with all dependencies, this is slow but reduces dependency issues

