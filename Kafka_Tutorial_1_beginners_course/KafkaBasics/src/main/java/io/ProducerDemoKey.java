package io;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Properties;

public class ProducerDemoKey {
    //Basic Message Producer to confirm that same key goes to same partition after running code multiple times
    private static final Logger log = LoggerFactory.getLogger(ProducerDemoKey.class.getSimpleName());
    public static void main(String[] args) {
        log.info("I am a Kafka Producer");

        // Create producer properties
        Properties props = new Properties();
        props.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

        // serialize data from objects to binary for Kafka
        props.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // Create producer
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);


        for(int i = 30;i<45;i++)
        {
            String topic = "first_topic";
            String key = "id_"+i;
            String value = "hello world from java with key "+i;

            ProducerRecord<String, String> producerRecord = new ProducerRecord<>(topic, key, value);
            // Send data async
            producer.send(producerRecord, new Callback() {
                @Override
                public void onCompletion(RecordMetadata metadata, Exception exception) {
                    // executes every time a record is successfully sent or exception is thrown
                    if(exception == null){
                        // the record was successfully sent
                        log.info("Received new metadata/ \n" +
                                "Topic: /" + metadata.topic() + "\n" +
                                "Key: /" + producerRecord.key() + "\n" +
                                "Partition: /" + metadata.partition() + "\n" +
                                "Offset: /" + metadata.offset() + "\n" +
                                "Timestamp: /" + metadata.timestamp());
                    } else {
                        log.error("Error while producing messages", exception);
                    }
                }
            });

            try{
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }

        // flush and close producer - async op. Block here until all data is sent as above does not wait and goes to close program.
        producer.flush();
        producer.close();
    }
}
