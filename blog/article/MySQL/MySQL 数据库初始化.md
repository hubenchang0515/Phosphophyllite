# MySQL 数据库初始化

首先通过root进行免密登录: 

```bash
sudo mysql
```

```sql
CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
CREATE DATABASE <database>;
GRANT CREATE,ALTER,DROP,INDEX,SELECT,INSERT,UPDATE,DELETE ON <database>.* TO 'planc'@'localhost';
```

## 修改密码

```
ALTER USER '<username>'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>';
```