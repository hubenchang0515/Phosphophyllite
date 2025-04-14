# MySQL 数据库初始化

## 创建用户

首先通过root进行免密登录: 

```bash
sudo mysql
```

```sql
CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
```

## 创建数据库并设置权限

```sql
CREATE DATABASE <database>;
GRANT CREATE,ALTER,DROP,INDEX,SELECT,INSERT,UPDATE,DELETE ON <database>.* TO '<username>'@'localhost';
```

## 修改用户密码

```
ALTER USER '<username>'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>';
```