## 3. *ribbon*
### 简介
Spring Cloud Ribbon是一个基于HTTP和TCP的客户端负载均衡工具，它基于Netflix Ribbon实现。通过Spring Cloud的封装，可以让我们轻松地将面向服务的REST模版请求自动转换成客户端负载均衡的服务调用。Spring Cloud Ribbon虽然只是一个工具类框架，它不像服务注册中心、配置中心、API网关那样需要独立部署，但是它几乎存在于每一个Spring Cloud构建的微服务和基础设施中。因为微服务间的调用，API网关的请求转发等内容，实际上都是通过Ribbon来实现的，包括后续我们将要介绍的Feign，它也是基于Ribbon实现的工具。所以，对Spring Cloud Ribbon的理解和使用，对于我们使用Spring Cloud来构建微服务非常重要。

来源：[简书](https://www.jianshu.com/p/1bd66db5dc46)

### 使用

#### 构建服务

使用项目[eureka-client](https://github.com/SanTeamo/spring-cloud-demo/tree/master/eureka-client)

1. 配置文件
    
    application-service1.yml
    ```yml
    spring:
      application:
        #应用名称
        name: eureka-client
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
      application:
        #应用名称
        name: eureka-client
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

#### 负载均衡

构建项目ribbon-service

1. *pom.xml*引入依赖

    ```xml
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-ribbon</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    ```

2. 配置文件
    
    application.yml
    ```yml
    Spring:
      application:
        name: ribbon-service
    server:
      port: 8777
    eureka:
      instance:
        hostname: ribbon-service
      client:
        service-url:
          defaultZone: http://register-master:8760/eureka/
    ```

3. 启动类

    `@LoadBalanced`放在RestTemplate上面，表明RestTemplate开启负载均衡

    ```java
    @SpringBootApplication
    @EnableEurekaClient
    @RestController
    public class RibbonApplication {

        public static void main(String[] args) {
            SpringApplication.run(RibbonApplication.class, args);
        }

        @Bean
        @LoadBalanced
        RestTemplate restTemplate() {
            return new RestTemplate();
        }

        @Value("${server.port}")
        String port;

        @Value("${spring.application.name}")
        String serviceName;

        @GetMapping("/")
        public String index(){
            return restTemplate().getForObject("http://eureka-client/",String.class);
        }

    }
    ```

4. 运行

    启动注册中心、分别使用application-service1和application-service2启动服务、启动负载均衡服务。

    访问`ribbon-service:8777`，会发现返回的字符串会不断变化

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/003/ribbon2.jpg)

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/003/ribbon2.jpg)

    负载均衡就实现了。
