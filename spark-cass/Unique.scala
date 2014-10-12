
import com.datastax.spark.connector._; 

val trigrams = sc.cassandraTable("testkeyspace","trigram");
println("There are " + trigrams.count + "trigrams");

println("Joining in spark" );
val firstwords = trigrams.keyBy(x => x(0));
val secondwords = trigrams.keyBy(x => x(1));

val joined = firstwords.join(secondwords);
joined.foreach(x => println("key: " + x._1 + " value: " + x._2));
println("There are " + joined.count + " joined results");
