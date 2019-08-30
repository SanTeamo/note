##1. HAVING vs WHERE
`WHERE` 的执行要优先于 `GROUP BY`，`HAVING` 的执行在 `GROUP BY` 之后

假设有一个表:
```
CREATE TABLE `table` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
 `value` int(10) unsigned NOT NULL,
 PRIMARY KEY (`id`),
 KEY `value` (`value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
```
有从1到10的10行数据
```
INSERT INTO `table`(`id`, `value`) VALUES (1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6),(7, 7),(8, 8),(9, 9),(10, 10);
```
执行以下2条查询
```
SELECT `value` v FROM `table` WHERE `value`>5; -- Get 5 rows
SELECT `value` v FROM `table` HAVING `value`>5; -- Get 5 rows
```
你会得到完全一样的结果，显然 **`HAVING` 可以脱离 `GROUP BY` 使用**。

不同之处在于：
```
SELECT `value` v FROM `table` WHERE `v`>5;
ORA-00904: "v": 标识符无效
SELECT `value` v FROM `table` HAVING `v`>5; -- Get 5 rows
```
`WHERE` 允许条件使用表的任意一列，但是**不可以**使用别名或者聚合函数。
`HAVING` 允许条件使用选定的列、别名或者聚合函数。

这是因为 `WHERE` 在 `SELECT` **之前**筛选数据，而 `HAVING` 在 `SELECT` **之后**过滤结果数据。

在一个表中有许多列数据时，在条件中使用 `WHERE` 将会**更高效**。
##2. WHERE