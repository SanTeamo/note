## 连接函数

* 第一种 **`concat`**
```sql
SELECT * FROM TEST_STU WHERE NAME LIKE CONCAT(CONCAT('%','张'),'%')
```
* 第二种 **`||`**
```sql
SELECT * FROM TEST_STU WHERE NAME LIKE '%' || '张' || '%'
```

**在oracle中 concat不支持三个参数的 如 `concat('%','张','%')`**