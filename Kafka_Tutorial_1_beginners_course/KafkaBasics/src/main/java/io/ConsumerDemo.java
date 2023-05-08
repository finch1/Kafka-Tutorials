package io;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Properties;

public class ConsumerDemo {
    //Basic Message Consumer
    private static final Logger log = LoggerFactory.getLogger(ConsumerDemo.class.getSimpleName());
    public static void main(String[] args) {

        String bootstrapServer = "localhost:9092";
        String topic = "first_topic";
        String groupID = "my-first-consumer-group";

        Properties props = new Properties();
        props.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServer);
        props.setProperty(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.setProperty(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.setProperty(ConsumerConfig.GROUP_ID_CONFIG, groupID);
        // Accepts 3 values - none, latest, earliest
        // none = if no previous offsets are found, do not start
        // earliest = read from the beginning of the topic. historical
        // latest = read from now of topic
        props.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        // Consumer
        KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String >(props);

        // subscribe consumer to topic
        // consumer.subscribe(Collections.singletonList(topic));

        // subscribe consumer to topics
        consumer.subscribe(Arrays.asList(topic));

        // poll for new data
        while(true){
            log.info("Pollong");
            // poll Kafka and get as many records as you can. If there are no more, go to the next line of code and create empty array
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));

            // iterate in received records
            for(ConsumerRecord<String, String> record : records){
                log.info("Key: " + record.key() + " ,Value: " + record.value());
                log.info("Partition: " + record.partition() + " ,Offset: " + record.offset());
            }
        }

    }
}
