## 5. thymeleaf模板

1. **pom.xml**引入依赖
```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```
2. 编写controller
```java
  @Controller
  @RequestMapping("/page")
  public class ThymeleafController {
  
      @RequestMapping("/hello")
      public String hello(ModelMap modelMap){
          modelMap.addAttribute("msg","hello world, this is a thymeleaf page");
          return "hello";
      }
  }
```
3. 配置
```
去除thymeleaf的html严格校验
spring.thymeleaf.mode=LEGACYHTML5
设定thymeleaf文件路径 默认为src/main/resources/templates
spring.thymeleaf.prefix=classpath:/templates/
设定静态文件路径，js,css等
spring.mvc.static-path-pattern=/static/**
是否开启模板缓存，默认true
关闭 Thymeleaf 的缓存，不然在开发过程中修改页面不会立刻生效需要重启，生产可配置为 true
spring.thymeleaf.cache=false
模板编码
spring.thymeleaf.encoding=UTF-8
```
4. 编写页面
```html
<!DOCTYPE html>
<!--解决th报错 -->
<html lang="en" xmlns:th="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="UTF-8">
    <title>thymeleaf</title>
</head>
<body>
<h1 th:text="${msg}"></h1>
</body>
</html>
```