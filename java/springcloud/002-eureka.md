
## 2. *Eureka*
### 简介

>eureka是Netflix开发的一款基于REST（Representational State Transfer）的服务。通常在AWS云服务中用于服务注册发现和负载均衡等，也是SpringCloud中使用的服务注册发现组件。eureka还提供有一个基于java的Client组件，用来与服务端交互，同时具有一套内置的负载均衡器，可以进行基本的轮询负载均衡

### 使用

#### 相关配置

- fetch-registry: 检索服务选项，当设置为true(默认值)时，会进行服务检索,注册中心不负责检索服务。
- register-with-eureka: 服务注册中心也会将自己作为客户端来尝试注册自己,为true（默认）时自动生效
- eureka.client.serviceUrl.defaultZone是一个默认的注册中心地址。配置该选项后，可以在服务中心进行注册。

>一般情况下，当我们设置服务为注册中心时，需要关闭eureka.client.fetch-registry与eureka.client.register-with-eureka，在做注册中心集群的时候，register-with-eureka必须打开，因为需要进行相互注册，不然副本无法可用。

#### 服务发现

##### 创建注册中心

1. *pom.xml*引入依赖

    引入*spring-cloud-starter-netflix-eureka-server*

    ```xml
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>
    </dependencies>
    ```

2. 开启注册中心注解

    加上`@EnableEurekaServer`注解

    ```java
    @SpringBootApplication
    @EnableEurekaServer
    public class EurekaServerApplication {

        public static void main(String[] args) {
            SpringApplication.run(EurekaServerApplication.class, args);
        }

    }
    ```
3. 配置文件

    写好配置文件后，需要在host文件中加入
    ```h
    127.0.0.1 register-master
    ```

    application-default.yml
    ```yml
    spring:
      # profile=default
      profiles: default
    server:
      port: 8760
    eureka:
      instance:
        hostname: register-master
    client:
      #表示是否将自己注册在EurekaServer上，默认为true。由于当前应用就是EurekaServer，所以置为false
      register-with-eureka: false
      #表示表示是否从EurekaServer获取注册信息，默认为true。单节点不需要同步其他的EurekaServer节点的数据
      fetch-registry: false
      #设置Eureka的地址
      service-url:
        defaultZone: http://${eureka.instance.hostname}:${server.port}/eureka/
    ```

##### 微服务与注册

新建项目eureka-client

1. *pom.xml*引入依赖

    引入*spring-cloud-starter-netflix-eureka-client*

    ```xml
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    ```

2. 编写启动类

    加上`@EnableEurekaClient`注解

    ```java
    @SpringBootApplication
    @EnableEurekaClient
    public class EurekaClientApplication {

        public static void main(String[] args) {
            SpringApplication.run(EurekaClientApplication.class, args);
        }

    }
    ```

3. 配置文件

    application.yml
    ```yml
    spring:
      application:
        #应用名称
        name: eureka-client
    eureka:
      client:
        service-url:
        #注入目标，配置服务中心url，与服务端的配置保持一致
        defaultZone: http://register-master:8760/eureka/
    ```
    
4. 启动

    启动后，访问`register-master:8670`，可以看到*Instances currently registered with Eureka*有了服务的注册信息。

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/eureka-client-register.png)

#### eureka集群

1. 配置文件

    写好配置文件后，需要在host文件中加入
    ```h
    127.0.0.1 register-master
    127.0.0.1 register-slave1
    127.0.0.1 register-slave2
    ```

    application-master.yml
    ```yml
    spring:
      profiles: master
    server:
      port: 8760
    eureka:
      instance:
        hostname: register-master
      client:
        service-url:
          defaultZone: http://register-slave1:8761/eureka/,http://register-slave2:8762/eureka/
    ```
    application-slave1.yml
    ```yml
    spring:
      profiles: slave1
    server:
      port: 8761
    eureka:
      instance:
        hostname: register-slave1
      client:
        service-url:
          defaultZone: http://register-master:8760/eureka/,http://register-slave2:8762/eureka/
    ```
    application-slave2.yml
    ```yml
    spring:
      profiles: slave2
    server:
      port: 8762
    eureka:
      instance:
        hostname: register-slave2
      client:
        service-url:
          defaultZone: http://register-master:8760/eureka/,http://register-slave1:8761/eureka/
    ```

2. 启动

    启动master，slave1，slave2

    分别访问`register-master:8760`、`register-slave1:8761`、`register-slave2:8762`，可以看到它们之间有相互的信息。

    register-master

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/master-cluster-info.png)

    register-slave1

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/slave1-cluster-info.png)

    register-slave2

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/slave2-cluster-info.png)

    此时再启动微服务

    配置文件加入3个注册地址
    ```yml
    spring:
      application:
        #应用名称
        name: eureka-client
    eureka:
      client:
        service-url:
          #注入目标，配置服务中心url，与服务端的配置保持一致
          defaultZone: http://register-master:8760/eureka/,http://register-slave1:8761/eureka/,http://register-slave2:8762/eureka/
    ```

    然后在3个注册中心可以看到
    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/eureka-client-cluster-register.png)


### 项目地址
[spring-cloud-demo](https://github.com/SanTeamo/spring-cloud-demo)