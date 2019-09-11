## Oracle数据库分页查询

* 物理分页使用**ROWNUM**，控制**ROMNUM**的范围来实现分页。
```sql
SELECT
	* 
FROM
	( SELECT a.*, ROWNUM RN FROM TEST_STU a ) 
WHERE
	( RN > 0 AND RN <= 10 )
```