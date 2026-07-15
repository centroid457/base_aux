// =====================================================================================================================
// 1. СОЗДАНИЕ ОБЪЕКТА
// ============================================================

// 1.1 Литерал (предпочтительный способ)
const source = {
    // Все ключи преобразуются в строки!
    name: 'value',
    "name2": 'value2',
    // ["arr1", 'arr11'],  // НЕЛЬЗЯ! – синтаксическая ошибка
    // ["arr1": 'arr11'],  // тоже нельзя

    "11": "intStr",
    11: "intInt",          // перезапишет предыдущий (т.к. ключ '11' уже есть)

    true: "bool",
    'key.with: specials!': "value.with: specials!",

    // Динамические ключи (вычисляемые)
    [keyFromVar]: "valueFromVar",

    // Сокращённая запись (ES6) – если имя переменной совпадает с ключом
    shortStyle,
};

// 1.2 Через new Object() (редко)
const obj1 = new Object();
obj1.prop = 'value';

// 1.3 Object.create() – с указанным прототипом
const proto = { shared: 42 };
const obj2 = Object.create(proto);
obj2.own = 10;
console.log(obj2.shared); // 42 (из прототипа)

// 1.4 Object.assign() – копирование свойств из других объектов
const obj3 = Object.assign({}, { a: 1 }, { b: 2 }); // { a:1, b:2 }

// 1.5 Из JSON-строки
const json = '{"x":1,"y":2}';
const fromJSON = JSON.parse(json); // { x:1, y:2 }

// 1.6 Из Map или массива пар через Object.fromEntries()
const map = new Map([['key1', 'val1'], ['key2', 'val2']]);
const fromMap = Object.fromEntries(map); // { key1:'val1', key2:'val2' }
const fromPairs = Object.fromEntries([['a',1], ['b',2]]); // { a:1, b:2 }

// 1.7 С геттерами/сеттерами (в литерале)
const withAccessors = {
    _value: 0,
    get value() { return this._value; },
    set value(v) { this._value = v; }
};
withAccessors.value = 5;
console.log(withAccessors.value); // 5

// 1.8 Пустой объект (литерал или Object.create(null) – без прототипа)
const empty = {};
const noProto = Object.create(null);
console.log(noProto.toString); // undefined (нет прототипа)

// =====================================================================================================================
// 2. ОСНОВНЫЕ ОПЕРАЦИИ С ОБЪЕКТОМ
// ============================================================
let obj = { a: 1, b: 2, c: 3 };

// 2.1 Доступ к свойствам
// Точечная нотация
console.log(obj.a);          // 1
// Квадратные скобки (для динамических ключей или с пробелами)
console.log(obj['b']);       // 2
console.log(obj['key.with: specials!']); // "value.with: specials!"

// 2.2 Добавление/изменение свойства
obj.d = 4;
obj['e'] = 5;

// 2.3 Удаление свойства (delete)
delete obj.c;
console.log(obj); // { a:1, b:2, d:4, e:5 }

// 2.4 Проверка наличия свойства
console.log('a' in obj);                  // true
console.log(obj.hasOwnProperty('a'));     // true (собственное, не из прототипа)
console.log(Object.hasOwn(obj, 'a'));     // ES2022 – более современный аналог

// 2.5 Деструктуризация (извлечение свойств)
const { a, b: second, ...rest } = obj;
console.log(a, second, rest); // 1, 2, { d:4, e:5 }

// =====================================================================================================================
// 3. ИТЕРАЦИЯ
// ============================================================
const sample = { x: 10, y: 20 };
sample.AttrNew = "valueNew";

// 3.1 [НЕБЕЗОПАСНО!!!]for...in – перебирает все перечисляемые свойства, включая унаследованные
let result;
result = [];
for (const key in sample) {
    result.push(key);
}
console.log(result);    //['x', 'y', 'AttrNew']

for (const key in sample) {
    if (sample.hasOwnProperty(key)) { // чтобы отсечь прототип
        console.log(key, sample[key]);
    }
}

// =====================================================================================================================
// 3.2 [БЕЗОПАСНО!!!]Object.keys/values/entries() – массив собственных(неунаследованных) перечисляемых ключей (строки)
console.log(Object.keys(sample));   // ['x','y']
console.log(Object.values(sample)); // [10,20]
console.log(Object.entries(sample)); // [['x',10], ['y',20]]

// БЕЗОПАСНЫЙ ПЕРЕБОР СВОЙСТВ (for...in vs Object.keys)
/*В любом месте, где вы перебираете свойства объекта, используйте Object.keys(), Object.values() или Object.entries(),
если вам нужны только собственные свойства. for...in используйте только тогда,
когда вы намеренно хотите включить унаследованные свойства (что бывает редко,
и обычно требует явной проверки hasOwnProperty).*/

const parent = { inherited: 'fromProto' };
const child = Object.create(parent);
child.own = 'myProp';

// НЕБЕЗОПАСНО – перебирает и унаследованные
for (const key in child) {  // IN !!!!
    console.log(key); // 'own', затем 'inherited'
}

// БЕЗОПАСНО – только собственные свойства
for (const key of Object.keys(child)) {  // OF !!!!
    console.log(key); // только 'own'
}

// Ещё безопаснее – проверка hasOwnProperty внутри for...in
for (const key in child) {
    if (Object.hasOwn(child, key)) {
        console.log(key); // только 'own'
    }
}
// или старая форма: if (child.hasOwnProperty(key))
// =====================================================================================================================

// 3.5 Object.getOwnPropertyNames() – все собственные ключи (включая неперечисляемые)
const withHidden = {};
Object.defineProperty(withHidden, 'hidden', { value: 42, enumerable: false });
console.log(Object.getOwnPropertyNames(withHidden)); // ['hidden']

// 3.6 Object.getOwnPropertySymbols() – собственные символьные ключи
const sym = Symbol('id');
const withSym = { [sym]: 123 };
console.log(Object.getOwnPropertySymbols(withSym)); // [Symbol(id)]

// =====================================================================================================================
// 4. СТАТИЧЕСКИЕ МЕТОДЫ OBJECT
// ============================================================

// 4.1 Object.keys/values/entries – уже показаны выше

// 4.2 Object.assign() – поверхностное копирование
const target = { a: 1 };
const merged = Object.assign(target, { b: 2 }, { c: 3 });
console.log(merged); // { a:1, b:2, c:3 } (target также изменился)

// 4.3 Object.freeze() – делает объект неизменяемым (нельзя добавлять/удалять/менять)
const frozen = { value: 100 };
Object.freeze(frozen);
frozen.value = 200;    // в строгом режиме – ошибка, в обычном – игнорируется
delete frozen.value;   // игнорируется
console.log(frozen.value); // 100

// 4.4 Object.seal() – запрещает добавление/удаление, но разрешает изменение существующих
const sealed = { count: 5 };
Object.seal(sealed);
sealed.count = 10;     // работает
sealed.newProp = 42;   // игнорируется (в строгом – ошибка)
delete sealed.count;   // игнорируется
console.log(sealed);   // { count:10 }

// 4.5 Object.preventExtensions() – запрещает добавление новых свойств (существующие можно менять/удалять)
const nonExt = { a: 1 };
Object.preventExtensions(nonExt);
nonExt.a = 2;          // работает
nonExt.b = 3;          // игнорируется

// 4.6 Object.defineProperty() – точная настройка свойства (дескриптор)
const desc = {};
Object.defineProperty(desc, 'age', {
    value: 25,
    writable: false,   // нельзя перезаписать
    enumerable: true,
    configurable: false // нельзя удалить или изменить дескриптор
});
console.log(desc.age); // 25
desc.age = 30;         // игнорируется (writable:false)
delete desc.age;       // игнорируется (configurable:false)

// 4.7 Object.defineProperties() – сразу несколько свойств
const multi = {};
Object.defineProperties(multi, {
    first: { value: 1, enumerable: true },
    second: { value: 2, enumerable: true }
});

// 4.8 Object.getPrototypeOf() / Object.setPrototypeOf()
const parent = { inherited: 'fromParent' };
const child = {};
Object.setPrototypeOf(child, parent);
console.log(Object.getPrototypeOf(child) === parent); // true
console.log(child.inherited); // 'fromParent'

// 4.9 Object.fromEntries() – уже показано выше

// 4.10 Object.is() – строгое сравнение (отличается от === для NaN и -0)
console.log(Object.is(NaN, NaN));  // true
console.log(Object.is(0, -0));     // false

// 4.11 Object.groupBy() – экспериментальный (ES2024) – группировка элементов массива
// const grouped = Object.groupBy([...], item => item.type); // пока не везде доступно

// =====================================================================================================================
// 5. ПРОТОТИПНОЕ НАСЛЕДОВАНИЕ (кратко)
// ============================================================
function Person(name) {
    this.name = name;
}
Person.prototype.sayHi = function() { return `Hi, ${this.name}`; };
const alice = new Person('Alice');
console.log(alice.sayHi()); // "Hi, Alice"
console.log(alice.__proto__ === Person.prototype); // true (устаревший способ)
console.log(Object.getPrototypeOf(alice) === Person.prototype); // современный

// =====================================================================================================================
// 6. ОСОБЕННОСТИ ОБЪЕКТОВ
// ============================================================

// 6.1 Ключи всегда строки (или символы). Числа преобразуются в строки.
const numeric = { 1: 'one', '1': 'two' }; // второй перезапишет первый
console.log(numeric[1]);    // 'two'
console.log(numeric['1']);  // 'two'

// 6.2 Порядок свойств (целочисленные индексы сортируются по возрастанию,
//     остальные – в порядке добавления)
const order = { '3': 'c', '1': 'a', '2': 'b', 'x': 'X' };
console.log(Object.keys(order)); // ['1','2','3','x'] – числовые индексы сначала

// 6.3 Дескрипторы свойств (атрибуты)
const propDesc = Object.getOwnPropertyDescriptor(order, '1');
console.log(propDesc); // { value: 'a', writable: true, enumerable: true, configurable: true }

// 6.4 Символы как ключи – не перечисляются в for...in, Object.keys и т.д.
const symObj = { [Symbol('secret')]: 'hidden' };
console.log(Object.keys(symObj)); // []
console.log(Object.getOwnPropertySymbols(symObj)); // [Symbol(secret)]

// 6.5 Объект как Map? – не рекомендуется, т.к. ключи только строки/символы,
//     прототип может мешать. Для словарей лучше использовать Map.

// =====================================================================================================================
// 7. ПРОВЕРКА ТИПА
// ============================================================
const testObj = {};
console.log(typeof testObj);                 // 'object'
console.log(testObj instanceof Object);      // true
console.log(Object.prototype.toString.call(testObj)); // '[object Object]'
// Для null: typeof null === 'object' (историческая ошибка)
console.log(typeof null); // 'object'

// =====================================================================================================================
// 8. ДЕМОНСТРАЦИЯ ВАШЕГО ОРИГИНАЛЬНОГО КОДА
// (с неработающими операциями, чтобы показать ошибки)
// ============================================================
const keyFromVar = 'keyFromVar';
const shortStyle = 'shortStyle_Value';

let src = {
    //ВСЕ КЛЮЧИ ПРЕОБРАЗУЮТСЯ В STR!
    name: 'value',
    "name2": 'value2',
    "11": "intStr",
    11: "intInt",    //ПЕРЕЗАПИШЕТ! предыдущий!
    true: "bool",
    'key.with: specials!': "value.with: specials!",
    [keyFromVar]: "valueFromVar",
    shortStyle,
};

console.log(src);
console.log(String(src));    //[object Object]

// ОБРАЩЕНИЕ К ЗНАЧЕНИЮ
console.log(src[0]);        // undefined – ищет ключ '0', не индекс!
console.log(src["11"]);     // intInt
console.log(src[11]);       // intInt (число преобразуется в строку)
console.log(src.name);      // value – работает

// Добавление свойства (работает)
src.nameNEW = "valueNEW";
console.log(src.nameNEW);   // "valueNEW"

// НЕ РАБОТАЮТ методы массивов:
// src.push("valueNEW");        // TypeError: src.push is not a function
// src.delete(11);              // TypeError: src.delete is not a function

// Удаление свойства (delete)
delete src[11];
console.log(src);           // { name:'value', name2:'value2', ... без ключа '11' }

// =====================================================================================================================
// 9. КРАТКИЙ СПРАВОЧНИК ПО ПОЛЕЗНЫМ МЕТОДАМ
// ============================================================
console.log('=== Краткий справочник ===');
console.log('Object.keys(obj) – массив собственных перечисляемых ключей');
console.log('Object.values(obj) – массив значений');
console.log('Object.entries(obj) – массив пар [key, value]');
console.log('Object.assign(target, ...sources) – поверхностное копирование');
console.log('Object.freeze(obj) – заморозка');
console.log('Object.seal(obj) – герметизация');
console.log('Object.defineProperty(obj, prop, descriptor) – настройка свойства');
console.log('Object.getPrototypeOf(obj) – получить прототип');
console.log('Object.setPrototypeOf(obj, proto) – установить прототип');
console.log('Object.fromEntries(iterable) – создать объект из пар');
console.log('Object.hasOwn(obj, prop) – проверка собственного свойства (ES2022)');
console.log('Object.is(val1, val2) – сравнение (учёт NaN и -0)');


// =====================================================================================================================
