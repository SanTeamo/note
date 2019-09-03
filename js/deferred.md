## Deferred
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