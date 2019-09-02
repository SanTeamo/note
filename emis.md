## 1、SpringMVC接收数组 ##

#### 可以使用JS模块封装好的**bingThis**函数，设置一个属性名进行提交   
```javascript
delBtn: function() {
    var grid = mini.get("datagrid1");
    var rows = grid.getSelecteds();
    console.log(rows)
    if (rows.length>0) {
        view.confirm("确定删除选中记录？", "提示", 'info', 
        ['确定', {text: '取消'}]).ok(function () {
        var ids = [];
        for (var i = 0, l = rows.length; i < l; i++) {
            var r = rows[i];
            ids.push(r.id);//[1,2,3]
        }
        var id = ids.join(',');
        view.delStu(id);
        });
    } else {
        view.showErrorTip("请选中一条记录");
    }
},

delStu: function(ids){
    ……
    view.withWaiting(stuService.bindThis('delStudent'))({
        'ids': ids
    }).then(
        ……
    }).catch(function (reason) {
        ……
    });
},
``` 
#### 使用SpringMVC注解@RequestParam
```java
@RequestMapping(value = "/delStudent", method = {RequestMethod.POST})
@ResponseBody
public JsonResult delStudent(@RequestParam(value = "ids[]")Integer[] ids) {
    Boolean result = studentHandler.delStudentStudent(ids);

    return new JsonResult(DescribableEnum.SUCCESS,result);
}
```
## 2、Oracle数据库分页查询

* 物理分页使用**ROWNUM**，控制**ROMNUM**的范围来实现分页。
```sql
SELECT *
FROM (SELECT a.*,ROWNUM RN FROM TEST_STU a)
WHERE RN > 0 AND RN <= 10)
```

## 3、Oracle排序查询
* 理解mybatis中 $与#

   在mybatis中的$与#都是在sql中动态的传入参数。

   **eg**:select id,name,age from student where name=#{name}  这个name是动态的，可变的。当你传入什么样的值，就会根据你传入的值执行sql语句。

* 使用$与#

  1. \#{}: 解析为一个 JDBC 预编译语句（prepared statement）的参数标记符，一个 #{ } 被解析为一个参数占位符 。

  2. ${}: 仅仅为一个纯碎的 string 替换，在动态 SQL 解析阶段将会进行变量替换。

        传入一个不改变的字符串或者传入数据库字段(列名)，例如要传入order by 后边的参数

        这种情况下必须使用${}。

**综上，#{}方式一般用于传入字段值，并将该值作为字符串加到执行sql中，一定程度防止sql注入；
${}方式一般用于传入数据库对象，例如传入表名，不能防止sql注入，存在风险。
模糊查询中，如果使用如下方式：select * from reason_detail where reason_en like '%${reason}%'，
此处只能使用$，使用#的话，反而会被解析为列，报错java.sql.SQLException: Column 'reason' not found**

```sql
SELECT *
FROM (SELECT A.*,ROWNUM RN
FROM TEST_STU A
<if test="sortField != null and sortField != ''">
    ORDER BY ${sortField} ${sortOrder}
</if>
)
WHERE RN > #{pageIndex}*#{pageSize} AND RN <= #{pageIndex}*#{pageSize}+#{pageSize}
```

## 3、Oracle数据库模糊查询

#### 类似于分页查询中的ORDER BY

* 第一种 **concat**
```sql
SELECT * FROM TEST_STU WHERE NAME LIKE CONCAT(CONCAT('%',#{NAME}),'%')
```
* 第二种 **||**
```sql
SELECT * FROM TEST_STU WHERE NAME LIKE '%' || #{NAME} || '%'
```

**在oracle中 concat不支持三个参数的 如concat('%',#{},'%')**

## 4、There is no getter for property named 'key' in 'class java.lang.String'

#### 在使用mybaitis传参数的时候，如果仅传入一个类型为String的参数，那么在 xml文件中应该使用_parameter来代替参数名。


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

* 也可以在mapper的接口中，给这个方法的参数加上@Param(value=“id”)，这样就能在.xml中使用#{key,jdbcType=VARCHAR} 了。
```java
int getStudentCount(@Param("key") String key);
```

## 5、$.Deferred()
#### A factory function that returns a chainable utility object with methods to register multiple callbacks into callback queues, invoke callback queues, and relay the success or failure state of any synchronous or asynchronous function.
#### 是一个构造函数，用来返回一个链式实用对象方法来注册多个回调，并且调用回调队列，传递任何同步或异步功能成功或失败的状态

- 用例1
```js
    // Existing object
var obj = {
	hello: function( name ) {
	  alert( "Hello " + name );
	}
},

    // Create a Deferred
defer = $.Deferred();

    // Set object as a promise
    defer.promise( obj );

    // Resolve the deferred
defer.resolve( "John" );

    // Use the object as a Promise
obj.done(function( name ) {
  obj.hello( name );
}).hello( "Karl" );
```
- 用例2
```js
function asyncEvent() {
	var dfd = jQuery.Deferred();

	// Resolve after a random interval
	setTimeout(function() {
		dfd.resolve( "resolve" );
	}, Math.floor( 400 + Math.random() * 2000 ) );

	// Reject after a random interval
	setTimeout(function() {
		dfd.reject( "reject" );
	}, Math.floor( 400 + Math.random() * 2000 ) );

	// Show a "working..." message every half-second
	setTimeout(function working() {
		if ( dfd.state() === "pending" ) {
			dfd.notify( "working... " );
			setTimeout( working, 500 );
		}
	}, 1 );
	
	// Return the Promise so caller can't change the Deferred
	return dfd.promise();
}
// Attach a done, fail, and progress handler for the asyncEvent
$.when( asyncEvent() ).then(
	function( status ) {
		alert( status + ", function done!" );
	},
	function( status ) {
		alert( status + ", function fail!" );
	},
	function( status ) {
		$( "body" ).append( status );
	}
);
```

## 6、箭头函数

```js
var elements = [
  'Hydrogen',
  'Helium',
  'Lithium',
  'Beryllium'
];

elements.map(function(element) { 
  return element.length; 
}); // 返回数组：[8, 6, 7, 9]

// 上面的普通函数可以改写成如下的箭头函数
elements.map((element) => {
  return element.length;
}); // [8, 6, 7, 9]

// 当箭头函数只有一个参数时，可以省略参数的圆括号
elements.map(element => {
 return element.length;
}); // [8, 6, 7, 9]

// 当箭头函数的函数体只有一个 `return` 语句时，可以省略 `return` 关键字和方法体的花括号
elements.map(element => element.length); // [8, 6, 7, 9]

// 在这个例子中，因为我们只需要 `length` 属性，所以可以使用参数解构
// 需要注意的是字符串 `"length"` 是我们想要获得的属性的名称，而 `lengthFooBArX` 则只是个变量名，
// 可以替换成任意合法的变量名
elements.map(({ "length": lengthFooBArX }) => lengthFooBArX); // [8, 6, 7, 9]
```
- 递归

```js
var fact = (x) => ( x==0 ?  1 : x*fact(x-1) );

alert(fact(5));
```