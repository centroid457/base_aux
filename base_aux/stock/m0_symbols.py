# =====================================================================================================================
class Symbols:
    # FINAM COMMON AVAILABLE
    # see https://docs.comon.ru/general-information/schedule-and-financial-instruments/

    SYMBOLS__SORTED_TRADED_VOLUME_CURRENCY: set[str] = {
        # from SYMBOLS__RUS_FINAM!!!!
        # + https://www.moex.com/ru/marketdata/?g=4#/mode=groups&group=4&collection=3&boardgroup=57&data_type=current&category=main

        # START
        'GAZP', 'SBER', 'LKOH', 'PLZL',

        # 1 MRD
        'MGNT', 'NVTK', 'YNDX', 'VTBR', 'GMKN', 'SNGS',

        # 500 MLN
        'ROSN',
        'VKCO',
        'CHMF',

        # 400 MLN
        # 'TRUR',     # БПИФ ТинькофВечныйПортфель
        'SIBN', 'NLMK', 'ALRS', 'OZON', 'TCSG',

        # 300 MLN
        'PHOR', 'SBERP',
        # 'ORUP',     # ПАО ОР ГРУПП
        # 'KMAZ',
        # 'TGLD',     # БПИФ ТинькофЗолото
        'MOEX', 'SNGSP', 'RUAL', 'SGZH', 'FEES', 'CBOM', 'MTSS',
        "POLY",     # не попал изза иностранного названия!!!

        # 200 MLN
        'TATN', 'MAGN', 'MTLR', 'FIVE', 'AFLT', 'AFKS', 'IRAO', 'ENPG', 'VRSB', 'ABRD',
        # 'SBRB'      # СберРублевыеКорпОблигации

        # 100 MLN
    }

    SYMBOLS__BLUE: set[str] = {
        "SBER", "SBERP", "VTBR",
        "LKOH", "NVTK", "GAZP", "ROSN", "TATN", "SNGS", "SNGSP",
        "CHMF", "GMKN", "ALRS",
        "MGNT", "FIVE",
        "YNDX", "MTSS",
    }
    SYMBOLS__over100mln: set[str] = {
        *SYMBOLS__BLUE,
        "MOEX",
        "POLY", "MAGN", "MTLR", "NLMK", "PLZL", "RASP", "RUAL",
        "AKRN",
        "AFKS", "IRAO",
        "AFLT",
        "PIKK",
        "HYDR",
        "PHOR",
    }
    SYMBOLS__ALL: set[str] = {
        *SYMBOLS__over100mln
    }

    SYMBOLS__RUS_FINAM: set[str] = [
        'ABRD', 'AFKS', 'AFLT', 'AGRO', 'AKMB', 'AKME', 'AKRN', 'ALRS', 'APTK', 'AQUA', 'ARSA', 'ASSB', 'AVAN',
        'BANE', 'BANEP', 'BCSB', 'BELU', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP',
        'CBOM', 'CHGZ', 'CHKZ', 'CHMF', 'CHMK', 'CNTL', 'CNTLP',
        'DASB', 'DIOD', 'DIVD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP',
        'EELT', 'ELTZ', 'ENPG', 'ENRU', 'ESGR', 'ETLN',
        'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT', 'FMUS',
        'GAZA', 'GAZAP', 'GAZC', 'GAZP', 'GAZS', 'GAZT', 'GCHE', 'GEMA', 'GLTR', 'GMKN', 'GPBM', 'GPBS', 'GRNT', 'GTRK',
        'HHRU', 'HIMCP', 'HYDR',
        'IDVP', 'IGST', 'IGSTP', 'INGR', 'IRAO', 'IRKT', 'ISKJ',
        'JNOS', 'JNOSP',
        'KAZT', 'KAZTP', 'KBSB', 'KCHE', 'KCHEP', 'KGKC', 'KGKCP', 'KLSB', 'KMAZ', 'KMEZ', 'KMTZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKOP', 'KROT',
              'KROTP', 'KRSB', 'KRSBP', 'KTSB', 'KTSBP', 'KUBE', 'KUZB', 'KZOS', 'KZOSP',
        'LIFE', 'LKOH', 'LNZL', 'LNZLP', 'LPSB', 'LSNG', 'LSNGP', 'LSRG', 'LVHK', 'LENT',
        'MAGE', 'MAGEP', 'MAGN', 'MDMG', 'MERF', 'MFGS', 'MFGSP', 'MGNT', 'MGTS', 'MGTSP', 'MISB', 'MISBP', 'MOEX', 'MRKC', 'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV',
              'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS', 'MSTT', 'MTEK', 'MTLR', 'MTLRP', 'MTSS', 'MVID',
        'NAUK', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB', 'NNSBP', 'NSVZ', 'NVTK',
        'ODVA', 'OGKB', 'OKEY', 'OMZZP', 'OZON',
        'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB', 'PMSBP', 'PRFN', 'PRMB', 'POSI',
        'RASP', 'RBCM', 'RCMX', 'RDRB', 'RGSS', 'RKKE', 'RNFT', 'ROLO', 'ROSB', 'ROSN', 'ROST', 'RSTI', 'RSTIP', 'RTGZ', 'RTKM', 'RTKMP',
              'RTSB', 'RTSBP', 'RUAL', 'RUGR', 'RUSI', 'RZSB', 'RENI',
        'SAGO', 'SAGOP', 'SARE', 'SAREP', 'SBER', 'SBERP', 'SBGB', 'SBMX', 'SBRB', 'SBRI', 'SELG', 'SFIN', 'SIBN', 'SLEN', 'SMLT', 'SNGS', 'SNGSP', 'STSB', 'STSBP',
              'SUGB', 'SVAV', 'SVET',
        'TASB', 'TASBP', 'TATN', 'TATNP', 'TCSG', 'TEUR', 'TGKA', 'TGKB', 'TGKBP', 'TGKN',
              'TGLD', 'TMOS', 'TNSE', 'TORS', 'TORSP', 'TRMK', 'TRNFP', 'TRUR', 'TSPX', 'TTLK', 'TUSD', 'TUZA',
        'UCSS', 'UKUZ', 'UNAC', 'UNKL', 'UPRO', 'URKZ', 'USBN', 'UTAR', 'UWGN',
        'VGSB', 'VGSBP', 'VJGZ', 'VJGZP', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP', 'VTBR',
        'WTCM', 'WTCMP', 'WUSH',
        'YAKG', 'YKEN', 'YKENP', 'YRSB', 'YRSBP',
        'ZILL', 'ZVEZ',

        'SGZH', 'GEMC', 'FMRU', 'VKCO', 'OBLG', 'LQDT', 'GOLD', 'EQMX', 'SPBE',
        'RCUS', 'SBGD', 'ORUP', 'SFTL']   # count = 275


# =====================================================================================================================
