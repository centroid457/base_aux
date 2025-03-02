# =====================================================================================================================
NAME_IMPORT: str = "private_values"
KEYWORDS: list[str] = [
    "environs", "environment",
    "private",
    "rc", "ini", "csv"
                 "json"
]

DESCRIPTION_SHORT: str = "update values into class aux_attr from OsEnvironment or Ini/Json File"
DESCRIPTION_LONG: str = """
Designed to use private data like username/pwd kept secure in OsEnvironment or Ini/Json-File for your several home projects at ones.  
And not open it in public.  

**CAUTION:**  
in requirements for other projects use fixed version! because it might be refactored so you would get exception soon.
"""
FEATURES: list[str] = [
    # "feat1",
    # ["feat2", "block1", "block2"],

    ["load values to instance aux_attr from",
     "Environment",
     "IniFile",
     "JsonFile",
     "CsvFile",
     "direct text instead of file",
     "direct dict instead of file",
     ],

    ["attr access",
     "via any lettercase",
     "by instance attr",
     "like dict key on instance", ],

    ["work with dict", "apply", "update", "preupdate"],

    "update_dict as cumulative result - useful in case of settings result",
]


# =====================================================================================================================
