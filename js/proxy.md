# *proxy*

[官方文档](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy)

## 简介

为对象提供一个代理对象。

## 语法

```js
let p = new Proxy(target, handler);
```

### 参数

* target

> 用`Proxy`包装的目标对象（可以是任何类型的对象，包括原生数组，函数，甚至另一个代理）。

* handler

> 一个对象，其属性是当执行一个操作时定义代理的行为的函数。

## *target*
## *handler*