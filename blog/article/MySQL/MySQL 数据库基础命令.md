# MySQL 数据库基础命令

> 本文中尖括号 `<>` 表示占位符，方括号 `[]` 表示可选，而圆括号 `()` 则是 MySQL 语法的一部分。

## 数据库的操作命令

```sql
-- 创建数据库
CREATE DATABASE <数据库名>;

-- 删除数据库
DROP DATABASE <数据库名>;

-- 修改数据库
ALTER DATABASE <数据库名> MODIFY <字段> = <值>;

-- 使用数据库
USE <数据库名>;

-- 查看数据库中的所有表
SHOW TABLES;
```

例如：  

```sql
-- 修改数据库名称
ALTER DATABASE db_name MODIFY NAME = new_db_name;
```

## 授权命令

```sql
GRANT <操作列表> ON <数据库名>.<表名> TO '<用户名>'@'<主机>';
```

例如：  

```sql
-- 运行 user 用户操作 localhost 上的 db_name 数据库中的所有表
GRANT CREATE,ALTER,DROP,INDEX,SELECT,INSERT,UPDATE,DELETE ON db_name.* TO 'user'@'localhost';
```

## 表的操作命令

```sql
-- 创建表
CREATE TABLE [IF NOT EXISTS] <表名> (
    <列名1> <数据类型> [约束条件] [COMMENT '<注释>']
    <列名2> <数据类型> [约束条件] [COMMENT '<注释>']
    ...
    [PRIMARY KEY (<列名>)]                                  -- 主键
    [INDEX <索引名> (<列名>)]                               -- 索引
    [UNIQUE (<列名>)]                                       -- 唯一约束
    [FOREIGN KEY (<列名>) REFERENCES <其它表>(<列名>)]      -- 外键约束
)

-- 删除表
DROP TABLE [IF EXISTS] <表名>;

-- 修改表名
ALTER TABLE <原表名> RENAME TO <新表名>;
RENAME TABLE <原表名> TO <新表名>;

-- 查看表结构
DESC <表名>；
SHOW CREATE TABLE <表名>;
SHOW COLUMNS FROM <表名>;
SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '<表名>';

-- 查看表的状态
SHOW TABLE STATUS WHERE name='<表名>';
```

## 数据的增删改查

```sql
-- 插入数据
INSERT INTO <表名> (<列名1>, <列名2>, ...) VALUES 
(<值1>, <值2>, ...) 
[ , (<值1>, <值2>, ...), ... ];

-- 查询数据
SELECT <列名1>, <列名2>, ... FROM <表名> 
[ WHERE <条件> ]             
[ ORDER BY <列名> [DESC] ]  -- 排序
[ LIMIT <数量> ]            -- 分页
[ LIMIT <偏移量> ]
[ GROUP BY <列名> ];        -- 分组

-- 更新数据
UPDATE <表名> SET 
<列名1>=<值1>
[ , <列名2>=<值2>, ... ]
[ WHERE <条件> ];

-- 删除数据
DELETE FROM <表名> [ WHERE <条件> ];
```


## 事务

```sql
-- 开始事务
START TRANSACTION;

-- 提交事务
COMMIT；

-- 回滚事务
ROLLBACK；
```