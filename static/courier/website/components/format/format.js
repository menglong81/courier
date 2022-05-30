/**
 * Created by menglong.zhou on 2019/5/27.
 */
/*
用法:
console.log('my name is ${name}.'.format({name:'lake'}))
my name is lake.
*/
String.prototype.format = function(opts) {//use 'my name is ${name}'.format({name:'lake'})
    var data = Array.prototype.slice.call(arguments, 0),
        toString = Object.prototype.toString;
    if (data.length) {
        data = data.length == 1 ?
            (opts !== null && (/\[object Array\]|\[object Object\]/.test(toString.call(opts))) ? opts : data) : data;
        return this.replace(/\$\{(.+?)\}/g, function(match, key) {
            var replacer = data[key];
            // chrome 下 typeof /a/ == 'function'

            if ('[object Function]' == toString.call(replacer)) {
                replacer = replacer(key);
            }
            return ('undefined' == typeof replacer ? '' : replacer);
        });
    }
    return this;
};