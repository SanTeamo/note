## 8.SpringBoot使用WebJars

### Tip
原本我们在进行web开发时，一般上都是讲静态资源文件放置在webapp目录下，在SpringBoot里面，一般是将资源文件放置在src/main/resources/static目录下。而在Servlet3中，允许我们直接访问WEB-INF/lib下的jar包中的/META-INF/resources目录资源，即WEB-INF/lib/{*.jar}/META-INF/resources下的资源可以直接访问。

所以其实，WebJars也是利用了此功能，将所有前端的静态文件打包成一个jar包，这样对于引用放而言，和普通的jar引入是一样的，还能很好的对前端静态资源进行管理。

### 使用
引入pom依赖
```xml
<dependency>
    <groupId>org.webjars</groupId>
    <artifactId>jquery</artifactId>
    <version>x.x.x</version>
</dependency>
```
thymeleaf引用
```html
<script th:src="@{/webjars/jquery/x.x.x/jquery.min.js}"></script>
```