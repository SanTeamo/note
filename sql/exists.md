# EXISTS
## 作用
EXISTS用于检查子查询是否至少会返回一行数据，该子查询实际上并不返回任何数据，而是返回值True或False

语法： EXISTS subquery

参数： subquery 是一个受限的 SELECT 语句 (不允许有 COMPUTE 子句和 INTO 关键字)。

结果类型： Boolean 如果子查询包含行，则返回 TRUE ，否则返回 FLASE 

EXIST强调的是是否返回结果集，不要求知道返回什么, 比如：
```sql
SELECT
	NAME 
FROM
	STUDENT 
WHERE
	SEX = 'm' 
	AND MARK EXISTS ( SELECT 1 FROM GRADE WHERE...)
```
只要exists引导的子句有结果集返回，那么exists这个条件就算成立了。返回的字段始终为1，如果改成“select 2 from grade where ...”，那么返回的字段就是2，这个数字没有意义。所以exists子句不在乎返回什么，而是在乎是不是有结果集返回。

## EXISTS与IN的区别

### IN
确定给定的值是否与子查询或列表中的值相匹配。in在查询的时候，首先查询子查询的表，然后将内表和外表做一个笛卡尔积，然后按照条件进行筛选。所以相对内表比较小的时候，in的速度较快。
```sql
SELECT
    *
FROM
    `user`
WHERE
    `user`.id IN (
        SELECT
            `order`.user_id
        FROM
            `order`
    )
```
首先，在数据库内部，查询子查询，执行如下代码：
```sql
SELECT
    `order`.user_id
FROM
    `order
```
此时，将查询到的结果和原有的user表做一个笛卡尔积，再根据
```user.id IN order.user_id```的条件，将结果进行筛选（即比较id列和user_id 列的值是否相等，将不相等的删除）。最后，得到符合条件的数据。

### EXISTS
指定一个子查询，检测行的存在。遍历循环外表，然后看外表中的记录有没有和内表的数据一样的。匹配上就将结果放入结果集中。
```sql
SELECT
    `user`.*
FROM
    `user`
WHERE
    EXISTS (
        SELECT
            `order`.user_id
        FROM
            `order`
        WHERE
            `user`.id = `order`.user_id
    )
```
这条sql语句的执行结果和上面的in的执行结果是一样的。
但是，不一样的是它们的执行流程完全不一样：

使用exists关键字进行查询的时候，首先，我们先查询的不是子查询的内容，而是查我们的主查询的表，也就是说，我们先执行的sql语句是：
```sql
SELECT `user`.* FROM `user` 
```
然后，根据表的每一条记录，执行以下语句，依次去判断where后面的条件是否成立：
```sql
EXISTS (
	SELECT
		`order`.user_id
	FROM
		`order`
	WHERE
		`user`.id = `order`.user_id
)
```
如果成立则返回true不成立则返回false。如果返回的是true的话，则该行结果保留，如果返回的是false的话，则删除该行，最后将得到的结果返回。

### 区别

如果子查询得出的结果集记录较少，主查询中的表较大且又有索引时应该用in, 反之如果外层的主查询记录较少，子查询中的表大，又有索引时使用exists。其实我们区分in和exists主要是造成了驱动顺序的改变(这是性能变化的关键)，如果是exists，那么以外层表为驱动表，先被访问，如果是IN，那么先执行子查询，所以我们会以驱动表的快速返回为目标，那么就会考虑到索引及结果集的关系了 ，另外IN时不对NULL进行处理。

in 是把外表和内表作hash 连接，而exists是对外表作loop循环，每次loop循环再对内表进行查询。一直以来认为exists比in效率高的说法是不准确的。