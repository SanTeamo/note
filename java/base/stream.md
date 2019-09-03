# Java 8 Stream

----------

## 什么是 Stream? ##
Stream（流）是一个来自数据源的元素队列并支持聚合操作

- 元素是特定类型的对象，形成一个队列。 Java中的Stream并不会存储元素，而是按需计算。
- 数据源 流的来源。 可以是集合，数组，I/O channel， 产生器generator 等。
- 聚合操作 类似SQL语句一样的操作， 比如filter, map, reduce, find, match, sorted等。

和以前的Collection操作不同， Stream操作还有两个基础的特征：

- Pipelining: 中间操作都会返回流对象本身。 这样多个操作可以串联成一个管道， 如同流式风格（fluent style）。 这样做可以对操作进行优化， 比如延迟执行(laziness)和短路( short-circuiting)。
- 内部迭代： 以前对集合遍历都是通过Iterator或者For-Each的方式, 显式的在集合外部进行迭代， 这叫做外部迭代。 Stream提供了内部迭代的方式， 通过访问者模式(Visitor)实现。

stream的特性
1. stream不存储数据
2. stream不改变源数据
3. stream的延迟执行特性

## 生成流 ##

1. 集合
Collection.stream
```
List<Integer> integerList = Arrays.asList(1,2,3,4,5);
Stream stream1 = integerList.stream();
```
2. 数组
Arrays.stream
```
Integer[] integers = new Integer[]{1,2,3,4,5};
Stream<Integer> stream2 = Arrays.stream(integers);
```
3. Stream 静态方法

 - Stream.of
```
Stream<Integer> stream3 = Stream.of(1,2,3,4,5);
```
 - Stream.iterate
    无限流
```
Stream<Integer> stream4 = Stream.iterate(0,(x)->x+2);
```
 - Stream.generate
    无限流
```
Stream<Double> stream5 = Stream.generate(Math::random);
```

## 操作流 ##
初始化一个集合
```
static List<Student> userList = new ArrayList<>();

static {

    Student student1 = new Student("s1",77);
    Student student2 = new Student("s2",62);
    Student student3 = new Student("s3",82);
    Student student4 = new Student("s4",93);
    Student student5 = new Student("s5",54);
    Student student6 = new Student("s6",74);
    Student student7 = new Student("s7",82);
    Student student8 = new Student("s8",70);

    userList.add(student1);
    userList.add(student2);
    userList.add(student3);
    userList.add(student4);
    userList.add(student5);
    userList.add(student6);
    userList.add(student7);
    userList.add(student8);
}
```
### forEach ###
迭代流中数据
```
@Test
public void forEachTest(){
    userList.stream().forEach(System.out::println);
}
```

### filter ###
留下满足filter()中条件的元素。
```
@Test
public void filterTest(){
    userList.stream().filter(student -> student.getScore()>80).forEach(System.out::println);
}
```
### sorted ###
对流进行排序
```
@Test
public void sortTest(){
    userList.stream().sorted(Comparator.comparing(Student::getScore).reversed()).forEach(System.out::println);
}
```
### map ###
转换流，将一种类型的流转换为另外一种流
```
@Test
public void mapTest(){
    String[] arr = new String[]{"yes", "YES", "no", "NO"};
    Arrays.stream(arr).map(x -> x.toLowerCase()).forEach(System.out::println);
}
```
### Collectors ###
```
@Test
public void collectTest(){
    List<Student> list = userList.stream().filter(s -> s.getScore()>70).collect(Collectors.toList());
    list.stream().forEach(System.out::println);
}
```
### 提取，组合 ###

```
@Before
public void init(){
    arr1 = new String[]{"a","b","c","d"};
    arr2 = new String[]{"d","e","f","g"};
    arr3 = new String[]{"i","j","k","l"};
}
/**
 * limit，限制从流中获得前n个数据
 */
@Test
public void testLimit(){
    Stream.iterate(1,x->x+2).limit(10).forEach(System.out::println);
}

/**
 * skip，跳过前n个数据
 */
@Test
public void testSkip(){
//        Stream.of(arr1).skip(2).limit(2).forEach(System.out::println);
    Stream.iterate(1,x->x+2).skip(1).limit(5).forEach(System.out::println);
}

/**
 * 可以把两个stream合并成一个stream（合并的stream类型必须相同）
 * 只能两两合并
 */
@Test
public void testConcat(){
    Stream<String> stream1 = Stream.of(arr1);
    Stream<String> stream2 = Stream.of(arr2);
    Stream.concat(stream1,stream2).distinct().forEach(System.out::println);
 }
```
