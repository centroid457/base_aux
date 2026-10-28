# ======================================================================================================================
"""
как отправить команду на устройство
1. настроить порт - требуется каждый раз после перезагрузки

2. отправить команду
timeout 5.0 cat /dev/ttyUSB2 & sleep 0.3; printf 'AT+CLBS=?\r\n' > /dev/ttyUSB2
"""
# ======================================================================================================================
import pytest


# ======================================================================================================================
AT_GROUPS: dict[str, dict[str, str | list[str, tuple[str, str]]]] = {
    # =========================================================================
    # СТРУКТУРА группы команд!!!
    # -------------------------------------------------------------------------
    # 0=DANGER+USELESS -------------------------------
    # 1=ACCURATE -------------------------------------
    # 2=DOUBT ----------------------------------------
    # 3=UNKNOWN --------------------------------------

    # =========================================================================
    # =========================================================================
    # =========================================================================
    # GROUPS
    # =========================================================================
    "--=V25TER_BASIC(V.25TER БАЗОВЫЕ/управление/настройки модемом)": {
        # 0=DANGER+USELESS -------------------------------
        # "A/": "[DANGER]повторить последнюю команду",

        # "ATD": "dial (голосовой/данные)",
        # "ATD><mem><n>": "dial из памяти (SM/ME/DC...)",
        # "ATD><n>": "dial из активной памяти",
        # "ATD><str>": "dial по имени из памяти",
        # "ATA": "[DANGER]answer (ответ на входящий)",
        # "ATH": "[DANGER]hang up (положить трубку)",
        # "ATS0": "[DANGER]auto-answer (число гудков)",
        # "+++": "[DANGER]escape из data mode в command mode",
        # "ATO": "[DANGER]вернуться в data mode",
        # "AT+ICF": "[DANGER]character framing (data/parity/stop)",
        # "AT+IFC": "[DANGER]flow control (RTS/CTS)",
        # "AT&C": "[DANGER]DCD function mode",
        # "AT&D": "[DANGER]DTR function mode",
        # "AT&S": "[DANGER]DSR function mode",
        # "AT&F": "[DANGER]factory defaults=for all settings!",
        # "ATQ": "[DANGER]result code presentation mode",
        # "AT&W": "[DANGER]save user settings",
        # "ATZ": "[DANGER]restore user settings",
        # 'AT+IPR': ['[NONEUSEFULL]baud rate (temporarily)',
        #            ('AT+IPR=?',
        #             '+IPR: (300,600,1200,2400,4800,9600,19200,38400,57600,115200,230400,460800,921600,1842000,3686400)\nOK'),
        #            ('AT+IPR', 'OK'),
        #            ('AT+IPR?', '+IPR: 115200\nOK'),
        #            ('AT+IPR=300', 'OK'),
        #            ('AT+IPR?', '+IPR: 300\nOK'),
        #            ('AT+IPR=600', 'OK'),
        #            ('AT+IPR?', '+IPR: 600\nOK'),
        #            ('AT+IPR=1200', 'OK'),
        #            ('AT+IPR?', '+IPR: 1200\nOK'),
        #            ('AT+IPR=2400', 'OK'),
        #            ('AT+IPR?', '+IPR: 2400\nOK'),
        #            ('AT+IPR=4800', 'OK'),
        #            ('AT+IPR?', '+IPR: 4800\nOK'),
        #            ('AT+IPR=9600', 'OK'),
        #            ('AT+IPR?', '+IPR: 9600\nOK'),
        #            ('AT+IPR=19200', 'OK'),
        #            ('AT+IPR?', '+IPR: 19200\nOK'),
        #            ('AT+IPR=38400', 'OK'),
        #            ('AT+IPR?', '+IPR: 38400\nOK'),
        #            ('AT+IPR=57600', 'OK'),
        #            ('AT+IPR?', '+IPR: 57600\nOK'),
        #            ('AT+IPR=115200', 'OK'),
        #            ('AT+IPR?', '+IPR: 115200\nOK'),
        #            ],
        # 'AT+IPREX': ['[NONEUSEFULL]bbaud rate (permanently)',
        #              ('AT+IPREX=?',
        #               '+IPREX: (300,600,1200,2400,4800,9600,19200,38400,57600,115200,230400,460800,921600,1842000,3686400)\nOK'),
        #              ('AT+IPREX', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 115200\nOK'),
        #              ('AT+IPREX=300', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 300\nOK'),
        #              ('AT+IPREX=600', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 600\nOK'),
        #              ('AT+IPREX=1200', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 1200\nOK'),
        #              ('AT+IPREX=2400', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 2400\nOK'),
        #              ('AT+IPREX=4800', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 4800\nOK'),
        #              ('AT+IPREX=9600', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 9600\nOK'),
        #              ('AT+IPREX=19200', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 19200\nOK'),
        #              ('AT+IPREX=38400', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 38400\nOK'),
        #              ('AT+IPREX=57600', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 57600\nOK'),
        #              ('AT+IPREX=115200', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 115200\nOK'),
        #              ],

        # нетиповая команда!!!
        "-ATE": ["echo on/off, ATE0->off, ATE1->on",
                 ('ATE=?', 'ERROR'),
                 ('ATE', 'OK'),
                 ('ATE?', 'ERROR'),
                 ],
        "-ATE0": ["echo off=its not about OK! just not repeating source command",
                  ('ATE0=?', 'ERROR'),
                  ('ATE0', 'OK'),
                  ('ATE0?', 'ERROR'),
                  ],
        "-ATE1": ["echo on",
                  ('ATE1=?', 'ERROR'),
                  ('ATE1', 'OK'),
                  ('ATE1?', 'ERROR'),
                  ],
        #
        'ATV': ['result code format (numeric/verbose)',
                # с симкой и без
                ('ATV=?', 'ERROR'),
                ('ATV', 'OK'),
                ('ATV?', 'ERROR'),
                ],
        'ATX': ['CONNECT result code format',
                # с симкой и без
                ('ATX=?', 'ERROR'),
                ('ATX', 'OK'),
                ('ATX?', 'ERROR'),
                ],
        'AT&E': ['CONNECT result code format (speed)',
                 ('AT&E=?', 'ERROR'),
                 ('AT&E', 'ERROR'),  # без симки
                 ('AT&E', 'OK'),  # с симкой
                 ('AT&E?', 'ERROR'),
                 ],
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
        'AT&V': ['display current configuration=',
                 # AT&V=ДОЛЖЕН ПОКАЗАТЬ НАСТРОЙКИ!!!
                 # &C: 0; &D: 2; &F: 0; E: 1; L: 0; M: 0; Q: 0; V: 1; X: 0; Z: 0; S0: 0;
                 # S3: 13; S4: 10; S5: 8; S6: 2; S7: 50; S8: 2; S9: 6; S10: 14; S11: 95;
                 # +FCLASS: 0; +ICF: 3,3; +IFC: 2,2; +IPR: 115200; +DR: 0; +DS: 0,0,2048,6;
                 # +WS46: 12; +CBST: 0,0,1;
                 # ……
                 # OK
                 ('AT&V=?', 'ERROR'),
                 ('AT&V', 'ERROR'),  # без симки
                 ('AT&V',  # с симкой
                  '&C: 1; &D: 0; &F: 0; &W: 0; E: 0; Q: 0; V: 1; X: 1; Z: 0; S0: 0; S2: 43; S3: 13; S4: 10; S5: 8; S6: 2; S7: 1; S8: 2; S9: 6; S10: 7; S11: 63; S30: 10; +FCLASS: 0; +IFC: 0,0; +IPR: 115200; +CSCS: UCS2; +CREG: 0; +CGREG: 0; +CEREG: 0; +CGDCONT: (1,"IP","next"); +CGDSCONT: ; +CGACT: (1,0); +CGEQMIN: (1,4,0,0,0,0,2,0,"0E0","0E0",3,0,0,0,0); +CGQMIN: (1,3,4,5,1,1); +CGEREP: (2,0); +CGCLASS: "A"; +CGAUTH: (1,0); +CPBS: "SM"; +CMEE: 2; +CFUN: 1; +CMGF: 0; +CSCA: ("++79006199795",145); +CSMP: 17,167,0,0; +CSDH: 0; +CPMS: "SM",0,30,"SM",0,30,"SM",0,30;\nOK'),
                 ('AT&V?', 'ERROR'),
                 ],
    },
    # =========================================================================
    "-1=MODEM": {
        # 0=DANGER+USELESS -------------------------------

        # "AT+CSCS": "[DANGER]выбор TE character set (IRA/GSM/UCS2/HEX)",
        # "AT+SIMEI": "[DANGER]установка IMEI (только для service)",
        # "AT+CUSBPIDSWITCH": "[DANGER]смена USB PID (перезагружает модуль!)",
        # "AT+CLCK": "[DANGER] facility lock (блокировка SIM/сети)",
        # "AT+CSCLK": "[DANGER]UART sleep control",
        # "AT+CMUX": "[DANGER]мультиплексор UART (4 виртуальных порта) # DANGER",
        # "AT+CUSBPIDSWITCH": "[DANGER]смена USB PID # DANGER (reset)",

        # MAIN PWR ----------------------------------------
        '---AT+CPOF': ['[DANGER]Power down the module=фактически перезагрузка!!!',
                    ('AT+CPOF=?', '+CPOF: (0,1)\nOK'),
                    ('AT+CPOF', 'OK\nPOWER DOWN'),
                    ('AT+CPOF?', 'ERROR'),
                    ('AT+CPOF=1', 'OK\nPOWER DOWN'),

                    # NAVIA
                    ('AT+CPOF=?', 'OK'),
                    ('AT+CPOF', '''OK
                    
                    ---- Sent utf8 encoded message: "AT+CPOF\r\n" ----
                    AT+CPOF
                    OK
                    +CGEV: ME DETACH
                    *ATREADY: 1
                    +CPIN: READY
                    SMS DONE
                    +CGEV: EPS PDN ACT 1
                    PB DONE
                    '''),
                    ('AT+CPOF?', 'ERROR'),
                    ('AT+CPOF=1', 'OK\nPOWER DOWN'),
                    ],
        '---AT+CRESET': ['[DANGER]Reset the module',
                        ('AT+CRESET=?', 'OK'),
                        ('AT+CRESET', 'OK'),  # ЗДЕСЬ ПЕРЕЗАГРУЗИТСЯ!!!
                        ('AT+CRESET?', 'ERROR'),
                        ],

        # DIAGNOSTIC ----------------------------------
        'AT': ['эхо, проверка связи с модемом=ответ OK если связь есть',
               # без симки + с симкой
               ('AT=?', 'ERROR'),
               ('AT', 'OK'),
               ('AT?', 'ERROR'),
               ],

        # SETTINGS ----------------------------------
        'AT+CMEE': ['формат ошибок (+CME ERROR: numeric/verbose)',
            ('AT+CMEE=?', '+CMEE: (0-2)\nOK'),
            ('AT+CMEE', 'OK'),
            ('AT+CMEE?', '+CMEE: 2\nOK'),
            ('AT+CMEE=0', 'OK'),
            ('AT+CMEE?', '+CMEE: 0\nOK'),
            ('AT+CMEE=1', 'OK'),
            ('AT+CMEE?', '+CMEE: 1\nOK'),
            ('AT+CMEE=2', 'OK'),
            ('AT+CMEE?', '+CMEE: 2\nOK'),
            ],

        # ID -------------------------------------
        'ATI': ['информация о производителе/модели/ревизии/IMEI',
            # без симки + с симкой
            # HARVESTER
            ('ATI=?', 'ERROR'),
            ('ATI', 'Manufacturer: INCORPORATED\nModel: A7682E-R\nRevision: A7682M6_V1.11.1\nIMEI1: 865286077380516\nIMEI2: 865286076965218\n+GCAP: +CGSM,+FCLASS,+DS\nOK'),
            ('ATI?', 'ERROR'),

            # NAVIA
            ('ATI',
                '''
                Manufacturer: INCORPORATED
                Model: A7672E-FASE
                Revision: A7672M7_V1.11.1
                IMEI: 868569082628848
                +GCAP: +CGSM,+FCLASS,+DS
                '''),
                ],
        # ATI1 - 9 TODO: add???
        'AT+CGMI': ['ID=manufacturer',
            # без симки + с симкой
            ('AT+CGMI=?', 'OK'),
            ('AT+CGMI', 'INCORPORATED\nOK'),
            ('AT+CGMI?', 'INCORPORATED\nOK'),
            ],
        'AT+CGMM': ['ID=model',
            # без симки + с симкой
            ('AT+CGMM=?', 'OK'),
            ('AT+CGMM', 'A7682E-R\nOK'),
            ('AT+CGMM?', 'A7682E-R\nOK'),
            ],
        'AT+CGMR': ['ID=revision',
                    # без симки + с симкой
                    ('AT+CGMR=?', 'OK'),
                    ('AT+CGMR', '+CGMR: A011B02A7682M6_DS_FOTA\nOK'),
                    ('AT+CGMR?', '+CGMR: A011B02A7682M6_DS_FOTA\nOK'),
                    ],
        'AT+CGSN': ['ID=IMEI / serial number / ProductSn',
                    # без симки + с симкой
                    ('AT+CGSN=?', 'OK'),
                    ('AT+CGSN', '865286077380516\nOK'),
                    ('AT+CGSN?', 'ERROR'),
                    ],
        'AT+GSN': ['ID=IMEI (алиас)',
                   # без симки + с симкой
                   ('AT+GSN=?', 'OK'),
                   ('AT+GSN', '865286077380516\nOK'),
                   ('AT+GSN?', 'ERROR'),
                   ],



        'AT+CPAS': ['phone activity status',
                    # без симки + с симкой
                    ('AT+CPAS=?', '+CPAS: (0,3,4)\nOK'),
                    ('AT+CPAS', '+CPAS: 0\nOK'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=0', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=3', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=4', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ],
        'AT+CCLK?': ['real time clock',
                     # без симки + с симкой
                     ('AT+CCLK=?', 'OK'),
                     ('AT+CCLK', 'ERROR'),
                     ('AT+CCLK?', '+CCLK: "70/01/01,00:23:56+00"\nOK'),
                     ],
        'AT+CATR?': ['''URC destination interface=used to configure the serial port which will be used to output URCs.
        7500_SIM7600 Series_AT Command Manual_V1.10 6 4 2018-10-08
<port>
0 – all ports
1 – use UART port to output URCs
2 – use MODEM port to output URCs
3 – use ATCOM port to output URCs
4 – use cmux vritual port1 to output URCs
5 – use cmux virtual port2 to output URCs
6 – use cmux vritual port3 to output URCs
7 – use cmux vritual port4 to output URCs
        ''',
             # без симки + с симкой
             ('AT+CATR=?', '+CATR: (0-7)\nOK'),
             ('AT+CATR', 'ERROR'),
             ('AT+CATR?', '+CATR: 0\nOK'),
             ('AT+CATR=0', 'OK'),
             ('AT+CATR?', '+CATR: 0\nOK'),
             ('AT+CATR=1', 'OK'),
             ('AT+CATR?', '+CATR: 1\nOK'),
             ('AT+CATR=2', 'OK'),
             ('AT+CATR?', '+CATR: 2\nOK'),
             ('AT+CATR=3', 'OK'),
             ('AT+CATR?', '+CATR: 3\nOK'),
             ('AT+CATR=4', 'OK'),
             ('AT+CATR?', '+CATR: 4\nOK'),
             ('AT+CATR=5', 'OK'),
             ('AT+CATR?', '+CATR: 5\nOK'),
             ('AT+CATR=6', 'OK'),
             ('AT+CATR?', '+CATR: 6\nOK'),
             ('AT+CATR=7', 'OK'),
             ('AT+CATR?', '+CATR: 7\nOK'),
             ],
        'AT+CSPN?': ['service provider name',
             # без симки
             ('AT+CSPN=?', 'ERROR'),
             ('AT+CSPN', 'ERROR'),
             ('AT+CSPN?', 'ERROR'),

             # с симкой
             ('AT+CSPN=?', 'OK'),
             ('AT+CSPN', 'ERROR'),
             ('AT+CSPN?', '+CSPN: "Next Mobile",1\nOK'),
             ],
        'AT+GCAP?': ['''список поддерживаемых возможностей (+CGSM, +FCLASS, +DS)
            List of additional capabilities.
            +CGSM GSM function is supported
            +FCLASS FAX function is supported
            +DS Data compression is supported
            +ES Synchronous data mode is supported.
            +CIS707-A CDMA data service command set
            +CIS-856 EVDO data service command set
            +MS Mobile Specific command set
            
            AT+GCAP
            +GCAP:+CGSM,+FCLASS,+DS
            OK
            ''',
             # без симки
             ('AT+GCAP=?', 'OK'),
             ('AT+GCAP', 'ERROR'),
             ('AT+GCAP?', 'ERROR'),

             # с симкой
             ('AT+GCAP=?', 'OK'),
            ('AT+GCAP', '+GCAP: +CGSM,+FCLASS,+DS\nOK'),
            ('AT+GCAP?', '+GCAP: +CGSM,+FCLASS,+DS\nOK'),
            ],
        # 2=DOUBT ----------------------------------------
        'AT+CACM?': ['accumulated call meter',
                     # без симки + с симкой
                     ('AT+CACM=?', 'OK'),
                     ('AT+CACM', '+CME ERROR: Operation not supported'),
                     ('AT+CACM?', '+CME ERROR: unknown error'),
                     ],
        'AT+CAMM?': ['accumulated call meter maximum',
                     # без симки + с симкой
                     ('AT+CAMM=?', 'OK'),
                     ('AT+CAMM', '+CME ERROR: Operation not supported'),
                     ('AT+CAMM?', '+CME ERROR: unknown error'),
                     ],
        '-AT+CPUC?': ['price per unit and currency',
                     # без симки + с симкой
                     ('AT+CPUC=?', 'OK'),
                     ('AT+CPUC', 'ERROR'),
                     ('AT+CPUC?', '+CME ERROR: unknown error'),
                     ],

        '-AT+CGGMM': ['model identification (SIMCom-вариант)',
            # без симки + с симкой
            ('AT+CGGMM=?', 'ERROR'),
            ('AT+CGGMM', 'ERROR'),
            ('AT+CGGMM?', 'ERROR'),
            ],
        '-AT+CGGMR': ['revision identification (SIMCom-вариант)',
            # без симки + с симкой
            ('AT+CGGMR=?', 'ERROR'),
            ('AT+CGGMR', 'ERROR'),
            ('AT+CGGMR?', 'ERROR'),
            ],
        '-AT+SMEID': ['MEID (CDMA)',
            # без симки + с симкой
            ('AT+SMEID=?', 'ERROR'),
            ('AT+SMEID', 'ERROR'),
            ('AT+SMEID?', 'ERROR'),
            ],
    },

    # =========================================================================
    "-2=GSM-1=SIM": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CPWD": "[DANGER]смена пароля (PIN/PUK)",

        '--AT+CSVM': ['[USELESS]voice mail subscriber number',
            ('AT+CSVM=?', 'ERROR'),
            ('AT+CSVM', 'ERROR'),
            ('AT+CSVM?', 'ERROR'),
            ],

        # DIAGNOSTIC -------------------------------------
        'AT+CPIN?': ['проверка присутствия SIM=статус PIN (READY / SIM PIN / SIM PUK)',
                     ('AT+CPIN=?', 'OK'),
                     ('AT+CPIN', 'ERROR'),
                     ('AT+CPIN?', '+CME ERROR: SIM not inserted'),  # без симки
                     ('AT+CPIN?', '+CPIN: READY\nOK'),  # с симкой
                     ],
        'AT+SPIC': ['остаток попыток ввода PIN/PUK',
                    ('AT+SPIC=?', 'OK'),
                    ('AT+SPIC', '+CME ERROR: SIM not inserted'),  # без симки
                    ('AT+SPIC', '+SPIC: 3,10,3,10\nOK'),  # с симкой
                    ('AT+SPIC?', 'ERROR'),
                    ],
        'AT+CPINR?': ['',
                      # no sim
                      ('AT+CPINR=?', '+CPINR: (0-3),(0-3),(0-10),(0-10)\nOK'),
                      ('AT+CPINR', '+CME ERROR: Operation not supported'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=0', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=1', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=2', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=3', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=4', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=5', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=6', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=7', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=8', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=9', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),

                      # sim
                      ('AT+CPINR=?', '+CPINR: (0-3),(0-3),(0-10),(0-10)\nOK'),
                      ('AT+CPINR', '+CME ERROR: Operation not supported'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=0', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=1', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=2', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=3', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=4', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=5', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=6', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=7', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=8', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ('AT+CPINR=9', 'ERROR'),
                      ('AT+CPINR?', '+CPINR:3,3,10,10\nOK'),
                      ],
        # ID -------------------------------------
        'AT+CNUM?': ['основной запрос номера (недоступен на M2M sim)',
                     # ПРИМЕР ИЗ ДОКУМЕНТАЦИИ ------------------------
                     # [+CNUM: <alpha>,<number>,<type>[<CR><LF>
                     # +CNUM: <alpha>, <number>,<type> [...]]]

                     # +CNUM: "","13697252277",129

                     # РЕАЛЬНО НА M2M sim - harvester ------------------------
                     # без симки
                     ('AT+CNUM=?', 'ERROR'),
                     ('AT+CNUM', 'ERROR'),
                     ('AT+CNUM?', 'ERROR'),

                     # с симкой!!! +navia
                     ('AT+CNUM=?', 'OK'),
                     ('AT+CNUM', 'OK'),
                     ('AT+CNUM?', '+CME ERROR: Operation not supported'),
                     ],
        'AT+CICCID': ['ICCID SIM-карты',
                      # без симки
                      ('AT+CICCID=?', 'OK'),
                      ('AT+CICCID', '+CME ERROR: SIM not inserted'),
                      ('AT+CICCID?', '+CME ERROR: SIM not inserted'),

                      # с симкой!!!
                      ('AT+CICCID=?', 'OK'),
                      ('AT+CICCID', '+ICCID: 8970147000029053642\nOK'),
                      ('AT+CICCID?', '+CME ERROR: Operation not supported'),
                      ],
        'AT+CIMI': ['IMSI (IMSI SIM-карты) international mobile subscriber identity (460010222028133)',
                    ('AT+CIMI=?', 'OK'),
                    ('AT+CIMI', '+CME ERROR: SIM failure'),   # без симки
                    ('AT+CIMI', '250470002905364\nOK'),       # с симкой navia
                    ('AT+CIMI?', '+CME ERROR: Operation not supported'),
                    ],
        '---AT+CIMIM': ['IMSI (второй симки?) (USIM)',
                        # с симкой и без!
                        ('AT+CIMIM=?', 'ERROR'),
                        ('AT+CIMIM', 'ERROR'),
                        ('AT+CIMIM?', 'ERROR'),
                        ],
        '--AT+CEID': ['Read EID from eSIM card',
                    # ДИПСИК
                    ('AT+CEID=?', 'OK'),
                    ('AT+CEID', '+EID:3506000000000000025000000764040\nOK'),
                    ('AT+CEID?', 'ERROR'),

                    # NAVIA
                    ('AT+CEID=?', 'ERROR'),
                    ('AT+CEID', 'ERROR'),
                    ('AT+CEID?', 'ERROR'),
                    ],
    },

    # =========================================================================
    "-4=GSM=STATUS_CONTROL(управление состоянием)": {
        # 0=DANGER+USELESS -------------------------------
        '-AT+CFUN': ["[DANGER]уровень функциональности (0=min, 1=full, 4=offline(flight), 7=reset)",
            ('AT+CFUN=?', '+CFUN: (0-1,4-8),(0-1)\nOK'),
            ('AT+CFUN', 'ERROR'),
            ('AT+CFUN?', '+CFUN: 1\nOK'),
            ('AT+CFUN=0', '+SIMCARD: NOT AVAILABLE\n+CGEV: ME DETACH\nOK'),
            ('AT+CFUN=0', '+SIMCARD: NOT AVAILABLE\n+CGEV: ME DETACH\n+CGEV: NW PDN DEACT 1\nOK'),  # navia
            ('AT+CFUN?', '+CFUN: 0\nOK'),
            ('AT+CFUN=1', 'OK\n+CPIN: SIM REMOVED\nOK'),
            ('AT+CFUN=1', '''
                OK
                +CPIN: READY
                +CGEV: EPS PDN ACT 1
                SMS DONE
                PB DONE'''),      # navia

            ('AT+CFUN?', '+CFUN: 1\nOK'),
            ('AT+CFUN=4', '+CGEV: ME DETACH\nOK'),
            ('AT+CFUN=4', '''
                +CGEV: ME DETACH
                +CGEV: NW PDN DEACT 1
                OK
                '''),
            ('AT+CFUN?', '+CFUN: 4\nOK'),
            ('AT+CFUN=5', 'OK'),
            ('AT+CFUN?', '+CFUN: 5\nOK'),
            ('AT+CFUN=6', 'OK\n+CGEV: ME DETACH'),
            ('AT+CFUN?',
             'cat: /dev/ttyUSB4: No such file or directory\n[1]+  Exit 1                  timeout 5.0 cat /dev/ttyUSB4'),
            ('AT+CFUN=7', 'AT+CFUN?\n[1]+  Done                    timeout 5.0 cat /dev/ttyUSB4'),
            ('AT+CFUN?', 'AT+CFUN=7\n[1]+  Done                    timeout 5.0 cat /dev/ttyUSB4'),
            ('AT+CFUN=8', 'AT+CFUN?\n[1]+  Done                    timeout 5.0 cat /dev/ttyUSB4'),
            ('AT+CFUN?', 'AT+CFUN=8\n[1]+  Done                    timeout 5.0 cat /dev/ttyUSB4'),
        ],
        # "AT+CMEE": "error format",
        '--AT+SIMEI': ['[DANGER]Set IMEI for the module',
                     ('AT+SIMEI=?', 'OK'),
                     ('AT+SIMEI', 'ERROR'),
                     ('AT+SIMEI?', '+SIMEI: 357396012183175\nOK'),
                     ('AT+SIMEI=357396012183175', 'OK'),
                     ],

        # 1=ACCURATE -------------------------------------
        'AT+CSQ': ['signal quality (RSSI, BER) разные значения не нужны! это строго чтение, а не запись! чем больше тем лучше! 99=неизвестно',
                   ('AT+CSQ=?', '+CSQ: (0-31,99),(0-7,99)\nOK'),
                   ('AT+CSQ', '+CSQ: 12,99\nOK'),   # БЕЗ АНТЕННЫ!!! с симкой
                   ('AT+CSQ', '+CSQ: 18,99\nOK'),   # момент включения антенны-1
                   ('AT+CSQ', '+CSQ: 19,99\nOK'),   # момент включения антенны-2
                   ('AT+CSQ', '+CSQ: 21,99\nOK'),   # момент включения антенны-3
                   ('AT+CSQ', '+CSQ: 20,99\nOK'),   # момент включения антенны-4
                   ('AT+CSQ', '+CSQ: 21,99\nOK'),   # момент включения антенны-5

                   ('AT+CSQ', '+CSQ: 23,0\nOK'),    # без симки
                   ('AT+CSQ', '+CSQ: 25,0\nOK'),    # с симкой
                   ('AT+CSQ', '+CSQ: 28,99\nOK'),   # с симкой

                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=0', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=1', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=2', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=3', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=4', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=5', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=6', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=7', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=8', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=9', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ],
        'AT+AUTOCSQ?': ['автоматический отчёт CSQ',
                        # без и с симкой
                        ('AT+AUTOCSQ=?', '+AUTOCSQ: (0-1),(0-1)\nOK'),
                        ('AT+AUTOCSQ', 'ERROR'),
                        ('AT+AUTOCSQ?', '+AUTOCSQ: 1,0\nOK'),
                        ('AT+AUTOCSQ=0', 'OK'),
                        ('AT+AUTOCSQ?', '+AUTOCSQ: 0,0\nOK'),
                        ('AT+AUTOCSQ=1', 'OK'),
                        ('AT+AUTOCSQ?', '+AUTOCSQ: 1,0\nOK'),
                        ],
        'AT+CSQDELTA?': ['set RSSI delta threshold for signal strength reporting.',
                         # без и с симкой
                         ('AT+CSQDELTA=?', '+CSQDELTA: (0-5)\nOK'),
                         ('AT+CSQDELTA', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 5\nOK'),
                         ('AT+CSQDELTA=0', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 0\nOK'),
                         ('AT+CSQDELTA=1', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 1\nOK'),
                         ('AT+CSQDELTA=2', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 2\nOK'),
                         ('AT+CSQDELTA=3', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 3\nOK'),
                         ('AT+CSQDELTA=4', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 4\nOK'),
                         ('AT+CSQDELTA=5', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 5\nOK'),
                         ],

        'AT+CPAS': ['phone activity status',
                    # без и с симкой
                    ('AT+CPAS=?', '+CPAS: (0,3,4)\nOK'),
                    ('AT+CPAS', '+CPAS: 0\nOK'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=0', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=3', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=4', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ],
        # 2=DOUBT ----------------------------------------
        'AT+CSIM': ['generic SIM access (APDU)',
                    # без и с симкой
                    ('AT+CSIM=?', 'OK'),
                    ('AT+CSIM', 'ERROR'),
                    ('AT+CSIM?', '+CME ERROR: Operation not supported'),
                    ],
        'AT+CRSM': ['restricted SIM access (READ/UPDATE BINARY/RECORD)',
                    # без и с симкой
                    ('AT+CRSM=?', 'OK'),
                    ('AT+CRSM', 'ERROR'),
                    ('AT+CRSM?', '+CME ERROR: Operation not supported'),
                    ],

        # 3=UNKNOWN --------------------------------------
        '---AT+CSVM': ['voice mail number',
                    # без и с симкой
                    ('AT+CSVM=?', 'ERROR'),
                    ('AT+CSVM', 'ERROR'),
                    ('AT+CSVM?', 'ERROR'),
                    ],
    },

    # =========================================================================
    "-5=GSM-2=NETWORK(СЕТЬ/РЕГИСТРАЦИЯ/ОПЕРАТОР)": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CLCK": "[DANGER]facility lock (network)",
        # "AT+CPWD": "[DANGER]change password",
        # "AT+CCUG": "[DANGER]closed user group",
        # "AT+CNMP": "[DANGER]preferred mode selection",
        # "AT+CNBP": """[DANGER]preferred band selection
            # Value:
            # 0xFFFFFFFF7FFFFFFF Any (any value)
            # 7 GSM_DCS_1800
            # 8 GSM_EGSM_900
            # 9 GSM_PGSM_900
            # 16 GSM_450
            # 17 GSM_480
            # 18 GSM_750
            # 19 GSM_850
            # 20 GSM_RGSM_900
            # 21 GSM_PCS_1900
            # 22 WCDMA_IMT_2000
            # 23 WCDMA_PCS_1900
            # 24 WCDMA_III_1700
            # 25 WCDMA_IV_1700
            # 26 WCDMA_850
            # 27 WCDMA_800
            # 48 WCDMA_VII_2600
            # 49 WCDMA_VIII_900
            # 50 WCDMA_IX_1700
        # """,
        # "AT+NETMODE": "[DANGER]WCDMA/TDSCDMA mode select",
        # "AT+WS46": "[DANGER]RAT selection (12=LTE, 22=..., 28=...)",

        # 'AT+COPN': ['[#FIXME!]read operator names (BLOCKING) ЭТО ВООБЩЕ НЕ НУЖНО!!!',
        #             ('AT+COPN=?', 'ERROR\n+CME ERROR: SIM failure'),
        #             ('AT+COPN',
        #              'OK\n+COPN: "20201","C-OTE"\n+COPN: "20205","voda GR"\n+COPN: "20209","WIND"\n+COPN: "20210","WIND"\n+COPN: "20402","Tele2"\n+COPN: "20404","voda NL"\n+COPN: "20408","NL KPN"\n+COPN: "20412","NL Tlfrt"\n+COPN: "20416","TMO NL"\n+COPN: "20601","PROXI"\n+COPN: "20610","mobi*"\n+COPN: "20620","BASE"\n+COPN: "20801","Orange"\n+COPN: "20802","Contact"\n+COPN: "20809","SFR"\n+COPN: "20810","SFR"\n+COPN: "20811","SFR"\n+COPN: "20813","Contact"\n+COPN: "20815","Free"\n+COPN: "20820","BYTEL"\n+COPN: "20888","Contact"\n+COPN: "21201","vala"\n+COPN: "21210","MONACO"\n+COPN: "21303","M-AND"\n+COPN: "21401","voda ES"\n+COPN: "21403","Orange"\n+COPN: "21404","YOIGO"\n+COPN: "21407","Movistar"\n+COPN: "21601","TelenorH"\n+COPN: "21630","THU"\n+COPN: "21670","voda HU"\n+COPN: "21803","HT ERONET"\n+COPN: "21805","m:tel"\n+COPN: "21890","BHMobile"\n+COPN: "21901","HT HR"\n+COPN: "21902","Tele2 HR"\n+COPN: "21910","VIP"\n+COPN: "22001","Telenor"\n+COPN: "22002","ProMonte"\n+COPN: "22003","MTS"\n+COPN: "22004","TMO CG"\n+COPN: "22005","Vip SRB"\n+COPN: "22201","TIM"\n+COPN: "22210","voda IT"\n+COPN: "22288","I WIND"\n+COPN: "22299","3 ITA"\n+COPN: "22601","VF-RO"\n+COPN: "22603","COSMOTE"\n+COPN: "22605","Digi"\n+COPN: "22610","ORANGE"\n+COPN: "22801","Swisscom"\n+COPN: "22802","Sunrise"\n+COPN: "22803","Orange"\n+COPN: "22807","In&Phone"\n+COPN: "22815","OnAir"\n+COPN: "23001","TMO CZ"\n+COPN: "23002","O2 - CZ"\n+COPN: "23003","Vodafone"\n+COPN: "23101","Orange"\n+COPN: "23102","Telekom"\n+COPN: "23106","O2 - SK"\n+COPN: "23201","A1"\n+COPN: "23203","TMA"\n+COPN: "23205","3 AT"\n+COPN: "23207","telering"\n+COPN: "23210","3 AT"\n+COPN: "23212","A1"\n+COPN: "23401","UK01"\n+COPN: "23403","ATL-VOD"\n+COPN: "23407","C&W UK"\n+COPN: "23410","O2 - UK"\n+COPN: "23415","voda UK"\n+COPN: "23419","PMN"\n+COPN: "23420","3 UK"\n+COPN: "23428","Marathon"\n+COPN: "23430","EE"\n+COPN: "23431","EE"\n+COPN: "23432","EE"\n+COPN: "23433","EE"\n+COPN: "23450","JT"\n+COPN: "23455","Sure"\n+COPN: "23458","MANX"'),
        #             ('AT+COPN?',
        #              '+COPN: "23802","TelenoDK"\n+COPN: "23806","3 DK"\n+COPN: "23820","Telia"\n+COPN: "23866","TT DK"\n+COPN: "23877","TelenoDK"\n+COPN: "24001","TELIA"\n+COPN: "24002","3 SE"\n+COPN: "24004","SWE"\n+COPN: "24005","Sweden3G"\n+COPN: "24007","Tele2 SE"\n+COPN: "24008","TelenorS"\n+COPN: "24024","MobileS"\n+COPN: "24201","TELENOR"\n+COPN: "24202","NetCom"\n+COPN: "24204","Mobile N"\n+COPN: "24205","Mobile N"\n+COPN: "24403","DNA"\n+COPN: "24405","elisa"\n+COPN: "24412","DNA"\n+COPN: "24414","FI AMT"\n+COPN: "24491","SONERA"\n+COPN: "24601","OMT"\n+COPN: "24602","BITE"\n+COPN: "24603","Tele2 LT"\n+COPN: "24701","LMT"\n+COPN: "24702","Tele2 LV"\n+COPN: "24705","BITE LV"\n+COPN: "24801","EMT"\n+COPN: "24802","elisa"\n+COPN: "24803","Tele2 EE"\n+COPN: "25001","MTS"\n+COPN: "25002","MegaFon"\n+COPN: "25003","RTC"\n+COPN: "25004","RUS_SCN"\n+COPN: "25005","RTC"\n+COPN: "25007","SMARTS"\n+COPN: "25010","DTC"\n+COPN: "25012","RTC"\n+COPN: "25013","KUGSM"\n+COPN: "25015","SMARTS"\n+COPN: "25016","NTC"\n+COPN: "25017","RTC"\n+COPN: "25019","INDIGO"\n+COPN: "25020","TELE2 RU"\n+COPN: "25028","Beeline"\n+COPN: "25035","MOTIV"\n+COPN: "25037","KODOTEL"\n+COPN: "25038","RTC"\n+COPN: "25039","RTC"\n+COPN: "25099","Beeline"\n+COPN: "25501","MTS UKR"\n+COPN: "25502","Beeline"\n+COPN: "25503","UA-KS"\n+COPN: "25505","GT"\n+COPN: "25506","life:)"\n+COPN: "25507","TriMob"\n+COPN: "25701","VELCOM"\n+COPN: "25702","MTS"\n+COPN: "25704","life:) BY"\n+COPN: "25901","Orange"\n+COPN: "25902","MDCELL"\n+COPN: "25905","UNITE"\n+COPN: "26001","PLUS"\n+COPN: "26002","TM PL"\n+COPN: "26003","Orange"\n+COPN: "26004","Tele2"\n+COPN: "26006","Play"\n+COPN: "26007","Premium"\n+COPN: "26008","E-Telko"\n+COPN: "26016","Mobyland"\n+COPN: "26017","Aero2"\n+COPN: "26201","TDG"\n+COPN: "26202","Vodafone"\n+COPN: "26203","E-Plus"\n+COPN: "26207","o2 - de"\n+COPN: "26208","o2 - de"\n+COPN: "26213","MobilCom"\n+COPN: "26601","GIBTEL"\n+COPN: "26606","CTS"\n+COPN: "26609","Shine"\n+COPN: "26801","voda P"\n+COPN: "26803","OPTIM"\n+COPN: "26806","P MEO"\n+COPN: "27001","Post"\n+COPN: "27077","TANGO"\n+COPN: "27099","Orange"\n+COPN: "27201","voda IE"\n+COPN: "27202","O2-IRL"\n+COPN: "27203","METEOR"\n+COPN: "27205","3 IRL"'),
        #             ],
        # 'AT+CNAOP': ['[#FIXME!]acquisitions order preference',
        #              ('AT+CNAOP=?',
        #               '+COPN: "27402","Vodafone"\n+COPN: "27404","Viking"\n+COPN: "27408","On-waves"\n+COPN: "27411","NOVA"\n+COPN: "27412","Siminn"\n+COPN: "27601","A M C"\n+COPN: "27602","Voda AL"\n+COPN: "27603","EAGLE AL"\n+COPN: "27604","PLUS AL"\n+COPN: "27801","voda MT"\n+COPN: "27821","gomobile"\n+COPN: "27877","MT"\n+COPN: "28001","CYTAVODA"\n+COPN: "28010","MTN"\n+COPN: "28201","GCELL"\n+COPN: "28202","MAGTI"\n+COPN: "28204","BEELINE"\n+COPN: "28300","MTS Arm"\n+COPN: "28301","Beeline"\n+COPN: "28305","MTS Arm"\n+COPN: "28310","Orange"\n+COPN: "28401","Mtel"\n+COPN: "28403","Vivacom"\n+COPN: "28405","GLOBUL"\n+COPN: "28601","TCELL"\n+COPN: "28602","VF TR"\n+COPN: "28603","AVEA"\n+COPN: "28801","FT-GSM"\n+COPN: "28802","VODAFONE"\n+COPN: "29001","TELE GRL"\n+COPN: "29201","SMT"\n+COPN: "29340","Si.mobil"\n+COPN: "29341","MOBITEL"\n+COPN: "29364","T-2"\n+COPN: "29370","TUS"\n+COPN: "29401","TMO MK"\n+COPN: "29402","ONE"\n+COPN: "29403","Vip MKD"\n+COPN: "29501","Swiss FL"\n+COPN: "29502","OFL"\n+COPN: "29505","FL1"\n+COPN: "29577","Alpmobil"\n+COPN: "29701","Telenor"\n+COPN: "29702","T.me"\n+COPN: "302066","MTS"\n+COPN: "302072","ROGERS"\n+COPN: "302220","TELUS"\n+COPN: "302270","Eastlink"\n+COPN: "302320","Mobilicity"\n+COPN: "302340","Execulink"\n+COPN: "302370","Fido"\n+COPN: "302380","DMTS"\n+COPN: "302490","WIND"\n+COPN: "302610","Bell"\n+COPN: "302660","MTS"\n+COPN: "302720","ROGERS"\n+COPN: "302730","TStarSol"\n+COPN: "302770","RuralCom"\n+COPN: "302780","SaskTel"\n+COPN: "302880","FastRoam"\n+COPN: "302940","Wightman"\n+COPN: "30801","AMERIS"\n+COPN: "310000","CBW"\n+COPN: "310002","NEPW"\n+COPN: "310009","NEPW"\n+COPN: "310020","UnionTel"\n+COPN: "310030","CENT USA"\n+COPN: "310031","T-Mobile"\n+COPN: "310032","IT&E"\n+COPN: "310046","SIMMETRY"\n+COPN: "310070","AT&T"\n+COPN: "310080","Corr"\n+COPN: "310090","AT&T"\n+COPN: "310100","PLATEAU"\n+COPN: "310120","Sprint"\n+COPN: "310140","GTA"\n+COPN: "310150","AT&T"\n+COPN: "310160","T-Mobile"\n+COPN: "310170","AT&T"\n+COPN: "310190","D-HARBOR"\n+COPN: "310200","T-Mobile"\n+COPN: "310210","T-Mobile"\n+COPN: "310220","T-Mobile"\n+COPN: "310230","T-Mobile"\n+COPN: "310240","T-Mobile"\n+COPN: "310250","T-Mobile"\n+COPN: "310260","T-Mobile"\n+COPN: "310270","T-Mobile"\n+COPN: "310290","NEPW"\n+COPN: "310300","Big Sky"\n+COPN: "310310","T-Mobile"\n+COPN: "310320","Cell"\n+COPN: "310340","WestLink"\n+COPN: "310380","AT&T"\n+COPN: "310390","CELL 1 ET"\n+COPN: "310400","iCAN_GSM"\n+COPN: "310410","AT&T"\n+COPN: "310420","CBW"\n+COPN: "310450","NECCI"\n+COPN: "310460","USA1L"\n+COPN: "310470","DOCOMOPA"\n+COPN: "310490","SunCom"\n+COPN: "310530","IWS"\n+COPN: "310560","AT&T"\n+COPN: "310570","Chinook"\n+COPN: "310580","T-Mobile"\n+COPN: "310590","Verizon"\n+COPN: "310630","AMERLINK"\n+COPN: "310640","ARDGMC"\n+COPN: "310650","Jasper"\n+COPN: "310660","T-Mobile"\n+COPN: "310680","AT&T"\n+COPN: "310690","IMMIX"\n+COPN: "310710","ASTAC"\n+COPN: "310730","USCC"\n+COPN: "310740","OTZ"\n+COPN: "310770","IWS"\n+COPN: "310800","T-Mobile"\n+COPN: "310840","telna"\n+COPN: "310870","PACE"\n+COPN: "310880","ACSIAC"\n+COPN: "310890","Verizon"\n+COPN: "310950","XIT"\n+COPN: "310980","AT&T"\n+COPN: "311000","Mid-Tex"\n+COPN: "311001","WILKES"\n+COPN: "311005","WILKES"\n+COPN: "311030","Indigo"'),
        #              ('AT+CNAOP',
        #               '+COPN: "311080","PINECell"\n+COPN: "311090","SXLP"\n+COPN: "311150","WILKES"\n+COPN: "311170","Broadpoint"\n+COPN: "311180","WCW"\n+COPN: "311190","C1ECI"\n+COPN: "311240","CWCI"\n+COPN: "311260",""\n+COPN: "311310","LamarCel"\n+COPN: "311330","BTW"\n+COPN: "311360","STELERA"\n+COPN: "311370","GCI"\n+COPN: "311380","AT&T"\n+COPN: "311410","AT&T"\n+COPN: "311480","Verizon"\n+COPN: "311500","MOSAIC"\n+COPN: "311530","USANW"\n+COPN: "311540","ProxMo"\n+COPN: "311580","USCC"\n+COPN: "311680","Green Fly"\n+COPN: "311710","NEWN"\n+COPN: "311720","MainePCS"\n+COPN: "311730","ProxMo"\n+COPN: "311940","CLEAR"\n+COPN: "31260","CvgCo"\n+COPN: "312230","SRTW"\n+COPN: "312260","USACL"\n+COPN: "330110","Claro"\n+COPN: "330120","Open Mob"\n+COPN: "33403","movistar"\n+COPN: "33409","Nextel3G"\n+COPN: "33420","TELCEL"\n+COPN: "33450","Iusacell"\n+COPN: "33490","Nextel3G"\n+COPN: "338005","DIGICEL"\n+COPN: "338050","DIGICEL"\n+COPN: "338070","ClaroJam"\n+COPN: "338180","LIME"\n+COPN: "34001","Orange"\n+COPN: "34002","ONLY"\n+COPN: "34003","CHIPPIE"\n+COPN: "34008","DAUPHIN"\n+COPN: "34020","DigicelF"\n+COPN: "342600","LIME"\n+COPN: "342750","DIGICEL"\n+COPN: "344030","imobile"\n+COPN: "344920","LIME"\n+COPN: "344930","Cingular"\n+COPN: "346140","LIME"\n+COPN: "348170","LIME"\n+COPN: "348570","CCTBVI"\n+COPN: "35000","CELLONE"\n+COPN: "35002","M3 WIREL"\n+COPN: "35010","Cingular"\n+COPN: "352030","DIGICEL"\n+COPN: "352110","LIME"\n+COPN: "354860","LIME"\n+COPN: "356110","LIME"\n+COPN: "358050","DIGICEL"\n+COPN: "358110","LIME"\n+COPN: "360070","DIGICEL"\n+COPN: "360110","LIME"\n+COPN: "36251","Telcell"\n+COPN: "36269","CT GSM"\n+COPN: "36291","CHIPPIE"\n+COPN: "362951","CHIPPIE"\n+COPN: "36301","SETARGSM"\n+COPN: "36320","DIGICEL"\n+COPN: "36439","BaTelCel"\n+COPN: "365840","LIME"\n+COPN: "366020","Cingular"\n+COPN: "366110","LIME"\n+COPN: "36801","CUBACEL"\n+COPN: "37001","Orange"\n+COPN: "37002","ClaroDOM"\n+COPN: "37004","VIVA"\n+COPN: "37201","VOILA"\n+COPN: "37203","Natcom"\n+COPN: "37412","TSTT"\n+COPN: "376350","LIME"\n+COPN: "376360","ICOM TCI"\n+COPN: "40001","ACELL"\n+COPN: "40002","BAKCELL"\n+COPN: "40004","Nar"\n+COPN: "40101","Beeline"\n+COPN: "40102","KCELL"\n+COPN: "40107","ALTEL"\n+COPN: "40177","NEO"\n+COPN: "40211","B-Mobile"\n+COPN: "40277","TASHICELL"\n+COPN: "40401","Vodafone"\n+COPN: "40402","airtel"\n+COPN: "40403","airtel"\n+COPN: "40404","IDEA"\n+COPN: "40405","Vodafone"\n+COPN: "40407","IDEA"\n+COPN: "40409","RELIANCE"\n+COPN: "40410","airtel"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "40412","IDEA"\n+COPN: "40413","Vodafone"\n+COPN: "40414","IDEA"\n+COPN: "40415","Vodafone"\n+COPN: "40416","airtel"\n+COPN: "40417","AIRCEL"\n+COPN: "40418","RELIANCE"\n+COPN: "40419","IDEA"\n+COPN: "40420","Vodafone"\n+COPN: "40421","BPL MOBILE"\n+COPN: "40422","IDEA"\n+COPN: "40424","IDEA"\n+COPN: "40425","AIRCEL"\n+COPN: "40427","Vodafone"\n+COPN: "40428","AIRCEL"\n+COPN: "40429","AIRCEL"\n+COPN: "40430","Vodafone"\n+COPN: "40431","airtel"\n+COPN: "40433","AIRCEL"\n+COPN: "40434","CellOne"\n+COPN: "40435","AIRCEL"\n+COPN: "40436","RELIANCE"\n+COPN: "40437","AIRCEL"\n+COPN: "40438","CellOne"\n+COPN: "40440","airtel"\n+COPN: "40441","AIRCEL"\n+COPN: "40442","AIRCEL"\n+COPN: "40443","Vodafone"\n+COPN: "40444","IDEA"\n+COPN: "40445","airtel"\n+COPN: "40446","Vodafone"\n+COPN: "40449","airtel"\n+COPN: "40450","RELIANCE"\n+COPN: "40451","CellOne"\n+COPN: "40452","RELIANCE"\n+COPN: "40453","CellOne"\n+COPN: "40454","CellOne"\n+COPN: "40455","CellOne"\n+COPN: "40456","IDEA"\n+COPN: "40457","CellOne"\n+COPN: "40458","CellOne"\n+COPN: "40459","CellOne"\n+COPN: "40460","Vodafone"\n+COPN: "40462","CellOne"\n+COPN: "40464","CellOne"\n+COPN: "40466","CellOne"\n+COPN: "40467","RELIANCE"\n+COPN: "40468","DOLPHIN"\n+COPN: "40469","DOLPHIN"\n+COPN: "40470","airtel"\n+COPN: "40471","CellOne"\n+COPN: "40472","CellOne"\n+COPN: "40473","CellOne"\n+COPN: "40474","CellOne"\n+COPN: "40475","CellOne"\n+COPN: "40476","CellOne"\n+COPN: "40477","CellOne"\n+COPN: "40478","IDEA"\n+COPN: "40479","CellOne"\n+COPN: "40480","CellOne"\n+COPN: "40481","CellOne"\n+COPN: "40482","IDEA"\n+COPN: "40483","Reliance"\n+COPN: "40484","Vodafone"\n+COPN: "40485","RELIANCE"\n+COPN: "40486","Vodafone"\n+COPN: "40487","IDEA"\n+COPN: "40488","Vodafone"\n+COPN: "40489","IDEA"\n+COPN: "40490","airtel"\n+COPN: "40491","Aircel"\n+COPN: "40492","airtel"\n+COPN: "40493","airtel"\n+COPN: "40494","airtel"\n+COPN: "40495","airtel"\n+COPN: "40496","airtel"\n+COPN: "40497","airtel"\n+COPN: "40498","airtel"\n+COPN: "40501","Reliance"\n+COPN: "40505","Reliance"\n+COPN: "40506","Reliance"\n+COPN: "40507","Reliance"\n+COPN: "40509","Reliance"\n+COPN: "40510","Reliance"\n+COPN: "40511","Reliance"\n+COPN: "40513","Reliance"\n+COPN: "40515","Reliance"\n+COPN: "40518","Reliance"\n+COPN: "40519","Reliance"\n+COPN: "40520","Reliance"\n+COPN: "40521","Reliance"\n+COPN: "40522","Reliance"\n+COPN: "405025","TATA DO"\n+COPN: "405027","TATA DO"\n+COPN: "405029","TATA DO"\n+COPN: "405030","TATA DO"\n+COPN: "405031","TATA DO"\n+COPN: "405032","TATA DO"\n+COPN: "405034","TATA DO"\n+COPN: "405035","TATA DO"\n+COPN: "405036","TATA DO"\n+COPN: "405037","TATA DO"\n+COPN: "405038","TATA DO"'),
        #              ('AT+CNAOP=27402',
        #               '+COPN: "405811","Aircel"\n+COPN: "405812","Aircel"\n+COPN: "405813","UNITECH"\n+COPN: "405814","UNITECH"\n+COPN: "405815","UNITECH"\n+COPN: "405816","UNITECH"\n+COPN: "405817","UNITECH"\n+COPN: "405818","UNITECH"\n+COPN: "405819","UNITECH"\n+COPN: "405820","UNITECH"\n+COPN: "405821","UNITECH"\n+COPN: "405822","UNITECH"\n+COPN: "405823","VIDEOCON"\n+COPN: "405824","VIDEOCON"\n+COPN: "405825","VIDEOCON"\n+COPN: "405827","VIDEOCON"\n+COPN: "405828","VIDEOCON"\n+COPN: "405829","VIDEOCON"\n+COPN: "405830","VIDEOCON"\n+COPN: "405831","VIDEOCON"\n+COPN: "405832","VIDEOCON"\n+COPN: "405833","VIDEOCON"\n+COPN: "405834","VIDEOCON"\n+COPN: "405835","VIDEOCON"\n+COPN: "405836","VIDEOCON"\n+COPN: "405837","VIDEOCON"\n+COPN: "405838","VIDEOCON"\n+COPN: "405839","VIDEOCON"\n+COPN: "405840","VIDEOCON"\n+COPN: "405841","VIDEOCON"\n+COPN: "405842","VIDEOCON"\n+COPN: "405843","VIDEOCON"\n+COPN: "405844","UNITECH"\n+COPN: "405845","IDEA"\n+COPN: "405846","IDEA"\n+COPN: "405848","IDEA"\n+COPN: "405849","IDEA"\n+COPN: "405850","IDEA"\n+COPN: "405852","IDEA"\n+COPN: "405853","IDEA"\n+COPN: "405854","LoopMobile"\n+COPN: "405855","LoopMobile"\n+COPN: "405856","LoopMobile"\n+COPN: "405857","LoopMobile"\n+COPN: "405858","LoopMobile"\n+COPN: "405859","LoopMobile"\n+COPN: "405860","LoopMobile"\n+COPN: "405861","LoopMobile"\n+COPN: "405862","LoopMobile"\n+COPN: "405863","LoopMobile"\n+COPN: "405864","LoopMobile"\n+COPN: "405865","LoopMobile"\n+COPN: "405866","LoopMobile"\n+COPN: "405867","LoopMobile"\n+COPN: "405868","LoopMobile"\n+COPN: "405869","LoopMobile"\n+COPN: "405870","LoopMobile"\n+COPN: "405871","LoopMobile"\n+COPN: "405872","LoopMobile"\n+COPN: "405873","LoopMobile"\n+COPN: "405874","LoopMobile"\n+COPN: "405875","UNITECH"\n+COPN: "405876","UNITECH"\n+COPN: "405877","UNITECH"\n+COPN: "405878","UNITECH"\n+COPN: "405879","UNITECH"\n+COPN: "405880","UNITECH"\n+COPN: "405912","etisalat"\n+COPN: "405913","etisalat"\n+COPN: "405914","etisalat"\n+COPN: "405915","etisalat"\n+COPN: "405916","etisalat"\n+COPN: "405917","etisalat"\n+COPN: "405918","etisalat"\n+COPN: "405919","etisalat"\n+COPN: "405920","etisalat"\n+COPN: "405921","etisalat"\n+COPN: "405922","etisalat"\n+COPN: "405923","etisalat"\n+COPN: "405924","etisalat"\n+COPN: "405925","UNITECH"\n+COPN: "405926","UNITECH"\n+COPN: "405927","UNITECH"\n+COPN: "405928","UNITECH"\n+COPN: "405929","UNITECH"\n+COPN: "405932","VIDEOCON"\n+COPN: "41001","Mobilink"\n+COPN: "41003","UFONE"\n+COPN: "41004","ZONG"\n+COPN: "41006","TELENOR"\n+COPN: "41007","WaridTel"\n+COPN: "41201","AWCC"\n+COPN: "41220","ROSHAN"\n+COPN: "41240","MTN"\n+COPN: "41250","Etisalat"\n+COPN: "41301","MOBITEL"\n+COPN: "41302","DIALOG"\n+COPN: "41303","Etisalat"\n+COPN: "41305","airtel"\n+COPN: "41308","Hutch"\n+COPN: "41401","MPTGSM"\n+COPN: "41501","alfa"\n+COPN: "41503","MTC LIBAN"\n+COPN: "41505","OM"\n+COPN: "41601","Zain JO"\n+COPN: "41603","UMNIAH"\n+COPN: "41677","Orange JO"\n+COPN: "41701","SYRIATEL"\n+COPN: "41702","MTN"\n+COPN: "41800","ASIACELL"\n+COPN: "41805","ASIACELL"\n+COPN: "41820","zain IQ"\n+COPN: "41830","IRAQNA"\n+COPN: "41840","KOREK"\n+COPN: "41902","zain KW"\n+COPN: "41903","WATANIYA"\n+COPN: "41904","VIVA"\n+COPN: "42001","STC"\n+COPN: "42003","Mobily"\n+COPN: "42004","Zain SA"\n+COPN: "42101","SABAFON"\n+COPN: "42102","MTN"\n+COPN: "42104","Y"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "42202","OMAN"\n+COPN: "42203","nawras"\n+COPN: "42402","ETISALAT"\n+COPN: "42403","du"\n+COPN: "42501","Orange IL"\n+COPN: "42502","Cellcom"\n+COPN: "42503","PCL"\n+COPN: "42505","JAWWAL"\n+COPN: "42506","WM"\n+COPN: "42507","Hot Mobile"\n+COPN: "42601","BATELCO"\n+COPN: "42602","Zain BH"\n+COPN: "42604","VIVA BH"\n+COPN: "42701","Ooredoo"\n+COPN: "42702","VF-QA"\n+COPN: "42806","GMOBILE"\n+COPN: "42888","UNTLMN"\n+COPN: "42899","MobiCom"\n+COPN: "42901","NT"\n+COPN: "42902","Ncell"\n+COPN: "43211","IR-TCI"\n+COPN: "43214","KIFZO"\n+COPN: "43219","MTCE"\n+COPN: "43220","IRN 20"\n+COPN: "43232","Taliya"\n+COPN: "43235","Irancell"\n+COPN: "43404","Beeline"\n+COPN: "43405","Ucell"\n+COPN: "43407","UZB MTS"\n+COPN: "43601","TCELL"\n+COPN: "43602","TCELL"\n+COPN: "43603","MegaFon"\n+COPN: "43604","Babilon"\n+COPN: "43605","BEELINE"\n+COPN: "43701","Beeline KG"\n+COPN: "43705","MEGACOM"\n+COPN: "43709","O!"\n+COPN: "43801","MTS TM"\n+COPN: "43802","TM CELL"\n+COPN: "44000","EMOBILE"\n+COPN: "44010","DOCOMO"\n+COPN: "44020","SoftBank"\n+COPN: "44050","KDDI"\n+COPN: "45001","Samsung"\n+COPN: "45002","KT"\n+COPN: "45005","SKT"\n+COPN: "45006","LG U+"\n+COPN: "45008","KT"\n+COPN: "45200","VN MOBIF"\n+COPN: "45201","VN MobiFon"\n+COPN: "45202","GPC"\n+COPN: "45204","VIETTEL"\n+COPN: "45205","VNMOBILE"\n+COPN: "45207","Gmobile"\n+COPN: "45400","CSL"\n+COPN: "45402","CSL"\n+COPN: "45403","3"\n+COPN: "45404","3(2G)"\n+COPN: "45406","SMC HK"\n+COPN: "45410","CSL"\n+COPN: "45412","CMHK"\n+COPN: "45413","CMHK"\n+COPN: "45415","SMC HK"\n+COPN: "45416","PCCW-HKT"\n+COPN: "45417","SMC HK"\n+COPN: "45418","CSL"\n+COPN: "45419","PCCW-HKT"\n+COPN: "45420","PCCW-HKT"\n+COPN: "45500","SMC MAC"\n+COPN: "45501","CTM"\n+COPN: "45503","3 Macau"\n+COPN: "45504","CTM"\n+COPN: "45505","3 Macau"\n+COPN: "45601","Cellcard"\n+COPN: "45602","Hello"\n+COPN: "45604","CADCOMMS"\n+COPN: "45605","SMART"\n+COPN: "45606","SMART"\n+COPN: "45608","Metfone"\n+COPN: "45609","Beeline"\n+COPN: "45618","Mfone"\n+COPN: "45701","LAO GSM"\n+COPN: "45702","ETLMNW"\n+COPN: "45703","UNITEL"\n+COPN: "45708","TIGO"\n+COPN: "46000","CMCC"\n+COPN: "46001","UNICOM"\n+COPN: "46002","CMCC"\n+COPN: "46003","CTCC"\n+COPN: "46005","CTCC"\n+COPN: "46006","UNICOM"\n+COPN: "46007","CMCC"\n+COPN: "46008","CMCC"\n+COPN: "46009","UNICOM"\n+COPN: "46011","CTCC"\n+COPN: "46601","FET"'),
        #              ('AT+CNAOP=Vodafone',
        #               '+COPN: "51505","SUN"\n+COPN: "51511","ACeS"\n+COPN: "52000","TH 3G+"\n+COPN: "52001","TH GSM"\n+COPN: "52002","TH CAT"\n+COPN: "52003","AIS 3G"\n+COPN: "52004","TRUE 3G+"\n+COPN: "52005","dtac"\n+COPN: "52015","TOT3G"\n+COPN: "52018","DTAC"\n+COPN: "52020","ACeS"\n+COPN: "52023","GSM 1800"\n+COPN: "52099","TRUE"\n+COPN: "52501","SingTel"\n+COPN: "52502","SingTel"\n+COPN: "52503","M1"\n+COPN: "52505","STARHUB"\n+COPN: "52507","CallZone"\n+COPN: "52802","b-mobile"\n+COPN: "52811","DSTCom"\n+COPN: "53001","voda NZ"\n+COPN: "53005","Telecom"\n+COPN: "53024","2degrees"\n+COPN: "53701","BMobile"\n+COPN: "53703","DIGICEL"\n+COPN: "53730","Digicel"\n+COPN: "53901","U-CALL"\n+COPN: "53988","Digicel"\n+COPN: "54001","BREEZE"\n+COPN: "54002","Bemobile"\n+COPN: "54101","SMILE"\n+COPN: "54105","Digicel"\n+COPN: "54201","VODAFONE"\n+COPN: "54202","DIGICEL"\n+COPN: "542542","Digicel "\n+COPN: "544110","BLUESKY"\n+COPN: "54509","KI-FRIG"\n+COPN: "54601","MOBNCL"\n+COPN: "54715","VF PF"\n+COPN: "54720","VINI"\n+COPN: "54801","KOKANET"\n+COPN: "54900","DIGICEL"\n+COPN: "54927","Bluesky"\n+COPN: "55001","FSMTC"\n+COPN: "55101","NTA"\n+COPN: "55201","PalauCel"\n+COPN: "55280","PLWPMC"\n+COPN: "60201","MobiNiL"\n+COPN: "60202","voda EG"\n+COPN: "60203","Etisalat"\n+COPN: "60301","Mobilis"\n+COPN: "60302","Djezzy"\n+COPN: "60303","Ooredoo"\n+COPN: "60400","MEDITEL"\n+COPN: "60401","IAM"\n+COPN: "60402","inwi"\n+COPN: "60501","Orange"\n+COPN: "60502","TUNTEL"\n+COPN: "60503","TUNSIANA"\n+COPN: "60600","L"\n+COPN: "60601","Al Madar"\n+COPN: "60701","GAMCEL"\n+COPN: "60702","AFRICELL"\n+COPN: "60703","GMCOMIUM"\n+COPN: "60704","QC"\n+COPN: "60801","ALIZE"\n+COPN: "60802","SENTEL"\n+COPN: "60803","Expresso"\n+COPN: "60901","MATTEL"\n+COPN: "60902","EMR"\n+COPN: "60910","MAURITEL"\n+COPN: "61001","MALITEL"\n+COPN: "61002","OML"\n+COPN: "61101","ORANGEGN"\n+COPN: "61102","LAGUI"\n+COPN: "61104","GNAreeba"\n+COPN: "61105","CellcomGN"\n+COPN: "61202","ETISALAT"\n+COPN: "61203","Orange"\n+COPN: "61204","KoZ"\n+COPN: "61205","MTN CI"\n+COPN: "61302","Celtel"\n+COPN: "61402","CELTEL"\n+COPN: "61403","ETISALAT"\n+COPN: "61404","Orange"\n+COPN: "61501","TGCELL"\n+COPN: "61503","ETISALAT"\n+COPN: "61602","ETISALAT"\n+COPN: "61603","MTN BENIN"\n+COPN: "61604","BBCOM"\n+COPN: "61605","GloBenin"\n+COPN: "61701","CELL +"\n+COPN: "61703","MTML"\n+COPN: "61710","EMTEL"\n+COPN: "61801","LoneStar"\n+COPN: "61804","Novafone"\n+COPN: "61807","Celcom"\n+COPN: "61900","SLE COMI"\n+COPN: "61901","CELTEL"\n+COPN: "61904","SLE COMIUM"\n+COPN: "61905","Africell"\n+COPN: "61907","GreenN "\n+COPN: "62001","MTN"\n+COPN: "62002","Vodafone"\n+COPN: "62003","tiGO GHANA"\n+COPN: "62006","Airtel"\n+COPN: "62007","Glo Ghana"\n+COPN: "62120","AirtelNG"\n+COPN: "62130","MTN-NG"\n+COPN: "62150","glo"\n+COPN: "62160","Etisalat"\n+COPN: "62201","CELTEL"\n+COPN: "62203","Tigo"\n+COPN: "62207","SALAM"\n+COPN: "62301","ETISALAT"\n+COPN: "62302","Telecel"\n+COPN: "62304","NL-RCA"\n+COPN: "62401","MTN CAM"\n+COPN: "62402","Orange"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "62502","T+"\n+COPN: "62601","CSTmovel"\n+COPN: "62701","GETESA"\n+COPN: "62703","Muni-GQ"\n+COPN: "62801","LIBERTIS"\n+COPN: "62802","ETISALAT"\n+COPN: "62803","ZAIN"\n+COPN: "62902","AZUR COG"\n+COPN: "62907","WARIDRC"\n+COPN: "62910","MTN-CG"\n+COPN: "63001","VODACOM"\n+COPN: "63002","CELTEL"\n+COPN: "63005","SCELL"\n+COPN: "63086","Orange"\n+COPN: "63088","Smart"\n+COPN: "63089","TIGO"\n+COPN: "63090","AFRICELL"\n+COPN: "63102","UNITEL"\n+COPN: "63202","MTN"\n+COPN: "63203","ORANGE BS"\n+COPN: "63301","C&W SEY"\n+COPN: "63310","AIRTEL"\n+COPN: "63401","Zain SD"\n+COPN: "63402","MTN"\n+COPN: "63405","Vivacell"\n+COPN: "63510","MTN Rwanda"\n+COPN: "63513","TIGO RW"\n+COPN: "63514","AR"\n+COPN: "63601","ET-MTN"\n+COPN: "63701","Tele"\n+COPN: "63704","SOMAFONE"\n+COPN: "63720","SOMNET"\n+COPN: "63730","Golis"\n+COPN: "63740","MONTYSOM"\n+COPN: "63771","SOMTEL"\n+COPN: "63782","Telsom"\n+COPN: "63801","EVATIS"\n+COPN: "63902","SAF-COM"\n+COPN: "63903","Airtel"\n+COPN: "63907","GSMTKL"\n+COPN: "64002","TIGO"\n+COPN: "64003","ZANTEL"\n+COPN: "64004","VodaCom"\n+COPN: "64005","celtel"\n+COPN: "64008","Smart TZA"\n+COPN: "64101","CELTEL"\n+COPN: "64110","MTN-UG"\n+COPN: "64111","UTL"\n+COPN: "64114","OUL"\n+COPN: "64122","WaridTel"\n+COPN: "64201","EWB"\n+COPN: "64202","TEMPO-AF"\n+COPN: "64203","ONATEL"\n+COPN: "64207","SMART"\n+COPN: "64282","BDITL"\n+COPN: "64301","mCel"\n+COPN: "64303","MOVITEL"\n+COPN: "64304","VodaCom"\n+COPN: "64501","CELTEL"\n+COPN: "64502","MTN ZM"\n+COPN: "64601","ZAIN"\n+COPN: "64602","OrangeMG"\n+COPN: "64604","TELMA"\n+COPN: "64700","Orange"\n+COPN: "64702","OUTREMER"\n+COPN: "64710","SFR RU"\n+COPN: "64801","NETONE"\n+COPN: "64803","TELECEL"\n+COPN: "64804","ECONET"\n+COPN: "64901","MTCNAM"\n+COPN: "64903","tnmobile"\n+COPN: "65001","TNM"\n+COPN: "65010","CELTEL"\n+COPN: "65101","Vodacom-LS"\n+COPN: "65102","ETL"\n+COPN: "65201","MASCOM"\n+COPN: "65202","Orange"\n+COPN: "65204","beMOBILE"\n+COPN: "65310","SwaziMTN"\n+COPN: "65401","HURI"\n+COPN: "65501","VODA"\n+COPN: "65502","TelkomSA"\n+COPN: "65507","Cell C"\n+COPN: "65510","MTN"\n+COPN: "65902","MTN"\n+COPN: "65903","Gemtel"\n+COPN: "65904","Vivacell"'),
        #              ('AT+CNAOP=27404',
        #               '+COPN: "70267","BTL"\n+COPN: "70401","ClaroGTM"\n+COPN: "70402","COMCEL"\n+COPN: "70403","Movistar"\n+COPN: "70601","ClaroSLV"\n+COPN: "70602","DIGICEL"\n+COPN: "70603","TM"\n+COPN: "70604","movistar"\n+COPN: "70801","ClaroHND"\n+COPN: "70802","CELTEL"\n+COPN: "70830","HT - 200"\n+COPN: "71021","ClaroNIC"\n+COPN: "71073","ClaroNIC"\n+COPN: "710300","movistar"\n+COPN: "71200","I.C.E."\n+COPN: "71201","I.C.E."\n+COPN: "71202","I.C.E."\n+COPN: "71203","CLARO CR"\n+COPN: "71204","Movistar"\n+COPN: "71401","PANCW"\n+COPN: "71403","CLARO PA"\n+COPN: "71404","DIGICEL"\n+COPN: "71420","Movistar"\n+COPN: "71606","MOVISTAR"\n+COPN: "71610","ClaroPER"\n+COPN: "71615","VTP"\n+COPN: "71617","NXT3"\n+COPN: "72201","Movistar"\n+COPN: "72207","Movistar"\n+COPN: "72210","Movistar"\n+COPN: "72234","AR TP"\n+COPN: "72236","AR TP"\n+COPN: "722310","CLARO AR"\n+COPN: "722341","AR TP"\n+COPN: "72402","TIM"\n+COPN: "72403","TIM"\n+COPN: "72404","TIM"\n+COPN: "72405","Claro"\n+COPN: "72406","VIVO"\n+COPN: "72410","VIVO"\n+COPN: "72411","VIVO"\n+COPN: "72415","SCTL"\n+COPN: "72416","Oi"\n+COPN: "72423","VIVO"\n+COPN: "72424","AMAZONIA"\n+COPN: "72431","Oi"\n+COPN: "72432","CTBC"\n+COPN: "72433","CTBC"\n+COPN: "72434","CTBC"\n+COPN: "72439","Nextel 3G"\n+COPN: "73001","ENTEL"\n+COPN: "73002","Movistar"\n+COPN: "73003","ClaroCHL"\n+COPN: "73007","Movistar"\n+COPN: "73008","VTR"\n+COPN: "73009","Nextel3G"\n+COPN: "73010","ENTEL"\n+COPN: "730730","Movistar"\n+COPN: "73200","Comcel S"\n+COPN: "732101","Claro"\n+COPN: "732103","TIGO COL"\n+COPN: "732111","TIGO COL"\n+COPN: "732123","Movistar"\n+COPN: "73401","DIGITEL"\n+COPN: "73402","DIGITEL"\n+COPN: "73403","DIGITEL"\n+COPN: "73404","movistar"\n+COPN: "73406","Movilnet"\n+COPN: "73601","VIVA"\n+COPN: "73602","EMOVIL"\n+COPN: "73603","Telecel"\n+COPN: "73801","DIGICEL"\n+COPN: "73802","CLNKPLS"\n+COPN: "738592","CLNKPLS"\n+COPN: "74000","Movistar"\n+COPN: "74001","CLARO"\n+COPN: "74002","CNT"\n+COPN: "74401","HPGYSA"\n+COPN: "74402","CLARO PY"\n+COPN: "74404","TIGO"\n+COPN: "74405","Personal"\n+COPN: "74602","TeleG"\n+COPN: "74603","DIGICEL"\n+COPN: "74604","UNIQA"\n+COPN: "74801","Antel"\n+COPN: "74807","Movistar"\n+COPN: "74810","CLARO UY"\n+COPN: "75001","C&W FLK"\n+COPN: "79502","TM CELL"\n+COPN: "90105","Thuraya"\n+COPN: "90106","Thuraya"\n+COPN: "90111","INX"\n+COPN: "90112","MCP"\n+COPN: "90114","AeroMob"\n+COPN: "90115","OnAir"\n+COPN: "90118","WMS"\n+COPN: "90121","Seanet"\n+COPN: "90126","TIM@sea"\nOK\n+COPN: "20201","C-OTE"\n+COPN: "20205","voda GR"\n+COPN: "20209","WIND"\n+COPN: "20210","WIND"\n+COPN: "20402","Tele2"\n+COPN: "20404","voda NL"\n+COPN: "20408","NL KPN"\n+COPN: "20412","NL Tlfrt"\n+COPN: "20416","TMO NL"\n+COPN: "20601","PROXI"\n+COPN: "20610","mobi*"\n+COPN: "20620","BASE"\n+COPN: "20801","Orange"\n+COPN: "20802","Contact"\n+COPN: "20809","SFR"\n+COPN: "20810","SFR"\n+COPN: "20811","SFR"\n+COPN: "20813","Contact"\n+COPN: "20815","Free"\n+COPN: "20820","BYTEL"\n+COPN: "20888","Contact"\n+COPN: "21201","vala"\n+COPN: "21210","MONACO"\n+COPN: "21303","M-AND"\n+COPN: "21401","voda ES"\n+COPN: "21403","Orange"\n+COPN: "21404","YOIGO"\n+COPN: "21407","Movistar"\n+COPN: "21601","TelenorH"\n+COPN: "21630","THU"\n+COPN: "21670","voda HU"\n+COPN: "21803","HT ERONET"\n+COPN: "21805","m:tel"\n+COPN: "21890","BHMobile"\n+COPN: "21901","HT HR"\n+COPN: "21902","Tele2 HR"\n+COPN: "21910","VIP"\n+COPN: "22001","Telenor"\n+COPN: "22002","ProMonte"\n+COPN: "22003","MTS"\n+COPN: "22004","TMO CG"\n+COPN: "22005","Vip SRB"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "22201","TIM"\n+COPN: "22210","voda IT"\n+COPN: "22288","I WIND"\n+COPN: "22299","3 ITA"\n+COPN: "22601","VF-RO"\n+COPN: "22603","COSMOTE"\n+COPN: "22605","Digi"\n+COPN: "22610","ORANGE"\n+COPN: "22801","Swisscom"\n+COPN: "22802","Sunrise"\n+COPN: "22803","Orange"\n+COPN: "22807","In&Phone"\n+COPN: "22815","OnAir"\n+COPN: "23001","TMO CZ"\n+COPN: "23002","O2 - CZ"\n+COPN: "23003","Vodafone"\n+COPN: "23101","Orange"\n+COPN: "23102","Telekom"\n+COPN: "23106","O2 - SK"\n+COPN: "23201","A1"\n+COPN: "23203","TMA"\n+COPN: "23205","3 AT"\n+COPN: "23207","telering"\n+COPN: "23210","3 AT"\n+COPN: "23212","A1"\n+COPN: "23401","UK01"\n+COPN: "23403","ATL-VOD"\n+COPN: "23407","C&W UK"\n+COPN: "23410","O2 - UK"\n+COPN: "23415","voda UK"\n+COPN: "23419","PMN"\n+COPN: "23420","3 UK"\n+COPN: "23428","Marathon"\n+COPN: "23430","EE"\n+COPN: "23431","EE"\n+COPN: "23432","EE"\n+COPN: "23433","EE"\n+COPN: "23450","JT"\n+COPN: "23455","Sure"\n+COPN: "23458","MANX"\n+COPN: "23801","TDC Mobil"\n+COPN: "23802","TelenoDK"\n+COPN: "23806","3 DK"\n+COPN: "23820","Telia"\n+COPN: "23866","TT DK"\n+COPN: "23877","TelenoDK"\n+COPN: "24001","TELIA"\n+COPN: "24002","3 SE"\n+COPN: "24004","SWE"\n+COPN: "24005","Sweden3G"\n+COPN: "24007","Tele2 SE"\n+COPN: "24008","TelenorS"\n+COPN: "24024","MobileS"\n+COPN: "24201","TELENOR"\n+COPN: "24202","NetCom"\n+COPN: "24204","Mobile N"\n+COPN: "24205","Mobile N"\n+COPN: "24403","DNA"\n+COPN: "24405","elisa"\n+COPN: "24412","DNA"\n+COPN: "24414","FI AMT"\n+COPN: "24491","SONERA"\n+COPN: "24601","OMT"\n+COPN: "24602","BITE"\n+COPN: "24603","Tele2 LT"\n+COPN: "24701","LMT"\n+COPN: "24702","Tele2 LV"\n+COPN: "24705","BITE LV"\n+COPN: "24801","EMT"\n+COPN: "24802","elisa"\n+COPN: "24803","Tele2 EE"\n+COPN: "25001","MTS"\n+COPN: "25002","MegaFon"\n+COPN: "25003","RTC"\n+COPN: "25004","RUS_SCN"\n+COPN: "25005","RTC"\n+COPN: "25007","SMARTS"\n+COPN: "25010","DTC"\n+COPN: "25012","RTC"\n+COPN: "25013","KUGSM"\n+COPN: "25015","SMARTS"\n+COPN: "25016","NTC"\n+COPN: "25017","RTC"\n+COPN: "25019","INDIGO"\n+COPN: "25020","TELE2 RU"\n+COPN: "25028","Beeline"'),
        #              ('AT+CNAOP=Viking',
        #               '+COPN: "25037","KODOTEL"\n+COPN: "25038","RTC"\n+COPN: "25039","RTC"\n+COPN: "25099","Beeline"\n+COPN: "25501","MTS UKR"\n+COPN: "25502","Beeline"\n+COPN: "25503","UA-KS"\n+COPN: "25505","GT"\n+COPN: "25506","life:)"\n+COPN: "25507","TriMob"\n+COPN: "25701","VELCOM"\n+COPN: "25702","MTS"\n+COPN: "25704","life:) BY"\n+COPN: "25901","Orange"\n+COPN: "25902","MDCELL"\n+COPN: "25905","UNITE"\n+COPN: "26001","PLUS"\n+COPN: "26002","TM PL"\n+COPN: "26003","Orange"\n+COPN: "26004","Tele2"\n+COPN: "26006","Play"\n+COPN: "26007","Premium"\n+COPN: "26008","E-Telko"\n+COPN: "26016","Mobyland"\n+COPN: "26017","Aero2"\n+COPN: "26201","TDG"\n+COPN: "26202","Vodafone"\n+COPN: "26203","E-Plus"\n+COPN: "26207","o2 - de"\n+COPN: "26208","o2 - de"\n+COPN: "26213","MobilCom"\n+COPN: "26601","GIBTEL"\n+COPN: "26606","CTS"\n+COPN: "26609","Shine"\n+COPN: "26801","voda P"\n+COPN: "26803","OPTIM"\n+COPN: "26806","P MEO"\n+COPN: "27001","Post"\n+COPN: "27077","TANGO"\n+COPN: "27099","Orange"\n+COPN: "27201","voda IE"\n+COPN: "27202","O2-IRL"\n+COPN: "27203","METEOR"\n+COPN: "27205","3 IRL"\n+COPN: "27401","Siminn"\n+COPN: "27402","Vodafone"\n+COPN: "27404","Viking"\n+COPN: "27408","On-waves"\n+COPN: "27411","NOVA"\n+COPN: "27412","Siminn"\n+COPN: "27601","A M C"\n+COPN: "27602","Voda AL"\n+COPN: "27603","EAGLE AL"\n+COPN: "27604","PLUS AL"\n+COPN: "27801","voda MT"\n+COPN: "27821","gomobile"\n+COPN: "27877","MT"\n+COPN: "28001","CYTAVODA"\n+COPN: "28010","MTN"\n+COPN: "28201","GCELL"\n+COPN: "28202","MAGTI"\n+COPN: "28204","BEELINE"\n+COPN: "28300","MTS Arm"\n+COPN: "28301","Beeline"\n+COPN: "28305","MTS Arm"\n+COPN: "28310","Orange"\n+COPN: "28401","Mtel"\n+COPN: "28403","Vivacom"\n+COPN: "28405","GLOBUL"\n+COPN: "28601","TCELL"\n+COPN: "28602","VF TR"\n+COPN: "28603","AVEA"\n+COPN: "28801","FT-GSM"\n+COPN: "28802","VODAFONE"\n+COPN: "29001","TELE GRL"\n+COPN: "29201","SMT"\n+COPN: "29340","Si.mobil"\n+COPN: "29341","MOBITEL"\n+COPN: "29364","T-2"\n+COPN: "29370","TUS"\n+COPN: "29401","TMO MK"\n+COPN: "29402","ONE"\n+COPN: "29403","Vip MKD"\n+COPN: "29501","Swiss FL"\n+COPN: "29502","OFL"\n+COPN: "29505","FL1"\n+COPN: "29577","Alpmobil"\n+COPN: "29701","Telenor"\n+COPN: "29702","T.me"\n+COPN: "302066","MTS"\n+COPN: "302072","ROGERS"\n+COPN: "302220","TELUS"\n+COPN: "302270","Eastlink"\n+COPN: "302320","Mobilicity"\n+COPN: "302340","Execulink"\n+COPN: "302370","Fido"\n+COPN: "302380","DMTS"\n+COPN: "302490","WIND"\n+COPN: "302610","Bell"\n+COPN: "302660","MTS"\n+COPN: "302720","ROGERS"\n+COPN: "302730","TStarSol"\n+COPN: "302770","RuralCom"\n+COPN: "302780","SaskTel"\n+COPN: "302880","FastRoam"\n+COPN: "302940","Wightman"\n+COPN: "30801","AMERIS"\n+COPN: "310000","CBW"\n+COPN: "310002","NEPW"\n+COPN: "310009","NEPW"\n+COPN: "310020","UnionTel"\n+COPN: "310030","CENT USA"\n+COPN: "310031","T-Mobile"\n+COPN: "310032","IT&E"\n+COPN: "310046","SIMMETRY"\n+COPN: "310070","AT&T"\n+COPN: "310080","Corr"\n+COPN: "310090","AT&T"\n+COPN: "310100","PLATEAU"\n+COPN: "310120","Sprint"\n+COPN: "310140","GTA"\n+COPN: "310150","AT&T"\n+COPN: "310160","T-Mobile"\n+COPN: "310170","AT&T"\n+COPN: "310190","D-HARBOR"\n+COPN: "310200","T-Mobile"\n+COPN: "310210","T-Mobile"\n+COPN: "310220","T-Mobile"\n+COPN: "310230","T-Mobile"\n+COPN: "310240","T-Mobile"\n+COPN: "310250","T-Mobile"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "310270","T-Mobile"\n+COPN: "310290","NEPW"\n+COPN: "310300","Big Sky"\n+COPN: "310310","T-Mobile"\n+COPN: "310320","Cell"\n+COPN: "310340","WestLink"\n+COPN: "310380","AT&T"\n+COPN: "310390","CELL 1 ET"\n+COPN: "310400","iCAN_GSM"\n+COPN: "310410","AT&T"\n+COPN: "310420","CBW"\n+COPN: "310450","NECCI"\n+COPN: "310460","USA1L"\n+COPN: "310470","DOCOMOPA"\n+COPN: "310490","SunCom"\n+COPN: "310530","IWS"\n+COPN: "310560","AT&T"\n+COPN: "310570","Chinook"\n+COPN: "310580","T-Mobile"\n+COPN: "310590","Verizon"\n+COPN: "310630","AMERLINK"\n+COPN: "310640","ARDGMC"\n+COPN: "310650","Jasper"\n+COPN: "310660","T-Mobile"\n+COPN: "310680","AT&T"\n+COPN: "310690","IMMIX"\n+COPN: "310710","ASTAC"\n+COPN: "310730","USCC"\n+COPN: "310740","OTZ"\n+COPN: "310770","IWS"\n+COPN: "310800","T-Mobile"\n+COPN: "310840","telna"\n+COPN: "310870","PACE"\n+COPN: "310880","ACSIAC"\n+COPN: "310890","Verizon"\n+COPN: "310950","XIT"\n+COPN: "310980","AT&T"\n+COPN: "311000","Mid-Tex"\n+COPN: "311001","WILKES"\n+COPN: "311005","WILKES"\n+COPN: "311030","Indigo"\n+COPN: "311040","Commnet"\n+COPN: "311080","PINECell"\n+COPN: "311090","SXLP"\n+COPN: "311150","WILKES"\n+COPN: "311170","Broadpoint"\n+COPN: "311180","WCW"\n+COPN: "311190","C1ECI"\n+COPN: "311240","CWCI"\n+COPN: "311260",""\n+COPN: "311310","LamarCel"\n+COPN: "311330","BTW"\n+COPN: "311360","STELERA"\n+COPN: "311370","GCI"\n+COPN: "311380","AT&T"\n+COPN: "311410","AT&T"\n+COPN: "311480","Verizon"\n+COPN: "311500","MOSAIC"\n+COPN: "311530","USANW"\n+COPN: "311540","ProxMo"\n+COPN: "311580","USCC"\n+COPN: "311680","Green Fly"\n+COPN: "311710","NEWN"\n+COPN: "311720","MainePCS"\n+COPN: "311730","ProxMo"\n+COPN: "311940","CLEAR"\n+COPN: "31260","CvgCo"\n+COPN: "312230","SRTW"\n+COPN: "312260","USACL"\n+COPN: "330110","Claro"\n+COPN: "330120","Open Mob"\n+COPN: "33403","movistar"\n+COPN: "33409","Nextel3G"\n+COPN: "33420","TELCEL"\n+COPN: "33450","Iusacell"\n+COPN: "33490","Nextel3G"\n+COPN: "338005","DIGICEL"\n+COPN: "338050","DIGICEL"\n+COPN: "338070","ClaroJam"\n+COPN: "338180","LIME"\n+COPN: "34001","Orange"\n+COPN: "34002","ONLY"\n+COPN: "34003","CHIPPIE"\n+COPN: "34008","DAUPHIN"\n+COPN: "34020","DigicelF"\n+COPN: "342600","LIME"\n+COPN: "342750","DIGICEL"\n+COPN: "344030","imobile"\n+COPN: "344920","LIME"\n+COPN: "344930","Cingular"'),
        #              ('AT+CNAOP=27408',
        #               '+COPN: "348170","LIME"\n+COPN: "348570","CCTBVI"\n+COPN: "35000","CELLONE"\n+COPN: "35002","M3 WIREL"\n+COPN: "35010","Cingular"\n+COPN: "352030","DIGICEL"\n+COPN: "352110","LIME"\n+COPN: "354860","LIME"\n+COPN: "356110","LIME"\n+COPN: "358050","DIGICEL"\n+COPN: "358110","LIME"\n+COPN: "360070","DIGICEL"\n+COPN: "360110","LIME"\n+COPN: "36251","Telcell"\n+COPN: "36269","CT GSM"\n+COPN: "36291","CHIPPIE"\n+COPN: "362951","CHIPPIE"\n+COPN: "36301","SETARGSM"\n+COPN: "36320","DIGICEL"\n+COPN: "36439","BaTelCel"\n+COPN: "365840","LIME"\n+COPN: "366020","Cingular"\n+COPN: "366110","LIME"\n+COPN: "36801","CUBACEL"\n+COPN: "37001","Orange"\n+COPN: "37002","ClaroDOM"\n+COPN: "37004","VIVA"\n+COPN: "37201","VOILA"\n+COPN: "37203","Natcom"\n+COPN: "37412","TSTT"\n+COPN: "376350","LIME"\n+COPN: "376360","ICOM TCI"\n+COPN: "40001","ACELL"\n+COPN: "40002","BAKCELL"\n+COPN: "40004","Nar"\n+COPN: "40101","Beeline"\n+COPN: "40102","KCELL"\n+COPN: "40107","ALTEL"\n+COPN: "40177","NEO"\n+COPN: "40211","B-Mobile"\n+COPN: "40277","TASHICELL"\n+COPN: "40401","Vodafone"\n+COPN: "40402","airtel"\n+COPN: "40403","airtel"\n+COPN: "40404","IDEA"\n+COPN: "40405","Vodafone"\n+COPN: "40407","IDEA"\n+COPN: "40409","RELIANCE"\n+COPN: "40410","airtel"\n+COPN: "40411","Vodafone"\n+COPN: "40412","IDEA"\n+COPN: "40413","Vodafone"\n+COPN: "40414","IDEA"\n+COPN: "40415","Vodafone"\n+COPN: "40416","airtel"\n+COPN: "40417","AIRCEL"\n+COPN: "40418","RELIANCE"\n+COPN: "40419","IDEA"\n+COPN: "40420","Vodafone"\n+COPN: "40421","BPL MOBILE"\n+COPN: "40422","IDEA"\n+COPN: "40424","IDEA"\n+COPN: "40425","AIRCEL"\n+COPN: "40427","Vodafone"\n+COPN: "40428","AIRCEL"\n+COPN: "40429","AIRCEL"\n+COPN: "40430","Vodafone"\n+COPN: "40431","airtel"\n+COPN: "40433","AIRCEL"\n+COPN: "40434","CellOne"\n+COPN: "40435","AIRCEL"\n+COPN: "40436","RELIANCE"\n+COPN: "40437","AIRCEL"\n+COPN: "40438","CellOne"\n+COPN: "40440","airtel"\n+COPN: "40441","AIRCEL"\n+COPN: "40442","AIRCEL"\n+COPN: "40443","Vodafone"\n+COPN: "40444","IDEA"\n+COPN: "40445","airtel"\n+COPN: "40446","Vodafone"\n+COPN: "40449","airtel"\n+COPN: "40450","RELIANCE"\n+COPN: "40451","CellOne"\n+COPN: "40452","RELIANCE"\n+COPN: "40453","CellOne"\n+COPN: "40454","CellOne"\n+COPN: "40455","CellOne"\n+COPN: "40456","IDEA"\n+COPN: "40457","CellOne"\n+COPN: "40458","CellOne"\n+COPN: "40459","CellOne"\n+COPN: "40460","Vodafone"\n+COPN: "40462","CellOne"\n+COPN: "40464","CellOne"\n+COPN: "40466","CellOne"\n+COPN: "40467","RELIANCE"\n+COPN: "40468","DOLPHIN"\n+COPN: "40469","DOLPHIN"\n+COPN: "40470","airtel"\n+COPN: "40471","CellOne"\n+COPN: "40472","CellOne"\n+COPN: "40473","CellOne"\n+COPN: "40474","CellOne"\n+COPN: "40475","CellOne"\n+COPN: "40476","CellOne"\n+COPN: "40477","CellOne"\n+COPN: "40478","IDEA"\n+COPN: "40479","CellOne"\n+COPN: "40480","CellOne"\n+COPN: "40481","CellOne"\n+COPN: "40482","IDEA"\n+COPN: "40483","Reliance"\n+COPN: "40484","Vodafone"\n+COPN: "40485","RELIANCE"\n+COPN: "40486","Vodafone"\n+COPN: "40487","IDEA"\n+COPN: "40488","Vodafone"\n+COPN: "40489","IDEA"\n+COPN: "40490","airtel"\n+COPN: "40491","Aircel"\n+COPN: "40492","airtel"\n+COPN: "40493","airtel"\n+COPN: "40494","airtel"\n+COPN: "40495","airtel"\n+COPN: "40496","airtel"\n+COPN: "40497","airtel"\n+COPN: "40498","airtel"\n+COPN: "40501","Reliance"\n+COPN: "40505","Reliance"\n+COPN: "40506","Reliance"\n+COPN: "40507","Reliance"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "40510","Reliance"\n+COPN: "40511","Reliance"\n+COPN: "40513","Reliance"\n+COPN: "40515","Reliance"\n+COPN: "40518","Reliance"\n+COPN: "40519","Reliance"\n+COPN: "40520","Reliance"\n+COPN: "40521","Reliance"\n+COPN: "40522","Reliance"\n+COPN: "405025","TATA DO"\n+COPN: "405027","TATA DO"\n+COPN: "405029","TATA DO"\n+COPN: "405030","TATA DO"\n+COPN: "405031","TATA DO"\n+COPN: "405032","TATA DO"\n+COPN: "405034","TATA DO"\n+COPN: "405035","TATA DO"\n+COPN: "405036","TATA DO"\n+COPN: "405037","TATA DO"\n+COPN: "405038","TATA DO"\n+COPN: "405039","TATA DO"\n+COPN: "405041","TATA DO"\n+COPN: "405042","TATA DO"\n+COPN: "405043","TATA DO"\n+COPN: "405044","TATA DO"\n+COPN: "405045","TATA DO"\n+COPN: "405046","TATA DO"\n+COPN: "405047","TATA DO"\n+COPN: "40551","airtel"\n+COPN: "40552","airtel"\n+COPN: "40553","airtel"\n+COPN: "40554","airtel"\n+COPN: "40555","airtel"\n+COPN: "40556","airtel"\n+COPN: "40566","Vodafone"\n+COPN: "40567","Vodafone"\n+COPN: "40570","IDEA"\n+COPN: "405750","Vodafone"\n+COPN: "405751","Vodafone"\n+COPN: "405752","Vodafone"\n+COPN: "405753","Vodafone"\n+COPN: "405754","Vodafone"\n+COPN: "405755","Vodafone"\n+COPN: "405756","Vodafone"\n+COPN: "405799","IDEA"\n+COPN: "405800","Aircel"\n+COPN: "405801","Aircel"\n+COPN: "405802","Aircel"\n+COPN: "405803","Aircel"\n+COPN: "405804","Aircel"\n+COPN: "405805","Aircel"\n+COPN: "405806","Aircel"\n+COPN: "405807","Aircel"\n+COPN: "405808","Aircel"\n+COPN: "405809","Aircel "\n+COPN: "405810","Aircel"\n+COPN: "405811","Aircel"\n+COPN: "405812","Aircel"\n+COPN: "405813","UNITECH"\n+COPN: "405814","UNITECH"\n+COPN: "405815","UNITECH"\n+COPN: "405816","UNITECH"\n+COPN: "405817","UNITECH"\n+COPN: "405818","UNITECH"\n+COPN: "405819","UNITECH"\n+COPN: "405820","UNITECH"\n+COPN: "405821","UNITECH"\n+COPN: "405822","UNITECH"\n+COPN: "405823","VIDEOCON"\n+COPN: "405824","VIDEOCON"\n+COPN: "405825","VIDEOCON"\n+COPN: "405827","VIDEOCON"\n+COPN: "405828","VIDEOCON"\n+COPN: "405829","VIDEOCON"\n+COPN: "405830","VIDEOCON"\n+COPN: "405831","VIDEOCON"\n+COPN: "405832","VIDEOCON"\n+COPN: "405833","VIDEOCON"\n+COPN: "405834","VIDEOCON"\n+COPN: "405835","VIDEOCON"\n+COPN: "405836","VIDEOCON"\n+COPN: "405837","VIDEOCON"\n+COPN: "405838","VIDEOCON"\n+COPN: "405839","VIDEOCON"\n+COPN: "405840","VIDEOCON"\n+COPN: "405841","VIDEOCON"\n+COPN: "405842","VIDEOCON"\n+COPN: "405843","VIDEOCON"\n+COPN: "405844","UNITECH"\n+COPN: "405845","IDEA"\n+COPN: "405846","IDEA"\n+COPN: "405848","IDEA"\n+COPN: "405849","IDEA"\n+COPN: "405850","IDEA"\n+COPN: "405852","IDEA"\n+COPN: "405853","IDEA"\n+COPN: "405854","LoopMobile"\n+COPN: "405855","LoopMobile"\n+COPN: "405856","LoopMobile"\n+COPN: "405857","LoopMobile"\n+COPN: "405858","LoopMobile"'),
        #              ('AT+CNAOP=On-waves',
        #               '+COPN: "405860","LoopMobile"\n+COPN: "405861","LoopMobile"\n+COPN: "405862","LoopMobile"\n+COPN: "405863","LoopMobile"\n+COPN: "405864","LoopMobile"\n+COPN: "405865","LoopMobile"\n+COPN: "405866","LoopMobile"\n+COPN: "405867","LoopMobile"\n+COPN: "405868","LoopMobile"\n+COPN: "405869","LoopMobile"\n+COPN: "405870","LoopMobile"\n+COPN: "405871","LoopMobile"\n+COPN: "405872","LoopMobile"\n+COPN: "405873","LoopMobile"\n+COPN: "405874","LoopMobile"\n+COPN: "405875","UNITECH"\n+COPN: "405876","UNITECH"\n+COPN: "405877","UNITECH"\n+COPN: "405878","UNITECH"\n+COPN: "405879","UNITECH"\n+COPN: "405880","UNITECH"\n+COPN: "405912","etisalat"\n+COPN: "405913","etisalat"\n+COPN: "405914","etisalat"\n+COPN: "405915","etisalat"\n+COPN: "405916","etisalat"\n+COPN: "405917","etisalat"\n+COPN: "405918","etisalat"\n+COPN: "405919","etisalat"\n+COPN: "405920","etisalat"\n+COPN: "405921","etisalat"\n+COPN: "405922","etisalat"\n+COPN: "405923","etisalat"\n+COPN: "405924","etisalat"\n+COPN: "405925","UNITECH"\n+COPN: "405926","UNITECH"\n+COPN: "405927","UNITECH"\n+COPN: "405928","UNITECH"\n+COPN: "405929","UNITECH"\n+COPN: "405932","VIDEOCON"\n+COPN: "41001","Mobilink"\n+COPN: "41003","UFONE"\n+COPN: "41004","ZONG"\n+COPN: "41006","TELENOR"\n+COPN: "41007","WaridTel"\n+COPN: "41201","AWCC"\n+COPN: "41220","ROSHAN"\n+COPN: "41240","MTN"\n+COPN: "41250","Etisalat"\n+COPN: "41301","MOBITEL"\n+COPN: "41302","DIALOG"\n+COPN: "41303","Etisalat"\n+COPN: "41305","airtel"\n+COPN: "41308","Hutch"\n+COPN: "41401","MPTGSM"\n+COPN: "41501","alfa"\n+COPN: "41503","MTC LIBAN"\n+COPN: "41505","OM"\n+COPN: "41601","Zain JO"\n+COPN: "41603","UMNIAH"\n+COPN: "41677","Orange JO"\n+COPN: "41701","SYRIATEL"\n+COPN: "41702","MTN"\n+COPN: "41800","ASIACELL"\n+COPN: "41805","ASIACELL"\n+COPN: "41820","zain IQ"\n+COPN: "41830","IRAQNA"\n+COPN: "41840","KOREK"\n+COPN: "41902","zain KW"\n+COPN: "41903","WATANIYA"\n+COPN: "41904","VIVA"\n+COPN: "42001","STC"\n+COPN: "42003","Mobily"\n+COPN: "42004","Zain SA"\n+COPN: "42101","SABAFON"\n+COPN: "42102","MTN"\n+COPN: "42104","Y"\n+COPN: "421700","Y"\n+COPN: "42202","OMAN"\n+COPN: "42203","nawras"\n+COPN: "42402","ETISALAT"\n+COPN: "42403","du"\n+COPN: "42501","Orange IL"\n+COPN: "42502","Cellcom"\n+COPN: "42503","PCL"\n+COPN: "42505","JAWWAL"\n+COPN: "42506","WM"\n+COPN: "42507","Hot Mobile"\n+COPN: "42601","BATELCO"\n+COPN: "42602","Zain BH"\n+COPN: "42604","VIVA BH"\n+COPN: "42701","Ooredoo"\n+COPN: "42702","VF-QA"\n+COPN: "42806","GMOBILE"\n+COPN: "42888","UNTLMN"\n+COPN: "42899","MobiCom"\n+COPN: "42901","NT"\n+COPN: "42902","Ncell"\n+COPN: "43211","IR-TCI"\n+COPN: "43214","KIFZO"\n+COPN: "43219","MTCE"\n+COPN: "43220","IRN 20"\n+COPN: "43232","Taliya"\n+COPN: "43235","Irancell"\n+COPN: "43404","Beeline"\n+COPN: "43405","Ucell"\n+COPN: "43407","UZB MTS"\n+COPN: "43601","TCELL"\n+COPN: "43602","TCELL"\n+COPN: "43603","MegaFon"\n+COPN: "43604","Babilon"\n+COPN: "43605","BEELINE"\n+COPN: "43701","Beeline KG"\n+COPN: "43705","MEGACOM"\n+COPN: "43709","O!"\n+COPN: "43801","MTS TM"\n+COPN: "43802","TM CELL"\n+COPN: "44000","EMOBILE"\n+COPN: "44010","DOCOMO"\n+COPN: "44020","SoftBank"\n+COPN: "44050","KDDI"\n+COPN: "45001","Samsung"\n+COPN: "45002","KT"\n+COPN: "45005","SKT"\n+COPN: "45006","LG U+"\n+COPN: "45008","KT"\n+COPN: "45200","VN MOBIF"\n+COPN: "45201","VN MobiFon"\n+COPN: "45202","GPC"\n+COPN: "45204","VIETTEL"\n+COPN: "45205","VNMOBILE"\n+COPN: "45207","Gmobile"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "45402","CSL"\n+COPN: "45403","3"\n+COPN: "45404","3(2G)"\n+COPN: "45406","SMC HK"\n+COPN: "45410","CSL"\n+COPN: "45412","CMHK"\n+COPN: "45413","CMHK"\n+COPN: "45415","SMC HK"\n+COPN: "45416","PCCW-HKT"\n+COPN: "45417","SMC HK"\n+COPN: "45418","CSL"\n+COPN: "45419","PCCW-HKT"\n+COPN: "45420","PCCW-HKT"\n+COPN: "45500","SMC MAC"\n+COPN: "45501","CTM"\n+COPN: "45503","3 Macau"\n+COPN: "45504","CTM"\n+COPN: "45505","3 Macau"\n+COPN: "45601","Cellcard"\n+COPN: "45602","Hello"\n+COPN: "45604","CADCOMMS"\n+COPN: "45605","SMART"\n+COPN: "45606","SMART"\n+COPN: "45608","Metfone"\n+COPN: "45609","Beeline"\n+COPN: "45618","Mfone"\n+COPN: "45701","LAO GSM"\n+COPN: "45702","ETLMNW"\n+COPN: "45703","UNITEL"\n+COPN: "45708","TIGO"\n+COPN: "46000","CMCC"\n+COPN: "46001","UNICOM"\n+COPN: "46002","CMCC"\n+COPN: "46003","CTCC"\n+COPN: "46005","CTCC"\n+COPN: "46006","UNICOM"\n+COPN: "46007","CMCC"\n+COPN: "46008","CMCC"\n+COPN: "46009","UNICOM"\n+COPN: "46011","CTCC"\n+COPN: "46601","FET"\n+COPN: "46668","ACeS"\n+COPN: "46688","KGT"\n+COPN: "46689","VIBO"\n+COPN: "46692","Chunghwa"\n+COPN: "46693","TW MOB"\n+COPN: "46697","TWM"\n+COPN: "467005","KL-DPRK"\n+COPN: "47001","Grameen"\n+COPN: "47002","ROBIAXIATA"\n+COPN: "47003","B-LINK"\n+COPN: "47004","bMobile"\n+COPN: "47007","Airtel"\n+COPN: "47201","DHIRAAGU"\n+COPN: "47202","Ooredoo"\n+COPN: "50212","MY MAXIS"\n+COPN: "50213","CELCOM"\n+COPN: "50216","DiGi"\n+COPN: "50218","U MOBILE"\n+COPN: "50219","CELCOM"\n+COPN: "50501","Telstra"\n+COPN: "50502","Optus"\n+COPN: "50503","voda AU"\n+COPN: "50506","3TELSTRA"\n+COPN: "50510","NT"\n+COPN: "51000","ACeS"\n+COPN: "51001","INDOSAT"\n+COPN: "51008","AXIS"\n+COPN: "51010","T-SEL"\n+COPN: "51011","XL"\n+COPN: "51021","INDOSAT"\n+COPN: "51089","3"\n+COPN: "510510","Mobile-8"\n+COPN: "51402","TT"\n+COPN: "51501","ISLACOM"\n+COPN: "51502","GLOBE"\n+COPN: "51503","SMART"\n+COPN: "51505","SUN"\n+COPN: "51511","ACeS"\n+COPN: "52000","TH 3G+"\n+COPN: "52001","TH GSM"\n+COPN: "52002","TH CAT"\n+COPN: "52003","AIS 3G"\n+COPN: "52004","TRUE 3G+"\n+COPN: "52005","dtac"\n+COPN: "52015","TOT3G"\n+COPN: "52018","DTAC"'),
        #              ('AT+CNAOP=27411',
        #               '+COPN: "52023","GSM 1800"\n+COPN: "52099","TRUE"\n+COPN: "52501","SingTel"\n+COPN: "52502","SingTel"\n+COPN: "52503","M1"\n+COPN: "52505","STARHUB"\n+COPN: "52507","CallZone"\n+COPN: "52802","b-mobile"\n+COPN: "52811","DSTCom"\n+COPN: "53001","voda NZ"\n+COPN: "53005","Telecom"\n+COPN: "53024","2degrees"\n+COPN: "53701","BMobile"\n+COPN: "53703","DIGICEL"\n+COPN: "53730","Digicel"\n+COPN: "53901","U-CALL"\n+COPN: "53988","Digicel"\n+COPN: "54001","BREEZE"\n+COPN: "54002","Bemobile"\n+COPN: "54101","SMILE"\n+COPN: "54105","Digicel"\n+COPN: "54201","VODAFONE"\n+COPN: "54202","DIGICEL"\n+COPN: "542542","Digicel "\n+COPN: "544110","BLUESKY"\n+COPN: "54509","KI-FRIG"\n+COPN: "54601","MOBNCL"\n+COPN: "54715","VF PF"\n+COPN: "54720","VINI"\n+COPN: "54801","KOKANET"\n+COPN: "54900","DIGICEL"\n+COPN: "54927","Bluesky"\n+COPN: "55001","FSMTC"\n+COPN: "55101","NTA"\n+COPN: "55201","PalauCel"\n+COPN: "55280","PLWPMC"\n+COPN: "60201","MobiNiL"\n+COPN: "60202","voda EG"\n+COPN: "60203","Etisalat"\n+COPN: "60301","Mobilis"\n+COPN: "60302","Djezzy"\n+COPN: "60303","Ooredoo"\n+COPN: "60400","MEDITEL"\n+COPN: "60401","IAM"\n+COPN: "60402","inwi"\n+COPN: "60501","Orange"\n+COPN: "60502","TUNTEL"\n+COPN: "60503","TUNSIANA"\n+COPN: "60600","L"\n+COPN: "60601","Al Madar"\n+COPN: "60701","GAMCEL"\n+COPN: "60702","AFRICELL"\n+COPN: "60703","GMCOMIUM"\n+COPN: "60704","QC"\n+COPN: "60801","ALIZE"\n+COPN: "60802","SENTEL"\n+COPN: "60803","Expresso"\n+COPN: "60901","MATTEL"\n+COPN: "60902","EMR"\n+COPN: "60910","MAURITEL"\n+COPN: "61001","MALITEL"\n+COPN: "61002","OML"\n+COPN: "61101","ORANGEGN"\n+COPN: "61102","LAGUI"\n+COPN: "61104","GNAreeba"\n+COPN: "61105","CellcomGN"\n+COPN: "61202","ETISALAT"\n+COPN: "61203","Orange"\n+COPN: "61204","KoZ"\n+COPN: "61205","MTN CI"\n+COPN: "61302","Celtel"\n+COPN: "61402","CELTEL"\n+COPN: "61403","ETISALAT"\n+COPN: "61404","Orange"\n+COPN: "61501","TGCELL"\n+COPN: "61503","ETISALAT"\n+COPN: "61602","ETISALAT"\n+COPN: "61603","MTN BENIN"\n+COPN: "61604","BBCOM"\n+COPN: "61605","GloBenin"\n+COPN: "61701","CELL +"\n+COPN: "61703","MTML"\n+COPN: "61710","EMTEL"\n+COPN: "61801","LoneStar"\n+COPN: "61804","Novafone"\n+COPN: "61807","Celcom"\n+COPN: "61900","SLE COMI"\n+COPN: "61901","CELTEL"\n+COPN: "61904","SLE COMIUM"\n+COPN: "61905","Africell"\n+COPN: "61907","GreenN "\n+COPN: "62001","MTN"\n+COPN: "62002","Vodafone"\n+COPN: "62003","tiGO GHANA"\n+COPN: "62006","Airtel"\n+COPN: "62007","Glo Ghana"\n+COPN: "62120","AirtelNG"\n+COPN: "62130","MTN-NG"\n+COPN: "62150","glo"\n+COPN: "62160","Etisalat"\n+COPN: "62201","CELTEL"\n+COPN: "62203","Tigo"\n+COPN: "62207","SALAM"\n+COPN: "62301","ETISALAT"\n+COPN: "62302","Telecel"\n+COPN: "62304","NL-RCA"\n+COPN: "62401","MTN CAM"\n+COPN: "62402","Orange"\n+COPN: "62501","CMOVEL"\n+COPN: "62502","T+"\n+COPN: "62601","CSTmovel"\n+COPN: "62701","GETESA"\n+COPN: "62703","Muni-GQ"\n+COPN: "62801","LIBERTIS"\n+COPN: "62802","ETISALAT"\n+COPN: "62803","ZAIN"\n+COPN: "62902","AZUR COG"\n+COPN: "62907","WARIDRC"\n+COPN: "62910","MTN-CG"\n+COPN: "63001","VODACOM"\n+COPN: "63002","CELTEL"\n+COPN: "63005","SCELL"\n+COPN: "63086","Orange"\n+COPN: "63088","Smart"\n+COPN: "63089","TIGO"\n+COPN: "63090","AFRICELL"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "63202","MTN"\n+COPN: "63203","ORANGE BS"\n+COPN: "63301","C&W SEY"\n+COPN: "63310","AIRTEL"\n+COPN: "63401","Zain SD"\n+COPN: "63402","MTN"\n+COPN: "63405","Vivacell"\n+COPN: "63510","MTN Rwanda"\n+COPN: "63513","TIGO RW"\n+COPN: "63514","AR"\n+COPN: "63601","ET-MTN"\n+COPN: "63701","Tele"\n+COPN: "63704","SOMAFONE"\n+COPN: "63720","SOMNET"\n+COPN: "63730","Golis"\n+COPN: "63740","MONTYSOM"\n+COPN: "63771","SOMTEL"\n+COPN: "63782","Telsom"\n+COPN: "63801","EVATIS"\n+COPN: "63902","SAF-COM"\n+COPN: "63903","Airtel"\n+COPN: "63907","GSMTKL"\n+COPN: "64002","TIGO"\n+COPN: "64003","ZANTEL"\n+COPN: "64004","VodaCom"\n+COPN: "64005","celtel"\n+COPN: "64008","Smart TZA"\n+COPN: "64101","CELTEL"\n+COPN: "64110","MTN-UG"\n+COPN: "64111","UTL"\n+COPN: "64114","OUL"\n+COPN: "64122","WaridTel"\n+COPN: "64201","EWB"\n+COPN: "64202","TEMPO-AF"\n+COPN: "64203","ONATEL"\n+COPN: "64207","SMART"\n+COPN: "64282","BDITL"\n+COPN: "64301","mCel"\n+COPN: "64303","MOVITEL"\n+COPN: "64304","VodaCom"\n+COPN: "64501","CELTEL"\n+COPN: "64502","MTN ZM"\n+COPN: "64601","ZAIN"\n+COPN: "64602","OrangeMG"\n+COPN: "64604","TELMA"\n+COPN: "64700","Orange"\n+COPN: "64702","OUTREMER"\n+COPN: "64710","SFR RU"\n+COPN: "64801","NETONE"\n+COPN: "64803","TELECEL"\n+COPN: "64804","ECONET"\n+COPN: "64901","MTCNAM"\n+COPN: "64903","tnmobile"\n+COPN: "65001","TNM"\n+COPN: "65010","CELTEL"\n+COPN: "65101","Vodacom-LS"\n+COPN: "65102","ETL"\n+COPN: "65201","MASCOM"\n+COPN: "65202","Orange"\n+COPN: "65204","beMOBILE"\n+COPN: "65310","SwaziMTN"\n+COPN: "65401","HURI"\n+COPN: "65501","VODA"\n+COPN: "65502","TelkomSA"\n+COPN: "65507","Cell C"\n+COPN: "65510","MTN"\n+COPN: "65902","MTN"\n+COPN: "65903","Gemtel"\n+COPN: "65904","Vivacell"\n+COPN: "65906","ZAIN SS"\n+COPN: "70267","BTL"\n+COPN: "70401","ClaroGTM"\n+COPN: "70402","COMCEL"\n+COPN: "70403","Movistar"\n+COPN: "70601","ClaroSLV"\n+COPN: "70602","DIGICEL"\n+COPN: "70603","TM"\n+COPN: "70604","movistar"\n+COPN: "70801","ClaroHND"\n+COPN: "70802","CELTEL"\n+COPN: "70830","HT - 200"\n+COPN: "71021","ClaroNIC"\n+COPN: "71073","ClaroNIC"\n+COPN: "710300","movistar"\n+COPN: "71200","I.C.E."\n+COPN: "71201","I.C.E."\n+COPN: "71202","I.C.E."\n+COPN: "71203","CLARO CR"\n+COPN: "71204","Movistar"\n+COPN: "71401","PANCW"\n+COPN: "71403","CLARO PA"\n+COPN: "71404","DIGICEL"\n+COPN: "71420","Movistar"'),
        #              ('AT+CNAOP=NOVA',
        #               '+COPN: "71610","ClaroPER"\n+COPN: "71615","VTP"\n+COPN: "71617","NXT3"\n+COPN: "72201","Movistar"\n+COPN: "72207","Movistar"\n+COPN: "72210","Movistar"\n+COPN: "72234","AR TP"\n+COPN: "72236","AR TP"\n+COPN: "722310","CLARO AR"\n+COPN: "722341","AR TP"\n+COPN: "72402","TIM"\n+COPN: "72403","TIM"\n+COPN: "72404","TIM"\n+COPN: "72405","Claro"\n+COPN: "72406","VIVO"\n+COPN: "72410","VIVO"\n+COPN: "72411","VIVO"\n+COPN: "72415","SCTL"\n+COPN: "72416","Oi"\n+COPN: "72423","VIVO"\n+COPN: "72424","AMAZONIA"\n+COPN: "72431","Oi"\n+COPN: "72432","CTBC"\n+COPN: "72433","CTBC"\n+COPN: "72434","CTBC"\n+COPN: "72439","Nextel 3G"\n+COPN: "73001","ENTEL"\n+COPN: "73002","Movistar"\n+COPN: "73003","ClaroCHL"\n+COPN: "73007","Movistar"\n+COPN: "73008","VTR"\n+COPN: "73009","Nextel3G"\n+COPN: "73010","ENTEL"\n+COPN: "730730","Movistar"\n+COPN: "73200","Comcel S"\n+COPN: "732101","Claro"\n+COPN: "732103","TIGO COL"\n+COPN: "732111","TIGO COL"\n+COPN: "732123","Movistar"\n+COPN: "73401","DIGITEL"\n+COPN: "73402","DIGITEL"\n+COPN: "73403","DIGITEL"\n+COPN: "73404","movistar"\n+COPN: "73406","Movilnet"\n+COPN: "73601","VIVA"\n+COPN: "73602","EMOVIL"\n+COPN: "73603","Telecel"\n+COPN: "73801","DIGICEL"\n+COPN: "73802","CLNKPLS"\n+COPN: "738592","CLNKPLS"\n+COPN: "74000","Movistar"\n+COPN: "74001","CLARO"\n+COPN: "74002","CNT"\n+COPN: "74401","HPGYSA"\n+COPN: "74402","CLARO PY"\n+COPN: "74404","TIGO"\n+COPN: "74405","Personal"\n+COPN: "74602","TeleG"\n+COPN: "74603","DIGICEL"\n+COPN: "74604","UNIQA"\n+COPN: "74801","Antel"\n+COPN: "74807","Movistar"\n+COPN: "74810","CLARO UY"\n+COPN: "75001","C&W FLK"\n+COPN: "79502","TM CELL"\n+COPN: "90105","Thuraya"\n+COPN: "90106","Thuraya"\n+COPN: "90111","INX"\n+COPN: "90112","MCP"\n+COPN: "90114","AeroMob"\n+COPN: "90115","OnAir"\n+COPN: "90118","WMS"\n+COPN: "90121","Seanet"\n+COPN: "90126","TIM@sea"\nOK\n+CME ERROR: Operation not supported\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR'),
        #              ('AT+CNAOP?', 'ERROR'),
        #              ('AT+CNAOP=27412', 'ERROR'),
        #              ('AT+CNAOP?', 'ERROR'),
        #              ('AT+CNAOP=Siminn', 'ERROR'),
        #              ('AT+CNAOP?', 'ERROR'),
        #              ],

        # РЕГИСТРАЦИЯ В СЕТЯХ -------------------------------------
        'AT+CREG?': ['GSM=network registration (CS), =0>disable, =1>регистрация в домашней сети успешна! после изменения необходимо время!',
                     # без симки
                     ('AT+CREG=?', '+CREG: (0-2)\nOK'),
                     ('AT+CREG', 'OK'),
                     ('AT+CREG?', '+CREG: 0,0\nOK'),        # СЕТИ НЕ ЗАРЕГИСТРИРОВАНЫ???
                     ('AT+CREG=0', 'OK'),
                     ('AT+CREG?', '+CREG: 0,0\nOK'),
                     ('AT+CREG=1', 'OK'),
                     ('AT+CREG?', '+CREG: 1,0\nOK'),
                     ('AT+CREG=2', 'OK'),
                     ('AT+CREG?', '+CREG: 2,0\nOK'),

                     # с симкой
                     ('AT+CREG=?', '+CREG: (0-2)\nOK'),
                     ('AT+CREG', 'OK'),
                     ('AT+CREG?', '+CREG: 0,1\nOK'),
                     ('AT+CREG=0', 'OK'),
                     ('AT+CREG?', '+CREG: 0,1\nOK'),
                     ('AT+CREG=1', 'OK'),
                     ('AT+CREG?', '+CREG: 1,1\nOK'),
                     ('AT+CREG=2', 'OK'),
                     ('AT+CREG?', '+CREG: 2,1,0321,000008B1\nOK'),
                     ('AT+CREG?', '+CREG: 2,1,0B3D,0BD1591A\nOK'),  # navia

                     # после изменения нужно выждать время!
                     # ---- Sent utf8 encoded message: "AT+CREG=2\r\n" ----
                     # AT+CREG=2
                     # OK
                     # ---- Sent utf8 encoded message: "AT+CREG\r\n" ----
                     # AT+CREG
                     # OK
                     # ---- Sent utf8 encoded message: "AT+CREG?\r\n" ----
                     # AT+CREG?
                     # +CREG: 0,1
                     #
                     # OK
                     # ---- Sent utf8 encoded message: "AT+CREG=2\r\n" ----
                     # AT+CREG=2
                     # OK
                     # ---- Sent utf8 encoded message: "AT+CREG?\r\n" ----
                     # AT+CREG?
                     # +CREG: 2,1,0B3D,0BD1591A
                     #
                     # OK

                     ],
        'AT+CGREG?': ['GPRS=registration (PS)=1 registered, также нужно ждать время после изменения!',
                      # без симки
                      ('AT+CGREG=?', '+CGREG: (0-2)\nOK'),
                      ('AT+CGREG', 'OK'),
                      ('AT+CGREG?', '+CGREG: 0,0\nOK'),
                      ('AT+CGREG=0', 'OK'),
                      ('AT+CGREG?', '+CGREG: 0,0\nOK'),
                      ('AT+CGREG=1', 'OK'),
                      ('AT+CGREG?', '+CGREG: 1,0\nOK'),
                      ('AT+CGREG=2', 'OK'),
                      ('AT+CGREG?', '+CGREG: 2,0,"0000","00000000"\nOK'),

                      # с симкой
                      ('AT+CGREG=?', '+CGREG: (0-2)\nOK'),
                      ('AT+CGREG', 'OK'),
                      ('AT+CGREG?', '+CGREG: 0,1\nOK'),
                      ('AT+CGREG=0', 'OK'),
                      ('AT+CGREG?', '+CGREG: 0,1\nOK'),
                      ('AT+CGREG=1', 'OK'),
                      ('AT+CGREG?', '+CGREG: 1,1\nOK'),
                      ('AT+CGREG=2', 'OK'),     # после изменения также ждать требуется!
                      ('AT+CGREG?', '+CGREG: 2,1,"0321","000008b1"\nOK'),
                      ('AT+CGREG?', '+CGREG: 2,1,0B3D,0BD1591A\nOK'),   # navia
                      ],
        'AT+CEREG?': ['EPS (LTE/4G) registration=',
                      # без симки и с
                      ('AT+CEREG=?', '+CEREG: (0-2)\nOK'),
                      ('AT+CEREG', 'OK'),
                      ('AT+CEREG?', '+CEREG: 0,0\nOK'),
                      ('AT+CEREG=0', 'OK'),
                      ('AT+CEREG?', '+CEREG: 0,0\nOK'),
                      ('AT+CEREG=1', 'OK'),
                      ('AT+CEREG?', '+CEREG: 1,0\nOK'),
                      ('AT+CEREG=2', 'OK'),    # после изменения вроде ждать требуется - но хуже тоо что пока не вернешь в 0 - будет слать постоянно отчет один и тот же!
                      ('AT+CEREG?', '+CEREG: 2,0,0000,00000000\nOK'),
                      ('AT+CEREG?', '+CEREG: 1,0B3D,0BC24B66,7\nOK'),
                      ],

        # -------------------------------------------
        '-AT+COPS?': ["[DANGER=БЛОК на 80секунд на запросе параметров =?]operator selection",
             # NAVIA!

            ("AT+COPS=?",   # [DANGER] запрос блокирует на 80сек!!! ответ одной строкой без разноса!
             '+COPS: (2,"Next B","Next B","25099",7),(1,"Next MF","Next MF","25002",0),(1,"Next B","Next B","25099",0),(1,"Next M","Next M","25001",0),(1,"Next M","Next M","25001",7),(1,"Next T","Next T","25020",7),(1,"Next MF","Next MF","25002",7),(1,"YOTA","YOTA","25011",7),,(0,1,2,3,4),(0,1,2)'),
            ('AT+COPS', 'ERROR'),
            ("AT+COPS?", "+COPS: 0,2,\"25099\",7\nOK"),

            ("AT+COPS?", "+COPS: 0,2,\"25020\",7\nOK"), # хз

            # наверное без симки???? хз!
            ('AT+COPS=?', ''),
            ('AT+COPS', ''),
            ('AT+COPS?', ''),
        ],
        # -------------------------------------------
        'AT+CUSD?': ['USSD',
                     # без симки и с
                     ('AT+CUSD=?', '+CUSD: (0-2)\nOK'),
                     ('AT+CUSD', 'OK'),
                     ('AT+CUSD?', '+CUSD: 0\nOK'),
                     ('AT+CUSD=0', 'OK'),
                     ('AT+CUSD?', '+CUSD: 0\nOK'),
                     ('AT+CUSD=1', 'OK'),
                     ('AT+CUSD?', '+CUSD: 1\nOK'),
                     ('AT+CUSD=2', 'OK'),
                     ('AT+CUSD?', '+CUSD: 1\nOK'),
                     ],
        'AT+CAOC?': ['advice of charge',
                     # без симки и с
                     ('AT+CAOC=?', '+CAOC: (0-2)\nOK'),
                     ('AT+CAOC', 'ERROR'),
                     ('AT+CAOC?', '+CAOC: 2\nOK'),
                     ('AT+CAOC=0', '+CAOC:"000000"\nOK'),
                     ('AT+CAOC?', '+CAOC: 2\nOK'),
                     ('AT+CAOC=1', 'OK'),
                     ('AT+CAOC?', '+CAOC: 1\nOK'),
                     ('AT+CAOC=2', 'OK'),
                     ('AT+CAOC?', '+CAOC: 2\nOK'),
                     ],
        'AT+CSSN?': ['supplementary service notifications',
                     # без симки и с
                     ('AT+CSSN=?', '+CSSN: (0-1),(0-1)\nOK'),
                     ('AT+CSSN', 'ERROR'),
                     ('AT+CSSN?', '+CSSN: 1,0\nOK'),
                     ('AT+CSSN=0', 'OK'),
                     ('AT+CSSN?', '+CSSN: 0,0\nOK'),
                     ('AT+CSSN=1', 'OK'),
                     ('AT+CSSN?', '+CSSN: 1,0\nOK'),
                     ],
        'AT+CPSI?': ['UE system information=ВЫШКА СОТОВАЯ',
                     ('AT+CPSI=?', 'OK'),
                     ('AT+CPSI', 'ERROR'),
                     ('AT+CPSI?', '+CPSI: NO SERVICE,Online\nOK'),  # без симки
                     ('AT+CPSI?', '+CPSI: GSM,Online,250-01,0x321,2225,874 DCS 1800,47,0,29-61\nOK'),   # с симкой
                     ('AT+CPSI?', '+CPSI: LTE,Online,250-99,0xB3D,198269305,464,EUTRAN-BAND1,525,4,0,0,33,43,-7\nOK'),   # Navia
                     ],
        'AT+CTZU?': ['automatic time zone update, 1=set AUTO, 0=disable',
                     # без симки и с
                     ('AT+CTZU=?', '+CTZU: (0-1)\nOK'),
                     ('AT+CTZU', 'ERROR'),
                     ('AT+CTZU?', '+CTZU: 1\nOK'),
                     ('AT+CTZU=0', 'OK'),
                     ('AT+CTZU?', '+CTZU: 0\nOK'),
                     ('AT+CTZU=1', 'OK'),
                     ('AT+CTZU?', '+CTZU: 1\nOK'),
                     ],
        'AT+CTZR?': ['time zone reporting',
                     # без симки и с
                     ('AT+CTZR=?', '+CTZR: (0-1)\nOK'),
                     ('AT+CTZR', 'OK'),
                     ('AT+CTZR?', '+CTZR: 0\nOK'),
                     ('AT+CTZR=0', 'OK'),
                     ('AT+CTZR?', '+CTZR: 0\nOK'),
                     ('AT+CTZR=1', 'OK'),
                     ('AT+CTZR?', '+CTZR: 1\nOK'),
                     ],
        'AT+CESQ': ['extended signal quality',
                    ('AT+CESQ=?', '+CESQ: (0-63,99),(0-7,99),(0-96,255),(0-49,255),(0-34,255),(0-97,255)\nOK'),
                    ('AT+CESQ', '+CESQ: 45,0,255,255,255,255\nOK'),     # без симки
                    ('AT+CESQ', '+CESQ: 51,0,255,255,255,255\nOK'),     # с симкой
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=0', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=1', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=2', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=3', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=4', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=5', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=6', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=7', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=8', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=9', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),

                    # еще вариант с симкой!!!
                    ('AT+CESQ=?', '+CESQ: (0-63,99),(0-7,99),(0-96,255),(0-49,255),(0-34,255),(0-97,255)\nOK'),
                    ('AT+CESQ', '+CESQ: 47,0,255,255,255,255\nOK'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=0', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=1', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=2', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=3', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=4', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=5', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=6', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=7', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=8', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ('AT+CESQ=9', '+CME ERROR: 100'),
                    ('AT+CESQ?', '+CME ERROR: 100'),
                    ],
        'AT+CPOL?': ['preferred operator list',
                    # без симки
                    ('AT+CPOL=?', '+CME ERROR: SIM failure'),
                    ('AT+CPOL', 'ERROR\n+CME ERROR: SIM failure'),
                    ('AT+CPOL?', 'ERROR\n+CME ERROR: SIM failure'),

                    # с симкой
                    ('AT+CPOL=?', '+CPOL: (1-30),(0-2)\nOK'),
                    ('AT+CPOL', '+CME ERROR: Incorrect parameters'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,0,1\n+CPOL: 2,2,"25020",0,0,1,0\n+CPOL: 3,2,"25020",1,0,0,0\n+CPOL: 4,2,"25039",0,0,0,1\n+CPOL: 5,2,"25039",0,0,1,0\n+CPOL: 6,2,"25039",1,0,0,0\n+CPOL: 7,2,"25099",0,0,0,1\n+CPOL: 8,2,"25099",0,0,1,0\n+CPOL: 9,2,"25099",1,0,0,0\n+CPOL: 10,2,"25095",0,0,0,1\n+CPOL: 11,2,"25095",0,0,1,0\n+CPOL: 12,2,"25095",1,0,0,0\n+CPOL: 13,2,"25001",0,0,0,1\n+CPOL: 14,2,"25001",0,0,1,0\n+CPOL: 15,2,"25001",1,0,0,0\n+CPOL: 16,2,"25058",0,0,0,1\n+CPOL: 17,2,"25058",0,0,1,0\n+CPOL: 18,2,"25058",1,0,0,0\n+CPOL: 19,2,"25002",0,0,0,1\n+CPOL: 20,2,"25002",0,0,1,0\n+CPOL: 21,2,"25002",1,0,0,0\n+CPOL: 22,2,"25007",0,0,0,1\n+CPOL: 23,2,"25007",0,0,1,0\n+CPOL: 24,2,"25007",1,0,0,0\n+CPOL: 25,2,"25035",0,0,0,1\n+CPOL: 26,2,"25035",0,0,1,0\n+CPOL: 27,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=0', '+CME ERROR: Incorrect parameters'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,0,1\n+CPOL: 2,2,"25020",0,0,1,0\n+CPOL: 3,2,"25020",1,0,0,0\n+CPOL: 4,2,"25039",0,0,0,1\n+CPOL: 5,2,"25039",0,0,1,0\n+CPOL: 6,2,"25039",1,0,0,0\n+CPOL: 7,2,"25099",0,0,0,1\n+CPOL: 8,2,"25099",0,0,1,0\n+CPOL: 9,2,"25099",1,0,0,0\n+CPOL: 10,2,"25095",0,0,0,1\n+CPOL: 11,2,"25095",0,0,1,0\n+CPOL: 12,2,"25095",1,0,0,0\n+CPOL: 13,2,"25001",0,0,0,1\n+CPOL: 14,2,"25001",0,0,1,0\n+CPOL: 15,2,"25001",1,0,0,0\n+CPOL: 16,2,"25058",0,0,0,1\n+CPOL: 17,2,"25058",0,0,1,0\n+CPOL: 18,2,"25058",1,0,0,0\n+CPOL: 19,2,"25002",0,0,0,1\n+CPOL: 20,2,"25002",0,0,1,0\n+CPOL: 21,2,"25002",1,0,0,0\n+CPOL: 22,2,"25007",0,0,0,1\n+CPOL: 23,2,"25007",0,0,1,0\n+CPOL: 24,2,"25007",1,0,0,0\n+CPOL: 25,2,"25035",0,0,0,1\n+CPOL: 26,2,"25035",0,0,1,0\n+CPOL: 27,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=1', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25020",1,0,0,0\n+CPOL: 3,2,"25039",0,0,0,1\n+CPOL: 4,2,"25039",0,0,1,0\n+CPOL: 5,2,"25039",1,0,0,0\n+CPOL: 6,2,"25099",0,0,0,1\n+CPOL: 7,2,"25099",0,0,1,0\n+CPOL: 8,2,"25099",1,0,0,0\n+CPOL: 9,2,"25095",0,0,0,1\n+CPOL: 10,2,"25095",0,0,1,0\n+CPOL: 11,2,"25095",1,0,0,0\n+CPOL: 12,2,"25001",0,0,0,1\n+CPOL: 13,2,"25001",0,0,1,0\n+CPOL: 14,2,"25001",1,0,0,0\n+CPOL: 15,2,"25058",0,0,0,1\n+CPOL: 16,2,"25058",0,0,1,0\n+CPOL: 17,2,"25058",1,0,0,0\n+CPOL: 18,2,"25002",0,0,0,1\n+CPOL: 19,2,"25002",0,0,1,0\n+CPOL: 20,2,"25002",1,0,0,0\n+CPOL: 21,2,"25007",0,0,0,1\n+CPOL: 22,2,"25007",0,0,1,0\n+CPOL: 23,2,"25007",1,0,0,0\n+CPOL: 24,2,"25035",0,0,0,1\n+CPOL: 25,2,"25035",0,0,1,0\n+CPOL: 26,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=2', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25039",0,0,0,1\n+CPOL: 3,2,"25039",0,0,1,0\n+CPOL: 4,2,"25039",1,0,0,0\n+CPOL: 5,2,"25099",0,0,0,1\n+CPOL: 6,2,"25099",0,0,1,0\n+CPOL: 7,2,"25099",1,0,0,0\n+CPOL: 8,2,"25095",0,0,0,1\n+CPOL: 9,2,"25095",0,0,1,0\n+CPOL: 10,2,"25095",1,0,0,0\n+CPOL: 11,2,"25001",0,0,0,1\n+CPOL: 12,2,"25001",0,0,1,0\n+CPOL: 13,2,"25001",1,0,0,0\n+CPOL: 14,2,"25058",0,0,0,1\n+CPOL: 15,2,"25058",0,0,1,0\n+CPOL: 16,2,"25058",1,0,0,0\n+CPOL: 17,2,"25002",0,0,0,1\n+CPOL: 18,2,"25002",0,0,1,0\n+CPOL: 19,2,"25002",1,0,0,0\n+CPOL: 20,2,"25007",0,0,0,1\n+CPOL: 21,2,"25007",0,0,1,0\n+CPOL: 22,2,"25007",1,0,0,0\n+CPOL: 23,2,"25035",0,0,0,1\n+CPOL: 24,2,"25035",0,0,1,0\n+CPOL: 25,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=3', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25039",0,0,0,1\n+CPOL: 3,2,"25039",1,0,0,0\n+CPOL: 4,2,"25099",0,0,0,1\n+CPOL: 5,2,"25099",0,0,1,0\n+CPOL: 6,2,"25099",1,0,0,0\n+CPOL: 7,2,"25095",0,0,0,1\n+CPOL: 8,2,"25095",0,0,1,0\n+CPOL: 9,2,"25095",1,0,0,0\n+CPOL: 10,2,"25001",0,0,0,1\n+CPOL: 11,2,"25001",0,0,1,0\n+CPOL: 12,2,"25001",1,0,0,0\n+CPOL: 13,2,"25058",0,0,0,1\n+CPOL: 14,2,"25058",0,0,1,0\n+CPOL: 15,2,"25058",1,0,0,0\n+CPOL: 16,2,"25002",0,0,0,1\n+CPOL: 17,2,"25002",0,0,1,0\n+CPOL: 18,2,"25002",1,0,0,0\n+CPOL: 19,2,"25007",0,0,0,1\n+CPOL: 20,2,"25007",0,0,1,0\n+CPOL: 21,2,"25007",1,0,0,0\n+CPOL: 22,2,"25035",0,0,0,1\n+CPOL: 23,2,"25035",0,0,1,0\n+CPOL: 24,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=4', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25039",0,0,0,1\n+CPOL: 3,2,"25039",1,0,0,0\n+CPOL: 4,2,"25099",0,0,1,0\n+CPOL: 5,2,"25099",1,0,0,0\n+CPOL: 6,2,"25095",0,0,0,1\n+CPOL: 7,2,"25095",0,0,1,0\n+CPOL: 8,2,"25095",1,0,0,0\n+CPOL: 9,2,"25001",0,0,0,1\n+CPOL: 10,2,"25001",0,0,1,0\n+CPOL: 11,2,"25001",1,0,0,0\n+CPOL: 12,2,"25058",0,0,0,1\n+CPOL: 13,2,"25058",0,0,1,0\n+CPOL: 14,2,"25058",1,0,0,0\n+CPOL: 15,2,"25002",0,0,0,1\n+CPOL: 16,2,"25002",0,0,1,0\n+CPOL: 17,2,"25002",1,0,0,0\n+CPOL: 18,2,"25007",0,0,0,1\n+CPOL: 19,2,"25007",0,0,1,0\n+CPOL: 20,2,"25007",1,0,0,0\n+CPOL: 21,2,"25035",0,0,0,1\n+CPOL: 22,2,"25035",0,0,1,0\n+CPOL: 23,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=5', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25039",0,0,0,1\n+CPOL: 3,2,"25039",1,0,0,0\n+CPOL: 4,2,"25099",0,0,1,0\n+CPOL: 5,2,"25095",0,0,0,1\n+CPOL: 6,2,"25095",0,0,1,0\n+CPOL: 7,2,"25095",1,0,0,0\n+CPOL: 8,2,"25001",0,0,0,1\n+CPOL: 9,2,"25001",0,0,1,0\n+CPOL: 10,2,"25001",1,0,0,0\n+CPOL: 11,2,"25058",0,0,0,1\n+CPOL: 12,2,"25058",0,0,1,0\n+CPOL: 13,2,"25058",1,0,0,0\n+CPOL: 14,2,"25002",0,0,0,1\n+CPOL: 15,2,"25002",0,0,1,0\n+CPOL: 16,2,"25002",1,0,0,0\n+CPOL: 17,2,"25007",0,0,0,1\n+CPOL: 18,2,"25007",0,0,1,0\n+CPOL: 19,2,"25007",1,0,0,0\n+CPOL: 20,2,"25035",0,0,0,1\n+CPOL: 21,2,"25035",0,0,1,0\n+CPOL: 22,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=6', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25039",0,0,0,1\n+CPOL: 3,2,"25039",1,0,0,0\n+CPOL: 4,2,"25099",0,0,1,0\n+CPOL: 5,2,"25095",0,0,0,1\n+CPOL: 6,2,"25095",1,0,0,0\n+CPOL: 7,2,"25001",0,0,0,1\n+CPOL: 8,2,"25001",0,0,1,0\n+CPOL: 9,2,"25001",1,0,0,0\n+CPOL: 10,2,"25058",0,0,0,1\n+CPOL: 11,2,"25058",0,0,1,0\n+CPOL: 12,2,"25058",1,0,0,0\n+CPOL: 13,2,"25002",0,0,0,1\n+CPOL: 14,2,"25002",0,0,1,0\n+CPOL: 15,2,"25002",1,0,0,0\n+CPOL: 16,2,"25007",0,0,0,1\n+CPOL: 17,2,"25007",0,0,1,0\n+CPOL: 18,2,"25007",1,0,0,0\n+CPOL: 19,2,"25035",0,0,0,1\n+CPOL: 20,2,"25035",0,0,1,0\n+CPOL: 21,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=7', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25039",0,0,0,1\n+CPOL: 3,2,"25039",1,0,0,0\n+CPOL: 4,2,"25099",0,0,1,0\n+CPOL: 5,2,"25095",0,0,0,1\n+CPOL: 6,2,"25095",1,0,0,0\n+CPOL: 7,2,"25001",0,0,1,0\n+CPOL: 8,2,"25001",1,0,0,0\n+CPOL: 9,2,"25058",0,0,0,1\n+CPOL: 10,2,"25058",0,0,1,0\n+CPOL: 11,2,"25058",1,0,0,0\n+CPOL: 12,2,"25002",0,0,0,1\n+CPOL: 13,2,"25002",0,0,1,0\n+CPOL: 14,2,"25002",1,0,0,0\n+CPOL: 15,2,"25007",0,0,0,1\n+CPOL: 16,2,"25007",0,0,1,0\n+CPOL: 17,2,"25007",1,0,0,0\n+CPOL: 18,2,"25035",0,0,0,1\n+CPOL: 19,2,"25035",0,0,1,0\n+CPOL: 20,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=8', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25039",0,0,0,1\n+CPOL: 3,2,"25039",1,0,0,0\n+CPOL: 4,2,"25099",0,0,1,0\n+CPOL: 5,2,"25095",0,0,0,1\n+CPOL: 6,2,"25095",1,0,0,0\n+CPOL: 7,2,"25001",0,0,1,0\n+CPOL: 8,2,"25058",0,0,0,1\n+CPOL: 9,2,"25058",0,0,1,0\n+CPOL: 10,2,"25058",1,0,0,0\n+CPOL: 11,2,"25002",0,0,0,1\n+CPOL: 12,2,"25002",0,0,1,0\n+CPOL: 13,2,"25002",1,0,0,0\n+CPOL: 14,2,"25007",0,0,0,1\n+CPOL: 15,2,"25007",0,0,1,0\n+CPOL: 16,2,"25007",1,0,0,0\n+CPOL: 17,2,"25035",0,0,0,1\n+CPOL: 18,2,"25035",0,0,1,0\n+CPOL: 19,2,"25035",1,0,0,0\nOK'),
                    ('AT+CPOL=9', 'OK'),
                    ('AT+CPOL?',
                     '+CPOL: 1,2,"25020",0,0,1,0\n+CPOL: 2,2,"25039",0,0,0,1\n+CPOL: 3,2,"25039",1,0,0,0\n+CPOL: 4,2,"25099",0,0,1,0\n+CPOL: 5,2,"25095",0,0,0,1\n+CPOL: 6,2,"25095",1,0,0,0\n+CPOL: 7,2,"25001",0,0,1,0\n+CPOL: 8,2,"25058",0,0,0,1\n+CPOL: 9,2,"25058",1,0,0,0\n+CPOL: 10,2,"25002",0,0,0,1\n+CPOL: 11,2,"25002",0,0,1,0\n+CPOL: 12,2,"25002",1,0,0,0\n+CPOL: 13,2,"25007",0,0,0,1\n+CPOL: 14,2,"25007",0,0,1,0\n+CPOL: 15,2,"25007",1,0,0,0\n+CPOL: 16,2,"25035",0,0,0,1\n+CPOL: 17,2,"25035",0,0,1,0\n+CPOL: 18,2,"25035",1,0,0,0\nOK'),
                    ],
        # 2=DOUBT ----------------------------------------
        'AT+CIREG': ['IMS registration (может быть не поддержано)',
                     # без симки
                     ('AT+CIREG=?', '+CIREG: (0-3)\nOK'),
                     ('AT+CIREG', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=0', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=1', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=2', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=3', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),

                     # c симкой - на одном и томже блоке дает то один вариант то другой!!!
                     ('AT+CIREG=?', '+CIREG: (0-3)\nOK'),
                     ('AT+CIREG', '+CME ERROR: 4'),
                     ('AT+CIREG?', '+CME ERROR: 4'),
                     ('AT+CIREG=0', '+CME ERROR: 4'),
                     ('AT+CIREG?', '+CME ERROR: 4'),
                     ('AT+CIREG=1', '+CME ERROR: 4'),
                     ('AT+CIREG?', '+CME ERROR: 4'),
                     ('AT+CIREG=2', '+CME ERROR: 4'),
                     ('AT+CIREG?', '+CME ERROR: 4'),
                     ('AT+CIREG=3', '+CME ERROR: 4'),
                     ('AT+CIREG?', '+CME ERROR: 4'),
                     ],
        # 3=UNKNOWN --------------------------------------
        'AT+CSMOD': ['show network system mode, 8 = LTE, 7 = HSPA, 1 = GSM. Первое число = включён ли автоотчёт',
                     # без симки и с, даже на navia с включенным питанием!!!
                     ('AT+CSMOD=?', 'ERROR'),
                     ('AT+CSMOD', 'ERROR'),
                     ('AT+CSMOD?', 'ERROR'),

                     # из доков
                     ('AT+CSMOD?', '+CSMOD: 0,8'),
                     ],

        'AT+CIMS': ['IMS status (может быть не поддержано)',
                    # без симки и с
                    ('AT+CIMS=?', 'ERROR'),
                    ('AT+CIMS', 'ERROR'),
                    ('AT+CIMS?', 'ERROR'),
                    ],
        '-AT+CLBS?': ['[NOTE=wait longer!!! нужно около 10сек!!!]base station location (LBS)',
                    # no sim
                    ('AT+CLBS=?', '+CLBS: (1,2,3,4,9),(1-15),(-180.000000-180.000000),(-90.000000-90.000000),(0-2)\nOK'),
                    ('AT+CLBS', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=0', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=1', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=2', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=3', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=4', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=5', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=6', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=7', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=8', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=9', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),

                    # sim
                     ('AT+CLBS=?', '+CLBS: (1,2,3,4,9),(1-15),(-180.000000-180.000000),(-90.000000-90.000000),(0-2)\nOK'),
                     ('AT+CLBS', 'ERROR'),
                     ('AT+CLBS?', '+CSQ: 23,99\nOK\n+CNSMOD: 1,8\nOK'),

                      ('AT+CLBS=?', '+CLBS: (1,2,3,4,9),(1-15),(-180.000000-180.000000),(-90.000000-90.000000),(0-2)\nOK'),
                      ('AT+CLBS', 'ERROR'),
                      ('AT+CLBS?', 'ERROR'),
                     ],
        'AT+CLBSCFG': ['LBS configure',
                       # без симки и с
                       # navia
                       ('AT+CLBSCFG=?', '+CLBSCFG: (0,1),(1-3),"ParamValue"\nOK'),
                       ('AT+CLBSCFG', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=0', '+CLBSCFG: 0,1,""\nOK'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=1', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=2', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=3', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=ParamValue', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ],
        'AT+CASSISTLOC': ['base station location for LTE/CDMA',
                          # без симки и с
                          # navia
                          ('AT+CASSISTLOC=?', 'ERROR'),
                          ('AT+CASSISTLOC', 'ERROR'),
                          ('AT+CASSISTLOC?', 'ERROR'),
                          ],

        'AT+SIGNS': ['Query the antenna RSRP RSRQ RSSI',
                     ('AT+SIGNS=?', '+SIGNS:\nOK'),
                     ('AT+SIGNS',
                      '+RSRP0:-93\n+RSRP1:-112\n+RSRQ0:-7\n+RSRQ1:-8\n+RSSI0:-48\n+RSSI1:-67\n+TXPOWER:24\n+MAXTXPOWER:23\nOK'),
                     ('AT+SIGNS?',
                      '+RSRP0:-93\n+RSRP1:-112\n+RSRQ0:-7\n+RSRQ1:-8\n+RSSI0:-48\n+RSSI1:-67\n+TXPOWER:24\n+MAXTXPOWER:23\nOK'),

                     # navia с питанием
                     ('AT+SIGNS=?', 'ERROR'),
                     ('AT+SIGNS', 'ERROR'),
                     ('AT+SIGNS?', 'ERROR'),
                     ],
    },
    # =========================================================================
    "-HARDWARE(питание/ADC/GPIO/I2C)": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CMTE": "[DANGER]temperature control / shutdown",
        # "AT+CDELTA": "[DANGER]go to recovery mode",
        # "AT+CRIIC": "[DANGER]read I2C register",
        # "AT+CWIIC": "[DANGER]write I2C register",
        # "AT+CGFUNC": "[DANGER]GPIO function enable/disable",
        # "AT+CGDRT": "[DANGER]GPIO direction (in/out)",
        # "AT+CGSETV": "[DANGER]GPIO set value (high/low)",
        # "AT+CSCLK": "[DANGER]UART sleep",
        # "AT+CMUX": "[DANGER]UART multiplexer # DANGER",

        # "AT+CVALARM": ["[DANGER??]low/high voltage alarm",
        #                # с сим
        #                ('AT+CVALARM=?', '+CVALARM: (0,1),(3300-4000),(4001-4300)\nOK'),
        #                ('AT+CVALARM', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 0,3300,4300\nOK'),
        #                ('AT+CVALARM=0', 'OK'),
        #                ('AT+CVALARM?', '+CVALARM: 0,3300,4300\nOK'),
        #                ('AT+CVALARM=1', 'OK'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ('AT+CVALARM=3300', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ('AT+CVALARM=3301', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ('AT+CVALARM=3302', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ('AT+CVALARM=3303', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ('AT+CVALARM=3304', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ('AT+CVALARM=3305', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ('AT+CVALARM=3306', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ('AT+CVALARM=3307', 'ERROR'),
        #                ('AT+CVALARM?', '+CVALARM: 1,3300,4300\nOK'),
        #                ],
        # "AT+CPMVT": "[DANGER???]low/high voltage power off",
        # 1=ACCURATE -------------------------------------
        'AT+CBC': ['battery/voltage',
                   ('AT+CBC=?', 'ERROR'),
                   ('AT+CBC', '+CBC: 3.820V\nOK'),
                   ('AT+CBC?', 'ERROR'),
                   ],
        'AT+CPMUTEMP': ['module temperature',
                        ('AT+CPMUTEMP=?', 'ERROR'),
                        ('AT+CPMUTEMP', '+CPMUTEMP: 109\nOK'),
                        ('AT+CPMUTEMP?', 'ERROR'),
                        ],
        'AT+CVAUXS?': ['state of VREG_AUX1 pin',
                       # без симки и с
                       ('AT+CVAUXS=?', '+CVAUXS: (0,1)\nOK'),
                       ('AT+CVAUXS', 'ERROR'),
                       ('AT+CVAUXS?', '+CVAUXS: 1\nOK'),
                       ('AT+CVAUXS=0', 'OK'),
                       ('AT+CVAUXS?', '+CVAUXS: 0\nOK'),
                       ('AT+CVAUXS=1', 'OK'),
                       ('AT+CVAUXS?', '+CVAUXS: 1\nOK'),
                       ],
        'AT+CVAUXV?': ['voltage of VREG_AUX1 pin',
                       # без симки и с
                       ('AT+CVAUXV=?', '+CVAUXV: (2500,2600,2700,2800,2850,2900,3000,3100,3300)\nOK'),
                       ('AT+CVAUXV', 'ERROR'),
                       ('AT+CVAUXV?', '+CVAUXV: 3000\nOK'),
                       ('AT+CVAUXV=2500', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2500\nOK'),
                       ('AT+CVAUXV=2600', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2600\nOK'),
                       ('AT+CVAUXV=2700', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2700\nOK'),
                       ('AT+CVAUXV=2800', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2800\nOK'),
                       ('AT+CVAUXV=2850', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2850\nOK'),
                       ('AT+CVAUXV=2900', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2900\nOK'),
                       ('AT+CVAUXV=3000', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 3000\nOK'),
                       ('AT+CVAUXV=3100', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 3100\nOK'),
                       ('AT+CVAUXV=3300', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 3300\nOK'),
                       ],
        '-AT+CFGRI?': ['RI pin on URC',
                      # без симки и с
                      ('AT+CFGRI=?', '+CFGRI: (0-1),(10-6000),(20-6000)\nOK'),
                      ('AT+CFGRI', 'OK'),
                      ('AT+CFGRI?', '+CFGRI: 0,60,120\nOK'),
                      ('AT+CFGRI=0', 'OK'),
                      ('AT+CFGRI?', '+CFGRI: 0,60,120\nOK'),
                      ('AT+CFGRI=1', 'OK'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=10', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=11', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=12', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=13', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=14', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=15', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=16', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=17', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ],
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
        'AT+CADC': ['read ADC value',
                    # без симки и с
                    ('AT+CADC=?', '+CADC: (0,2)\nOK'),
                    ('AT+CADC', 'ERROR'),
                    ('AT+CADC?', 'ERROR'),
                    ('AT+CADC=0', '+CADC: 205\nOK'),
                    ('AT+CADC?', 'ERROR'),
                    ('AT+CADC=2', '+CADC: 0\nOK'),
                    ('AT+CADC?', 'ERROR'),
                    ],
        'AT+CADC2': ['read ADC2 value',
                     # без симки и с
                     ('AT+CADC2=?', 'ERROR'),
                     ('AT+CADC2', 'ERROR'),
                     ('AT+CADC2?', 'ERROR'),
                     ],
        'AT+CGGETV': ['GPIO get value',
                      # без симки и с
                      ('AT+CGGETV=?', '+CGGETV: (1,2,3,4,5,6)\nOK'),
                      ('AT+CGGETV', 'ERROR'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=1', '+CGGETV: 1,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=2', '+CGGETV: 2,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=3', '+CGGETV: 3,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=4', '+CGGETV: 4,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=5', '+CGGETV: 5,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=6', '+CGGETV: 6,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ],
        'AT+CGISR': ['GPIO interrupt trigger',
                     # без симки и с
                     ('AT+CGISR=?', 'ERROR'),
                     ('AT+CGISR', 'ERROR'),
                     ('AT+CGISR?', 'ERROR'),
                     ],
    },

    # =========================================================================
    "---6=CALL_CONTROL": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CCWA": "[DANGER]call waiting",
        # "AT+VTS": "[DANGER]DTMF and tone generation",
        # "AT+CSTA": "[DANGER]select type of address",
        # 'AT+CHUP': ['[USELESS]hang up call',
        #             ('AT+CHUP=?', 'OK'),
        #             ('AT+CHUP', 'OK'),
        #             ('AT+CHUP?', 'ERROR'),
        #             ],
        # 'AT+CMOD?': ['[USELESS]call mode',
        #              ('AT+CMOD=?', '+CMOD: (0)\nOK'),
        #              ('AT+CMOD', 'OK'),
        #              ('AT+CMOD?', '+CMOD: 0\nOK'),
        #              ('AT+CMOD=0', 'OK'),
        #              ('AT+CMOD?', '+CMOD: 0\nOK'),
        #              ],
        # 'AT+VTD?': ['[USELESS]tone duration',
        #            ('AT+VTD=?', '+VTD: (300-600)\nOK'),
        #            ('AT+VTD', 'ERROR'),
        #            ('AT+VTD?', '+VTD: 300\nOK'),
        #            ('AT+VTD=300', 'OK'),
        #            ('AT+VTD?', '+VTD: 300\nOK'),
        #            ('AT+VTD=301', 'OK'),
        #            ('AT+VTD?', '+VTD: 301\nOK'),
        #            ('AT+VTD=302', 'OK'),
        #            ('AT+VTD?', '+VTD: 302\nOK'),
        #            ('AT+VTD=303', 'OK'),
        #            ('AT+VTD?', '+VTD: 303\nOK'),
        #            ('AT+VTD=304', 'OK'),
        #            ('AT+VTD?', '+VTD: 304\nOK'),
        #            ('AT+VTD=305', 'OK'),
        #            ('AT+VTD?', '+VTD: 305\nOK'),
        #            ('AT+VTD=306', 'OK'),
        #            ('AT+VTD?', '+VTD: 306\nOK'),
        #            ('AT+VTD=307', 'OK'),
        #            ('AT+VTD?', '+VTD: 307\nOK'),
        #            ('AT+VTD=308', 'OK'),
        #            ('AT+VTD?', '+VTD: 308\nOK'),
        #            ('AT+VTD=309', 'OK'),
        #            ('AT+VTD?', '+VTD: 309\nOK'),
        #            ],
        # 'AT+VMUTE': ['[USELESS]speaker mute',
        #              ('AT+VMUTE=?', '+VMUTE: (0-1)\nOK'),
        #              ('AT+VMUTE', 'ERROR'),
        #              ('AT+VMUTE?', '+VMUTE: 0\nOK'),
        #              ('AT+VMUTE=0', 'ERROR'),
        #              ('AT+VMUTE?', '+VMUTE: 0\nOK'),
        #              ('AT+VMUTE=1', 'ERROR'),
        #              ('AT+VMUTE?', '+VMUTE: 0\nOK'),
        #              ],
        # 'AT+CMUT': ['[USELESS]microphone mute',
        #             ('AT+CMUT=?', '+CMUT: (0-1)\nOK'),
        #             ('AT+CMUT', 'ERROR'),
        #             ('AT+CMUT?', '+CMUT: 0\nOK'),
        #             ('AT+CMUT=0', 'ERROR'),
        #             ('AT+CMUT?', '+CMUT: 0\nOK'),
        #             ('AT+CMUT=1', 'ERROR'),
        #             ('AT+CMUT?', '+CMUT: 0\nOK'),
        #             ],
        # 'AT+MORING': ['[USELESS]MO ring URC',
        #               ('AT+MORING=?', 'ERROR'),
        #               ('AT+MORING', 'ERROR'),
        #               ('AT+MORING?', 'ERROR'),
        #               ],
        # 'AT+CLVL': ['[USELESS]loudspeaker volume',
        #             ('AT+CLVL=?', 'ERROR'),
        #             ('AT+CLVL', 'ERROR'),
        #             ('AT+CLVL?', 'ERROR'),
        #             ],
        # 'AT+SIDET': ['[USELESS]sidetone',
        #              ('AT+SIDET=?', 'ERROR'),
        #              ('AT+SIDET', 'ERROR'),
        #              ('AT+SIDET?', 'ERROR'),
        #              ],
        # 1=ACCURATE -------------------------------------
        'AT+CVHU?': ['voice hang up control',
                     ('AT+CVHU=?', '+CVHU: (0-1)\nOK'),
                     ('AT+CVHU', 'OK'),
                     ('AT+CVHU?', '+CVHU: 1\nOK'),
                     ('AT+CVHU=0', 'OK'),
                     ('AT+CVHU?', '+CVHU: 0\nOK'),
                     ('AT+CVHU=1', 'OK'),
                     ('AT+CVHU?', '+CVHU: 1\nOK'),
                     ],
        'AT+CRLP?': ['radio link protocol',
                     ('AT+CRLP=?', '+CRLP: (0-61),(0-61),(39-255),(1-255),(0-1),(3-255)\nOK'),
                     ('AT+CRLP', 'OK'),
                     ('AT+CRLP?', '+CRLP: 61,61,128,255,1,3\nOK'),
                     ('AT+CRLP=0', 'OK'),
                     ('AT+CRLP?', '+CRLP: 0,61,128,255,1,3\nOK'),
                     ('AT+CRLP=1', 'OK'),
                     ('AT+CRLP?', '+CRLP: 1,61,128,255,1,3\nOK'),
                     ('AT+CRLP=2', 'OK'),
                     ('AT+CRLP?', '+CRLP: 2,61,128,255,1,3\nOK'),
                     ('AT+CRLP=3', 'OK'),
                     ('AT+CRLP?', '+CRLP: 3,61,128,255,1,3\nOK'),
                     ('AT+CRLP=4', 'OK'),
                     ('AT+CRLP?', '+CRLP: 4,61,128,255,1,3\nOK'),
                     ('AT+CRLP=5', 'OK'),
                     ('AT+CRLP?', '+CRLP: 5,61,128,255,1,3\nOK'),
                     ('AT+CRLP=6', 'OK'),
                     ('AT+CRLP?', '+CRLP: 6,61,128,255,1,3\nOK'),
                     ('AT+CRLP=7', 'OK'),
                     ('AT+CRLP?', '+CRLP: 7,61,128,255,1,3\nOK'),
                     ('AT+CRLP=8', 'OK'),
                     ('AT+CRLP?', '+CRLP: 8,61,128,255,1,3\nOK'),
                     ('AT+CRLP=9', 'OK'),
                     ('AT+CRLP?', '+CRLP: 9,61,128,255,1,3\nOK'),
                     ],
        'AT+CRC?': ['cellular result codes',
                    ('AT+CRC=?', '+CRC: (0,1)\nOK'),
                    ('AT+CRC', 'OK'),
                    ('AT+CRC?', '+CRC: 0\nOK'),
                    ('AT+CRC=0', 'OK'),
                    ('AT+CRC?', '+CRC: 0\nOK'),
                    ('AT+CRC=1', 'OK'),
                    ('AT+CRC?', '+CRC: 1\nOK'),
                    ],
        'AT+CLCC?': ['list current calls',
                     ('AT+CLCC=?', '+CLCC: (0-1)\nOK'),
                     ('AT+CLCC', 'OK'),
                     ('AT+CLCC?', '+CLCC: 1\nOK'),
                     ('AT+CLCC=0', 'OK'),
                     ('AT+CLCC?', '+CLCC: 0\nOK'),
                     ('AT+CLCC=1', 'OK'),
                     ('AT+CLCC?', '+CLCC: 1\nOK'),
                     ],
        'AT+CEER': ['extended error report',
                    ('AT+CEER=?', 'OK'),
                    ('AT+CEER', '+CEER: "0 Unknown"\nOK'),
                    ('AT+CEER?', 'ERROR'),
                    ],
        'AT+CSDVC?': ['switch voice channel device',
                      ('AT+CSDVC=?', '+CSDVC: (1,3)\nOK'),
                      ('AT+CSDVC', 'ERROR'),
                      ('AT+CSDVC?', '+CSDVC: 1\nOK'),
                      ('AT+CSDVC=1', 'OK'),
                      ('AT+CSDVC?', '+CSDVC: 1\nOK'),
                      ('AT+CSDVC=3', 'OK'),
                      ('AT+CSDVC?', '+CSDVC: 3\nOK'),
                      ],

        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
        'AT+CBST?': ['bearer service type',
                    ('AT+CBST=?',
                     '+CBST: (0,1,2,3,4,5,6,7,12,14,15,16,17,34,36,38,39,43,47,48,49,50,51,65,66,68,70,71,75,79,80,81,82,83,84,115,116,120,121,130,131,132,133,134),(0-7),(0-3)\nOK'),
                    ('AT+CBST', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=0', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=1', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=2', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=3', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=4', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=5', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=6', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=7', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=12', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ('AT+CBST=14', '+CME ERROR: Operation not supported'),
                    ('AT+CBST?', '+CME ERROR: unknown error'),
                    ],
        'AT+CR': ['service reporting control',
                  ('AT+CR=?', 'ERROR'),
                  ('AT+CR', 'ERROR'),
                  ('AT+CR?', 'ERROR'),
                  ],
        'AT+CHLD': ['call related supplementary services',
                    ('AT+CHLD=?', '+CHLD: (0,1,1x,2,2x,3,4)\nOK'),
                    ('AT+CHLD', 'ERROR'),
                    ('AT+CHLD?', '+CME ERROR: Operation not supported'),
                    ],
        'AT+CCFC': ['call forwarding',
                    ('AT+CCFC=?', '+CCFC: (0,1,2,3,4,5)\nOK'),
                    ('AT+CCFC', 'ERROR'),
                    ('AT+CCFC?', 'ERROR'),
                    ('AT+CCFC=0', 'ERROR'),
                    ('AT+CCFC?', 'ERROR'),
                    ('AT+CCFC=1', 'ERROR'),
                    ('AT+CCFC?', 'ERROR'),
                    ('AT+CCFC=2', 'ERROR'),
                    ('AT+CCFC?', 'ERROR'),
                    ('AT+CCFC=3', 'ERROR'),
                    ('AT+CCFC?', 'ERROR'),
                    ('AT+CCFC=4', 'ERROR'),
                    ('AT+CCFC?', 'ERROR'),
                    ('AT+CCFC=5', 'ERROR'),
                    ('AT+CCFC?', 'ERROR'),
                    ],
        'AT+CLIP': ['calling line identification presentation',
                    ('AT+CLIP=?', '+CLIP: (0-1)\nOK'),
                    ('AT+CLIP', 'ERROR'),
                    ('AT+CLIP?', 'ERROR'),
                    ('AT+CLIP=0', 'ERROR'),
                    ('AT+CLIP?', 'ERROR'),
                    ('AT+CLIP=1', 'ERROR'),
                    ('AT+CLIP?', 'ERROR'),
                    ],
        'AT+CLIR': ['calling line identification restriction',
                    ('AT+CLIR=?', '+CLIR: (0-2)\nOK'),
                    ('AT+CLIR', 'ERROR'),
                    ('AT+CLIR?', '+CME ERROR: unknown error'),
                    ('AT+CLIR=0', 'OK'),
                    ('AT+CLIR?', '+CME ERROR: unknown error'),
                    ('AT+CLIR=1', 'OK'),
                    ('AT+CLIR?', '+CME ERROR: unknown error'),
                    ('AT+CLIR=2', 'OK'),
                    ('AT+CLIR?', '+CME ERROR: unknown error'),
                    ],
        'AT+COLP': ['connected line identification presentation',
                    ('AT+COLP=?', '+COLP: (0-1)\nOK'),
                    ('AT+COLP', 'ERROR'),
                    ('AT+COLP?', 'ERROR'),
                    ('AT+COLP=0', 'ERROR'),
                    ('AT+COLP?', 'ERROR'),
                    ('AT+COLP=1', 'ERROR'),
                    ('AT+COLP?', 'ERROR'),
                    ],
    },

    # =========================================================================
    "---7=AUDIO/DSP(голосовые параметры)": {
        # 0=DANGER+USELESS -------------------------------
        # 1=ACCURATE -------------------------------------
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------


        # "AT+CACDBFN": "[DANGER]change default ACDB filename",
        # "AT+CCMXPLAY": "[DANGER]play audio (mp3/aac/amr/...)",
        # "AT+CCMXSTOP": "[DANGER]stop audio",
        # 'AT+CCMXPLAYWAV': ['[NONEUSEFULL]play wav',
        #                    ('AT+CCMXPLAYWAV=?', 'ERROR'),
        #                    ('AT+CCMXPLAYWAV', 'ERROR'),
        #                    ('AT+CCMXPLAYWAV?', 'ERROR'),
        #                    ],
        # 'AT+CCMXSTOPWAV': ['[NONEUSEFULL]stop wav',
        #                    ('AT+CCMXSTOPWAV=?', 'ERROR'),
        #                    ('AT+CCMXSTOPWAV', 'ERROR'),
        #                    ('AT+CCMXSTOPWAV?', 'ERROR'),
        #                    ],

        'AT+CPCMREG': ['USB audio control',
                       ('AT+CPCMREG=?', 'ERROR'),
                       ('AT+CPCMREG', 'ERROR'),
                       ('AT+CPCMREG?', 'ERROR'),
                       ],
        'AT+CMICGAIN': ['mic gain',
                        ('AT+CMICGAIN=?', '+CMICGAIN: (0-7)\nOK'),
                        ('AT+CMICGAIN', 'ERROR'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 7\nOK'),
                        ('AT+CMICGAIN=0', 'OK'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 0\nOK'),
                        ('AT+CMICGAIN=1', 'OK'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 1\nOK'),
                        ('AT+CMICGAIN=2', 'OK'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 2\nOK'),
                        ('AT+CMICGAIN=3', 'OK'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 3\nOK'),
                        ('AT+CMICGAIN=4', 'OK'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 4\nOK'),
                        ('AT+CMICGAIN=5', 'OK'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 5\nOK'),
                        ('AT+CMICGAIN=6', 'OK'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 6\nOK'),
                        ('AT+CMICGAIN=7', 'OK'),
                        ('AT+CMICGAIN?', '+CMICGAIN: 7\nOK'),
                        ],
        'AT+COUTGAIN': ['out gain',
                        ('AT+COUTGAIN=?', '+COUTGAIN: (0-7)\nOK'),
                        ('AT+COUTGAIN', 'ERROR'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 7\nOK'),
                        ('AT+COUTGAIN=0', 'OK'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 0\nOK'),
                        ('AT+COUTGAIN=1', 'OK'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 1\nOK'),
                        ('AT+COUTGAIN=2', 'OK'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 2\nOK'),
                        ('AT+COUTGAIN=3', 'OK'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 3\nOK'),
                        ('AT+COUTGAIN=4', 'OK'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 4\nOK'),
                        ('AT+COUTGAIN=5', 'OK'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 5\nOK'),
                        ('AT+COUTGAIN=6', 'OK'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 6\nOK'),
                        ('AT+COUTGAIN=7', 'OK'),
                        ('AT+COUTGAIN?', '+COUTGAIN: 7\nOK'),
                        ],
        'AT+CTXVOL': ['TX voice mic volume',
                      ('AT+CTXVOL=?', 'ERROR'),
                      ('AT+CTXVOL', 'ERROR'),
                      ('AT+CTXVOL?', 'ERROR'),
                      ],
        'AT+CTXMICGAIN': ['TX voice mic gain',
                          ('AT+CTXMICGAIN=?', 'ERROR'),
                          ('AT+CTXMICGAIN', 'ERROR'),
                          ('AT+CTXMICGAIN?', 'ERROR'),
                          ],
        'AT+CRXVOL': ['RX voice output speaker volume',
                      ('AT+CRXVOL=?', 'ERROR'),
                      ('AT+CRXVOL', 'ERROR'),
                      ('AT+CRXVOL?', 'ERROR'),
                      ],
        'AT+CECH': ['inhibit far-end echo',
                    ('AT+CECH=?', 'ERROR'),
                    ('AT+CECH', 'ERROR'),
                    ('AT+CECH?', 'ERROR'),
                    ],
        'AT+CECDT': ['inhibit echo during doubletalk',
                     ('AT+CECDT=?', 'ERROR'),
                     ('AT+CECDT', 'ERROR'),
                     ('AT+CECDT?', 'ERROR'),
                     ],
        'AT+CECWB': ['inhibit echo in high band',
                     ('AT+CECWB=?', 'ERROR'),
                     ('AT+CECWB', 'ERROR'),
                     ('AT+CECWB?', 'ERROR'),
                     ],
        'AT+CSNS': ['MIC noise suppression',
                    ('AT+CSNS=?', 'ERROR'),
                    ('AT+CSNS', 'ERROR'),
                    ('AT+CSNS?', 'ERROR'),
                    ],
        'AT+CSLIM': ['MIC noise suppression (limit)',
                     ('AT+CSLIM=?', 'ERROR'),
                     ('AT+CSLIM', 'ERROR'),
                     ('AT+CSLIM?', 'ERROR'),
                     ],
        'AT+CFNSMOD': ['fnsMode of RX_VOICE_FNS',
                       ('AT+CFNSMOD=?', 'ERROR'),
                       ('AT+CFNSMOD', 'ERROR'),
                       ('AT+CFNSMOD?', 'ERROR'),
                       ],
        'AT+CFNSIN': ['fnsInputGain of RX_VOICE_FNS',
                      ('AT+CFNSIN=?', 'ERROR'),
                      ('AT+CFNSIN', 'ERROR'),
                      ('AT+CFNSIN?', 'ERROR'),
                      ],
        'AT+CFNSLVL': ['fnsTargetNS of RX_VOICE_FNS',
                       ('AT+CFNSLVL=?', 'ERROR'),
                       ('AT+CFNSLVL', 'ERROR'),
                       ('AT+CFNSLVL?', 'ERROR'),
                       ],
        'AT+CECRX': ['VOICE_MOD_ENABLE',
                     ('AT+CECRX=?', 'ERROR'),
                     ('AT+CECRX', 'ERROR'),
                     ('AT+CECRX?', 'ERROR'),
                     ],
        'AT+CNLPPG': ['NLPP_gain',
                      ('AT+CNLPPG=?', 'ERROR'),
                      ('AT+CNLPPG', 'ERROR'),
                      ('AT+CNLPPG?', 'ERROR'),
                      ],
        'AT+CNLPPL': ['NLPP_limit',
                      ('AT+CNLPPL=?', 'ERROR'),
                      ('AT+CNLPPL', 'ERROR'),
                      ('AT+CNLPPL?', 'ERROR'),
                      ],
        'AT+CECM': ['echo canceller mode',
                    ('AT+CECM=?', 'ERROR'),
                    ('AT+CECM', 'ERROR'),
                    ('AT+CECM?', 'ERROR'),
                    ],
        'AT+CPCMFRM': ['USB audio sample rate 16k',
                       ('AT+CPCMFRM=?', 'ERROR'),
                       ('AT+CPCMFRM', 'ERROR'),
                       ('AT+CPCMFRM?', 'ERROR'),
                       ],
        'AT+CPTONE': ['play tone',
                      ('AT+CPTONE=?', 'ERROR'),
                      ('AT+CPTONE', 'ERROR'),
                      ('AT+CPTONE?', 'ERROR'),
                      ],
        'AT+CREC': ['record wav',
                    ('AT+CREC=?', '+CREC: (0-3),[{non-ascii}]"FILEPATH"\nOK'),
                    ('AT+CREC', 'ERROR'),
                    ('AT+CREC?', '+CREC: 0\nOK'),
                    ('AT+CREC=0', '+CREC: 0\nOK'),
                    ('AT+CREC?', '+CREC: 0\nOK'),
                    ('AT+CREC=1', 'ERROR'),
                    ('AT+CREC?', '+CREC: 0\nOK'),
                    ('AT+CREC=2', 'ERROR'),
                    ('AT+CREC?', '+CREC: 0\nOK'),
                    ('AT+CREC=3', 'ERROR'),
                    ('AT+CREC?', '+CREC: 0\nOK'),
                    ('AT+CREC=FILEPATH', 'ERROR'),
                    ('AT+CREC?', '+CREC: 0\nOK'),
                    ],
    },

    # =========================================================================
    "---8=SMS": {
        # 0=DANGER+USELESS -------------------------------
        # 1=ACCURATE -------------------------------------
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------

        # "AT+CMGF": "[DANGER]SMS format (0=PDU, 1=text)",
        # "AT+CSMP": "[DANGER]text mode parameters",
        # "AT+CMGS": "[DANGER]send SMS # DANGER (ждёт > и Ctrl+Z)",
        # "AT+CMSS": "[DANGER]send SMS from storage",
        # "AT+CMGW": "[DANGER]write SMS to memory # DANGER (ждёт >)",
        # "AT+CMGD": "[DANGER]delete SMS",
        # "AT+CMGMT": "[DANGER]change message status",
        # "AT+CMGRD": "[DANGER]read+delete SMS",
        # "AT+CMGSEX": "[DANGER]send SMS (extended)",
        # "AT+CMSSEX": "[DANGER]send multi SMS from storage",
        # "AT+CMGP": "[DANGER]cdma/evdo text mode parameters",

        'AT+CSMS': ['select message service',
                    ('AT+CSMS=?', '+CSMS: (0-1)\nOK'),
                    ('AT+CSMS', 'ERROR'),
                    ('AT+CSMS?', '+CSMS: 0,1,1,1\nOK'),
                    ('AT+CSMS=0', '+CSMS: 1,1,1\nOK'),
                    ('AT+CSMS?', '+CSMS: 0,1,1,1\nOK'),
                    ('AT+CSMS=1', '+CSMS: 1,1,1\nOK'),
                    ('AT+CSMS?', '+CSMS: 1,1,1,1\nOK'),
                    ],
        'AT+CPMS': ['preferred message storage',
                    ('AT+CPMS=?', '+CPMS: ("ME","SM"),("ME","SM"),("ME","SM")\nOK'),
                    ('AT+CPMS', '+CMS ERROR: (U)SIM busy'),
                    ('AT+CPMS?', '+CMS ERROR: unknown error'),
                    ('AT+CPMS=ME', 'ERROR'),
                    ('AT+CPMS?', '+CMS ERROR: unknown error'),
                    ('AT+CPMS=SM', 'ERROR'),
                    ('AT+CPMS?', '+CMS ERROR: unknown error'),
                    ],
        'AT+CSCA': ['SMS service centre address',
                    ('AT+CSCA=?', 'OK'),
                    ('AT+CSCA', 'ERROR'),
                    ('AT+CSCA?', '+CMS ERROR: unknown error'),
                    ],
        'AT+CSCB': ['cell broadcast message indication',
                    ('AT+CSCB=?', '+CSCB: (0-1)\nOK'),
                    ('AT+CSCB', 'ERROR'),
                    ('AT+CSCB?', '+CMS ERROR: unknown error'),
                    ('AT+CSCB=0', '+CMS ERROR: unknown error'),
                    ('AT+CSCB?', '+CMS ERROR: unknown error'),
                    ('AT+CSCB=1', '+CMS ERROR: unknown error'),
                    ('AT+CSCB?', '+CMS ERROR: unknown error'),
                    ],
        'AT+CSDH': ['show text mode parameters',
                    ('AT+CSDH=?', '+CSDH: (0-1)\nOK'),
                    ('AT+CSDH', 'OK'),
                    ('AT+CSDH?', '+CSDH: 0\nOK'),
                    ('AT+CSDH=0', 'OK'),
                    ('AT+CSDH?', '+CSDH: 0\nOK'),
                    ('AT+CSDH=1', 'OK'),
                    ('AT+CSDH?', '+CSDH: 1\nOK'),
                    ],
        'AT+CNMA': ['new message acknowledgement',
                    ('AT+CNMA=?', '+CNMA: (0-2)\nOK'),
                    ('AT+CNMA', '+CMS ERROR: NO +CNMA ACK EXPECTED'),
                    ('AT+CNMA?', 'ERROR'),
                    ('AT+CNMA=0', '+CMS ERROR: NO +CNMA ACK EXPECTED'),
                    ('AT+CNMA?', 'ERROR'),
                    ('AT+CNMA=1', '+CMS ERROR: NO +CNMA ACK EXPECTED'),
                    ('AT+CNMA?', 'ERROR'),
                    ('AT+CNMA=2', '+CMS ERROR: NO +CNMA ACK EXPECTED'),
                    ('AT+CNMA?', 'ERROR'),
                    ],
        'AT+CNMI': ['new message indications',
                    ('AT+CNMI=?', '+CNMI: (0,1,2),(0,1,2,3),(0,2),(0,1,2),(0,1)\nOK'),
                    ('AT+CNMI', 'OK'),
                    ('AT+CNMI?', '+CNMI: 2,1,0,0,0\nOK'),
                    ('AT+CNMI=0', 'OK'),
                    ('AT+CNMI?', '+CNMI: 0,0,0,0,0\nOK'),
                    ('AT+CNMI=1', 'OK'),
                    ('AT+CNMI?', '+CNMI: 1,0,0,0,0\nOK'),
                    ('AT+CNMI=2', 'OK'),
                    ('AT+CNMI?', '+CNMI: 2,0,0,0,0\nOK'),
                    ('AT+CNMI=3', '+CMS ERROR: Operation not allowed'),
                    ('AT+CNMI?', '+CNMI: 2,0,0,0,0\nOK'),
                    ],
        'AT+CGMS': ['service for MO SMS',
                    ('AT+CGMS=?', 'ERROR'),
                    ('AT+CGMS', 'ERROR'),
                    ('AT+CGMS?', 'ERROR'),
                    ],
        'AT+CGSMS': ['service for MO SMS (3GPP)',
                     ('AT+CGSMS=?', '+CGSMS: (0-3)\nOK'),
                     ('AT+CGSMS', 'ERROR'),
                     ('AT+CGSMS?', '+CMS ERROR: unknown error'),
                     ('AT+CGSMS=0', '+CMS ERROR: unknown error'),
                     ('AT+CGSMS?', '+CMS ERROR: unknown error'),
                     ('AT+CGSMS=1', '+CMS ERROR: unknown error'),
                     ('AT+CGSMS?', '+CMS ERROR: unknown error'),
                     ('AT+CGSMS=2', '+CMS ERROR: unknown error'),
                     ('AT+CGSMS?', '+CMS ERROR: unknown error'),
                     ('AT+CGSMS=3', '+CMS ERROR: unknown error'),
                     ('AT+CGSMS?', '+CMS ERROR: unknown error'),
                     ],
        'AT+CMGL': ['list SMS',
                    ('AT+CMGL=?', '+CMGL: (0-4)\nOK'),
                    ('AT+CMGL', 'ERROR'),
                    ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
                    ('AT+CMGL=0', '+CMS ERROR: unknown error'),
                    ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
                    ('AT+CMGL=1', '+CMS ERROR: unknown error'),
                    ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
                    ('AT+CMGL=2', '+CMS ERROR: unknown error'),
                    ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
                    ('AT+CMGL=3', '+CMS ERROR: unknown error'),
                    ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
                    ('AT+CMGL=4', '+CMS ERROR: unknown error'),
                    ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
                    ],
        'AT+CMGR': ['read SMS',
                    ('AT+CMGR=?', 'OK'),
                    ('AT+CMGR', 'ERROR'),
                    ('AT+CMGR?', 'ERROR'),
                    ],
        'AT+CMVP': ['message valid period',
                    ('AT+CMVP=?', '+CMVP: (0-255)\nOK'),
                    ('AT+CMVP', 'ERROR'),
                    ('AT+CMVP?', '+CMVP: 167\nOK'),
                    ('AT+CMVP=0', 'OK'),
                    ('AT+CMVP?', '+CMVP: 0\nOK'),
                    ('AT+CMVP=1', 'OK'),
                    ('AT+CMVP?', '+CMVP: 1\nOK'),
                    ('AT+CMVP=2', 'OK'),
                    ('AT+CMVP?', '+CMVP: 2\nOK'),
                    ('AT+CMVP=3', 'OK'),
                    ('AT+CMVP?', '+CMVP: 3\nOK'),
                    ('AT+CMVP=4', 'OK'),
                    ('AT+CMVP?', '+CMVP: 4\nOK'),
                    ('AT+CMVP=5', 'OK'),
                    ('AT+CMVP?', '+CMVP: 5\nOK'),
                    ('AT+CMVP=6', 'OK'),
                    ('AT+CMVP?', '+CMVP: 6\nOK'),
                    ('AT+CMVP=7', 'OK'),
                    ('AT+CMVP?', '+CMVP: 7\nOK'),
                    ('AT+CMVP=8', 'OK'),
                    ('AT+CMVP?', '+CMVP: 8\nOK'),
                    ('AT+CMVP=9', 'OK'),
                    ('AT+CMVP?', '+CMVP: 9\nOK'),
                    ],
    },

    # =========================================================================
    "---PHONEBOOK": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CPBW": "[DANGER]write phonebook entry",
        # "AT+CPBF": "[USELESS]find phonebook entries",

        # 1=ACCURATE -------------------------------------
        'AT+CPBS': ['select phonebook memory (SM=sim/ME/DC/MC/RC/FD=sim fixdialling-phonebook/ON=MSISDN list/LD/EN)',
                    # SIM ВСТАВЛЕНА
                    ('AT+CPBS=?', '+CPBS: ("SM","FD","ON","AP")'),
                    ('AT+CPBS?', '+CPBS: "SM",0,100'),
                    ('AT+CPBS', 'OK'),

                    ('AT+CPBS=ON', 'ERROR'),
                    ('AT+CPBS="ON"', 'OK'),
                    ('AT+CPBS?', '+CPBS: "SM",0,100'),    # НЕСМОТРЯ НА ТО ЧТО БЫЛ ЗАПРОС НА УСТАНОВКУ НОВОГО ЗНАЧЕНИЯ и он прошел ОК - все равно значение по факту не изменилось!!!
                    ('AT+CPBS="AP"', 'OK'),
                    ('AT+CPBS?', '+CPBS: "+CPBS: "AP",0,0'),
                    ('AT+CPBS="FD"', 'OK'),
                    ('AT+CPBS?', '+CPBS: "+CPBS: "FD",0,20'),

                    # SIM НЕ ВСТАВЛЕНА
                    ('AT+CPBS=?', 'ERROR'),
                    ('AT+CPBS', 'ERROR'),
                    ('AT+CPBS?', 'ERROR'),
                    ],
        'AT+CPBR': ['read phonebook entries',
                    # 1=SIM СТОИТ!!!
                    ('AT+CPBR=?', '+CPBR: (1-100),20,28'),
                    ('AT+CPBR', 'ERROR'),
                    ('AT+CPBR?', '+CME ERROR: unknown error'),
                    # НЕТИПОВОЕ ИСПОЛЬЗОВАНИЕ - запрос индекса -> выдаст результат чтения с этого индекса!
                    ('AT+CPBR=0', '+CME ERROR: invalid index'),
                    ('AT+CPBR=1', '+CME ERROR: not found'),

                    # 2=SIM не вставлена!
                    ('AT+CPBR=?', '+CME ERROR: unknown error'),
                    ('AT+CPBR', 'ERROR'),
                    ('AT+CPBR?', '+CME ERROR: unknown error'),
                    ],
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
    },

    # =========================================================================
    "-9=GPRS/PDP": {
        # "AT+CGDSCONT": "[DANGER]define secondary PDP context",
        # "AT+CGDATA": "[DANGER]enter data state (PPP)",

        # 1=ВКЛЮЧЕНИЕ/АКТИВАЦИЯ -------------------
        "AT+CGACT?": ["[DANGER]PDP context activate/deactivate",
                     ('AT+CGACT=?', '+CGREG: (0-2)\nOK'),

                    # navia
                     ('AT+CGACT=?', 'AT+CGACT=?\nOK'),
                     ('AT+CGACT', 'ERROR'),
                     ('AT+CGACT?', '+CGACT: 1,1\nOK'),
                     ],

        # 2=INFO -------------------------------------
        "AT+CGDCONT": ["[DANGER]define PDP context (APN, type)=список всех APN профилей в модеме",
                       # хз!
                       ('AT+CGDCONT=?', '+CGREG: (0-2)\nOK'),
                       ('AT+CGDCONT', 'OK'),
                       ('AT+CGDCONT?', '+CGREG: 0,0\nOK'),

                       # NAVIA
                       ('AT+CGDCONT=?', '''
                        +CGDCONT: (1-15),"IP",,,(0-2),(0-1),(0-1),(0-2)
                        +CGDCONT: (1-15),"IPV6",,,(0-2),(0-1),(0-1),(0-2)
                        +CGDCONT: (1-15),"IPV4V6",,,(0-2),(0-1),(0-1),(0-2)
                       '''),
                       ('AT+CGDCONT', 'OK'),
                       ('AT+CGDCONT?', '+CGDCONT: 1,"IP","simsim.MNC047.MCC250.GPRS","10.4.12.216",0,0,,,,'),
                       ],
        'AT+CGREG': ['GPRS registration status',
                     # no sim
                     ('AT+CGREG=?', '+CGREG: (0-2)\nOK'),
                     ('AT+CGREG', 'OK'),
                     ('AT+CGREG?', '+CGREG: 0,0\nOK'),
                     ('AT+CGREG=0', 'OK'),
                     ('AT+CGREG?', '+CGREG: 0,0\nOK'),
                     ('AT+CGREG=1', 'OK'),
                     ('AT+CGREG?', '+CGREG: 1,0\nOK'),
                     ('AT+CGREG=2', 'OK'),
                     ('AT+CGREG?', '+CGREG: 2,0,"0000","00000000"\nOK'),

                    # sim
                     ('AT+CGREG=?', '+CGREG: (0-2)\nOK'),
                     ('AT+CGREG', 'OK'),
                     ('AT+CGREG?', '+CGREG: 0,1\nOK'),
                     ('AT+CGREG=0', 'OK'),
                     ('AT+CGREG?', '+CGREG: 0,1\nOK'),
                     ('AT+CGREG=1', 'OK'),
                     ('AT+CGREG?', '+CGREG: 1,1\nOK'),
                     ('AT+CGREG=2', 'OK'),
                     ('AT+CGREG?', '+CGREG: 2,1,"6835","00002860"\nOK'),
                     ],
        'AT+CGATT': ['packet domain attach/detach',
                     # без сим
                     ('AT+CGATT=?', '+CGATT: (0-1)\nOK'),
                     ('AT+CGATT', 'ERROR'),
                     ('AT+CGATT?', '+CGATT: 0\nOK'),
                     ('AT+CGATT=0', 'OK'),
                     ('AT+CGATT?', '+CGATT: 0\nOK'),
                     ('AT+CGATT=1', '+CME ERROR: operation not allowed'),
                     ('AT+CGATT?', '+CGATT: 0\nOK'),

                     # с сим
                     ('AT+CGATT=?', '+CGATT: (0-1)\nOK'),
                     ('AT+CGATT', 'ERROR'),
                     ('AT+CGATT?', '+CGATT: 1\nOK'),
                     ('AT+CGATT=0', '+CGEV: ME DETACH\nOK'),
                     ('AT+CGATT?', '+CGREG: 0\n+CEREG: 0\n+CGATT: 0\nOK'),
                     ('AT+CGATT=1', '+CGREG: 2\n+CGREG: 0'),
                     ('AT+CGATT?', '+CGREG: 1,6835,00002860\nOK\n+CGATT: 1\nOK'),
                     ],
        'AT+CGTFT': ['traffic flow template',
                     ('AT+CGTFT=?',
                      '+CGTFT: "IP",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\n+CGTFT: "IPV6",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\n+CGTFT: "IPV4V6",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\nOK'),
                     ('AT+CGTFT', 'OK'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=0', '+CME ERROR: Incorrect parameters'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=1', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=2', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=3', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=4', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=5', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=6', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=7', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=8', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=9', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),

                    # с сим
                     ('AT+CGTFT=?',
                      '+CGTFT: "IP",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\n+CGTFT: "IPV6",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\n+CGTFT: "IPV4V6",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\nOK'),
                     ('AT+CGTFT', 'OK'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=0', '+CME ERROR: Incorrect parameters'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=1', 'OK'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=2', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=3', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=4', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=5', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=6', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=7', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=8', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=9', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ],
        'AT+CGQREQ': ['QoS profile (requested)',
                      ('AT+CGQREQ=?', '+CGQREQ: "IP",(0-3),(0-4),(0-5),(0-9),(0-18,31)\nOK'),
                      ('AT+CGQREQ', 'OK'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=0', '+CME ERROR: Incorrect parameters'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=1', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=2', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=3', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=4', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=5', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=6', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=7', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=8', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=9', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),

                       #с сим
                      ('AT+CGQREQ=?', '+CGQREQ: "IP",(0-3),(0-4),(0-5),(0-9),(0-18,31)\nOK'),
                      ('AT+CGQREQ', 'OK'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=0', '+CME ERROR: Incorrect parameters'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=1', 'OK'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=2', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=3', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=4', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=5', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=6', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=7', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=8', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQREQ=9', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', '+CGQREQ: 1,0,0,0,0,0\nOK'),
                      ],
        'AT+CGEQREQ': ['3G QoS profile (requested)',
                       # без сим
                       ('AT+CGEQREQ=?',
                        '+CGEQREQ: "IP",(0-4),(0-256000),(0-256000),(0-256000),(0-256000),(0-2),(0-1520),("0E0","1E1","1E2","7E3","1E3","1E4","1E5","1E6"),("0E0","5E2","1E2","5E3","4E3","1E3","1E4","1E5","1E6","6E8"),(0-3),(0-950),(0-3),(0-1),(0-1)\nOK'),
                       ('AT+CGEQREQ', 'OK'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=0', '+CME ERROR: Incorrect parameters'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=1', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=2', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=3', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=4', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=5', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=6', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=7', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=8', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=9', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),

                       # с сим
                       ('AT+CGEQREQ=?',
                        '+CGEQREQ: "IP",(0-4),(0-256000),(0-256000),(0-256000),(0-256000),(0-2),(0-1520),("0E0","1E1","1E2","7E3","1E3","1E4","1E5","1E6"),("0E0","5E2","1E2","5E3","4E3","1E3","1E4","1E5","1E6","6E8"),(0-3),(0-950),(0-3),(0-1),(0-1)\nOK'),
                       ('AT+CGEQREQ', 'OK'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",3,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=0', '+CME ERROR: Incorrect parameters'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",3,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=1', 'OK'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=2', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=3', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=4', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=5', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=6', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=7', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=8', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQREQ=9', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', '+CGEQREQ: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ],
        'AT+CGQMIN': ['QoS profile (minimum acceptable)',
                      # без сим
                      ('AT+CGQMIN=?', '+CGQMIN: "IP",(0-3),(0-4),(0-5),(0-9),(0-18,31)\nOK'),
                      ('AT+CGQMIN', 'OK'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=0', '+CME ERROR: Incorrect parameters'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=1', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=2', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=3', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=4', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=5', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=6', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=7', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=8', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=9', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),

                      # с сим
                      ('AT+CGQMIN=?', '+CGQMIN: "IP",(0-3),(0-4),(0-5),(0-9),(0-18,31)\nOK'),
                      ('AT+CGQMIN', 'OK'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,3,4,5,1,1\nOK'),
                      ('AT+CGQMIN=0', '+CME ERROR: Incorrect parameters'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,3,4,5,1,1\nOK'),
                      ('AT+CGQMIN=1', 'OK'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQMIN=2', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQMIN=3', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQMIN=4', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQMIN=5', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQMIN=6', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQMIN=7', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQMIN=8', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ('AT+CGQMIN=9', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', '+CGQMIN: 1,0,0,0,0,0\nOK'),
                      ],
        'AT+CGEQMIN': ['3G QoS profile (minimum acceptable)',
                       # без сим
                       ('AT+CGEQMIN=?',
                        '+CGEQMIN: "IP",(0-4),(0-256000),(0-256000),(0-256000),(0-256000),(0-2),(0-1520),("0E0","1E1","1E2","7E3","1E3","1E4","1E5","1E6"),("0E0","5E2","1E2","5E3","4E3","1E3","1E4","1E5","1E6","6E8"),(0-3),(0-950),(0-3),(0-1),(0-1)\nOK'),
                       ('AT+CGEQMIN', 'OK'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=0', '+CME ERROR: Incorrect parameters'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=1', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=2', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=3', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=4', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=5', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=6', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=7', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=8', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=9', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),

                       # с сим
                       ('AT+CGEQMIN=?',
                        '+CGEQMIN: "IP",(0-4),(0-256000),(0-256000),(0-256000),(0-256000),(0-2),(0-1520),("0E0","1E1","1E2","7E3","1E3","1E4","1E5","1E6"),("0E0","5E2","1E2","5E3","4E3","1E3","1E4","1E5","1E6","6E8"),(0-3),(0-950),(0-3),(0-1),(0-1)\nOK'),
                       ('AT+CGEQMIN', 'OK'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",3,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=0', '+CME ERROR: Incorrect parameters'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",3,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=1', 'OK'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=2', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=3', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=4', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=5', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=6', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=7', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=8', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ('AT+CGEQMIN=9', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', '+CGEQMIN: 1,4,0,0,0,0,2,0,"0E0","0E0",0,0,0,0,0\nOK'),
                       ],
        'AT+CGPADDR': ['show PDP address (assigned)',
                       # без симки
                       ('AT+CGPADDR=?', '+CGPADDR: ()\nOK'),
                       ('AT+CGPADDR', 'OK'),
                       ('AT+CGPADDR?', 'ERROR'),

                       # с сим
                       ('AT+CGPADDR=?', '+CGPADDR: (1)\nOK'),
                       ('AT+CGPADDR', '+CGPADDR: 1,0.0.0.0\nOK'),
                       ('AT+CGPADDR?', 'ERROR'),
                       ('AT+CGPADDR=1', '+CGPADDR: 1,0.0.0.0\nOK'),
                       ('AT+CGPADDR?', 'ERROR'),

                       # NAVIA
                       ('AT+CGPADDR=?', '+CGPADDR: (1)\nOK'),
                       ('AT+CGPADDR', '+CGPADDR: 1,10.4.12.216\nOK'),
                       ('AT+CGPADDR?', 'ERROR'),
                       ('AT+CGPADDR=1', '+CGPADDR: 1,10.4.12.216\nOK'),
                       ],
        'AT+CGCLASS': ['GPRS mobile station class',
                       # без симки и с
                       ('AT+CGCLASS=?', '+CGCLASS: ("A")\nOK'),
                       ('AT+CGCLASS', 'OK'),
                       ('AT+CGCLASS?', '+CGCLASS: "A"\nOK'),
                       ('AT+CGCLASS=A', 'OK'),
                       ('AT+CGCLASS?', '+CGCLASS: "A"\nOK'),
                       ],
        'AT+CGEREP': ['GPRS event reporting',
                      # без симки и с
                      ('AT+CGEREP=?', '+CGEREP: (0-2),(0-1)\nOK'),
                      ('AT+CGEREP', 'OK'),
                      ('AT+CGEREP?', '+CGEREP: 2,0\nOK'),
                      ('AT+CGEREP=0', 'OK'),
                      ('AT+CGEREP?', '+CGEREP: 0,0\nOK'),
                      ('AT+CGEREP=1', 'OK'),
                      ('AT+CGEREP?', '+CGEREP: 1,0\nOK'),
                      ('AT+CGEREP=2', 'OK'),
                      ('AT+CGEREP?', '+CGEREP: 2,0\nOK'),
                      ],
        'AT+CGAUTH': ['PDP-IP authentication (PAP/CHAP)',
                      # без симки
                      ('AT+CGAUTH=?', 'ERROR'),
                      ('AT+CGAUTH', 'ERROR'),
                      ('AT+CGAUTH?', 'ERROR'),

                      # с симкой
                      ('AT+CGAUTH=?', '+CGAUTH: (1-15),(0-2),50,50\nOK'),
                      ('AT+CGAUTH', 'OK'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=0', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=1', 'OK'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=2', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=3', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=4', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=5', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=6', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=7', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=8', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ('AT+CGAUTH=9', 'ERROR'),
                      ('AT+CGAUTH?', '+CGAUTH: 1,0\nOK'),
                      ],
        'AT+CGCONTRDP': ['PDP context dynamic parameters',
                         # без симки и с
                         ('AT+CGCONTRDP=?', 'OK'),
                         ('AT+CGCONTRDP', 'OK'),
                         ('AT+CGCONTRDP?',
                          '+CGCONTRDP: (<p_cid>), (<bearer_id>),(<apn>),(<source_addr and subnet_mask>),(<gw_addr>), (<DNS_prim_addr>), (<DNS_sec_addr>), (<P-CSCF_prim_addr>), (<P-CSCF_sec_addr>),(<IM_CN_Signalling_Flag>)r\nOK'),
                         ('AT+CGCONTRDP=?', 'OK'),
                         ('AT+CGCONTRDP', 'OK'),
                         ('AT+CGCONTRDP?',
                          '+CGCONTRDP: (<p_cid>), (<bearer_id>),(<apn>),(<source_addr and subnet_mask>),(<gw_addr>), (<DNS_prim_addr>), (<DNS_sec_addr>), (<P-CSCF_prim_addr>), (<P-CSCF_sec_addr>),(<IM_CN_Signalling_Flag>)r\nOK'),

                          # no sim
                          ('AT+CGCONTRDP=?', 'OK'),
                          ('AT+CGCONTRDP', 'OK'),
                          ('AT+CGCONTRDP?',
                           '+CGCONTRDP: (<p_cid>), (<bearer_id>),(<apn>),(<source_addr and subnet_mask>),(<gw_addr>), (<DNS_prim_addr>), (<DNS_sec_addr>), (<P-CSCF_prim_addr>), (<P-CSCF_sec_addr>),(<IM_CN_Signalling_Flag>)r\nOK'),

                          # sim
                          ('AT+CGCONTRDP=?', '+CGCONTRDP: 1\nOK'),
                          ('AT+CGCONTRDP',
                           '+CGCONTRDP: 1,5,"next.MNC047.MCC250.GPRS","10.5.58.143","","100.77.4.4","100.77.8.8","","",0,01400\nOK'),
                          ('AT+CGCONTRDP?',
                           '+CGCONTRDP: (<p_cid>), (<bearer_id>),(<apn>),(<source_addr and subnet_mask>),(<gw_addr>), (<DNS_prim_addr>), (<DNS_sec_addr>), (<P-CSCF_prim_addr>), (<P-CSCF_sec_addr>),(<IM_CN_Signalling_Flag>)r\nOK'),

                          # NAVIA
                         ('AT+CGCONTRDP=?', '+CGCONTRDP: 1\nOK'),
                         ('AT+CGCONTRDP', '+CGCONTRDP: 1,5,"simsim.MNC047.MCC250.GPRS","10.4.12.216","","100.77.8.8","100.77.4.4","","",0,01400'),
                         ('AT+CGCONTRDP?',
                          '+CGCONTRDP: (<p_cid>), (<bearer_id>),(<apn>),(<source_addr and subnet_mask>),(<gw_addr>), (<DNS_prim_addr>), (<DNS_sec_addr>), (<P-CSCF_prim_addr>), (<P-CSCF_sec_addr>),(<IM_CN_Signalling_Flag>)r\nOK'),
                         ],
        'AT+CDNSSRV': ['DNS server IP',
                       # без симки и с
                       ('AT+CDNSSRV=?', 'ERROR'),
                       ('AT+CDNSSRV', 'ERROR'),
                       ('AT+CDNSSRV?', 'ERROR'),
                       ],
    },

    # =========================================================================
    "-INTERNET_SERVICE=(TCP/IP стек модуля)": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CSOCKSETPN": ["[DANGER]set active PDP context profile",
        #                 ('AT+CSOCKSETPN=?', '+CSOCKSETPN: 1,(1,6)'),
        #                 ('AT+CSOCKSETPN', 'ERROR'),
        #                 ('AT+CSOCKSETPN?', '+CSOCKSETPN: 1,1'),
        #               ],
        # "AT+CHTPUPDATE": "[DANGER]update time via HTP",
        # "AT+CNTP": "[DANGER]update time via NTP",

        # PING -------------------------------------------
        "AT+CPING": ["""ping address
            ПАРАМЕТРЫ
                "8.8.8.8" — адрес
                1 — тип (IPv4)
                4 — число пакетов (1–100)
                64 — размер (4–188 байт)
                1000 — интервал (мс)
                10000 — таймаут (мс)
                255 — TTL
            """,
                 # navia
                 ('AT+CPING=?', '+CPING: IP address,(1,2),(1-5),(4-188),(1000-10000),(10000-100000),(16-255)'),
                 ('AT+CPING', 'ERROR'),
                 ('AT+CPING?', 'ERROR'),

                # ping-1=IP
                 ('AT+CPING="8.8.8.8",1,1,64,1000,10000,255', '''
                     +CPING: 1,8.8.8.8,92,160,119   ### строка реального пинга
                     +CPING: 3,1,1,0,160,160,160    ### итоговый результат
                     
                     пинг с ошибками
                     ---- Sent utf8 encoded message: "AT+CPING=\"8.8.8.8\",1,1,64,1000,10000,255\r\n" ----
                    AT+CPING="8.8.8.8",1,1,64,1000,10000,255
                    OK
                    +CPING: 2
                    +CPING: 3,1,0,1,0,0,0
                    ---- Sent utf8 encoded message: "AT+CPING=\"8.8.8.8\",1,3,64,1000,10000,255\r\n" ----
                    AT+CPING="8.8.8.8",1,3,64,1000,10000,255
                    OK
                    +CPING: 2
                    +CPING: 2
                    +CPING: 2
                    +CPING: 3,3,0,3,0,0,0
                     '''),
                 # ping-2=NAME
                 ('AT+CPING="www.google.com",1,1,64,1000,10000,255', '''
                
                     пинг с ошибками
                    ---- Sent utf8 encoded message: "AT+CPING=\"www.google.com\",1,1,64,1000,10000,255\r\n" ----
                    AT+CPING="www.google.com",1,1,64,1000,10000,255
                    OK
                    
                    +CPING: 3,0,0,0,0,0,0
                    ---- Sent utf8 encoded message: "AT+CPING=\"www.google.com\",1,3,64,1000,10000,255\r\n" ----
                    AT+CPING="www.google.com",1,3,64,1000,10000,255
                    OK
                    
                    +CPING: 3,0,0,0,0,0,0
                    ---- Sent utf8 encoded message: "AT+CPING=\"www.google.com\",1,1,64,1000,10000,255\r\n" ----
                    AT+CPING="www.google.com",1,1,64,1000,10000,255
                    OK
                    
                    +CPING: 3,0,0,0,0,0,0
                    ---- Sent utf8 encoded message: "AT+CPING=\"ya.ru\",1,1,64,1000,10000,255\r\n" ----
                    AT+CPING="ya.ru",1,1,64,1000,10000,255
                    OK
                    
                    +CPING: 3,0,0,0,0,0,0
                     '''),
                     ],
        "AT+CPINGSTOP": ["stop ping=если пинг запущен и идет долго=НЕ РАБОТАЕТ!!! даже при запущенном ping!",
                         # navia - пинг не запущен
                         ('AT+CPINGSTOP=?', 'ERROR'),
                         ('AT+CPINGSTOP', 'ERROR'),
                         ('AT+CPINGSTOP?', 'ERROR'),
                         ],

        #  -------------------------------------
        'AT+CTCPKA?': ['TCP heartbeat',
                       # no +sim +navia
                       ('AT+CTCPKA=?', 'OK'),
                       ('AT+CTCPKA', 'ERROR'),
                       ('AT+CTCPKA?', '+CTCPKA: 0,120,10,10\nOK'),
                       ],
        # 2 ----------------------------------------
        # 3 --------------------------------------
        'AT+CDNSCFG?': ['DNS settings',
                        # NAVIA
                        ('AT+CDNSCFG=?', '+CDNSCFG: ("Primary DNS"),("Secondary DNS"),type'),
                        ('AT+CDNSCFG', 'ERROR'),
                        ('AT+CDNSCFG?', '''
                            Primary IPv4 DNS: 100.77.8.8,Secondary IPv4 DNS: 100.77.4.4
                            Primary IPv6 DNS: ::,Secondary IPv6 DNS: ::
                        '''),
                        ],
        'AT+CIPDNSSET': ['DNS query parameters',
                         # no +sim +navia
                         ('AT+CIPDNSSET=?', 'ERROR'),
                         ('AT+CIPDNSSET', 'ERROR'),
                         ('AT+CIPDNSSET?', 'ERROR'),
                         ],
        'AT+CDNSGIP': ['query IP by domain name',
                       # no +sim +navia
                       ('AT+CDNSGIP=?', 'OK'),
                       ('AT+CDNSGIP', 'ERROR'),
                       ('AT+CDNSGIP?', 'ERROR'),
                       ],
        'AT+CDNSGHNAME': ['query domain name by IP',
                          # no +sim +navia
                          ('AT+CDNSGHNAME=?', 'ERROR'),
                          ('AT+CDNSGHNAME', 'ERROR'),
                          ('AT+CDNSGHNAME?', 'ERROR'),
                          ],
        'AT+CTCPFIN': ['TCP FIN config',
                       # no +sim
                       ('AT+CTCPFIN=?', 'ERROR'),
                       ('AT+CTCPFIN', 'ERROR'),
                       ('AT+CTCPFIN?', 'ERROR'),
                       ],

        'AT+CTEUTP': ['unknown TCP packet echo',
                      # no +sim
                      ('AT+CTEUTP=?', 'ERROR'),
                      ('AT+CTEUTP', 'ERROR'),
                      ('AT+CTEUTP?', 'ERROR'),
                      ],
        'AT+CUPURE': ['UDP port unreachable ICMP echo=везде Error даже с ',
                      # no +sim
                      ('AT+CUPURE=?', 'ERROR'),
                      ('AT+CUPURE', 'ERROR'),
                      ('AT+CUPURE?', 'ERROR'),
                      ],
        'AT+CINICMPALLOW': ['ICMP filter',
                            # no +sim
                            ('AT+CINICMPALLOW=?', 'ERROR'),
                            ('AT+CINICMPALLOW', 'ERROR'),
                            ('AT+CINICMPALLOW?', 'ERROR'),
                            ],
        'AT+CDNSSRV': ['DNS server IP',
                       # no +sim
                       ('AT+CDNSSRV=?', 'ERROR'),
                       ('AT+CDNSSRV', 'ERROR'),
                       ('AT+CDNSSRV?', 'ERROR'),
                       ],
        'AT+CHTPSERV': ['HTP server info',
                        # no +sim
                        ('AT+CHTPSERV=?',
                         '+CHTPSERV: "ADD","HOST",(1-65535),(0-1)[,"PROXY",(1-65535)]\n+CHTPSERV: "DEL",(0-15)\nOK'),
                        ('AT+CHTPSERV', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=0', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=1', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=2', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=3', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=4', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=5', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=6', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=7', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=8', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=9', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ],
    },

    # =========================================================================
    "-SAT_STK=SIM APPLICATION TOOLKIT": {
        # 0=DANGER+USELESS -------------------------------
        # 1=ACCURATE -------------------------------------
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------

        # "AT+STK": "[DANGER]STK switch (on/off)",
        # "AT+STKFMT": "[DANGER]STK PDU format (0=decoded, 1=PDU) # DANGER (reboot)",
        # "AT+STSM": "[DANGER]get STK setup menu list (PDU)",

        'AT+STIN': ['SAT indication',
                    ('AT+STIN=?', 'ERROR'),
                    ('AT+STIN', 'ERROR'),
                    ('AT+STIN?', 'ERROR'),
                    ],
        'AT+STGI': ['get SAT information',
                    ('AT+STGI=?', 'ERROR'),
                    ('AT+STGI', 'ERROR'),
                    ('AT+STGI?', 'ERROR'),
                    ],
        'AT+STGR': ['SAT respond',
                    ('AT+STGR=?', 'ERROR'),
                    ('AT+STGR', 'ERROR'),
                    ('AT+STGR?', 'ERROR'),
                    ],
        'AT+STENV': ['original STK PDU envelope command',
                     ('AT+STENV=?', 'ERROR'),
                     ('AT+STENV', 'ERROR'),
                     ('AT+STENV?', 'ERROR'),
                     ],
    },

    # =========================================================================
    "---FILE_SYSTEM": {
        # 0=DANGER+USELESS -------------------------------
        # 1=ACCURATE -------------------------------------
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------

        # "AT+FSCD": "[DANGER]select current directory",
        # "AT+FSMKDIR": "[DANGER]make directory",
        # "AT+FSRMDIR": "[DANGER]delete directory",
        # "AT+FSDEL": "[DANGER]delete file",
        # "AT+FSRENAME": "[DANGER]rename file",
        # "AT+FSLOCA": "[DANGER]select storage place",
        # "AT+FSCOPY": "[DANGER]copy file",
        # "AT+CFTRANRX": "[DANGER]transfer file to EFS",
        # "AT+CFTRANTX": "[DANGER]transfer file from EFS",

        'AT+FSLS': ['list directories/files',
                    ('AT+FSLS=?', '+FSLS: (0-2)\nOK'),
                    ('AT+FSLS', 'OK'),
                    ('AT+FSLS?', '+FSLS: SUBDIRECTORIES:0,FILES:0\nOK'),
                    ('AT+FSLS=0', 'OK'),
                    ('AT+FSLS?', '+FSLS: SUBDIRECTORIES:0,FILES:0\nOK'),
                    ('AT+FSLS=1', 'OK'),
                    ('AT+FSLS?', '+FSLS: SUBDIRECTORIES:0,FILES:0\nOK'),
                    ('AT+FSLS=2', 'OK'),
                    ('AT+FSLS?', '+FSLS: SUBDIRECTORIES:0,FILES:0\nOK'),
                    ],
        'AT+FSATTRI': ['file attributes',
                       ('AT+FSATTRI=?', 'OK'),
                       ('AT+FSATTRI', 'ERROR'),
                       ('AT+FSATTRI?', 'ERROR'),
                       ],
        'AT+FSMEM': ['available memory',
                     ('AT+FSMEM=?', 'OK'),
                     ('AT+FSMEM', '+FSMEM: C:(720896,438272)\nOK'),
                     ('AT+FSMEM?', 'ERROR'),
                     ],
    },

    # =========================================================================
    "NETWORK_SOCKETS": {
        # 0=DANGER+USELESS -------------------------------
        # 1=ACCURATE -------------------------------------
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------

      'AT+CNETSTART': ['[DANGER]open packet network',
                ('AT+CNETSTART=?', 'ERROR'),
                ('AT+CNETSTART', 'ERROR'),
                ('AT+CNETSTART?', 'ERROR'),
                ],
        # "AT+CNETSTOP": "[DANGER]close network",
        # "AT+CNETIPADDR": "[DANGER]inquire PDP address",
    },

    # =========================================================================
    "GPS_GNSS=обязательно АКТИВИРОВАТЬ питание!": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CGPSDEL": ["[DANGER]delete GPS info=After executing the command, GPS start is cold start=must be executed after GPS stopped.",
        #         # NAVIA
        #         ('AT+CGPSDEL=?', 'ERROR'),
        #         ('AT+CGPSDEL', 'ERROR'),
        #         ('AT+CGPSDEL?', 'ERROR'),
        # ],
        # "AT+CGPSXD": "[DANGER]download XTRA file into module",
        #         # NAVIA
        #         ('AT+CGPSXD=?', 'ERROR'),
        #         ('AT+CGPSXD', 'ERROR'),
        #         ('AT+CGPSXD?', 'ERROR'),
        # ],

        # 1=ACCURATE -------------------------------------
        # ИНФО О ЧИПЕ
        'AT+CGNSSPROD': ['[TIME] Get GNSS Production Info - НУЖНО 10 СЕКУНД НА ОТВЕТ!!!!',
                         # NAVIA
                         ('AT+CGNSSPROD=?', 'OK'),
                         ('AT+CGNSSPROD', 'PRODUCT: UNICORECOMM,UC6228CI,R3.4.21.0Build16211\nOK'),
                         ('AT+CGNSSPROD?', 'ERROR'),

                        # из доков
                         ('AT+CGNSSPROD', 'PRODUCT: UC6228CI,G1L1E1,N/A,R3.4.21.0Build16211\nOK'),
                         ],
        # ВКЛЮЧЕНИЕ ПИТАНИЯ
        'AT+CGNSSPWR?': ['pwr for gnss module=не у всех есть! harvester-НЕТ! ',
                        # HARVESTER - ВСЕ ERROR!!!

                        # NAVIA
                        ('AT+CGNSSPWR=?', '+CGNSSPWR: (0,1),(0,1),(0,1)'),
                        ('AT+CGNSSPWR', 'ERROR'),
                        ('AT+CGNSSPWR?', '+CGNSSPWR: 1,0,1'),

                        ('AT+CGNSSPWR=1', 'OK\n+CGNSSPWR: READY!'),  # выдает через паузу!!! около 10с
                        ],

        # КООРДИНАТЫ-1=логи первички=спутников
        'AT+CGPSFTM': ['START GPS test mode',
                       # harvester
                       ('AT+CGPSFTM=?', 'ERROR'),
                       ('AT+CGPSFTM', 'ERROR'),
                       ('AT+CGPSFTM?', 'ERROR'),

                       # navia
                       ('AT+CGPSFTM=?', 'OK'),
                       ('AT+CGPSFTM', 'ERROR'),
                       ('AT+CGPSFTM?', '+CGPSFTM: 0'),

                       # включение
                       ('AT+CGPSFTM=1', '''
                       OK
                        +GPGSV,03,28,10,27,19,37,13,34,05,27,15,30,17,33,09,21,194,37
                        +GBGSV
                        +GAGSV,31,23,36,25
                        +GPGSV,03,27,10,27,19,35,13,35,05,23,15,25,17,34,09,21,194,37
                        +GBGSV
            
                        # вар 2
                        +GPGSV,04,37,24,38,03,30,06,25
                        +GLGSV
                        +GAGSV,17,22
                        +GPGSV,04,28,24,36,03,27,06,33
                        +GLGSV
                        +GAGSV,17,22
                        +GPGSV,04,34,24,36,03,30,06,33,14,31
                        +GLGSV
                        +GAGSV,17,22
                        +GPGSV,04,30,24,36,03,29,06,32,14,27
                        +GLGSV
                        +GAGSV,17,22
                        +GPGSV,04,30,24,36,03,25,06,25,14,30
                        +GLGSV
                        +GAGSV,17,22
                        +GPGSV,04,32,24,37,03,25,06,23,14,23
                        +GLGSV
                        +GAGSV,17,22
                        +GPGSV,04,32,24,37,03,31,06,30,14,32
                        +GLGSV
                        +GAGSV,17,22
                        +GPGSV,04,34,24,35,03,29,06,23,14,27
                        +GLGSV
                        +GAGSV,17,22
                        +GPGSV,04,32,24,37,03,28,06,26,14,30
                        +GLGSV
                        +GAGSV,17,22
                       '''),
                       ],
        # КООРДИНАТЫ-2=вычисленные достоверные
        'AT+CGPSINFO': ['get GPS fixed position=даст значения только если достоверные!!! иначе пустые запятые!!!',
                        # ИЗ ДОКУМЕНТАЦИИ -----------------
                        # ('AT+CGPSINFO=?', '+CGPSINFO: (0-255)'),
                        # ('AT+CGPSINFO', '+CGPSINFO:3113.343286,N,12121.234064,E,250311,072809.3,44.1,0.0,0'),
                        # ('AT+CGPSINFO?', '+CGPSINFO: 0'),

                        # РЕАЛЬНО -------------------------
                        # harvester
                        ('AT+CGPSINFO=?', 'ERROR'),
                        ('AT+CGPSINFO', 'ERROR'),
                        ('AT+CGPSINFO?', 'ERROR'),

                        # navia
                        ('AT+CGPSINFO=?', '+CGPSINFO: (0-255)'),
                        ('AT+CGPSINFO', '+CGPSINFO: ,,,,,,,,'),
                        ('AT+CGPSINFO?', '+CGPSINFO: 0'),

                        ('AT+CGPSINFO=6', 'OK'),
                        ('AT+CGPSINFO', '+CGPSINFO: ,,,,,,,,'),
                        ('AT+CGPSINFO?', '+CGPSINFO: 6'),
                        ],
        'AT+CGNSSINFO': ['GNSS fixed position',
                         # harvester noSim
                         ('AT+CGNSSINFO=?', 'ERROR'),
                         ('AT+CGNSSINFO', 'ERROR'),
                         ('AT+CGNSSINFO?', 'ERROR'),

                         # harvester noSim
                         ('AT+CGNSSINFO=?', '+CGNSSINFO: (0-255)'),
                         ('AT+CGNSSINFO', '+CGNSSINFO: ,,,,,,,,'),
                         ('AT+CGNSSINFO?', '+CGNSSINFO: 0'),
                         ],
        # CONTROL
        'AT+CGPSCOLD': ['cold start GPS',
                        ('AT+CGPSCOLD=?', 'ERROR'),
                        ('AT+CGPSCOLD', 'ERROR'),
                        ('AT+CGPSCOLD?', 'ERROR'),
                        ],
        'AT+CGPSWARM': ['Warm Start GPS',
                        ('AT+CGPSWARM=?', 'OK'),
                        ('AT+CGPSWARM', 'OK'),
                        ('AT+CGPSWARM?', 'ERROR'),
                        ],
        'AT+CGPSHOT': ['hot start GPS',
                       ('AT+CGPSHOT=?', 'ERROR'),
                       ('AT+CGPSHOT', 'ERROR'),
                       ('AT+CGPSHOT?', 'ERROR'),

                       # navia
                       ('AT+CGPSHOT=?', 'OK'),
                       ('AT+CGPSHOT', 'OK'),
                       ('AT+CGPSHOT?', 'ERROR'),
                       ],
        # SETTINGS
        'AT+CGNSSMODE': ['''GNSS support mode.
                        1 GPS
                        2 BDS
                        3 GPS + BDS
                        4 GLONASS
                        ''',
                         # harvester noSim
                         ('AT+CGNSSMODE=?', 'ERROR'),
                         ('AT+CGNSSMODE', 'ERROR'),
                         ('AT+CGNSSMODE?', 'ERROR'),

                         # navia SIM
                         ('AT+CGNSSMODE=?', '+CGNSSMODE: (1-4)'),
                         ('AT+CGNSSMODE', 'OK'),
                         ('AT+CGNSSMODE?', '+CGNSSINFO: 0'),

                         # navia-2=
                         ('AT+CGNSSMODE=?', '+CGNSSMODE: (1-4)'),
                         ('AT+CGNSSMODE', 'OK'),
                         ('AT+CGNSSMODE?', '+CGNSSINFO: 3'),
                         ],
        'AT+CGPSAUTO?': ['auto-start GPS',
                        # harvester
                        ('AT+CGPSAUTO=?', 'ERROR'),
                        ('AT+CGPSAUTO', 'ERROR'),
                        ('AT+CGPSAUTO?', 'ERROR'),

                        # navia
                        ('AT+CGPSAUTO=?', '+CGPSAUTO: (0,1)'),
                        ('AT+CGPSAUTO', 'OK'),
                        ('AT+CGPSAUTO?', '+CGPSAUTO: 0'),
                        ('AT+CGPSAUTO=0', 'OK'),
                        ('AT+CGPSAUTO?', '+CGPSAUTO: 0'),
                        ('AT+CGPSAUTO=1', 'OK'),
                        ('AT+CGPSAUTO?', '+CGPSAUTO: 1'),
                        ],

        'AT+CGPSNMEARATE': ['Set NMEA Output Rate',
                            # navia
                            ('AT+CGPSNMEARATE=?', '+CGPSNMEARATE: (1,2,5)\nOK'),
                            ('AT+CGPSNMEARATE', 'OK'),
                            ('AT+CGPSNMEARATE?', '+CGPSNMEARATE: 1\nOK'),
                            ('AT+CGPSNMEARATE=2', 'OK'),
                            ('AT+CGPSNMEARATE?', '+CGPSNMEARATE: 2\nOK'),
                            ],

        'AT+CGNSSPORTSWITCH': ['Select output port for NMEA',
                               # navia
                               ('AT+CGNSSPORTSWITCH=?', '+CGNSSPORTSWITCH: (0,1),(0,1)\nOK'),
                               ('AT+CGNSSPORTSWITCH', 'ERROR'),
                               ('AT+CGNSSPORTSWITCH?', '+CGNSSPORTSWITCH: 0,0\nOK'),
                               ('AT+CGNSSPORTSWITCH=0,1', 'OK'),
                               ('AT+CGNSSPORTSWITCH?', '+CGNSSPORTSWITCH: 0,1\nOK'),
                               ('AT+CGNSSPORTSWITCH=1,1', 'OK'),
                               ('AT+CGNSSPORTSWITCH?', '+CGNSSPORTSWITCH: 1,1\nOK'),
                               ],

        'AT+CGPS': ['start/stop GPS session=вроде нет такой чтоли???',
                    # ИЗ ДОКУМЕНТАЦИИ -----------------
                    # ('AT+CGPS=?', '+CGPSINFO: (0-255)'),
                    # ('AT+CGPS', '+CGPSINFO:3113.343286,N,12121.234064,E,250311,072809.3,44.1,0.0,0'),
                    # ('AT+CGPS?', '+CGPSINFO: 0'),

                    # ('AT+CGPS=0', 'OK'),    # disable
                    # ('AT+CGPS=1', 'OK'),    # enable
                    # ('AT+CGPS=1,1', 'OK'),    # enable

                    # РЕАЛЬНО harvester+navia -------------------------
                    ('AT+CGPS=?', 'ERROR'),
                    ('AT+CGPS', 'ERROR'),
                    ('AT+CGPS?', 'ERROR'),

                    ('AT+CGPS=0', 'ERROR'),
                    ('AT+CGPS=1', 'ERROR'),
                    ],
        # AGPS  --------------
        'AT+CAGPS': ['AGPS transport security',
                       # РЕАЛЬНО harvester+navia!!!---------------
                       ('AT+CAGPS=?', 'ERROR'),
                       ('AT+CAGPS', 'OK\n+AGPS: success.'),
                       ('AT+CAGPS?', 'ERROR'),
                       ],
        'AT+CGPSURL': ['AGPS server URL',
                       # ИЗ ДОКУМЕНТАЦИИ ---------------
                       # AT+CGPSURL=”123.123.123.123:8888”
                       # OK
                       # AT+CGPSURL?
                       # +CGPSURL: ”123.123.123.123:8888”

                       # РЕАЛЬНО harvester+navia!!! тоесть даже в navia ее нет!!!---------------
                       ('AT+CGPSURL=?', 'ERROR'),
                       ('AT+CGPSURL', 'ERROR'),
                       ('AT+CGPSURL?', 'ERROR'),
                       ],
        'AT+CGPSSSL': ['AGPS transport security',
                       # РЕАЛЬНО harvester+navia!!!---------------
                       ('AT+CGPSSSL=?', 'ERROR'),
                       ('AT+CGPSSSL', 'ERROR'),
                       ('AT+CGPSSSL?', 'ERROR'),
                       ],




        'AT+CGPSNMEA': ['NMEA sentence type',
                        # РЕАЛЬНО harvester+navia!!!---------------
                        ('AT+CGPSNMEA=?', 'ERROR'),
                        ('AT+CGPSNMEA', 'ERROR'),
                        ('AT+CGPSNMEA?', 'ERROR'),
                        ],
        'AT+CGPSNEMARATE': ['set NMEA output rate',
                        # РЕАЛЬНО harvester+navia!!!---------------
                        ('AT+CGPSNEMARATE=?', 'ERROR'),
                        ('AT+CGPSNEMARATE', 'ERROR'),
                        ('AT+CGPSNEMARATE?', 'ERROR'),
                        ],
        'AT+CGPSMD': ['AGPS MO method',
                      # РЕАЛЬНО harvester+navia!!!---------------
                      ('AT+CGPSMD=?', 'ERROR'),
                      ('AT+CGPSMD', 'ERROR'),
                      ('AT+CGPSMD?', 'ERROR'),
                      ],
        'AT+CGPSXE': ['GPS XTRA enable',
              # РЕАЛЬНО harvester+navia!! даже после вкл питания!---------------
              ('AT+CGPSXE=?', 'ERROR'),
              ('AT+CGPSXE', 'ERROR'),
              ('AT+CGPSXE?', 'ERROR'),
              ],
        'AT+CGPSXDAUTO': ['auto-download XTRA file into module',
              # РЕАЛЬНО harvester+navia!!! даже после вкл питания!---------------
              ('AT+CGPSXDAUTO=?', 'ERROR'),
              ('AT+CGPSXDAUTO', 'ERROR'),
              ('AT+CGPSXDAUTO?', 'ERROR'),
              ],
        'AT+CGPSINFOCFG': ['report NMEA-0183 sentence',
               # РЕАЛЬНО harvester+navia!!! даже после вкл питания!---------------
               ('AT+CGPSINFOCFG=?', 'ERROR'),
               ('AT+CGPSINFOCFG', 'ERROR'),
               ('AT+CGPSINFOCFG?', 'ERROR'),
               ],
        'AT+CGPSPMD': ['positioning mode',
               # РЕАЛЬНО harvester+navia!!! даже после вкл питания!---------------
               ('AT+CGPSPMD=?', 'ERROR'),
               ('AT+CGPSPMD', 'ERROR'),
               ('AT+CGPSPMD?', 'ERROR'),
               ],
        'AT+CGPSMSB': ['based mode switch to standalone',
               # РЕАЛЬНО harvester+navia!!! даже после вкл питания!---------------
               ('AT+CGPSMSB=?', 'ERROR'),
               ('AT+CGPSMSB', 'ERROR'),
               ('AT+CGPSMSB?', 'ERROR'),
               ],
        'AT+CGPSHOR': ['positioning accuracy',
               # РЕАЛЬНО harvester+navia!!! даже после вкл питания!---------------
               ('AT+CGPSHOR=?', 'ERROR'),
               ('AT+CGPSHOR', 'ERROR'),
               ('AT+CGPSHOR?', 'ERROR'),
               ],
        'AT+CGPSNOTIFY': ['LCS respond positioning request',
              # РЕАЛЬНО harvester+navia!!! даже после вкл питания!---------------
              ('AT+CGPSNOTIFY=?', 'ERROR'),
              ('AT+CGPSNOTIFY', 'ERROR'),
              ('AT+CGPSNOTIFY?', 'ERROR'),
              ],
    },

    # =========================================================================
    # 16. РАЗНОЕ
    # =========================================================================
    "MISC/VENDOR(может быть не указан в мануале)": {
        # 0=DANGER+USELESS -------------------------------
        # "AT*CNETSCAN": "[DANGER]vendor: network scan (может отсутствовать)",

        # 1=ACCURATE -------------------------------------
        'AT+WS46?': ['RAT selection',
                     # no sim
                     ('AT+WS46=?', '+WS46: (12,22,25,28,29,30,31)\nOK'),
                     ('AT+WS46', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=12', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=22', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=25', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=28', 'OK'),
                     ('AT+WS46?', '+WS46:28\nOK'),
                     ('AT+WS46=29', 'OK'),
                     ('AT+WS46?', '+WS46:28\nOK'),
                     ('AT+WS46=30', 'OK'),
                     ('AT+WS46?', '+WS46:30\nOK'),
                     ('AT+WS46=31', 'OK'),
                     ('AT+WS46?', '+WS46:30\nOK'),

                     # sim
                     ('AT+WS46=?', '+WS46: (12,22,25,28,29,30,31)\nOK'),
                     ('AT+WS46', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=12', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=22', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=25', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=28', '+CGREG: 0\n+CEREG: 0'),
                     ('AT+WS46?', 'OK\n+CGEV: ME DETACH\n+WS46:28\nOK\n+CREG: 0'),
                     ('AT+WS46=29', 'OK'),
                     ('AT+WS46?', '+WS46:28\nOK'),
                     ('AT+WS46=30', 'OK\n+CGEV: ME DETACH'),
                     ('AT+WS46?', '+WS46:30\nOK'),
                     ('AT+WS46=31', 'OK'),
                     ('AT+WS46?', '+WS46:30\nOK'),
                     ],
        'AT+CESQ': ['extended signal quality',
                    ('AT+CESQ=?', '+CESQ: (0-63,99),(0-7,99),(0-96,255),(0-49,255),(0-34,255),(0-97,255)\nOK'),
                    ('AT+CESQ', '+CESQ: 99,99,255,255,9,51\nOK'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=0', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=1', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=2', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=3', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=4', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=5', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=6', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=7', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=8', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=9', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),

                    # sim
                    ('AT+CESQ=?', '+CESQ: (0-63,99),(0-7,99),(0-96,255),(0-49,255),(0-34,255),(0-97,255)\nOK'),
                    ('AT+CESQ', '+CESQ: 99,99,255,255,255,255\nOK'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=0',
                     '+CEREG: 1,0B3D,0BD15979,7\n+CGREG: 1,0B3D,0BD15979\n+CGEV: EPS PDN ACT 1\n+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=1', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=2', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=3', '+CME ERROR: unknown error\n+CREG: 1,0B3D,0BD15979'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=4', '+CEREG: 1,0B3D,0BD1591A,7\n+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=5', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=6', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=7', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=8', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=9', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),

                    # NAVIA
                    # 1=значения постоянно меняются! -------------------------
                    # ---- Sent utf8 encoded message: "AT+CESQ\r\n" ----
                    # AT+CESQ
                    # +CESQ: 40,99,255,255,3,37
                    # ---- Sent utf8 encoded message: "AT+CESQ\r\n" ----
                    # AT+CESQ
                    # +CESQ: 40,99,255,255,3,37
                    # ---- Sent utf8 encoded message: "AT+CESQ\r\n" ----
                    # AT+CESQ
                    # +CESQ: 40,99,255,255,0,10
                    # ---- Sent utf8 encoded message: "AT+CESQ\r\n" ----
                    # AT+CESQ
                    # +CESQ: 40,99,255,255,0,10
                    # ---- Sent utf8 encoded message: "AT+CESQ\r\n" ----
                    # AT+CESQ
                    # +CESQ: 41,99,255,255,12,38
                    # ---- Sent utf8 encoded message: "AT+CESQ\r\n" ----
                    # AT+CESQ
                    # +CESQ: 41,99,255,255,12,38
                    # 2=все остальные установки дают пустоту!!! -------------
                    ('AT+CESQ=*', '+CME ERROR: unknown error'),
                    ],

        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
        'AT*CNTI': ['vendor: cell info (может отсутствовать)',
                    ('AT*CNTI=?', 'ERROR'),
                    ('AT*CNTI', 'ERROR'),
                    ('AT*CNTI?', 'ERROR'),
                    ],
        'AT*CPSI': ['vendor: PSI (может отсутствовать)',
                    ('AT*CPSI=?', 'ERROR'),
                    ('AT*CPSI', 'ERROR'),
                    ('AT*CPSI?', 'ERROR'),
                    ],
        'AT*CELLINFO': ['vendor: cell info (может отсутствовать)',
                    ('AT*CELLINFO=?', 'ERROR'),
                    ('AT*CELLINFO', 'ERROR'),
                    ('AT*CELLINFO?', 'ERROR'),
                    ],
        'AT+CRUSET': ['vendor: RU settings (может отсутствовать)',
                      ('AT+CRUSET=?', 'ERROR'),
                      ('AT+CRUSET', 'ERROR'),
                      ('AT+CRUSET?', 'ERROR'),
                      ],
        'AT+CCED': ['vendor: cell environment description',
                    ('AT+CCED=?', 'ERROR'),
                    ('AT+CCED', 'ERROR'),
                    ('AT+CCED?', 'ERROR'),
                    ],
        'AT+CIREG': ['IMS registration',
                     ('AT+CIREG=?', '+CIREG: (0-3)\nOK'),
                     ('AT+CIREG', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=0', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=1', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=2', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=3', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ],
        'AT+CIMS': ['IMS status',
                    ('AT+CIMS=?', 'ERROR'),
                    ('AT+CIMS', 'ERROR'),
                    ('AT+CIMS?', 'ERROR'),
                    ],
    },
    # =========================================================================
    "-11=TCP_IP_STACK(Socket Service)": {
        'AT+NETOPEN': ['[DANGER]Start Socket Service (Активирует PDP контекст)',
                       # navia
                       ('AT+NETOPEN=?', 'ERROR'),
                       ('AT+NETOPEN', '+NETOPEN: 0'),
                       ('AT+NETOPEN?', '+NETOPEN: 1'),

                       # из доков
                       ('AT+NETOPEN=?', '+NETOPEN: (1-15)\nOK'),
                       ('AT+NETOPEN', 'ERROR'),
                       ('AT+NETOPEN?', '+NETOPEN: 0\nOK'),
                       ('AT+NETOPEN=1', 'OK\n+NETOPEN: 0,1'),
                       ('AT+NETOPEN?', '+NETOPEN: 1\nOK'),
                       ],
        'AT+NETCLOSE': ['[DANGER]Stop Socket Service (Деактивирует PDP)',
                        # navia
                        ('AT+NETCLOSE=?', 'OK'),

                        # из доков
                        ('AT+NETCLOSE=?', 'OK'),
                        ('AT+NETCLOSE', 'ERROR'),
                        ('AT+NETCLOSE?', 'ERROR'),
                        ('AT+NETCLOSE=1', 'OK\n+NETCLOSE: 0,1'),
                        ],
        'AT+CIPOPEN': ['[DANGER]Establish Connection (TCP/UDP)',
                       # NAVIA
                       ('AT+CIPOPEN=?', '+CIPOPEN: (0-9),("TCP","UDP","UDP SERVER")\nOK'),
                       ('AT+CIPOPEN', 'ERROR'),
                       ('AT+CIPOPEN?', '+CIPOPEN: 0\n+CIPOPEN: 1\n+CIPOPEN: 2\n...\n+CIPOPEN: 9\nOK'),

                       ('AT+CIPOPEN=0,"TCP","1.1.1.1",80', 'OK\n+CIPOPEN: 0,0'),    # из доков
                       ],




        'AT+CIPSEND': ['[DANGER]Send Data (Ждет ввода данных и Ctrl+Z)',
                        # из доков
                       ('AT+CIPSEND=?', '+CIPSEND: (0-9),(1-1500)\nOK'),
                       ('AT+CIPSEND', 'ERROR'),
                       ('AT+CIPSEND?', 'OK'),
                       ('AT+CIPSEND=0,5', '> (ждет ввода)'),
                       ],
        'AT+CIPCLOSE': ['[DANGER]Close Socket',
                        # из доков
                        ('AT+CIPCLOSE=?', '+CIPCLOSE: (0-9)\nOK'),
                        ('AT+CIPCLOSE', 'ERROR'),
                        ('AT+CIPCLOSE?', '+CIPCLOSE: 0,0,0,0,0,0,0,0,0,0\nOK'),
                        ('AT+CIPCLOSE=0', 'OK\n+CIPCLOSE: 0,0'),
                        ],
        'AT+CIPRXGET': ['Set data retrieve mode',
                        # из доков
                        ('AT+CIPRXGET=?', '+CIPRXGET: (0-4),(0-9),(1-1500)\nOK'),
                        ('AT+CIPRXGET', 'ERROR'),
                        ('AT+CIPRXGET?', '+CIPRXGET: 1\nOK'),
                        ('AT+CIPRXGET=1', 'OK'),
                        ],
        'AT+CIPHEAD': ['Add IP Header',
                       # из доков
                       ('AT+CIPHEAD=?', '+CIPHEAD: (0-1)\nOK'),
                       ('AT+CIPHEAD', 'OK'),
                       ('AT+CIPHEAD?', '+CIPHEAD: 1\nOK'),
                       ('AT+CIPHEAD=1', 'OK'),
                       ],
        'AT+CIPMODE': ['Transparent mode (0/1)',
                       # из доков
                       ('AT+CIPMODE=?', '+CIPMODE: (0-1)\nOK'),
                       ('AT+CIPMODE', 'OK'),
                       ('AT+CIPMODE?', '+CIPMODE: 0\nOK'),
                       ('AT+CIPMODE=1', 'OK'),
                       ],
        'AT+SERVERSTART': ['[DANGER]Start TCP Server',
                           # из доков
                           ('AT+SERVERSTART=?', '+SERVERSTART: (0-65535),(0-3)\nOK'),
                           ('AT+SERVERSTART', 'ERROR'),
                           ('AT+SERVERSTART?', 'ERROR'),
                           ('AT+SERVERSTART=8080,0', 'OK'),
                           ],
        'AT+CIPSETAPN': ['Set up PDP/APN channels',
                         # из доков
                         ('AT+CIPSETAPN=?', 'OK'),
                         ('AT+CIPSETAPN', 'ERROR'),
                         ('AT+CIPSETAPN?', 'ERROR'),
                         ],
    },

    # =========================================================================
    "-12=HTTP_SERVICE": {
        'AT+HTTPINIT': ['[DANGER]Start HTTP Service',
                        # navia
                        ('AT+HTTPINIT=?', '+HTTPINIT: (1-n)\nOK'),
                        ('AT+HTTPINIT', 'OK'),
                        ('AT+HTTPINIT?', 'ERROR'),
                        ('AT+HTTPINIT=1', 'ERROR'),
                        ],
        'AT+HTTPTERM': ['Stop HTTP Service',
                        ('AT+HTTPTERM=?', '+HTTPTERM: (1-15)\nOK'),
                        ('AT+HTTPTERM', 'ERROR'),
                        ('AT+HTTPTERM?', 'ERROR'),
                        ('AT+HTTPTERM=1', 'OK\n+HTTPTERM: 0,1'),
                        ],
        'AT+HTTPPARA': ['Set HTTP Parameters (URL, ContentType)',
                        ('AT+HTTPPARA=?', 'OK'),    # navia
                        ('AT+HTTPPARA', 'ERROR'),   # navia
                        ('AT+HTTPPARA?', 'ERROR'),
                        ('AT+HTTPPARA="URL","http://example.com"', 'OK'),
                        ],
        'AT+HTTPACTION': ['HTTP Method Action (GET/POST/HEAD)',
                          ('AT+HTTPACTION=?', '+HTTPACTION: (0-4)\nOK'),# navia
                          ('AT+HTTPACTION', 'ERROR'),# navia
                          ('AT+HTTPACTION?', 'ERROR'),# navia
                          ('AT+HTTPACTION=0', 'OK\n+HTTPACTION: 0,200,1024'),
                          ],
        'AT+HTTPREAD': ['Read HTTP Response',
                        ('AT+HTTPREAD=?', 'OK'),# navia
                        ('AT+HTTPREAD', 'ERROR'),# navia
                        ('AT+HTTPREAD?', 'ERROR'),# navia

                        ('AT+HTTPREAD?', '+HTTPREAD: LEN,0\nOK'),
                        ('AT+HTTPREAD=0,100', 'OK\n+HTTPREAD: 100\n<data>'),
                        ],
        'AT+HTTPDATA': ['Input HTTP Data (POST)',
                        ('AT+HTTPDATA=?', 'OK'),# navia
                        ('AT+HTTPDATA', 'ERROR'),# navia
                        ('AT+HTTPDATA?', 'ERROR'),# navia
                        ('AT+HTTPDATA=10,1000', 'DOWNLOAD'),
                        ],
        'AT+HTTPHEAD': ['Read HTTP Header',
                        ('AT+HTTPHEAD=?', 'OK'),# navia
                        ('AT+HTTPHEAD', 'ERROR'),# navia
                        ('AT+HTTPHEAD?', 'ERROR'),# navia

                        ('AT+HTTPHEAD', '+HTTPHEAD: 200\n<data>'),
                        ],
    },
    # =========================================================================
    "-13=MQTT_SERVICE": {
        'AT+CMQTTSTART': ['[DANGER]Start MQTT Service',
                          ('AT+CMQTTSTART=?', '+CMQTTSTART: (1-15)\nOK'),
                          ('AT+CMQTTSTART', 'ERROR'),
                          ('AT+CMQTTSTART?', 'ERROR'),
                          ('AT+CMQTTSTART=1', 'OK\n+CMQTTSTART: 0,1'),
                          ],
        'AT+CMQTTSTOP': ['Stop MQTT Service',
                         ('AT+CMQTTSTOP=?', '+CMQTTSTOP: (1-15)\nOK'),
                         ('AT+CMQTTSTOP', 'ERROR'),
                         ('AT+CMQTTSTOP?', 'ERROR'),
                         ('AT+CMQTTSTOP=1', 'OK\n+CMQTTSTOP: 0,1'),
                         ],
        'AT+CMQTTACCQ': ['Acquire MQTT Client',
                         ('AT+CMQTTACCQ=?', '+CMQTTACCQ: (0-1),(1-128)[,(0-1)]\nOK'),# navia
                         ('AT+CMQTTACCQ', 'ERROR'),
                         ('AT+CMQTTACCQ?', '+CMQTTACCQ: 0,"clientID",0\nOK'),
                         ('AT+CMQTTACCQ=0,"clientID",0', 'OK'),
                         ],
        'AT+CMQTTCONNECT': ['Connect to MQTT Server',
                            ('AT+CMQTTCONNECT=?',
                             '+CMQTTCONNECT: (0-1),(9-256),(1-64800),(0-1)[,<user>,<pass>]\nOK'),# navia
                            ('AT+CMQTTCONNECT', 'ERROR'),# navia
                            ('AT+CMQTTCONNECT?', '+CMQTTCONNECT: 0\n+CMQTTCONNECT: 1\nOK'),# navia

                            ('AT+CMQTTCONNECT?', '+CMQTTCONNECT: 0,"tcp://1.2.3.4:1883",20,1\nOK'),
                            ('AT+CMQTTCONNECT=0,"tcp://1.2.3.4:1883",20,1', 'OK\n+CMQTTCONNECT: 0,0'),
                            ],
        'AT+CMQTTDISC': ['Disconnect from MQTT Server',
                         ('AT+CMQTTDISC=?', '+CMQTTDISC: (0-1),(0,1-180)\nOK'),
                         ('AT+CMQTTDISC', 'ERROR'),
                         ('AT+CMQTTDISC?', '+CMQTTDISC: 0,1\nOK'),
                         ('AT+CMQTTDISC=0', 'OK\n+CMQTTDISC: 0,0'),
                         ],
        'AT+CMQTTTOPIC': ['Input Topic of Publish',
                          ('AT+CMQTTTOPIC=?', '+CMQTTTOPIC: (0-1),(1-1024)\nOK'),
                          ('AT+CMQTTTOPIC', 'ERROR'),
                          ('AT+CMQTTTOPIC?', 'ERROR'),
                          ('AT+CMQTTTOPIC=0,9', '> (ждет топик)'),
                          ],
        'AT+CMQTTPAYLOAD': ['Input Payload of Publish',
                            ('AT+CMQTTPAYLOAD=?', '+CMQTTPAYLOAD: (0-1),(1-10240)\nOK'),
                            ('AT+CMQTTPAYLOAD', 'ERROR'),
                            ('AT+CMQTTPAYLOAD?', 'ERROR'),
                            ('AT+CMQTTPAYLOAD=0,5', '> (ждет payload)'),
                            ],
        'AT+CMQTTPUB': ['Publish Message',
                        ('AT+CMQTTPUB=?', '+CMQTTPUB: (0-1),(0-2),(1-180),(0-1),(0-1)\nOK'),
                        ('AT+CMQTTPUB', 'ERROR'),
                        ('AT+CMQTTPUB?', 'ERROR'),
                        ('AT+CMQTTPUB=0,1,60', 'OK\n+CMQTTPUB: 0,0'),
                        ],
        'AT+CMQTTSUB': ['Subscribe Topic',
                        ('AT+CMQTTSUB=?', '+CMQTTSUB: (0-1),(1-1024),(0-2),(0-1)\nOK'),
                        ('AT+CMQTTSUB', 'ERROR'),
                        ('AT+CMQTTSUB?', '+CMQTTSUB: \nOK'),
                        ('AT+CMQTTSUB=0,9,1', '> (ждет топик)'),
                        ],
        'AT+CMQTTUNSUB': ['Unsubscribe Topic',
                          ('AT+CMQTTUNSUB=?', '+CMQTTUNSUB: (0-1),(1-1024),(0-1)\nOK'),
                          ('AT+CMQTTUNSUB', 'ERROR'),
                          ('AT+CMQTTUNSUB?', 'ERROR'),
                          ('AT+CMQTTUNSUB=0,9', '> (ждет топик)'),
                          ],
        'AT+CMQTTREL': ['Release MQTT Client',
                        ('AT+CMQTTREL=?', '+CMQTTREL: (0-1)\nOK'),
                        ('AT+CMQTTREL', 'ERROR'),
                        ('AT+CMQTTREL?', 'OK'),
                        ('AT+CMQTTREL=0', 'OK'),
                        ],
    },
    # =========================================================================
    "---14=FTP_SERVICE": {
        'AT+CFTPSSTART': ['[DANGER]Start FTP Service',
                          ('AT+CFTPSSTART=?', '+CFTPSSTART: (1-n)\nOK'),# navia
                          ('AT+CFTPSSTART', 'OK'),# navia
                          ('AT+CFTPSSTART?', 'ERROR'),# navia
                          ('AT+CFTPSSTART=1', 'OK\n+CFTPSSTART: 0,1'),
                          ],
        'AT+CFTPSSTOP': ['Stop FTP Service',
                         ('AT+CFTPSSTOP=?', '+CFTPSSTOP: (1-15)\nOK'),
                         ('AT+CFTPSSTOP', 'ERROR'),
                         ('AT+CFTPSSTOP?', 'ERROR'),
                         ('AT+CFTPSSTOP=1', 'OK\n+CFTPSSTOP: 0,1'),
                         ],
        'AT+CFTPSLOGIN': ['Login to FTP Server',
                          ('AT+CFTPSLOGIN=?',
                           '+CFTPSLOGIN: "ADDRESS",(1-65535),"USERNAME","PASSWORD"[,(0-3)]\nOK'),
                          ('AT+CFTPSLOGIN', 'ERROR'),
                          ('AT+CFTPSLOGIN?', '+CFTPSLOGIN: 0\nOK'),
                          ('AT+CFTPSLOGIN="1.2.3.4",21,"user","pass",0', 'OK\n+CFTPSLOGIN: 0'),
                          ],
        'AT+CFTPSLOGOUT': ['Logout from FTP Server',
                           ('AT+CFTPSLOGOUT=?', 'OK'),
                           ('AT+CFTPSLOGOUT', 'ERROR'),
                           ('AT+CFTPSLOGOUT?', 'ERROR'),
                           ('AT+CFTPSLOGOUT', 'OK\n+CFTPSLOGOUT: 0'),
                           ],
        'AT+CFTPSLIST': ['List Directory',
                         ('AT+CFTPSLIST=?', 'OK'),
                         ('AT+CFTPSLIST', 'ERROR'),
                         ('AT+CFTPSLIST?', 'ERROR'),
                         ('AT+CFTPSLIST="/"', 'OK\n+CFTPSLIST: DATA,100\n...\n+CFTPSLIST: 0'),
                         ],
        'AT+CFTPSGETFILE': ['Download File from Server',
                            ('AT+CFTPSGETFILE=?', '+CFTPSGETFILE: "FILEPATH"[,(1-2)]\nOK'),
                            ('AT+CFTPSGETFILE', 'ERROR'),
                            ('AT+CFTPSGETFILE?', 'ERROR'),
                            ('AT+CFTPSGETFILE="test.txt",1', 'OK\n+CFTPSGETFILE: 0'),
                            ],
        'AT+CFTPSPUTFILE': ['Upload File to Server',
                            ('AT+CFTPSPUTFILE=?', '+CFTPSPUTFILE: "FILEPATH"[,(1-2)]\nOK'),
                            ('AT+CFTPSPUTFILE', 'ERROR'),
                            ('AT+CFTPSPUTFILE?', 'ERROR'),
                            ('AT+CFTPSPUTFILE="test.txt",1', 'OK\n+CFTPSPUTFILE: 0'),
                            ],
    },
    # =========================================================================
    "---20=WIFI(Только для ASR1803)": {
        'AT+CWMAP': ['Open/Close WIFI',
                    # navia
                     ('AT+CWMAP=?', 'ERROR'),
                     ('AT+CWMAP', 'ERROR'),
                     ('AT+CWMAP?', 'ERROR'),
                     ('AT+CWMAP=1', 'ERROR'),

                     # из доков
                     ('AT+CWMAP=?', '+CWMAP: (0-1)\nOK'),
                     ('AT+CWMAP', 'ERROR'),
                     ('AT+CWMAP?', '+CWMAP: 1\nOK'),
                     ('AT+CWMAP=0', 'OK'),
                     ],
        'AT+CWSSID': ['SSID setting',
                      # navia
                      ('AT+CWSSID=?', 'ERROR'),
                      ('AT+CWSSID', 'ERROR'),
                      ('AT+CWSSID?', 'ERROR'),

                      # из доков
                      ('AT+CWSSID=?', 'ERROR'),
                      ('AT+CWSSID', 'ERROR'),
                      ('AT+CWSSID?', '+CWSSID: Mrvl-uAP-X-C7FC\nOK'),
                      ('AT+CWSSID="MyWiFi"', 'OK'),
                      ],
        'AT+CWAUTH': ['Authentication setting',
                      # navia
                      ('AT+CWAUTH=?', 'ERROR'),
                      ('AT+CWAUTH', 'ERROR'),
                      ('AT+CWAUTH?', 'ERROR'),

                      # из доков
                      ('AT+CWAUTH=?', 'ERROR'),
                      ('AT+CWAUTH', 'ERROR'),
                      ('AT+CWAUTH?', '+CWAUTH: 5,4,"12345678"\nOK'),
                      ('AT+CWAUTH=5,4,"12345678"', 'OK'),
                      ],
        'AT+CWMACADDR': ['Get MAC address',
                         # navia
                         ('AT+CWMACADDR=?', 'ERROR'),
                         ('AT+CWMACADDR', 'ERROR'),
                         ('AT+CWMACADDR?', 'ERROR'),

                         # из доков
                         ('AT+CWMACADDR=?', '[<number>,<mac_addr>]\nOK'),
                         ('AT+CWMACADDR', 'ERROR'),
                         ('AT+CWMACADDR?', '0,00:0A:F5:88:88:8F\nOK'),
                         ],
        'AT+CWSTASCAN': ['Scan WIFI network',
                         ('AT+CWSTASCAN=?', '+CWSTASCAN: (0-1)\nOK'),
                         ('AT+CWSTASCAN', 'ERROR'),
                         ('AT+CWSTASCAN?', '+CWSTASCAN: 1\nOK'),
                         ('AT+CWSTASCAN=1', 'OK'),
                         ],
    },
    # =========================================================================
    "---21=BLUETOOTH": {
        'AT+BTPOWER': ['Open/Close BT Device = включение 3секунды до ответа OK!!!',
                       # navia
                       ('AT+BTPOWER=?', '+BTPOWER: (0-1)\nOK'),
                       ('AT+BTPOWER', 'ERROR'),
                       ('AT+BTPOWER?', '+BTPOWER: 0\nOK'),
                       ('AT+BTPOWER=1', 'OK'),
                       ('AT+BTPOWER?', '+BTPOWER: 1\nOK'),
                       ],
        'AT+BTHOST': ['Get/Set BT Device Name',
                      # navia
                      ('AT+BTHOST=?', 'OK'),
                      ('AT+BTHOST', 'ERROR'),
                      ('AT+BTHOST?', '+BTHOST: SIMOCM BT,14:00:20:9A:7D:DF\nOK'),
                      ('AT+BTHOST?', '+BTHOST: SIMCOM BT,11:22:23:33:33:80\nOK'),   # из доков

                      ('AT+BTHOST=SIMCOM_BT', 'OK'),
                      ],
        'AT+BTADDR': ['Get/Set BT Device Address',
                      # navia
                      ('AT+BTADDR=?', 'OK'),
                      ('AT+BTADDR', 'ERROR'),
                      ('AT+BTADDR?', '+BTADDR: 14:00:20:9A:7D:DF\nOK'),

                      ('AT+BTADDR=11:22:23:33:33:80', 'OK'),
                      ],
        'AT+BTSCAN': ['Scan BT Device',
                      # navia
                      ('AT+BTSCAN=?', '+BTSCAN: (0-1),(0-1),(6-48)\nOK'),
                      ('AT+BTSCAN=?', '+BTSCAN: (0-1),(0-1),(1-48)\nOK'), # из доков
                      ('AT+BTSCAN', 'ERROR'),
                      ('AT+BTSCAN?', 'ERROR'),      # почемуто не работает!!!
                      ('AT+BTSCAN=1,0,20', 'OK'),

                      ('AT+BTSCAN?', '+BTSCAN: 0,1,Mi Note 3,F4:F5:DB:C9:03:2C,178\nOK'),
                      ],
        'AT+BTPAIR': ['Pair With Other BT Device',
                      ('AT+BTPAIR=?', '+BTPAIR: (index)\nOK'),
                      ('AT+BTPAIR', 'ERROR'),
                      ('AT+BTPAIR?', 'ERROR'),
                      ('AT+BTPAIR=0,1', 'OK\n+BTPAIRING: 1,KK,04:8C:9A:D7:90:4C,466622'),
                      ],
        'AT+BTPAIRED': ['Get Paired BT Device',
                        # navia
                        ('AT+BTPAIRED=?', 'OK'),
                        ('AT+BTPAIRED', '\n'),  # ВООБШЕ НИЧЕГО НЕ ОТВЕЧАЕТ!!!!
                        ('AT+BTPAIRED?', 'OK'),

                        # дипсик
                        ('AT+BTPAIRED=?', 'ERROR'),
                        ('AT+BTPAIRED', 'ERROR'),
                        ('AT+BTPAIRED?', '+BTPAIRED: 1,KK,04:8C:9A:D7:90:4C\nOK'),
                        ],
        'AT+BTSPPSRV': ['Active/Deactive Local SPP Service',
                        ('AT+BTSPPSRV=?', '+BTSPPSRV: (0-1)\nOK'),
                        ('AT+BTSPPSRV', 'ERROR'),
                        ('AT+BTSPPSRV?', '+BTSPPSRV: 1\nOK'),
                        ('AT+BTSPPSRV=1', 'OK'),
                        ],
        'AT+BTSPPCONN': ['Establish/Release SPP Connection',
                         ('AT+BTSPPCONN=?', '+BTSPPCONN: (0-1)\nOK'),
                         ('AT+BTSPPCONN', 'ERROR'),
                         ('AT+BTSPPCONN?', '+BTSPPCONN: 1\nOK'),
                         ('AT+BTSPPCONN=1,1', 'OK\n+BTSPPCONN: 1,990,04:8C:9A:D7:90:4C'),
                         ],
        'AT+BTSPPSEND': ['SPP Send Data',
                         ('AT+BTSPPSEND=?', 'ERROR'),
                         ('AT+BTSPPSEND', 'ERROR'),
                         ('AT+BTSPPSEND?', 'ERROR'),
                         ('AT+BTSPPSEND="00310032"', 'OK\n+BTSPPSEND: 1'),
                         ],
    },
    # =========================================================================
    # =========================================================================
    # =========================================================================
    # =========================================================================
    # СЦЕНАРИИ РАБОТЫ
    "---check-1=GSM CHANNEL": [
        ("AT+CPIN?", ""),   # lambda r: "READY" in r)
        ("AT+CICCID", ""),   # lambda r: "+ICCID:" in r)

        ("Signal", "AT+CSQ", lambda r: int(r.split(",")[0].split(":")[1]) > 10),
        ("CS-reg", "AT+CREG?", lambda r: ",1" in r or ",5" in r),
        ("PS-reg", "AT+CGREG?", lambda r: ",1" in r or ",5" in r),
        ("LTE-reg", "AT+CEREG?", lambda r: ",1" in r or ",5" in r),
        ("APN", "AT+CGDCONT?", lambda r: "+CGDCONT: 1" in r),
        ("PDP act", "AT+CGACT?", lambda r: "+CGACT: 1,1" in r),
        ("IP", "AT+CGPADDR", lambda r: "0.0.0.0" not in r),
        ("DNS cfg", "AT+CDNSCFG?", lambda r: "Primary IPv4 DNS:" in r and "::" not in r.split("Secondary")[0]),
        ("DNS query", 'AT+CDNSGIP="www.google.com"', lambda r: "+CDNSGIP: 1," in r),
        ("Ping IP", 'AT+CPING="8.8.8.8",1,4,64,1000,10000,255',
         lambda r: "+CPING: 3,4,4,0" in r),
        ("Ping DNS", 'AT+CPING="www.google.com",1,4,64,1000,10000,255',
         lambda r: "+CPING: 3,4,4,0" in r),
    ]
}


# ======================================================================================================================
@pytest.mark.parametrize(
    argnames="group_name, cmds",
    argvalues=AT_GROUPS.items(),
    ids=AT_GROUPS.keys(),
)
def test__at_param__GROUPS(group_name, cmds, harvest, gsm_at__port):
    if group_name.startswith("-"):
        pytest.skip(f"skip group by startswith {group_name=}")
    harvest.at_cmds__explore(cmds=cmds, port=gsm_at__port)


# ======================================================================================================================
