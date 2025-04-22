# MySQL 全文索引

全文索引是一种对文本进行全文搜索的索引，类似搜索引擎的反向索引，可以大幅提升全文搜索的速度。但同时也会对插入性能造成较大影响。


## 创建全文索引

创建表时创建全文索引:

```sql
CREATE TABLE articles (
    id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    FULLTEXT KEY idx_search (title, content)  /*!50100 WITH PARSER ngram */
) ENGINE=InnoDB;
```

单独创建全文索引:

```sql
ALTER TABLE articles ADD FULLTEXT KEY idx_search (title, content)  /*!50100 WITH PARSER ngram */;
```

> 这里的 `/*!50100 WITH PARSER ngram */` 表示 MySQL 版本 ≥ 5.1.00 是附加 `WITH PARSER ngram`。
>
> `ngram` 是一个中文分词器，如果没有它，将无法搜索中文.


## 通过全文索引进行搜索

自然搜索：

```sql
SELECT * FROM articles WHERE MATCH(title, body) AGAINST('搜索内容');
```

布尔搜索：

```sql
SELECT * FROM articles 
WHERE MATCH(title, body) AGAINST('+MySQL -Oracle' IN BOOLEAN MODE);
```

* `+MySQL` 表示必须包含完整单词 MySQL
* `-Oracle` 表示必须不包含完整单词 Oracle