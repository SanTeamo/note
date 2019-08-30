## 4. thymeleaf模板

1. **pom.xml**引入依赖
```
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```
2. 编写controller
```
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
```
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

## 5. 国际化

1. 国际化基本原理

    在Spring程序中，国际化主要是通过ResourceBundleMessageSource这个类来实现的。
    
    Spring Boot通过MessageSourceAutoConfiguration是为我们自动配置好了管理国际化资源文件的组件的:
    
    在org.springframework.boot.autoconfigure.context.MessageSourceAutoConfiguration
    
    主要了解messageSource()这个方法。
    
    方法中首先声明了MessageSourceProperties这个对象
    
    类中首先声明了一个属性basename,默认值为messages。这是一个以逗号分隔的基本名称列表，如果它不包含包限定符（例如“org.mypackage”），它将从类的根路径解析。它的意思是如果你不在配置文件中指定以逗号分隔开的国际化资源文件名称的话，它默认会去类路径下找messages.properties作为国际化资源文件的基本文件。若国际化资源文件是在类路径某个包(如：i18n)下的话，就需要在配置文件中指定基本名称了。

2. 配置
```
spring.messages.basename=i18n/login/login
spring.messages.encoding=utf-8
```
3. 国际化
    1. 编写页面
    ```
    <!DOCTYPE html>
    <html xmlns:th="http://www.thymeleaf.org">
    <head>
        <meta charset="UTF-8"/>
        <title>internationalization</title>
    </head>
    <body>
    <form action="" method="post">
        <label th:text="#{login.username}">Username</label>
        <input type="text"  name="username"  placeholder="Username" th:placeholder="#{login.username}">
        <label th:text="#{login.password}">Password</label>
        <input type="password" name="password" placeholder="Password" th:placeholder="#{login.password}">
        <br> <br>
        <div>
            <label>
                <input type="checkbox" value="remember-me"/> [[#{login.remmber}]]
            </label>
        </div>
        <br>
        <button  type="submit" th:text="#{login.sign}">Sign in</button>
        <br> <br>
        <a>中文</a>
        <a>English</a>
    </form>
    </body>
    </html>
    ```
    2. Controller
    ```
    @RequestMapping("/internationalbylink")
    public String internationalbylink(){

        return "internationalbylink";
    }
    ```
    3. resource文件
    文件位置
    ![](pic/resource.jpg)
    login.properties
    ![](pic/resource_.jpg)
    login_en_US.properties
    ![](pic/resource_us.jpg)
    login_zh_CN.properties
    ![](pic/resource_cn.jpg)
    4. 测试
    使用Google浏览器，会根据浏览器的语言切换文字。
    ![](pic/result1_cn.jpg)
    5. 


