/**
 * Throttle util (for window resize event)
 * @param {Function} fn
 * @param {Int} delay
 */
var throttle = function (fn, delay) {
  var timer = null;
  return function () {
    var context = this,
      args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
};

export default throttle;
