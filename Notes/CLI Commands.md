# CLI Commands
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

> kafka-console-producer --topic Test1 --broker-list localhost:9092
> kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first_topic

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
> kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic


*This will pull all messages from all partitions, loosing order of how the producer actually sent the messages*
> kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic --from-beginning --property print.partition=true

*Consumer with more infomration*
> kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic --from-beginning --formatter kafka.tools.DefaultMessageFormatter --property print.timestamp=true --property print.key=true --property print.value=true
> ... offset latest --partition 0 ...
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
<img src="Pics/Fig M.png">

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

> kafkacat
> tcpdump


|GROUP                   | TOPIC       | PARTITION | NEW-OFFSET |
|------------------------|:------------|:----------|:-----------|
|my-first-consumer-group | first_topic | 0         | 0          |
|my-first-consumer-group | first_topic | 1         | 0          |
|my-first-consumer-group | first_topic | 2         | 112 |


## Getting Started with IntelliJ
Video 44

Ctrl + click on object reveals definition.

Ctrl + p reveals constructor args.

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
