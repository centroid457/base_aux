// ============================================================
// 0. ВЫЗОВ - КЛЮЧЕВЫЕ ОТЛИЧИЯ
// ============================================================

// 0.1 НЕЛЬЗЯ ВЫЗЫВАТЬ ИМЕНОВАННЫМИ ПАРАМЕТРАМИ
/*
Здесь нет строгого режима (функция объявлена глобально, без 'use strict').
При вызове f1(1, name2=22):
выполняется name2 = 22 → создаётся глобальная переменная name2 (или перезаписывается существующая) и возвращается 22.
Это значение 22 передаётся вторым аргументом.
f1 получает name1=1, name2=22 и выводит их.
Это работает случайно и только потому, что нет строгого режима. В классах и модулях такое не пройдёт.

ЗДЕСЬ ЭТО БУДЕТ РАБОТАТЬ НО В СОВРЕМЕННОМ КОДЕ - ПЛОХО!!!
*/
function f1(name1, name2=2) {
    console.log(name1, name2);
}
f1(1, 2); // 1,2
f1(1, name2=22);
f1(     //неправильная запись!!! - в STRICT режиме работать не будет!!! а это в любом современном коде с классами!!
    // m6_webui.js:377 Uncaught (in promise) ReferenceError: name1 is not defined
    name1=11,
    name2=22
    );
f1(     // ЕДИНСТВЕННО ПРАВИЛЬНАЯ запись!!!
    11,
    22
    );

// ============================================================
// 1. СОЗДАНИЕ ФУНКЦИЙ
// ============================================================

// 1.1 Function Declaration (объявление)
// – всплывает (hoisting) – можно вызывать до объявления
function declaredFunc(a, b) {
    return a + b;
}
console.log('declaredFunc(2,3):', declaredFunc(2, 3)); // 5

// 1.2 Function Expression (функциональное выражение)
// – не всплывает, создаётся в момент выполнения
const exprFunc = function(a, b) {
    return a * b;
};
console.log('exprFunc(2,3):', exprFunc(2, 3)); // 6

// 1.3 Named Function Expression (с именем, доступным внутри)
const namedExpr = function factorial(n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
};
console.log('namedExpr(5):', namedExpr(5)); // 120

// 1.4 Arrow Function (стрелочная, ES6)
// – нет своего this, arguments, super, не может быть конструктором
const arrow = (a, b) => a + b;
console.log('arrow(2,3):', arrow(2, 3)); // 5
// Если одно выражение – return неявный, если блок – нужен return
const arrowBlock = (a, b) => {
    const sum = a + b;
    return sum;
};
// Если один параметр – скобки можно опустить
const double = x => x * 2;

// 1.5 Конструктор Function (редко, динамическое создание)
// – создаёт функцию из строки, выполняется в глобальной области
const dynamic = new Function('a', 'b', 'return a - b;');
console.log('dynamic(5,2):', dynamic(5, 2)); // 3

// 1.6 IIFE – Immediately Invoked Function Expression
(function() {
    console.log('IIFE выполняется сразу');
})();
// Arrow-вариант
(() => console.log('IIFE стрелочная'))();

// 1.7 Generator Function (функция-генератор)
function* genFunc() {
    yield 1;
    yield 2;
    return 3;
}
const gen = genFunc();
console.log(gen.next()); // { value:1, done:false }
console.log(gen.next()); // { value:2, done:false }
console.log(gen.next()); // { value:3, done:true }

// 1.8 Async Function (асинхронная)
async function asyncFunc() {
    return 'result';
}
// Async arrow
const asyncArrow = async () => 'result';

// 1.9 Async Generator
async function* asyncGen() {
    yield 1;
    yield 2;
}

// 1.10 Function constructor (c new) – тоже самое, но синтаксис устарел

// ============================================================
// 2. СВОЙСТВА ФУНКЦИЙ
// ============================================================

function example(a, b, c = 10) { /* */ }
console.log('example.name:', example.name); // "example"
console.log('example.length:', example.length); // 2 (количество обязательных параметров до первого со значением по умолчанию)
// Для стрелочной анонимной – name может быть ""
const anon = () => {};
console.log('anon.name:', anon.name); // "" или "anon" в зависимости от окружения

// prototype – есть только у функций, объявленных через function (не у стрелочных)
console.log('typeof example.prototype:', typeof example.prototype); // "object"
// У стрелочных prototype – undefined
console.log('typeof arrow.prototype:', typeof arrow.prototype); // "undefined"

// ============================================================
// 3. ПАРАМЕТРЫ И АРГУМЕНТЫ
// ============================================================

// 3.1 Значения по умолчанию (ES6)
function withDefaults(a = 1, b = 2) {
    return a + b;
}
console.log('withDefaults():', withDefaults()); // 3
console.log('withDefaults(10):', withDefaults(10)); // 12

// 3.2 Rest-параметр (собирает оставшиеся аргументы в массив)
function sumAll(...numbers) {
    return numbers.reduce((acc, n) => acc + n, 0);
}
console.log('sumAll(1,2,3,4):', sumAll(1,2,3,4)); // 10

// 3.3 Деструктуризация параметров (объект/массив)
function printCoords({ x, y }) {
    console.log(`x=${x}, y=${y}`);
}
printCoords({ x: 5, y: 10 }); // x=5, y=10

function printFirstTwo([a, b]) {
    console.log(a, b);
}
printFirstTwo([1,2,3]); // 1 2

// 3.4 Объект arguments (доступен только в function, не в стрелочных)
function oldSchool() {
    console.log(arguments[0], arguments.length);
}
oldSchool('a', 'b'); // 'a', 2

// 3.5 Параметры по умолчанию могут ссылаться на предыдущие
function multiply(a, b = a) {
    return a * b;
}
console.log('multiply(3):', multiply(3)); // 9 (b=a)

// ============================================================
// 4. КОНТЕКСТ (this)
// ============================================================

// 4.1 this в обычной функции зависит от способа вызова
const obj = {
    name: 'Alice',
    sayHi: function() {
        console.log('Hi, ' + this.name);
    }
};
obj.sayHi(); // Hi, Alice – this = obj

const fn = obj.sayHi;
fn(); // Hi, undefined (или global, в strict – undefined) – потеря контекста

// 4.2 Стрелочная функция не имеет своего this – берёт из внешнего лексического окружения
const arrowObj = {
    name: 'Bob',
    sayHi: () => {
        console.log('Hi, ' + this.name); // this – глобальный или undefined
    }
};
arrowObj.sayHi(); // Hi, undefined (если в строгом режиме)

// 4.3 Явная привязка: call, apply, bind
function greet(greeting) {
    console.log(greeting + ', ' + this.name);
}
const person = { name: 'John' };
greet.call(person, 'Hello'); // Hello, John
greet.apply(person, ['Hi']); // Hi, John
const bound = greet.bind(person, 'Hey');
bound(); // Hey, John

// 4.4 this в конструкторах (при new) – указывает на новый объект
function Person(name) {
    this.name = name;
}
const p = new Person('Alice');
console.log(p.name); // Alice

// ============================================================
// 5. ЗАМЫКАНИЯ (Closures)
// ============================================================

function createCounter() {
    let count = 0;
    return function() {
        count++;
        return count;
    };
}
const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
// Внутренняя функция сохраняет доступ к переменной count

// ============================================================
// 6. МЕТОДЫ ФУНКЦИЙ (call, apply, bind)
// ============================================================

// 6.1 call – вызывает функцию с указанным this и аргументами по отдельности
function method(a, b) {
    return this.value + a + b;
}
const ctx = { value: 10 };
console.log(method.call(ctx, 1, 2)); // 13

// 6.2 apply – аналогично call, но аргументы передаются массивом
console.log(method.apply(ctx, [3, 4])); // 17

// 6.3 bind – создаёт новую функцию с привязанным this
const boundMethod = method.bind(ctx);
console.log(boundMethod(5, 6)); // 21

// ============================================================
// 7. СТРЕЛОЧНЫЕ ФУНКЦИИ – ОСОБЕННОСТИ
// ============================================================

// 7.1 Нет arguments
const arrowNoArgs = () => {
    // console.log(arguments); // ReferenceError
};

// 7.2 Нельзя использовать как конструктор (new)
// new arrowNoArgs(); // TypeError

// 7.3 Нет prototype
console.log('arrow.prototype:', arrowNoArgs.prototype); // undefined

// ============================================================
// 8. ГЕНЕРАТОРЫ И ИТЕРАТОРЫ
// ============================================================

function* range(start, end) {
    for (let i = start; i <= end; i++) {
        yield i;
    }
}
const it = range(1, 3);
console.log([...it]); // [1,2,3]

// yield* – делегирование другому генератору или итерируемому
function* combine() {
    yield* [10,20];
    yield* range(30,32);
}
console.log([...combine()]); // [10,20,30,31,32]

// ============================================================
// 9. АСИНХРОННЫЕ ФУНКЦИИ (async/await)
// ============================================================

// 9.1 async функция всегда возвращает Promise
async function fetchData() {
    return { data: 'ok' };
}
fetchData().then(res => console.log(res)); // { data: 'ok' }

// 9.2 await – ожидает разрешения Promise (только внутри async)
async function load() {
    const result = await Promise.resolve(42);
    console.log('await result:', result);
}
load();

// 9.3 Обработка ошибок с try/catch
async function withError() {
    try {
        await Promise.reject('oops');
    } catch (e) {
        console.error('caught:', e);
    }
}

// ============================================================
// 10. ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
// ============================================================

// 10.1 Function.prototype.toString – возвращает строку исходного кода
console.log('toString:', example.toString().slice(0, 50) + '...');

// 10.2 .call / .apply уже показаны

// ============================================================
// 11. ПРОВЕРКА ТИПА ФУНКЦИИ
// ============================================================

const testFn = () => {};
console.log('typeof testFn:', typeof testFn); // 'function'
console.log('testFn instanceof Function:', testFn instanceof Function); // true
console.log('Object.prototype.toString.call(testFn):', Object.prototype.toString.call(testFn)); // '[object Function]'

// ============================================================
// 12. БЕЗОПАСНОСТЬ И ОШИБКИ (отдельно)
// ============================================================

// 12.1 Не вызывайте функции, которые не являются функциями
// if (typeof callback === 'function') callback();

// 12.2 При работе с for...in для объектов – используйте Object.keys или hasOwnProperty
// (это не относится к функциям, но общее предостережение)

// ============================================================
// 13. КРАТКИЙ СПРАВОЧНИК
// ============================================================

console.log('=== Справочник функций ===');
console.log('Объявление: function name() {}');
console.log('Выражение: const fn = function() {};');
console.log('Стрелочная: const fn = () => {};');
console.log('Параметры по умолчанию: function(a=1) {}');
console.log('Rest: function(...args) {}');
console.log('Деструктуризация: function({key}) {}');
console.log('Call: fn.call(this, arg1, arg2)');
console.log('Apply: fn.apply(this, [args])');
console.log('Bind: const bound = fn.bind(this, ...args)');
console.log('Генератор: function* gen() { yield value; }');
console.log('Async: async function() { await ...; }');
console.log('Свойства: name, length, prototype');


// =====================================================================================================================
