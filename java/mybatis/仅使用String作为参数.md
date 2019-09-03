## There is no getter for property named 'key' in 'class java.lang.String'

在使用mybaitis传参数的时候，如果仅传入一个类型为String的参数，那么在 xml文件中应该使用_parameter来代替参数名。


* 正确的写法
```xml
<select id="getStudentCount" resultType="java.lang.Integer">
    SELECT COUNT(*)
    FROM TEST_STU
    <if test="key != null and key != ''">
        WHERE NAME LIKE CONCAT(CONCAT('%',#{_parameter,jdbcType=VARCHAR}),'%')
    </if>
</select>
```
  
* 错误的写法
```xml
<select id="getStudentCount" resultType="java.lang.Integer">
    SELECT COUNT(*)
    FROM TEST_STU
    <if test="key != null and key != ''">
        WHERE NAME LIKE CONCAT(CONCAT('%',#{key,jdbcType=VARCHAR}),'%')
    </if>
</select>
```

也可以在mapper的接口中，给这个方法的参数加上@Param(value=“id”)，这样就能在.xml中使用#{key,jdbcType=VARCHAR} 了。
```java
int getStudentCount(@Param("key") String key);
```