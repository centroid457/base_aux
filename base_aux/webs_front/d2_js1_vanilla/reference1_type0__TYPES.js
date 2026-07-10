// =====================================================================================================================
// ТИПИЗАЦИЯ = TYPING
// --------------------------------------------
// прямо в строке коде!!! в любой
class Event {
  constructor(name, listeners) {
    this.name = name;

    /** @type {Map<string, Function>} */
    this._listeners = new Map();
// --------------------------------------------


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
