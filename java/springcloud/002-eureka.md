
## 2. *Eureka*
### 简介

>eureka是Netflix开发的一款基于REST（Representational State Transfer）的服务。通常在AWS云服务中用于服务注册发现和负载均衡等，也是SpringCloud中使用的服务注册发现组件。eureka还提供有一个基于java的Client组件，用来与服务端交互，同时具有一套内置的负载均衡器，可以进行基本的轮询负载均衡

### 使用

#### *eureka server*

1. *pom.xml*引入依赖

    引入*spring-cloud-starter-netflix-eureka-server*

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <parent>
            <groupId>com.santeamo</groupId>
            <artifactId>spring-cloud-demo</artifactId>
            <version>1.0-SNAPSHOT</version>
        </parent>
        <artifactId>eureka-server</artifactId>
        <version>0.0.1-SNAPSHOT</version>
        <name>eureka-server</name>
        <description>Spring Cloud Eureka Server</description>

        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
            </dependency>
        </dependencies>

        <build>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                </plugin>
            </plugins>
        </build>

    </project>
    ```

2. 编写启动类

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
    127.0.0.1 server1
    127.0.0.1 server2
    ```

    application.yml
    ```yml
    spring:
    application:
        name: eureka-cluster
    ```
    application-server1.yml
    ```yml
    spring:
    # profile=server1
    profiles: server1
    server:
    port: 8761
    eureka:
    instance:
        hostname: server1
    client:
        # 表示是否注册自身到eureka服务器
        # register-with-eureka: false
        # 是否从eureka上获取注册信息
        # fetch-registry: false
        service-url:
        defaultZone: http://server2:8762/eureka
    ```
    application-server2.yml
    ```yml
    spring:
    # profile=server2
    profiles: server2
    server:
    port: 8762
    eureka:
    instance:
        hostname: server2
    client:
        # 表示是否注册自身到eureka服务器
        # register-with-eureka: false
        # 是否从eureka上获取注册信息
        # fetch-registry: false
        service-url:
        defaultZone: http://server1:8761/eureka
    ```
4. 启动

    配置好run configuration

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/server1-run-configuratuion.png)

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/server2-run-configuratuion.png)

    先启动server1，这时会报错
    ```java
    com.netflix.discovery.shared.transport.TransportException: Cannot execute request on any known server
    ```
    这是因为server2还没有启动，再启动server2。

    访问`server1:8761`和`server2:8762`，可以看到registered-replicas和available-replicas分别有了对方的地址。

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/server1-general-info.png)

    ![Image text](https://raw.githubusercontent.com/SanTeamo/note/master/picture/java/springcloud/002/server2-general-info.png)


