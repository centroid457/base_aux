// =====================================================================================================================
function explore_source(source) {
    //    let source;
    //    source = {11:11, 22:22,};
    //    source = [11, 22];
    source = new Map([ [11,11], [22,22] ]);

    function print_step(step) { console.log(`-----step=[${step}]-----`) };

    steps = {
        STRING: (source) => { return String(source) },
        TYPEOF: (source) => { return typeof source },
        GETITEM: (source) => { return source[11] },
        FOR_i_IN: (source) => {
            result = [];
            for (const item in source) {
                result.push(item);
            }
            return result;
        },
        FOR_i_OF: (source) => {
            result = [];
            for (const item of source) {
                result.push(item);
            }
            return result;
        },
        FOR_i_OF_ENTRIES: (source) => {
            result = [];
            for (const item of Object.entries(source)) {
                result.push(item);
                //console.log([name,value] = item);
                console.log(item);
            }
            return result;
        },
    };

    //WORK ---------------------------------------------
    for (const [name, func] of Object.entries(steps)) {
        print_step(name);
        try {result = func(source)} catch (exc) {result = exc}
        console.log(result);
    }
}


// =====================================================================================================================
function type_reference__ARRAY() {
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
}


// ---------------------------------------------------------------------------------------------------------------------
function type_reference__SET() {
    // ============================================================
    // 1. СОЗДАНИЕ SET
    // ============================================================

    // 1.1 Пустой Set (самый частый)
    const empty = new Set();
    console.log('empty size:', empty.size); // 0

    // 1.2 Из массива (дубликаты игнорируются)
    const fromArray = new Set([1, 2, 3, 3, 4]); // {1,2,3,4}
    console.log('fromArray:', [...fromArray]); // [1,2,3,4]

    // 1.3 Из строки (разбивается на символы)
    const fromString = new Set('hello'); // {'h','e','l','o'} (две 'l' схлопнуты)
    console.log('fromString:', [...fromString]); // ['h','e','l','o']

    // 1.4 Из другого Set (клонирование)
    const original = new Set([1,2,3]);
    const cloned = new Set(original);
    console.log('cloned:', [...cloned]); // [1,2,3]

    // 1.5 Из любого итерируемого объекта (генератор)
    function* gen() { yield 'a'; yield 'b'; yield 'a'; }
    const fromGen = new Set(gen()); // {'a','b'}
    console.log('fromGen:', [...fromGen]);

    // 1.6 Из объекта (только значения, ключи теряются)
    const obj = { a: 1, b: 2, c: 1 };
    const fromObjValues = new Set(Object.values(obj)); // {1,2}
    console.log('fromObjValues:', [...fromObjValues]);

    // 1.7 Из Map (только значения, ключи теряются)
    const map = new Map([['a',1], ['b',2], ['c',1]]);
    const fromMapValues = new Set(map.values()); // {1,2}
    // или new Set(map) – тогда будут пары [key,value] – не то
    console.log('fromMapValues:', [...fromMapValues]);

    // 1.8 Через добавление по одному (после создания)
    const set = new Set();
    set.add(1);
    set.add(2);
    set.add(2); // игнорируется
    console.log('set:', [...set]); // [1,2]

    // ============================================================
    // 2. ОСНОВНЫЕ СВОЙСТВА И МЕТОДЫ
    // ============================================================
    const s = new Set([10, 20, 30]);

    // 2.1 Размер
    console.log('size:', s.size); // 3

    // 2.2 Добавление (цепочка)
    s.add(40).add(50);
    console.log('after add:', [...s]); // [10,20,30,40,50]

    // 2.3 Проверка наличия
    console.log('has(20):', s.has(20));  // true
    console.log('has(99):', s.has(99));  // false

    // 2.4 Удаление одного элемента
    const deleted = s.delete(20);
    console.log('deleted 20:', deleted); // true
    console.log('after delete:', [...s]); // [10,30,40,50]

    // 2.5 Очистка всех
    s.clear();
    console.log('after clear size:', s.size); // 0

    // ============================================================
    // 3. ОСОБЕННОСТИ РАВЕНСТВА (NaN и объекты)
    // ============================================================
    const spec = new Set();
    spec.add(NaN);
    spec.add(NaN);      // второй NaN игнорируется – они считаются равными
    console.log('NaN size:', spec.size); // 1

    // Объекты сравниваются по ссылке
    const a = {};
    const b = {};
    spec.add(a);
    spec.add(b);        // два разных объекта – разные
    spec.add(a);        // тот же объект – игнорируется
    console.log('objects size:', spec.size); // 3 (NaN + a + b)

    // ============================================================
    // 4. ИТЕРАЦИЯ
    // ============================================================
    const data = new Set(['x', 'y', 'z']);

    // 4.1 for...of (значения)
    console.log('for...of:');
    for (const item of data) {
        console.log(item);
    }

    // 4.2 forEach (с индексом, но индекс = значение)
    console.log('forEach:');
    data.forEach((value, valueAgain, set) => {
        console.log(value, valueAgain); // одинаковые
    });

    // 4.3 keys() – синоним values() (для совместимости с Map)
    console.log('keys():', [...data.keys()]); // ['x','y','z']

    // 4.4 values() – то же самое
    console.log('values():', [...data.values()]); // ['x','y','z']

    // 4.5 entries() – возвращает пары [значение, значение]
    console.log('entries():', [...data.entries()]); // [['x','x'], ['y','y'], ['z','z']]

    // ============================================================
    // 5. ПРЕОБРАЗОВАНИЯ
    // ============================================================
    const set2 = new Set([1,2,3]);

    // 5.1 В массив (два способа)
    const arr1 = Array.from(set2);
    const arr2 = [...set2];
    console.log('array:', arr1); // [1,2,3]

    // 5.2 В строку (через join)
    console.log('join:', [...set2].join(', ')); // "1, 2, 3"

    // 5.3 В объект (если нужны ключи – только если ключи строковые)
    const objFromSet = Object.fromEntries([...set2].map(v => [v, v]));
    console.log('object:', objFromSet); // {1:1, 2:2, 3:3}

    // ============================================================
    // 6. ОПЕРАЦИИ НАД МНОЖЕСТВАМИ (не встроены, но легко сделать)
    // ============================================================
    const A = new Set([1,2,3]);
    const B = new Set([2,3,4]);

    // 6.1 Объединение
    const union = new Set([...A, ...B]); // {1,2,3,4}

    // 6.2 Пересечение
    const intersection = new Set([...A].filter(x => B.has(x))); // {2,3}

    // 6.3 Разность (A \ B)
    const difference = new Set([...A].filter(x => !B.has(x))); // {1}

    console.log('union:', [...union]);
    console.log('intersection:', [...intersection]);
    console.log('difference:', [...difference]);

    // ============================================================
    // 7. WEAKSET (кратко)
    // ============================================================
    // WeakSet – только объекты, нет size, не итерируется, автоматическое удаление
    const ws = new WeakSet();
    let obj1 = {};
    ws.add(obj1);
    console.log('WeakSet has obj1:', ws.has(obj1)); // true
    obj1 = null; // после сборки мусора элемент может исчезнуть

    // ============================================================
    // 8. ПРОВЕРКА ТИПА
    // ============================================================
    console.log('typeof set:', typeof set2);              // 'object'
    console.log('instanceof Set:', set2 instanceof Set);  // true
    console.log('toString:', Object.prototype.toString.call(set2)); // '[object Set]'
}


// =====================================================================================================================
function type_reference__OBJECT() {
    const keyFromVar = 'keyFromVar';
    const shortStyle = 'shortStyle_Value';

    let source;

    source = {
        //ВСЕ КЛЮЧИ ПРЕОБРАЗУЮТСЯ В STR!

        // Литерал (предпочтительно)
        name: 'value',
        "name2": 'value2',
        //["arr1", 'arr11'],  // НЕЛЬЗЯ!!!
        //["arr1": 'arr11'],  // НЕЛЬЗЯ!!!

        "11": "intStr",
        11: "intInt",    //ПЕРЕЗАПИШЕТ! предыдущий!

        true: "bool",
        'key.with: specials!': "value.with: specials!",

        // dynamic keys
        [keyFromVar]: "valueFromVar",

        //shortStyle = Сокращённая запись свойств (ES6)
        shortStyle,
    };

    // ------------------------------------------------------
    console.log(source);
    //{11: 'intInt', name1: 'value1', name2: 'value2', true: 'bool', key.with: specials!: 'value.with: specials!', keyFromVar: 'valueFromVar', …}
    console.log(String(source));    //[object Object]

    // ОБРАЩЕНИЕ К ЗНАЧЕНИЮ ---------------------------------
    //1=index
    console.log(source[0]);  //undefined - ИЩЕТ КЛЮЧ А НЕ ИНДЕКС!

    //2=item
    console.log(source["11"]);  //intInt
    console.log(source[11]);    //intInt

    //3=get
    //console.log(source.get("11"));  //нет метода! Uncaught TypeError: source.get is not a function
    //console.log(source.get(11));    //нет метода! Uncaught TypeError: source.get is not a function

    //4=dot
    console.log(source.name);  //value - РАБОТАЕТ!!

    //5=add/del
    source = {11:11};
    source.nameNEW = "valueNEW";    //РАБОТАЕТ!
    console.log(String(source));    //

    //    source.push("valueNEW");        //undefined.push
    //    source.delete(11);              //некорретно! - ВСЕГДА УДАЛЯЕТ ТОЛЬКО ПОСЛЕДНИЙ!!!
}


// ---------------------------------------------------------------------------------------------------------------------
function type_reference__MAP() {
    let source;

    // 1=массив пар
    source = new Map([
      ['name', 'value'],
      [11, '11'],
      [true, 'boolean key'],   // ключ может быть любого типа
    ]);

    // 2=из обьекта
    source = new Map(Object.entries({11:11,22:22, name:"value"}));

    // ------------------------------------------------------
    console.log(source);
    console.log(String(source));    //[object Map]

    // ОБРАЩЕНИЕ К ЗНАЧЕНИЮ ---------------------------------
    //1=index
    console.log(source[0]);  //НЕЛЬЗЯ ТАК -> undefined - ТОЖЕ НЕЛЬЗЯ!

    //2=item
    console.log(source["11"]);  //undefined -> НЕЛЬЗЯ ТАК
    console.log(source[11]);    //undefined -> НЕЛЬЗЯ ТАК

    //3=get
    console.log(source.get("11"));  //11    ЕДИНСТВЕННО ВЕРНО!
    console.log(source.get(11));    //undefined -> НЕЛЬЗЯ ТАК - не преобразует!

    //4=dot
    console.log(source.name);  //undefined -> НЕЛЬЗЯ ТАК НЕКОРРЕКТНО!!!

    //5=add/del
    source.set('key', 'value');
}


// =====================================================================================================================
