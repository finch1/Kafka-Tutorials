
<img width="1000" src="Fig R.png">

For network efficiency, messages are written to Kafka in batches, i.e. a collection of messages all of which are being produced to the same topic and partition. Observe the tradeoff between latency and throughput: the larger the batch, the more messages can be handled per unit time, but the longer it takes an individual message to propagate. Compressing messages mitigates data transfer efficiency and storage. 

By using well-defined schemas, and storing them in a common repository, the messages in Kafka can be understood between pub and sub without coordination. Messages are appended as read only in order of entry. Topics have multiple partitions and message order is not guaranteed in entire topic. Each partition can be hosted on a different server =  a topic can be scaled horizontally across multiple servers. Additionally partitions can be replicated across different servers. 

<img width="1000" src="Fig S.png">

The producer generates a message to a specific topic. By default, the producer will balance messages over all partitions of a topic evenly. A producer can direct messages to a specific partition using message key. Consumers subscribe to one or more topics and reads messages in the order produced to each partition. Consumers keep track of consumed messages by offset. Consumers can stop and restart as Kafka keeps track of the incrementing offsets. 

**Consumer group**  is one ore more consumers that work together to consume a topic. The group ensures that each partition is only consumed by one member. The mapping of a consumer to a partition is often called **ownership**. If a single consumer fails, partitions a reassigned.

<img src="Fig T.png">

A single Kafka server is called a broker. Messages are received from producers, assigned offset and stored to disk. Brokers are designed to operate as part of a **cluster**, where one broker functions as the controller by election. This controller is responsible for admin ops: assigning partitions to brokers and monitoring for broker failures. A partition is owned by one leader in a broker. Replication is assigned to additional brokers called **followers** of the partition. message retention is either by period or storage limit, messages expire and get deleted thereafter. Or also by key, keeping only the latest one. Consumers can reset offset and start reading from beginning. 

## Kafka Topics
*Topics* are a particular *stream* of data. Topics are identified by their *names*. The *sequence* of messages are called streams. Topics cannot be *queried*.
Topics are *immutable*. Once data is written to a partition, it cannot be changed.
Data is only *kept* for a default of one week, and is also configurable.

## Partitions and Offsets
Topics are split in *partitions*. *Messages* in each partition are *ordered* and given an incremental *offset* value.
Offsets only have a *meaning* in the partition and so order is only guaranteed in that partition. The same sequence is used across all partitions.
Offsets are not reused once message is *removed*. Similar to table PK. 
Data is randomly assigned to the topic's paritions, unless a key is provided.

<img src="Fig A.png">

## Producers
Producers know in advance to which partition to write to. It is not something that Kafka decides.
In case of failure, Kafka and Producers help with recovery.

- Producers may choose to send a key with the message (string, num, binary, etc)
- All messages with that key will be routed to the same partition.
- A key is typically sent to pserve order. Ex. messages by individual truck.
- Round Robin -> Data is distributed across all partitions in a topic.
- Key Based Ordering -> When we specify a key, then the same key is going to end up in the same partition

<img src="Fig C.png">

## Message
<img src="Fig D.png">

## Message Serializer
Kafka only accepts bytes as an input from producers and sends bytes out to consumers. This means some code needs to prepare data in bytes for Kafka.
Message serialization means transforming data/objects into bytes.

<img src="Fig E.png">

## Kafka message Key Hasshing
A Kafka partitioner is a code logic that takes a record and determines to which partition to send it into.

<img src="Fig F.png">

## Consumers
Consumers request data from Kafka. They read/pull data from a topic (identified by name).
Consumers automatically know which broker to read from.
In case of failures, consumers know how to recover.
Data is read in order from low to high offset, **within each partition**. Even when a couple of partitions are read by the same consumer, order is only for the part.

<img src="Fig G.png">

## Consumer Deserializer
Consumers transform serial byte data into objects
Consumers must know in advance the format of the message. Ex. if Key is Int, then use an Int Deserializer.
Topic format must never change, other wise stream shall corrupt. 

<img src="Fig H.png">

## Consumer Groups
Consumer groups are a bunch of consumers grouped together for a purpose:
- The same partition cannot be read by different consumers in the same group / two consumers in the same group cannot read the same partiton.
- Internally, Kafka keeps track of __consumer_offset per group.
- One consumer in one group can read from one or multiple partitions.
- Ex. one consumer group for the raw storage. Another group for real time risk detection.

<img src="Fig I.png">

## Delivery Semantics of Consumers
- By default, Java consumers will automatically commit offsets (at least once)
- At least once:
- - Offsets are commited after the message is processed
- - If the processing goes wrong, the message will be read again
- At most once:
- - Offsets are commited as messages are received
- Exactly once:
- - For Kafka -> Kafka workflows (from topic to topic): use Transactional API (Kafka Streams API)

## Kafka Cluster
A cluster is a group of multiple brokers. Where a broker is a server/node. Brokers receive and send data.
A broker is identified with an integer ID. 
Each broker will contain certain topic partitions.
Brokers are self identifiable to the clusters, it is only necessary to connect to one broker.
Same topic can be distributed/scaled across different brokers/servers

<img src="Fig J.png">

## Topic Replication Factor
Replication should be set to at least 2 or 3. In case of failure, systems can keep functioning.
At any one time, only ONE broker can be a leader for a given partition.
Producers can only send data to the broker that is leader of that partition.
If data is replicated fast enough, this is called *In Sync Replica*.
Kafka now allows consumers to read from a replica, perhaps its closer to the consumer.

<img src="Fig K.png">

## Partition Acknoledgements
Producers can choose to receive ack for data writes:
acks0 = Producers won't wait for acks (potential data loss)
acks1 = Producers will wait for leader acks (few data loss)
acksAll = Producers will wait for leader and replica acks (no data loss)

## Installin Kafk on Ub
Following Vid 23, 32:
- Downloaded latest version of Kafka from website. Followed CLI instructions from Kafka website.
- Followed this link to fix user permission error: https://www.tecmint.com/fix-user-is-not-in-the-sudoers-file-the-incident-will-be-reported-ubuntu/
- Installed Java Corretto from AWS website. This has more cloud oriented features then the Oracle version.
- Restart after adding PATH of kafka dir

*config/server.properties has path to LOGS*

Followed to copy paste bidir:
- https://linuxhint.com/enable-copy-paste-virtualbox-host/
- right CTRL + Home for drop down menu to mount image
- to find the installation media: vboxuser@Ubuntu:/media/vboxuser/VBox_GAs_7.0.4$ 
- to install the media: vboxuser@Ubuntu:/media/vboxuser/VBox_GAs_7.0.4$ sudo sh VBoxLinuxAdditions.run

## CLI Commands
**Start Kafka** 
>kafka-server-start.sh ~/kafka_2.13-3.3.1/config/kraft/server.properties

**List Available Topics**
>kafka-topics.sh --bootstrap-server localhost:9092 --list

**Create Topic**
>kafka-topics.sh --bootstrap-server localhost:9092 --create --topic first_topic --partitions 3 --replication-factor 1

**Show Topic Information**
>kafka-topics.sh --bootstrap-server localhost:9092 --topic first_topic --describe

>kafka-topics.sh --bootstrap-server localhost:9092 --describe

**Delete Topic**
>kafka-topics.sh --bootstrap-server localhost:9092 --topic first_topic --delete

**Send Message as Producer without KEY**

*sending messages without a key means that messages will be written to all partitions*

>kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first_topic

- Hello World
- The Name Is White
- Kafka is easy
- Cltr+C

>kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first_topic --producer-property acks=all

**Send Message as Producer with KEY**
>kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first_topic --property parse.key=true --property key.separator=:
- example key:example value
- user_id_1234:user value

**Pulling messages as Consumer**

*This will read the very last offset.*
>kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic

*This will pull all messages from all partitions, loosing order of how the producer actually sent the messages*
>kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic --from-beginning

*Consumer with more infomration*
>kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic --from-beginning --formatter kafka.tools.DefaultMessageFormatter --property print.timestamp=true --property print.key=true --property print.value=true

**Specify Consumer Group**

*Messages from the same producer will be split to differenet consumers. Different allocated partitions will feed consumers seperatly. The use of consumer groups is to spread the reads.*
>kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic --group my-first-consumer-group

*pointing to the same topic with a different group name will pull the same messages at once*
>kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic --group my-second-consumer-group

**List Consumer Groups**
>kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

*Shows if any messages are lagging read. Entering the consumer command with group parameters, reads all the lagging messages.*
>kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-first-consumer-group


#### Kafka spreading the reads of first_topic between two consumers in the same group
<img src="Fig M.png">

**Resetting Offsets**
#### Before
| GROUP                   | TOPIC          | PARTITION | CURRENT-OFFSET | LOG-END-OFFSET | LAG | CONSUMER-ID | HOST | CLIENT-ID |
|-------------------------|:--------------:|----------:|----------------|:--------------:|----:|-------------|:----:|----------:|
| my-first-consumer-group | first_topic    | 0         | 0              | 0              | 0   | -           | -    | - |
| my-first-consumer-group | first_topic    | 1         | 4              | 4              | 0   | -           | -    | - |
| my-first-consumer-group | first_topic    | 2         | 117            | 117            | 0   | -           | -    | - |     

#### Command
>kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-first-consumer-group --reset-offsets --to-earliest --execute --topic first_topic

#### After
| GROUP                   | TOPIC       | PARTITION | NEW-OFFSET |    
|-------------------------|:-----------:|----------:|------------|
| my-first-consumer-group | first_topic | 0         | 0          |     
| my-first-consumer-group | first_topic | 1         | 0          |     
| my-first-consumer-group | first_topic | 2         | 0       |

Offset is reset for consumer group to read from beginning

We can reset by a number of shifts backwards. This shift happenes an all partitions. When consumers read again, data is sent from partitions randomly not one after the other. Again, data order is not preserved.

>kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-first-consumer-group --reset-offsets --shift-by -5 --execute --topic first_topic
>>[2022-12-11 08:31:40,111] WARN New offset (-5) is lower than earliest offset for topic partition first_topic-0. Value will be set to 0 (kafka.admin.ConsumerGroupCommand$)

>>[2022-12-11 08:31:40,111] WARN New offset (-1) is lower than earliest offset for topic partition first_topic-1. Value will be set to 0 (kafka.admin.ConsumerGroupCommand$)

|GROUP                   | TOPIC       | PARTITION | NEW-OFFSET |
|------------------------|:------------|:----------|:-----------|
|my-first-consumer-group | first_topic | 0         | 0          |
|my-first-consumer-group | first_topic | 1         | 0          |
|my-first-consumer-group | first_topic | 2         | 112 |

#### Getting Started with IntelliJ
Video 44

Ctrl + click on object reveals definition.

Ctrl + p reveals constructor args.

### Sticky Partitioner
<img src="Fig N.png">

### Sending with Key
<img src="Fig O.png">

### Consumer Group and Partition Rebalance
Whenever consumers join and leave groups, partitions are going to be reassigned. This is called rebalance.
Rebalance/reassignment also happenes when new partitions are added to a topic

- **Kafka Consumer**: partition.assignment.strategy
  - *(Eager Rebalance Type) RangeAssignor*: assign partitions on a per-topic bases (can lead to imbalance)
  - *(Eager Type) RoundRobin*: assign partitions across all topics in round-robin fashion, optimal balance
  - *(Eager Type) StickyAssignor*: balanced like RoundRobin, and then minimizes partition movements when consumer join/leaves group in order to minimize movements
  - *(Cooperative Rebalance Type) CooperativeStickyAssignor*: rebalance strategy is identical to Sticky Assignor but supports cooperative rebalances and therefore consumer can keep consuming from topic
  - *The default assignor is [RangeAssignor, CooperativeStickyAssignor]*: which will use the RangeAssignor by default, but allows upgrading to CooperativeStickyAssignor with just a single roling bounce that removes the range assignor from the list. 

  - **Kafka Connect**: Cooperative rebalance
  - **Kafka Streams**: StreamsPartitionAssignor

  <img src="Fig P.png">

<img src="Fig Q.png">

#### Static Group Membership
- By default, when a consumer leaves a group, its partitions are revoked and reassigned
- If it re-joins, it will have a new *member ID* and new partitions will be reassigned
- If one specifies the *group.instance.id* it makes the consumer a **static member**
- Upon leaving, the consumer has up to *session.timeout.ms* to join back and get back its partitions (else they will be re-assinged), without triggering a rebalance
- This is helpful when consumers maintain local state and cache

Kafka can aggregate a stream with KsqlDB and a consumer can subscribe to the results. 