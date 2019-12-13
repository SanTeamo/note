## 4. *feign*
### 简介
Feign是一个声明式WebService客户端.使用Feign能让编写WebService客户端更加简单,它的使用方法是定义一个接口,然后在上面添加注解,同时也支持JAX-RS标准的注解.Feign也支持可拔插式的编码器和解码器.Spring Cloud对Feign进行了封装,使其支持了Spring MVC标准注解和HttpMessageConverters.Feign可以与Eureka和Ribbon组合使用以支持负载均衡。

来源：[简书](https://www.jianshu.com/p/94177e224ef8)

### 使用

#### 构建服务

使用项目[eureka-client](https://github.com/SanTeamo/spring-cloud-demo/tree/master/eureka-client)

1. 配置文件
    
    application.yml
    ```yml
    spring:
      application:
      #应用名称
        name: eureka-client
    ```

    application-service1.yml
    ```yml
    spring:
      profiles:
        service1
    server:
      port: 8761
    eureka:
      client:
        service-url:
          #注入目标，配置服务中心url，与服务端的配置保持一致
          defaultZone: http://register-master:8760/eureka/
    ```

    application-service2.yml
    ```yml
    spring:
      profiles:
        service2
    server:
      port: 8762
    eureka:
      client:
        service-url:
          #注入目标，配置服务中心url，与服务端的配置保持一致
          defaultZone: http://register-master:8760/eureka/
    ```
2. 启动类

    ```java
    @SpringBootApplication
    @EnableEurekaClient
    @RestController
    public class EurekaClientApplication {

        public static void main(String[] args) {
            SpringApplication.run(EurekaClientApplication.class, args);
        }

        @Value("${server.port}")
        String port;

        @Value("${spring.application.name}")
        String serviceName;

        @GetMapping("/")
        public String index(){
            return "serviceName=" + serviceName + "-------port=" + port;
        }

    }
    ```

#### 声明式服务调用

构建项目feign-service

1. *pom.xml*引入依赖

    ```xml
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-openfeign</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    ```

2. 配置文件
    
    application.yml
    ```yml
    server:
      port: 8778
    spring:
      application:
        name: feign-service
    eureka:
      instance:
        hostname: feign-service
    client:
      service-url:
        defaultZone: http://register-master:8760/eureka/

    feign:
      hystrix:
        enabled: true

    # Feign日志记录只能响应DEBUG日志级别，所以配置
    logging:
      level:
        com:
          santeamo:
            api:
              FeignInterface: DEBUG
    ```

3. 启动类

    ```java
    @SpringBootApplication
    @EnableEurekaClient
    @EnableFeignClients
    public class FeignServiceApplication {

        public static void main(String[] args) {
            SpringApplication.run(FeignServiceApplication.class, args);
        }

    }
    ```

4. 创建暴露接口

    创建Feign暴露接口，接口上加入`@FeignClient`注解。    
    eureka-client为要远程调用服务的名字，即你要调用服务的`spring.application.name`
    FeignFallbackService.class为远程调用失败后回调的方法

    ```java
    @FeignClient(value = "eureka-client",configuration = FeignConfig.class, fallback = FeignFallbackService.class)
    public interface FeignInterface {

        @GetMapping("/")
        String indexInfo();

        @RequestMapping(value = "/user/{name}")
        String user(@PathVariable( value = "name") String name);
    }
    ```

5. 创建远程调用失败回调类

    创建`FeignFallbackService`实现暴露接口`FeignInterface`

    ```java
    @Component
    public class FeignFallbackService implements FeignInterface {

        private String serviceName = "eureka-client";

        @Override
        public String indexInfo() {
            return "远程调用 [" + serviceName + "] 失败！";
        }

        @Override
        public String user(String name) {
            return "远程调用 [" + serviceName + "] 失败！参数 ===> "+name;
        }
    }
    ```

6. Controller

    将接口`FeignInterface`注入到Controller，以供调用

    ```java
    @RestController
    public class FeignController {

        @Autowired
        FeignInterface feignInterface;

        @GetMapping("/")
        public String indexInfo(){
            return feignInterface.indexInfo();
        }

        @RequestMapping(value = "/user/{name}")
        public String user(@PathVariable String name){
            return feignInterface.user(name);
        }

    }
    ```

7. 运行

    启动注册中心、分别使用application-service1和application-service2启动服务、启动feign。

    访问`feign-service:8778`、`feign-service:8778/user/z`，会发现返回的字符串会不断变化，这是因为feign实现了负载均衡。

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/004/feign-request1.jpg)

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/004/feign-request2.jpg)

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/004/feign-pathvariable1.jpg)

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/004/feign-pathvariable2.jpg)

    关掉两个服务，再次访问，发现有调用失败。

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/004/feign-fallback.jpg)

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/004/feign-fallback-pathvariable.jpg)
