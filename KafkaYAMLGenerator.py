import uuid
import copy

class KafkaNode():
    '''A class that generates YAML for broker and controller.
    Keyword Arguments:
    broker_nodeName:
    broker_image:
    broker_hostname:
    broker_container_name:
    broker_port:
    broker_protocol:

    CLUSTER_ID: Replace CLUSTER_ID with a unique base64 UUID using "bin/kafka-storage.sh random-uuid"
        See https://docs.confluent.io/kafka/operations-tools/kafka-tools.html#kafka-storage-sh

    KAFKA_CONTROLLER_LISTENER_NAMES: defines what interfaces, ports and associated security protocols Kafka will use to listen for client and controller connections. 
        The listener setting format is <LISTENERNAME or PROTOCOL>://<HOSTNAME>:<PORT>.
    KAFKA_ADVERTISED_LISTENERS: contains all listeners used by clients. A node that is only for a controller does not define advertised.listeners so validation for that needs to be removed.
    KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND:
    KAFKA_AUTHORIZER_CLASS_NAME:
    KAFKA_BROKER_ID:
    KAFKA_CONTROLLER_LISTENER_NAMES:
    KAFKA_CONTROLLER_QUORUM_VOTERS: specifies the minimum number of active voters needed to form a valid controller quorum. A valid controller quorum ensures that there are enough active controllers
        to maintain the availability and fault tolerance of the Kafka cluster. If the number of active voters falls below the specified value, the cluster may experience disruptions or become unavailable. 
        Values have to be put in the following order: {id}@{host}:{port}. Any other roles set to controllers, can be listed here.
    KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS:
    KAFKA_INTER_BROKER_LISTENER_NAME: brokers communicate between themselves usually on internal network. The IP must be accessible between brokers.
    KAFKA_JMX_HOSTNAME:
    KAFKA_JMX_PORT:
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP:
    KAFKA_LISTENERS: # define all exposed listeners
    KAFKA_LOG_DIRS:
    KAFKA_LOG4J_LOGGERS:
    KAFKA_NODE_ID: The property node.id replaces broker.id. Be sure that all identifiers in the cluster are unique across brokers and controllers. Used to specify a unique identifier of our node in the cluster.
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR:
    KAFKA_PROCESS_ROLES: A node can be both a broker or a controller. Set to broker,controller to enable both the controller and data planes on a node.
    KAFKA_TRANSACTION_STATE_LOG_MIN_ISR:
    KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR:
    KAFKA_ZOOKEEPER_CONNECT:

    '''

    DEFAULT_CONFIG = {
        'nodeName': '',
        'image': '',
        'hostname': '',
        'container_name': '',
        'port': '',
        'protocol': '',

        'CLUSTER_ID': '',
        'KAFKA_CONTROLLER_LISTENER_NAMES': '',
        'KAFKA_ADVERTISED_LISTENERS': '',
        'KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND': '',
        'KAFKA_AUTHORIZER_CLASS_NAME': '',
        'KAFKA_BROKER_ID': '',
        'KAFKA_CONTROLLER_LISTENER_NAMES': '',
        'KAFKA_CONTROLLER_QUORUM_VOTERS': '',
        'KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS': '',
        'KAFKA_INTER_BROKER_LISTENER_NAME': '',
        'KAFKA_JMX_HOSTNAME': 'localhost',
        'KAFKA_JMX_PORT': '',
        'KAFKA_LISTENER_SECURITY_PROTOCOL_MAP': '',
        'KAFKA_LISTENERS': '',
        'KAFKA_LOG_DIRS': '/tmp/kraft-combined-logs',
        'KAFKA_LOG4J_LOGGERS': '',
        'KAFKA_NODE_ID': '',
        'KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR': '',
        'KAFKA_PROCESS_ROLES': '',
        'KAFKA_TRANSACTION_STATE_LOG_MIN_ISR': '',
        'KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR': '',
        'KAFKA_ZOOKEEPER_CONNECT': ''
    }

    def __init__(self, **configs) -> None:
        self.config = copy.copy(self.DEFAULT_CONFIG)
        for key in self.config:
            if key in configs:
                self.config[key] = configs.pop(key)
        
'''
KAFKA_CONTROLLER_LISTENER_NAMES: controller_port[0].key(),
# defines what interfaces, ports and associated security protocols Kafka will use to listen for client and controller connections. 
# The listener setting format is <LISTENERNAME or PROTOCOL>://<HOSTNAME>:<PORT>.
# specifies the minimum number of active voters needed to form a valid controller quorum. A valid controller quorum ensures that there are enough active controllers to maintain the availability and fault tolerance of the Kafka cluster. 
# If the number of active voters falls below the specified value, the cluster may experience disruptions or become unavailable. Values have to be put in the following order: {id}@{host}:{port}.
# any other roles set to controllers, can be listed here
KAFKA_CONTROLLER_QUORUM_VOTERS: nodeID + "@" + controller_hostname + ":" + "909"+nodeID,
KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL,
KAFKA_JMX_HOSTNAME: "",
KAFKA_JMX_PORT: 9102,
KAFKA_LISTENERS: controller_port[0].key() + "://" + controller_hostname + ":" + "909"+nodeID,
KAFKA_LOG_DIRS: /tmp/kraft-controller-logs,
# The property node.id replaces broker.id. Be sure that all identifiers in the cluster are unique across brokers and controllers.
KAFKA_NODE_ID: nodeID,
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: offsetTopicReplicationFactor,
# A node can be both a broker or a controller. Set to broker,controller to enable both the controller and data planes on a node.
KAFKA_PROCESS_ROLES: controller,
KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1,
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
# KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181,zoo2:2182,zoo3:2183",
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP : ,
# define all exposed listeners
KAFKA_LISTENERS : ,
# contains all listeners used by clients. A node that is only for a controller does not define advertised.listeners so validation for that needs to be removed.
KAFKA_ADVERTISED_LISTENERS : ,
KAFKA_CONTROLLER_LISTENER_NAMES : "CONTROLLER",
KAFKA_CONTROLLER_QUORUM_VOTERS : ,
KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS : 0,
KAFKA_INTER_BROKER_LISTENER_NAME : "INTERNAL",
KAFKA_JMX_HOSTNAME : "localhost",
KAFKA_JMX_PORT : 0,
KAFKA_LISTENERS : ,
KAFKA_LOG_DIRS : "",
# used to specify a unique identifier of our node in the cluster
KAFKA_NODE_ID : nodeID,
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR : offsetTopicReplicationFactor,
# if I understood, each node can become" a controller
KAFKA_PROCESS_ROLES : "broker,controller,
KAFKA_TRANSACTION_STATE_LOG_MIN_ISR : 0,
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR : 0,
KAFKA_BROKER_ID: 1,
# KAFKA_LOG4J_LOGGERS: kafka.controller:INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO,
# KAFKA_AUTHORIZER_CLASS_NAME: kafka.security.authorizer.AclAuthorizer,
# KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND: "true"
    }
'''


version = 3
tag = "7.4.0"
cp_broker_image = f'confluentinc/cp-server:{0}', tag
nodeID = 1
offsetTopicReplicationFactor = 1
clusterID = uuid.uuid4()

# CONTROLLER BROKER
# This node is kept internally, hence it is not exposed
controller = 1
controller_nodeName = 'controller'
controller_image = cp_image
controller_hostname = controller_nodeName
controller_container_name = 'conf_controller'
controller_port = {'CONTROLLER': "909"+nodeID}
controller_protocol = 'PLAINTEXT'

ctrl = 1
controllerQuorumVoters = ''
for ctrl in range(1,ctrl):
    name = (f"controller-{0}",ctrl)
    controllerQuorumVoters = controllerQuorumVoters+(f"{0}@name:9093,")
    pass


brokers = 1

for brk in range(brokers, ctrl+brokers):
    name = (f"broker-{0}",brk)
    kn = KafkaNode( nodeName = name,
                    image = cp_broker_image,
                    hostname = name,
                    container_name = name,
                    port = 1,
                    protocol = 'PLAINTEXT',
                    CLUSTER_ID = clusterID,
                    KAFKA_PROCESS_ROLES = 'broker',
                    KAFKA_ADVERTISED_LISTENERS = {'INTERNAL': (f"{0}:9092", name), 'EXTERNAL': (f"localhost:{0}9092", brk)},
                    KAFKA_LISTENERS = '',
                    KAFKA_INTER_BROKER_LISTENER_NAME = 'INTERNAL',
                    KAFKA_CONTROLLER_QUORUM_VOTERS = controllerQuorumVoters,
                    KAFKA_MIN_INSYNC_REPLICAS = brokers
                    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
                    KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 1000
                    KAFKA_DEFAULT_REPLICATION_FACTOR: 3
                    
      
      KAFKA_CONTROLLER_LISTENER_NAMES: 'CONTROLLER'
               )
    











# NETWORK
networks = 1
compose_networks = {"networks": {"kafka_network" : {"driver" : "bridge"}}}







# increment number of brokers
nodeID += 1




broker_env['KAFKA_ADVERTISED_LISTENERS'] = {k:f"//{0}{1}:{2}"broker_hostname,k.index,index+v} for k, v in broker_port.items()
broker_env['KAFKA_LISTENER_SECURITY_PROTOCOL_MAP'] = {k:f"//{0}:{1}" broker_protocol} for k in broker_port.items()

# compose broker definition
compose_broker = {}

for brk in brokers:
    nodeName = f"{0}{1}",brk,brk.index
    broker_compose[nodeName] = {
        broker_image,
        broker_hostname,
        broker_container_name,
        broker_env        
    }

if ports:

if controller:
    broker_dependsOn

if networks:
    compose_controller['networks'] = compose_networks

# increment number of brokers
nodeID += 1

# SCHEMA REGISTRY
schemaReg = 1
schemaReg_nodeName = 'schemaRegistry'
schemaReg_image =  f"confluentinc/cp-schema-registry:{0}", tag
schemaReg_hostname = 'schemaRegistry'
schemaReg_container_name = 'conf_schemaRegistry'
schemaReg_port = "8081"

# SCHEMA REGISTRY ENV
schemaReg_env = {
    "SCHEMA_REGISTRY_HOST_NAME": schemaReg_hostname,
    "SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS": 'broker:29092',
    "SCHEMA_REGISTRY_LISTENERS": "http://:"+schemaReg_port,
}


# CONNECT
connect = 1
connect_nodeName = 'connect'
connect_image =  "cnfldemos/cp-server-connect-datagen:0.5.3-7.1.0"
connect_hostname = 'connect'
connect_container_name = 'conf_connect'
port = "8083"

# CONNECT ENV
connect_env = {
    "CONNECT_BOOTSTRAP_SERVERS": "'broker:29092'",
    "CONNECT_REST_ADVERTISED_HOST_NAME": connect_nodeName,
    "CONNECT_GROUP_ID": "compose-connect-group",
    "CONNECT_CONFIG_STORAGE_TOPIC": "docker-connect-configs",
    "CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR": "1",
    "CONNECT_OFFSET_FLUSH_INTERVAL_MS": "10000",
    "CONNECT_OFFSET_STORAGE_TOPIC": "docker-connect-offsets",
    "CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR": "1",
    "CONNECT_STATUS_STORAGE_TOPIC": "docker-connect-status",
    "CONNECT_STATUS_STORAGE_REPLICATION_FACTOR": "1",
    "CONNECT_KEY_CONVERTER": "org.apache.kafka.connect.storage.StringConverter",
    "CONNECT_VALUE_CONVERTER": "io.confluent.connect.avro.AvroConverter",
    "CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL": "http://" + schemaReg_hostname + ":" + schemaReg_port,
    # CLASSPATH required due to CC-2422
    "CLASSPATH": "/usr/share/java/monitoring-interceptors/monitoring-interceptors-7.4.0.jar",
    "CONNECT_PRODUCER_INTERCEPTOR_CLASSES": "io.confluent.monitoring.clients.interceptor.MonitoringProducerInterceptor",
    "CONNECT_CONSUMER_INTERCEPTOR_CLASSES": "io.confluent.monitoring.clients.interceptor.MonitoringConsumerInterceptor",
    "CONNECT_PLUGIN_PATH": "/usr/share/java,/usr/share/confluent-hub-components",
    "CONNECT_LOG4J_LOGGERS": "org.apache.zookeeper=ERROR,org.I0Itec.zkclient=ERROR,org.reflections=ERROR",
}

if controller:

if brokers:

if schemaReg:

# CONTROL CENTER
  # Control Center is a web-based tool for managing and monitoring Apache Kafka

controlCenter_nodeName = 'controllerCenter'
controlCenter_image = f"confluentinc/cp-enterprise-control-center:{0}", tag
controlCenter_hostname = 'controllerCenter'
controlCenter_container_name = 'conf_controllerCenter'
controlCenter_port = "9021"

controlCenter_env = {
   
  
    depends_on:
      - broker
      - controller
      - schema-registry
      - connect
      - ksqldb-server
    ports:
      - "9021:9021"
    environment:
      CONTROL_CENTER_BOOTSTRAP_SERVERS: 'broker:29092'
      CONTROL_CENTER_CONNECT_CONNECT-DEFAULT_CLUSTER: 'connect:8083'
      CONTROL_CENTER_KSQL_KSQLDB1_URL: "http://ksqldb-server:8088"
      CONTROL_CENTER_KSQL_KSQLDB1_ADVERTISED_URL: "http://localhost:8088"
      CONTROL_CENTER_SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      CONTROL_CENTER_REPLICATION_FACTOR: 1
      CONTROL_CENTER_INTERNAL_TOPICS_PARTITIONS: 1
      CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS: 1
      CONFLUENT_METRICS_TOPIC_REPLICATION: 1
      PORT: 9021


if controller:
    broker_dependsOn

for brk in brokers:
      
if schemaRegistry:

if connect:

if ksqldb-server:

if networks:
    broker_networks













# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CONTROLLER BROKER
# This node is kept internally, hence it is not exposed
controller = 1
controller_nodeName = 'controller'
controller_image = cp_image
controller_hostname = controller_nodeName
controller_container_name = 'conf_controller'
controller_port = {'CONTROLLER': "909"+nodeID}
controller_protocol = 'PLAINTEXT'

controller_env = {
      # Replace CLUSTER_ID with a unique base64 UUID using "bin/kafka-storage.sh random-uuid"
      # See https://docs.confluent.io/kafka/operations-tools/kafka-tools.html#kafka-storage-sh
      'CLUSTER_ID': clusterID,
      # defines what interfaces, ports and associated security protocols Kafka will use to listen for client and controller connections. 
      # The listener setting format is <LISTENERNAME or PROTOCOL>://<HOSTNAME>:<PORT>.
      'KAFKA_CONTROLLER_LISTENER_NAMES': controller_port[0].key(),
      # specifies the minimum number of active voters needed to form a valid controller quorum. A valid controller quorum ensures that there are enough active controllers to maintain the availability and fault tolerance of the Kafka cluster. 
      # If the number of active voters falls below the specified value, the cluster may experience disruptions or become unavailable. Values have to be put in the following order: {id}@{host}:{port}.
      # any other roles set to controllers, can be listed here
      'KAFKA_CONTROLLER_QUORUM_VOTERS': nodeID + "@" + controller_hostname + ":" + "909"+nodeID,
      'KAFKA_INTER_BROKER_LISTENER_NAME': 'INTERNAL',
      'KAFKA_JMX_HOSTNAME': "localhost",
      'KAFKA_JMX_PORT': 9102,
      'KAFKA_LISTENERS': controller_port[0].key() + "://" + controller_hostname + ":" + "909"+nodeID,
      'KAFKA_LOG_DIRS': '/tmp/kraft-controller-logs',
      # The property node.id replaces broker.id. Be sure that all identifiers in the cluster are unique across brokers and controllers.
      'KAFKA_NODE_ID': nodeID,
      'KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR': offsetTopicReplicationFactor,
      # A node can be both a broker or a controller. Set to broker,controller to enable both the controller and data planes on a node.
      'KAFKA_PROCESS_ROLES': 'controller',
      'KAFKA_TRANSACTION_STATE_LOG_MIN_ISR': 1,
      'KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR': 1
}

compose_controller = {}

if networks:
    compose_controller['networks'] = compose_networks

# increment number of brokers
nodeID += 1

# BROKER
# - PORTS	  	 
# Interbroker listener              - 9091 	Yes (internal topic replication only, so you should only allow traffic within the VPC, preferably only from the brokers)
# External PLAINTEXT listener 	    - 9092 	No 
# External TLS listener      	    - 9092 	No 
# Metadata Service (MDS)            - 8090 	No
# Confluent Server REST API         - 8090 	No
# Jolokia [*]                       - 7771 	No

brokers = 3
broker_nodeName = 'broker'
broker_image = cp_image
broker_hostname = broker_nodeName
broker_container_name = 'conf_broker'
broker_port = {'INTERNAL': "909"+nodeID, 'EXTERNAL_SAME_HOST': nodeID+"909"+nodeID, 'EXTERNAL_DIFFERENT_HOST': "909"+nodeID}
broker_protocol = 'PLAINTEXT'

# BROKER ENV
broker_env = {
    'CLUSTER_ID' : '',

    # 'KAFKA_ZOOKEEPER_CONNECT': "zoo1:2181,zoo2:2182,zoo3:2183",
    'KAFKA_LISTENER_SECURITY_PROTOCOL_MAP' : '',
    # define all exposed listeners
    'KAFKA_LISTENERS' : '',
    # contains all listeners used by clients. A node that is only for a controller does not define advertised.listeners so validation for that needs to be removed.
    'KAFKA_ADVERTISED_LISTENERS' : '',
    'KAFKA_CONTROLLER_LISTENER_NAMES' : 'CONTROLLER',
    'KAFKA_CONTROLLER_QUORUM_VOTERS' : '',
    'KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS' : 0,
    'KAFKA_INTER_BROKER_LISTENER_NAME' : 'INTERNAL',
    'KAFKA_JMX_HOSTNAME' : 'localhost',
    'KAFKA_JMX_PORT' : 0,
    'KAFKA_LISTENERS' : '',
    'KAFKA_LOG_DIRS' : '/tmp/kraft-combined-logs',
    # used to specify a unique identifier of our node in the cluster
    'KAFKA_NODE_ID' : nodeID,
    'KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR' : offsetTopicReplicationFactor,
    # if I understood, each node can become a controller
    'KAFKA_PROCESS_ROLES' : 'broker,controller',
    'KAFKA_TRANSACTION_STATE_LOG_MIN_ISR' : 0,
    'KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR' : 0,
    'KAFKA_BROKER_ID': 1,
    # 'KAFKA_LOG4J_LOGGERS': 'kafka.controller:INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO',
    # 'KAFKA_AUTHORIZER_CLASS_NAME': 'kafka.security.authorizer.AclAuthorizer',
    # 'KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND': "true"
}

broker_env['KAFKA_ADVERTISED_LISTENERS'] = {k:f"//{0}{1}:{2}"broker_hostname,k.index,index+v} for k, v in broker_port.items()
broker_env['KAFKA_LISTENER_SECURITY_PROTOCOL_MAP'] = {k:f"//{0}:{1}" broker_protocol} for k in broker_port.items()

# compose broker definition
compose_broker = {}

for brk in brokers:
    nodeName = f"{0}{1}",brk,brk.index
    broker_compose[nodeName] = {
        broker_image,
        broker_hostname,
        broker_container_name,
        broker_env        
    }

if ports:

if controller:
    broker_dependsOn

if networks:
    compose_controller['networks'] = compose_networks

# increment number of brokers
nodeID += 1

# SCHEMA REGISTRY
schemaReg = 1
schemaReg_nodeName = 'schemaRegistry'
schemaReg_image =  f"confluentinc/cp-schema-registry:{0}", tag
schemaReg_hostname = 'schemaRegistry'
schemaReg_container_name = 'conf_schemaRegistry'
schemaReg_port = "8081"

# SCHEMA REGISTRY ENV
schemaReg_env = {
    "SCHEMA_REGISTRY_HOST_NAME": schemaReg_hostname,
    "SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS": 'broker:29092',
    "SCHEMA_REGISTRY_LISTENERS": "http://:"+schemaReg_port,
}


# CONNECT
connect = 1
connect_nodeName = 'connect'
connect_image =  "cnfldemos/cp-server-connect-datagen:0.5.3-7.1.0"
connect_hostname = 'connect'
connect_container_name = 'conf_connect'
port = "8083"

# CONNECT ENV
connect_env = {
    "CONNECT_BOOTSTRAP_SERVERS": "'broker:29092'",
    "CONNECT_REST_ADVERTISED_HOST_NAME": connect_nodeName,
    "CONNECT_GROUP_ID": "compose-connect-group",
    "CONNECT_CONFIG_STORAGE_TOPIC": "docker-connect-configs",
    "CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR": "1",
    "CONNECT_OFFSET_FLUSH_INTERVAL_MS": "10000",
    "CONNECT_OFFSET_STORAGE_TOPIC": "docker-connect-offsets",
    "CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR": "1",
    "CONNECT_STATUS_STORAGE_TOPIC": "docker-connect-status",
    "CONNECT_STATUS_STORAGE_REPLICATION_FACTOR": "1",
    "CONNECT_KEY_CONVERTER": "org.apache.kafka.connect.storage.StringConverter",
    "CONNECT_VALUE_CONVERTER": "io.confluent.connect.avro.AvroConverter",
    "CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL": "http://" + schemaReg_hostname + ":" + schemaReg_port,
    # CLASSPATH required due to CC-2422
    "CLASSPATH": "/usr/share/java/monitoring-interceptors/monitoring-interceptors-7.4.0.jar",
    "CONNECT_PRODUCER_INTERCEPTOR_CLASSES": "io.confluent.monitoring.clients.interceptor.MonitoringProducerInterceptor",
    "CONNECT_CONSUMER_INTERCEPTOR_CLASSES": "io.confluent.monitoring.clients.interceptor.MonitoringConsumerInterceptor",
    "CONNECT_PLUGIN_PATH": "/usr/share/java,/usr/share/confluent-hub-components",
    "CONNECT_LOG4J_LOGGERS": "org.apache.zookeeper=ERROR,org.I0Itec.zkclient=ERROR,org.reflections=ERROR",
}

if controller:

if brokers:

if schemaReg:

# CONTROL CENTER
  # Control Center is a web-based tool for managing and monitoring Apache Kafka

controlCenter_nodeName = 'controllerCenter'
controlCenter_image = f"confluentinc/cp-enterprise-control-center:{0}", tag
controlCenter_hostname = 'controllerCenter'
controlCenter_container_name = 'conf_controllerCenter'
controlCenter_port = "9021"

controlCenter_env = {
   
  
    depends_on:
      - broker
      - controller
      - schema-registry
      - connect
      - ksqldb-server
    ports:
      - "9021:9021"
    environment:
      CONTROL_CENTER_BOOTSTRAP_SERVERS: 'broker:29092'
      CONTROL_CENTER_CONNECT_CONNECT-DEFAULT_CLUSTER: 'connect:8083'
      CONTROL_CENTER_KSQL_KSQLDB1_URL: "http://ksqldb-server:8088"
      CONTROL_CENTER_KSQL_KSQLDB1_ADVERTISED_URL: "http://localhost:8088"
      CONTROL_CENTER_SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      CONTROL_CENTER_REPLICATION_FACTOR: 1
      CONTROL_CENTER_INTERNAL_TOPICS_PARTITIONS: 1
      CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS: 1
      CONFLUENT_METRICS_TOPIC_REPLICATION: 1
      PORT: 9021


if controller:
    broker_dependsOn

for brk in brokers:
      
if schemaRegistry:

if connect:

if ksqldb-server:

if networks:
    broker_networks

# REST PROXY

# KSQLDB SERVER

# KSQLDB CLI

# KSQLDB DATAGEN


output = {}
services = {}


output['version'] = version
output['services'] = services
output.add(broker_compose)
