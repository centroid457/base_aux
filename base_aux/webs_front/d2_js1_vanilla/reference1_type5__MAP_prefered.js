// =====================================================================================================================
/* почему лушче чем OBJECT

потому что в MAP есть защита от смешивания с атрибутами самого обьекта как в OBJECT!!!
а object может быть прототип с именем или метод с таким же значением!!!

в MAP - имея с самого начала только строковые ключи
в теории будет похоже,
но на практике отделение методов и атрибутов от ключей и вложенных данных!!!
*/


// ============================================================
// 1. СОЗДАНИЕ MAP
// ============================================================

// 1.1 Пустой Map
const empty = new Map();
console.log('empty size:', empty.size); // 0

// 1.2 Из массива пар [key, value] (основной способ)
const fromPairs = new Map([
    ['name', 'Alice'],
    ['age', 30],
    [true, 'boolean key'],   // ключ может быть любого типа
    [{ id: 1 }, 'object key']
]);

// 1.3 Из другого Map (клонирование)
const original = new Map([['a', 1], ['b', 2]]);
const cloned = new Map(original);

// 1.4 Из объекта (через Object.entries)
const obj = { x: 10, y: 20, z: 30 };
const fromObject = new Map(Object.entries(obj));

// 1.5 Из любого итерируемого объекта, возвращающего пары (генератор)
function* pairGen() {
    yield ['key1', 'val1'];
    yield ['key2', 'val2'];
}
const fromGen = new Map(pairGen());

// 1.6 Из массива пар с использованием set (постепенное заполнение)
const map = new Map();
map.set('key', 'value');
map.set(123, 'number key');

// 1.7 Цепочка set
const chained = new Map().set('a', 1).set('b', 2);

// 1.8 Из Set пар (если Set содержит массивы)
const setOfPairs = new Set([['x', 10], ['y', 20]]);
const fromSet = new Map(setOfPairs);

// ============================================================
// 2. ОСНОВНЫЕ МЕТОДЫ И СВОЙСТВА
// ============================================================
const m = new Map([['a', 1], ['b', 2]]);

// 2.1 Размер
console.log('size:', m.size); // 2

// 2.2 Добавление/изменение (set)
m.set('c', 3);
m.set('a', 100); // перезаписывает существующий ключ
console.log('after set:', [...m]); // [['a',100], ['b',2], ['c',3]]

// 2.3 Получение значения (get)
console.log('get("b"):', m.get('b')); // 2
console.log('get("z"):', m.get('z')); // undefined

// 2.4 Проверка наличия (has)
console.log('has("a"):', m.has('a')); // true
console.log('has("z"):', m.has('z')); // false

// 2.5 Удаление одного элемента (delete)
const deleted = m.delete('b');
console.log('deleted b:', deleted); // true
console.log('after delete:', [...m]); // [['a',100], ['c',3]]

// 2.6 Очистка всех (clear)
m.clear();
console.log('after clear size:', m.size); // 0

// ============================================================
// 3. ОСОБЕННОСТИ КЛЮЧЕЙ
// ============================================================

// 3.1 Ключи любого типа (не только строки, в отличие от объекта)
const special = new Map();
special.set(1, 'number');
special.set('1', 'string');
special.set(true, 'boolean');
special.set({}, 'object');
special.set(Symbol('id'), 'symbol');
console.log('keys:', [...special.keys()]); // [1, '1', true, {}, Symbol(id)]

// 3.2 Сравнение ключей: используется SameValueZero (как Object.is)
// NaN равен NaN (в отличие от ===)
special.set(NaN, 'NaN');
special.set(NaN, 'another NaN'); // перезаписывает, т.к. NaN === NaN в Map
console.log('NaN value:', special.get(NaN)); // 'another NaN'

// 3.3 Объекты сравниваются по ссылке
const keyA = {};
const keyB = {};
special.set(keyA, 'A');
special.set(keyB, 'B');
console.log('get keyA:', special.get(keyA)); // 'A'
console.log('get keyB:', special.get(keyB)); // 'B'

// 3.4 -0 и +0 считаются равными
special.set(-0, 'minus zero');
console.log(special.get(+0)); // 'minus zero'

// ============================================================
// 4. ИТЕРАЦИЯ
// ============================================================
const data = new Map([['x', 1], ['y', 2], ['z', 3]]);

// 4.1 for...of по записям (по умолчанию)
console.log('for...of entries:');
for (const [key, value] of data) {
    console.log(key, value);
}

// 4.2 for...of по ключам
console.log('keys:');
for (const key of data.keys()) {
    console.log(key);
}

// 4.3 for...of по значениям
console.log('values:');
for (const val of data.values()) {
    console.log(val);
}

// 4.4 forEach (обратите внимание: value, key, map)
console.log('forEach:');
data.forEach((value, key, map) => {
    console.log(`${key} => ${value}`);
});

// 4.5 entries() – итератор пар
console.log('entries():', [...data.entries()]); // [['x',1], ['y',2], ['z',3]]

// ============================================================
// 5. ПРЕОБРАЗОВАНИЯ
// ============================================================
const mapToConvert = new Map([['a', 1], ['b', 2], ['c', 3]]);

// 5.1 В массив пар (два способа)
const arr1 = Array.from(mapToConvert);
const arr2 = [...mapToConvert];
console.log('array of pairs:', arr1); // [['a',1], ['b',2], ['c',3]]

// 5.2 В массив ключей
const keysArr = [...mapToConvert.keys()]; // ['a','b','c']

// 5.3 В массив значений
const valuesArr = [...mapToConvert.values()]; // [1,2,3]

// 5.4 В объект (только если ключи – строки или числа)
const objFromMap = Object.fromEntries(mapToConvert);
console.log('object:', objFromMap); // { a:1, b:2, c:3 }

// 5.5 В JSON (требуется сериализация – обычно через объект)
const json = JSON.stringify(Object.fromEntries(mapToConvert));
console.log('JSON:', json); // '{"a":1,"b":2,"c":3}'

// ============================================================
// 6. СРАВНЕНИЕ С OBJECT (ключевые отличия)
// ============================================================
console.log('=== Map vs Object ===');
console.log('1. Ключи Map – любые типы, ключи Object – только строки/символы');
console.log('2. Map сохраняет порядок вставки, Object – числовые ключи сортируются');
console.log('3. Map имеет size, Object – надо считать Object.keys().length');
console.log('4. Map – итерируемый (for...of), Object – нет (только for...in или Object.keys)');
console.log('5. Map не имеет прототипа (по умолчанию), объект наследует от Object.prototype');
console.log('6. Map оптимизирован для частых добавлений/удалений');

// ============================================================
// 7. СТАТИЧЕСКИЕ МЕТОДЫ (не встроены, но есть группа Map.groupBy в ES2024)
// ============================================================
// 7.1 Map.groupBy (экспериментально, ES2024)
// const people = [{name:'Alice', age:30}, {name:'Bob', age:25}];
// const grouped = Map.groupBy(people, p => p.age);
// console.log(grouped); // Map { 30 => [{...}], 25 => [{...}] }

// ============================================================
// 8. WEAKMAP (кратко)
// ============================================================
// WeakMap – ключи только объекты, нет size, не итерируется,
// автоматическое удаление при сборке мусора
const wm = new WeakMap();
let ref = {};
wm.set(ref, 'secret data');
console.log('WeakMap has ref:', wm.has(ref)); // true
ref = null; // после GC элемент может исчезнуть

// ============================================================
// 9. ПРОВЕРКА ТИПА
// ============================================================
const testMap = new Map();
console.log('typeof:', typeof testMap);                 // 'object'
console.log('instanceof Map:', testMap instanceof Map); // true
console.log('toString:', Object.prototype.toString.call(testMap)); // '[object Map]'

// ---------------------------------------------------------------------------------------------------------------------
// ============================================================
// 10. ДЕМОНСТРАЦИЯ ВАШЕГО ОРИГИНАЛЬНОГО КОДА
// (с операциями, которые работают и не работают)
// ============================================================
let src;

// 1=массив пар
src = new Map([
    ['name', 'value'],
    [11, '11'],
    [true, 'boolean key'],   // ключ может быть любого типа
]);

// 2=из объекта
src = new Map(Object.entries({11:11, 22:22, name:"value"}));

console.log(src);
console.log(String(src));    // [object Map]

// ОБРАЩЕНИЕ К ЗНАЧЕНИЮ (неправильные способы)
// 1=index (не работает)
console.log(src[0]);  // undefined

// 2=item через квадратные скобки (не работает)
console.log(src["11"]);  // undefined
console.log(src[11]);    // undefined

// 3=get (правильный способ)
console.log(src.get("11"));  // 11  – ключ "11" есть
console.log(src.get(11));    // undefined – такого ключа нет (число 11, а не строка)

// 4=dot (не работает)
console.log(src.name);  // undefined

// 5=add/del (правильные методы)
src.set('key', 'value');
src.delete(11);
console.log(src.has(11)); // false

// ============================================================
// 11. ПОЛЕЗНЫЕ ПРИЁМЫ
// ============================================================
const sample = new Map([['a', 1], ['b', 2], ['c', 3]]);

// 11.1 Преобразование ключей в массив и обратно
const keys = [...sample.keys()];
const newMap = new Map(keys.map(k => [k, sample.get(k) * 10]));

// 11.2 Фильтрация по значению
const filtered = new Map([...sample].filter(([k, v]) => v > 1));

// 11.3 Слияние двух Map (последний перезаписывает)
const mapA = new Map([['a', 1], ['b', 2]]);
const mapB = new Map([['b', 20], ['c', 3]]);
const mergedMap = new Map([...mapA, ...mapB]);
console.log('merged:', [...mergedMap]); // [['a',1], ['b',20], ['c',3]]

// 11.4 Преобразование в объект с кастомными ключами
const objFromMap2 = Object.fromEntries([...sample].map(([k,v]) => [k.toUpperCase(), v]));
console.log('obj from map:', objFromMap2); // { A:1, B:2, C:3 }

console.log('=== Map справочник завершён ===');


// =====================================================================================================================
