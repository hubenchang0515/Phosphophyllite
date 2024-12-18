# Kafka 部分常用配置

Kafka 有两种使用方式：基于 zookeeper 和基于 kraft.

* 基于 zookeeper

启动:  
```bash
./bin/zookeeper-server-start.sh ./config/zookeeper.properties
./bin/kafka-server-start.sh ./config/server.properties
```

* 基于 kraft

初始化: 

```bash
$ ./bin/kafka-storage.sh random-uuid
j5aJA66HT-uI4aMHcmfTsg
$ ./bin/kafka-storage.sh format -t j5aJA66HT-uI4aMHcmfTsg -c ./config/kraft/server.properties 
Formatting /tmp/kraft-combined-logs with metadata.version 3.4-IV0.
```

启动:  

```bash
./bin/kafka-server-start.sh ./config/kcraft/server.properties
```

它们使用不同的配置文件，因此下述配置要写在对应的配置文件中

## 最大消息尺寸

Kafka 默认一个消息最大 1MB，如果要收发更大的消息，需要对 Producer、Broker 和 Consumer 都进行配置。

生产者需要在代码中配置 `message.max.bytes`，表所最大可以发送的消息尺寸:  

```c++
conf->set("message.max.bytes", "10485760", errstr);
```

消费者需要在代码中配置 `fetch.message.max.bytes`，表示最大可以接收的消息尺寸:  

```c++
conf->set("fetch.message.max.bytes", "10240000", errstr);
```

Broker 需要在 `server.properties` 中配置 `message.max.bytes` 和 `replica.fetch.max.bytes`:

```ini
message.max.bytes=10485760        # 消息最大尺寸 10 MiB
replica.fetch.max.bytes=10485760  # 副本最大尺寸 10 MiB
```

## 会话超时时间

Kafka 限制每个消费者组中不同的消费者不能同时消费同一个 Topic。
如果消费者没有正确退出连接（例如进程崩溃），在超时之前，Kafka 会认为该消费者仍然在线。
此时程序重启将无法消费相同的 Topic，必须等到超时之后，Kafka 认为之前的消费者已经退出再重启。

Broker 需要在 `server.properties` 中配置 `group.min.session.timeout.ms` 和 group.max.session.timeout.ms表示超时时间和有效范围。
```ini
group.min.session.timeout.ms=100
group.max.session.timeout.ms=100000
```

消费者需要在代码中配置 `session.timeout.ms`，表示超时时间:  

```c++
conf->set("session.timeout.ms", "1000", errstr);
```


## 最大保留容量和最大保留时间

Kafka 会在 `/tmp` 目录中持久化保留消息，磁盘写满后将无法工作，可以配置最大缓存容量和最大缓存时间来解决这一问题。

```init
log.retention.bytes=1073741824          # 最大缓存容量 1 GiB
log.retention.hours=1                   # 最大缓存时间 1 小时
log.retention.check.interval.ms=300000  # 检查间隔时间 5 分钟
```

> Kafka 将每 5 分钟检查一次，如果此时保留容量或保留时间超出配置，则删除数据。在检查之前仍有超出容量的可能，此时可以减少间隔。