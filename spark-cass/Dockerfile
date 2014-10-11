FROM dockerfile/java:oracle-java7
MAINTAINER hubt

ENV CASSANDRA_JAVA_DRIVER http://downloads.datastax.com/java-driver/cassandra-java-driver-2.1.1.tar.gz
RUN curl -s http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0.tgz| tar -xz -C /usr/local/
#RUN curl -s http://mirrors.ibiblio.org/apache/cassandra/2.1.0/apache-cassandra-2.1.0-bin.tar.gz | tar -xz -C /usr/local/
RUN cd /usr/local ; ln -s spark-1.1.0 spark 
#RUN cd /usr/local ; ln -s apache-cassandra-2.1.0 cassandra
RUN cd /usr/local/spark ; sbt/sbt assembly
RUN echo "deb http://debian.datastax.com/community stable main"  >> /etc/apt/sources.list.d/cassandra.sources.list
RUN curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -


#ENV SPARK_JAR hdfs:///spark/spark-assembly-1.0.1-hadoop2.4.1.jar

#CMD [ '/etc/bootstrap.sh', '-d' ]

RUN sudo apt-add-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get -y install python2.7 python-support scala libjna-java
#RUN cd /usr/bin ; ln -s python2.7 python
RUN cd /usr/local; wget http://debian.datastax.com/community/pool/cassandra_2.0.10_all.deb ; dpkg -i cassandra_2.0.10_all.deb
#RUN python -V
#RUN echo 'PATH="/usr/local/spark/bin:/usr/local/cassandra/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"' >> /root/.profile
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

#ENV CLASSPATH /usr/local/spark-cassandra/spark-cassandra-connector-java/target/scala-2.10/spark-cassandra-connector-java_2.10-1.1.0-alpha2.jar 
#ENV SPARK_CLASSPATH /usr/local/spark-cassandra/spark-cassandra-connector-java/target/scala-2.10/spark-cassandra-connector-java_2.10-1.1.0-alpha2.jar 

# ENV SPARK_CLASSPATH /usr/local/spark-cassandra/spark-cassandra-connector/target/scala-2.10/spark-cassandra-connector_2.10-1.1.0-alpha2.jar,/usr/local/spark-cassandra/spark-cassandra-connector-java/target/scala-2.10/spark-cassandra-connector-java_2.10-1.1.0-alpha2.jar,/root/.ivy2/cache/com.datastax.cassandra/cassandra-driver-core/jars/cassandra-driver-core-2.1.0.jar,/usr/share/cassandra/apache-cassandra-thrift-2.0.10.jar,/usr/share/cassandra/lib/libthrift-0.9.1.jar

# RUN echo spark.executor.extraClassPath /usr/local/spark-cassandra/spark-cassandra-connector-java/target/scala-2.10/spark-cassandra-connector-java_2.10-1.1.0-alpha2.jar >> /usr/local/spark/conf/spark-defaults.conf
RUN echo "spark.cassandra.connection.host 127.0.0.1" >> /usr/local/spark/conf/spark-defaults.conf

#copy test

RUN curl http://downloads.datastax.com/java-driver/cassandra-java-driver-2.1.1.tar.gz

# build a nice simple script to run spark-cassandra
RUN echo '#!/bin/bash' > spark-cass
RUN echo 'spark-shell --jars /usr/local/spark-cassandra/spark-cassandra-connector/target/scala-2.10/spark-cassandra-connector_2.10-1.1.0-alpha2.jar,/usr/local/spark-cassandra/spark-cassandra-connector-java/target/scala-2.10/spark-cassandra-connector-java_2.10-1.1.0-alpha2.jar,/root/.ivy2/cache/com.datastax.cassandra/cassandra-driver-core/jars/cassandra-driver-core-2.1.0.jar,/usr/share/cassandra/apache-cassandra-thrift-2.0.10.jar,/usr/share/cassandra/lib/libthrift-0.9.1.jar' >> spark-cass
RUN chmod 755 spark-cass

