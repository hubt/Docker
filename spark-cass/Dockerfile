FROM dockerfile/java:oracle-java7
MAINTAINER hubt

RUN curl -s http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0.tgz| tar -xz -C /usr/local/
RUN curl -s http://mirrors.ibiblio.org/apache/cassandra/2.1.0/apache-cassandra-2.1.0-bin.tar.gz | tar -xz -C /usr/local/
RUN cd /usr/local ; ln -s spark-1.1.0 spark 
RUN cd /usr/local ; ln -s apache-cassandra-2.1.0 cassandra
RUN cd /usr/local/spark ; sbt/sbt assembly
#RUN $BOOTSTRAP &amp;&amp; $HADOOP_PREFIX/bin/hadoop dfsadmin -safemode leave &amp;&amp; $HADOOP_PREFIX/bin/hdfs dfs -put /usr/local/spark/assembly/target/scala-2.10 /spark

#ENV YARN_CONF_DIR $HADOOP_PREFIX/etc/hadoop
#ENV SPARK_JAR hdfs:///spark/spark-assembly-1.0.1-hadoop2.4.1.jar

#CMD [ '/etc/bootstrap.sh', '-d' ]

RUN sudo apt-add-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get -y install python2.7
RUN apt-get -y install scala
RUN cd /usr/bin ; ln -s python2.7 python
RUN echo 'PATH="/usr/local/spark/bin:/usr/local/cassandra/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"' >> /root/.profile
#RUN cd /usr/local ; ln -s /usr/local/spark/bin/* /usr/local/cassandra/bin/* bin/

# install ez_setup
RUN curl -s https://bootstrap.pypa.io/ez_setup.py | python
# install pycass
RUN easy_install cassandra-driver

# sbt
RUN curl -L -s https://dl.bintray.com/sbt/native-packages/sbt/0.13.6/sbt-0.13.6.tgz | tar -zx -C /usr/local

RUN curl -L -s https://github.com/datastax/spark-cassandra-connector/archive/v1.1.0-alpha2.tar.gz | tar -zx -C /usr/local
RUN cd /usr/local/; ln -s spark-cassandra-connector-1.1.0-alpha2/ spark-cassandra
RUN cd /usr/local/spark-cassandra ; sbt/sbt package

RUN /usr/local/cassandra/bin/cassandra -f > /var/log/cassandra.log &

ENV PATH /usr/local/spark/bin:/usr/local/cassandra/bin:/usr/local/sbt/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
# install test python program
COPY trigrams /root/trigrams
COPY setup.sql /root/setup.sql

RUN cd /root; cassandra ; sleep 15; cqlsh < setup.sql

ENV CLASSPATH /usr/local/spark-cassandra/spark-cassandra-connector-java/target/scala-2.10/spark-cassandra-connector-java_2.10-1.1.0-alpha2.jar 
ENV SPARK_CLASSPATH /usr/local/spark-cassandra/spark-cassandra-connector-java/target/scala-2.10/spark-cassandra-connector-java_2.10-1.1.0-alpha2.jar 

# RUN echo spark.executor.extraClassPath /usr/local/spark-cassandra/spark-cassandra-connector-java/target/scala-2.10/spark-cassandra-connector-java_2.10-1.1.0-alpha2.jar >> /usr/local/spark/conf/spark-defaults.conf
RUN echo "spark.cassandra.connector.host 127.0.0.1" >> /usr/local/spark/conf/spark-defaults.conf

