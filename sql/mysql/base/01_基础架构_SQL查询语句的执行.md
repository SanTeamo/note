# SQL查询语句的执行

## MySQL逻辑架构
![Image text](../../../picture/sql/mysql/base/0d2070e8f84c4801adbfa03bda1f98d9.webp)
<p style="text-align: center;">MySQL逻辑架构</p>

- 连接器
 
    连上数据库，首先等待的就是连接器。连接器负责负责跟客户端建立连接、获取权限、维持和管理连接

- 查询缓存

    MySQL拿到查询后，会先到查询缓存看是否有执行的语句。以key-value对的形式被直接缓存在内存中，有则直接返回value。
    
    多数情况不建议开启，因为一旦表数据有更新，缓存即会失效。

    可以使用参数 ```query_cache_type``` 控制。也可以使用 ```SQL_CACHE``` 显式指定缓存

    ```sql
    mysql> select SQL_CACHE * from T where ID=10；
    ```
    8.0版本开始已去除

- 分析器

    对SQL语句进行词法分析和语法分析（也会对表、列是否存在判断。优化器要决定索引，因此这一步需要判断列是否存在）

- 优化器
    
    是在表里有多个索引时，选择哪个索引；或者在多表关联时，决定各个表的连接顺序。

- 执行器

    开始执行语句，此时会判断用户对表有无查询执行权限，无则返回无权限错误，有则打开表继续执行。打开表的时候，执行器会根据表的引擎定义，调用对应数据库引擎的API执行（因此数据库引擎才是插件形式的）