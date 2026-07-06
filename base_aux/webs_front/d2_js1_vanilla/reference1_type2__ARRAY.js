// ============================================================
// 1. СОЗДАНИЕ ARRAY
// ============================================================
let source;

// СОЗДАНИЕ -------------------------------------
// Из строки
const fromString = 'a,b,c'.split(',');       // ['a','b','c']

// Из объекта (ключи/значения)
const obj = { a: 1, b: 2 };
const keys = Object.keys(obj);               // ['a','b']
const values = Object.values(obj);           // [1,2]
const entries = Object.entries(obj);         // [['a',1], ['b',2]]

// Из Set или Map
const set = new Set([1,2,3]);
const fromSet = Array.from(set);            // [1,2,3]
const map = new Map([['a',1], ['b',2]]);
const fromMap = Array.from(map);            // [['a',1], ['b',2]]

//    [...iterable]

// Создание с фиксированной длиной (редко)
source = new Array(5); // [пустые × 5]
const filled = new Array(3).fill('x'); // ['x','x','x']

// Array.of – создание из переданных аргументов
const arrOf = Array.of(1, 2, 3); // [1,2,3]

// Литерал (предпочтительно)
const sparse = [1, , 3];  //с пустыми полями
source = [11, 22, 'name', true];

// 1=str ------------------------------------------------
console.log(source);            //[11, 22, 'text', true]
console.log(String(source));    //11,22,text,true

// 2=type -----------------------------------------------
console.log(typeof source);         // object
console.log(Array.isArray(source)); // true

// ОБРАЩЕНИЕ К ЗНАЧЕНИЮ ---------------------------------
//1=index
console.log(source[0]);  //11 - единственная возможность доступа!

//2=item
console.log(source["11"]);  //undefined
console.log(source[11]);    //undefined

//3=get
//console.log(source.get("11"));  //нет метода! Uncaught TypeError: source.get is not a function
//console.log(source.get(11));    //нет метода! Uncaught TypeError: source.get is not a function

//4=dot
console.log(source.name);  //undefined

//5=ADD
source.nameNEW = "valueNEW";    //добавляет не элемент а свойство!
console.log(String(source));    //11,22,name,true - не добавляется!!!

source.unshift('first');   // добавить в начало

source.push("valueNEW");
console.log(String(source));    //11,22,name,true,valueNEW

source.splice(2, 0, 'new'); // вставить на позицию 2

//6=DEL
// clear FULL
source.length = 0; //
source = [];

// без удаления индекса - value=undefined
delete source[1];              // оставляет дырку (не сдвигает)

// с удалением позиции
source.shift();                 // удаляет первый элемент
source.splice(1, 1);            // удаляет элемент с индексом 1 ('name')

source.pop(11);                 //некорретно! - ВСЕГДА УДАЛЯЕТ ТОЛЬКО ПОСЛЕДНИЙ!!!
console.log(String(source));    //11,22,name,true
source.pop();                   //ЕДИНСТВЕННО КОРРЕКТНЫЙ!!!
console.log(String(source));    //11,22,name
source.pop(0);                  //тоже некорректно! - все равно удалит последний!
console.log(String(source));    //11,22
//source.lpop();                //нет такого!!!
//console.log(String(source));  //11,22

// LEN --------------------------
source = [];
console.log(source.length); // 0
source.push(11);
console.log(source.length); // 1
source.pop();
console.log(source.length); // 0

source.nameNEW = "valueNEW"; // добавляет не элемент, а свойство!
console.log(source.length); // 0
console.log(Object.keys(source));  // ["nameNEW"] – индексы + имя свойства

// проверка на пустоту
console.log(source.length === 0);
console.log(!source.length);

// ИТЕРАЦИЯ
source.forEach((item, index) => console.log(index, item));
for (const item of source) {
    console.log(item);
}
const arr = [11,22,33];
arr.customProp = 'test';
for (const key in arr) console.log(key);     // 0,1,2,'customProp'
for (const val of arr) console.log(val);     // 11,22,33

// CHECK_IN
console.log(1 in source);      // false

// -----------------------------------------------------
//пустые поля
const sparse = [1, , 3];
console.log(sparse.length);          // 3
console.log(sparse[1]);              // undefined
console.log(sparse.hasOwnProperty(1)); // false (дырка)
console.log(Object.keys(sparse));    // ['0','2'] (индексы с дырками не попадают)

// Поиск и проверка наличия
console.log(source.includes('name'));        // true
console.log(source.indexOf(22));             // 1
console.log(source.find(item => item > 20)); // 22
console.log(source.findIndex(item => item > 20)); // 1

console.log(source.some(item => typeof item === 'string')); // true
console.log(source.every(item => typeof item === 'number')); // false

//Преобразование и создание новых массивов
const doubled = source.map(item => item * 2);
const evens = source.filter(item => item % 2 === 0);
const sum = source.reduce((acc, val) => acc + val, 0);

// FLAT
const flat = source.flat(); // если есть вложенные массивы
const nested = [1, [2, [3]]];
console.log(nested.flat(2));          // [1,2,3]
console.log(nested.flatMap(x => x));  // [1,2,3] (для одномерных)

//СОРТИРОВКА +порядок
const numbers = [3, 1, 4, 1, 5];
numbers.reverse(); // [5, 4, 3, 1, 1]
numbers.sort((a, b) => a - b); // [1, 1, 3, 4, 5]

const users = [{name:'John', age:30}, {name:'Jane', age:25}];
users.sort((a,b) => a.age - b.age);

// преобразование типа
console.log(source.join(' | ')); // "11 | 22 | name | true"

// Копирование и срезы
const copy1 = source.slice();          // копия
const copy2 = [...source];             // спред-оператор
const part = source.slice(1, 3);       // элементы с 1 по 2
const merged = source.concat([99, 100]);

//Деструктуризация и rest-оператор
const [first, second, ...rest] = source;
console.log(first, second, rest);


// =====================================================================================================================
