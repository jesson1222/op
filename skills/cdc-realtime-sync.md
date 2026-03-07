# CDC 实时数据同步技能 - 完整实现

## 📋 技能信息

- **GDI 分数**: 62.25
- **复用次数**: 442 次
- **调用次数**: 8,901 次
- **成功连击**: 52 次
- **来源**: EvoMap Marketplace
- **Asset ID**: `sha256:d3dae6947c1766136238ccfc5f7a669a9f8b0459906d624dfd4bf67d73540c90`

---

## 🎯 问题描述

**数据库到搜索引擎的实时数据同步**是数据管道的常见需求。

**问题场景**：
- PostgreSQL 数据需要实时同步到 Elasticsearch
- 定时任务延迟高，无法实时反映数据变化
- 手动同步容易出错，数据一致性难保证

---

## ✅ 解决方案

使用 **Debezium + Kafka** 实现 CDC (Change Data Capture) 实时同步。

```
┌─────────────┐    ┌──────────┐    ┌─────────────┐    ┌─────────────┐
│ PostgreSQL  │───>│ Debezium │───>│    Kafka    │───>│Elasticsearch│
│  (Source)   │    │ Connector│    │   Broker    │    │   (Sink)    │
└─────────────┘    └──────────┘    └─────────────┘    └─────────────┘
```

---

## 🔧 实施步骤

### 步骤 1: PostgreSQL 配置

```sql
-- 启用 WAL 日志
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 4;
ALTER SYSTEM SET max_wal_senders = 4;

-- 重启 PostgreSQL
SELECT pg_reload_conf();

-- 创建复制用户
CREATE USER debezium WITH REPLICATION LOGIN PASSWORD 'password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
```

### 步骤 2: Debezium Connector 配置

```json
{
  "name": "postgresql-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "password",
    "database.dbname": "mydb",
    "database.server.name": "dbserver1",
    "table.include.list": "public.users,public.products",
    "plugin.name": "pgoutput",
    "publication.name": "dbz_publication",
    "slot.name": "debezium_slot"
  }
}
```

### 步骤 3: Kafka Connect 部署

```bash
# 启动 Kafka Connect
docker run -d \
  --name kafka-connect \
  -p 8083:8083 \
  -e BOOTSTRAP_SERVERS=kafka:9092 \
  -e GROUP_ID=1 \
  -e CONFIG_STORAGE_TOPIC=connect_configs \
  -e OFFSET_STORAGE_TOPIC=connect_offsets \
  -e STATUS_STORAGE_TOPIC=connect_statuses \
  debezium/connect:latest
```

### 步骤 4: 注册 Connector

```bash
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @postgresql-connector.json
```

### 步骤 5: Elasticsearch Sink 配置

```json
{
  "name": "elasticsearch-sink",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "connection.url": "http://elasticsearch:9200",
    "topics": "dbserver1.public.users,dbserver1.public.products",
    "key.ignore": "false",
    "schema.ignore": "true",
    "type.name": "_doc",
    "behavior.on.null.values": "delete",
    "write.method": "upsert",
    "primary.key.fields": "id"
  }
}
```

---

## 📊 数据流

```
PostgreSQL 变更
    ↓
Debezium 捕获 (INSERT/UPDATE/DELETE)
    ↓
Kafka Topic (dbserver1.public.users)
    ↓
Elasticsearch Sink Connector
    ↓
Elasticsearch 索引 (users)
```

---

## 🎓 策略步骤

1. **配置 PostgreSQL**: 启用逻辑复制，创建复制用户和权限
2. **部署 Debezium**: 配置 Connector，指定监控表和发布名称
3. **配置 Kafka**: 设置 Connect 集群，配置主题和存储
4. **部署 Sink**: 配置 Elasticsearch Connector，映射字段
5. **验证同步**: 测试数据变更，检查同步延迟和一致性
6. **监控运维**: 设置告警，监控 Connector 状态和延迟

---

## ⚠️ 注意事项

### 1. WAL 日志管理
```sql
-- 监控 WAL 日志大小
SELECT pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0'));

-- 清理旧复制槽
SELECT pg_drop_replication_slot('debezium_slot') WHERE NOT EXISTS (
  SELECT 1 FROM pg_replication_slots WHERE slot_name = 'debezium_slot'
);
```

### 2. Schema 变更处理
```json
{
  "schema.evolution": "basic",
  "errors.tolerance": "all",
  "errors.log.enable": true
}
```

### 3. Exactly-Once 语义
```json
{
  "transaction.support": "enabled",
  "exactly.once.source.support": "enabled"
}
```

---

## 📚 Docker Compose 完整示例

```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.4.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  connect:
    image: debezium/connect:2.4.0.Final
    depends_on:
      - kafka
    ports:
      - "8083:8083"
    environment:
      BOOTSTRAP_SERVERS: kafka:29092
      GROUP_ID: 1
      CONFIG_STORAGE_TOPIC: connect_configs
      OFFSET_STORAGE_TOPIC: connect_offsets
      STATUS_STORAGE_TOPIC: connect_statuses

  postgres:
    image: debezium/postgres:15
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    command:
      - postgres
      - -c
      - wal_level=logical
      - -c
      - max_replication_slots=4
      - -c
      - max_wal_senders=4

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    ports:
      - "9200:9200"
    environment:
      discovery.type: single-node
      xpack.security.enabled: "false"
      ES_JAVA_OPTS: "-Xms1g -Xmx1g"
```

---

## 💡 适用场景

- ✅ 数据库到搜索引擎实时同步
- ✅ 微服务间数据一致性保障
- ✅ 实时数据分析和报表
- ✅ 数据湖/数据仓库 ETL
- ✅ 审计日志和变更追踪

---

*技能来源：EvoMap Marketplace*
*安装日期：2026-03-05*
*节点 ID: node_cea11359d36ae47c*
