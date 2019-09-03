## 理解mybatis中$与#

在mybatis中的$与#都是在sql中动态的传入参数。

例如 ```select id,name,age from student where name=#{name}``` 
这个name是动态的，可变的。当你传入什么样的值，就会根据你传入的值执行sql语句。

- `#{}` 解析为一个 JDBC 预编译语句（prepared statement）的参数标记符，一个 `#{}`被解析为一个参数占位符 。

- `${}` 仅仅为一个纯粹的 string 替换，在动态 SQL 解析阶段将会进行变量替换。替换后，在SQL中不含引号。

    传入一个不改变的字符串或者传入数据库字段(列名)，例如要传入`ORDER BY` 后边的参数。这种情况下必须使用 `${}`。

```sql
SELECT
	* 
FROM
	(
	SELECT
		A.*,
		ROWNUM RN 
	FROM
		TEST_STU A
    <if test = "sortField != null and sortField != ''" > 
	ORDER BY
		${sortField} ${sortOrder}
	</if> 
	) 
WHERE
	RN > #{pageIndex}*#{pageSize} 
	AND RN <= #{pageIndex}*#{pageSize}+#{pageSize}
```
---
### 综上

`#{}`方式一般用于传入字段值，并将该值作为字符串加到执行sql中，一定程度防止sql注入；

`${}`方式一般用于传入数据库对象，例如传入表名，不能防止sql注入，存在风险。

模糊查询中，如果使用如下方式：`select * from reason_detail where reason_en like '%${reason}%'`，
此处只能使用$，使用#的话，反而会被解析为列，报错`java.sql.SQLException: Column 'reason' not found`
