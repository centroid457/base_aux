# ===================================================================
from base_aux.privates.m1_loader1_env import *
from base_aux.privates.m1_loader3_ini import *
from base_aux.privates.m1_loader4_json import *
from base_aux.privates.m1_loader5_auto import *
import pathlib


# ===================================================================
# by instance attr
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data.NAME
        name = self.data.NamE     # case insensitive

# like dict key on instance
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}


class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data["NAME"]
        name = self.data["NamE"]   # case insensitive

# ===================================================================
### use annotations for your param names (best practice!)
# when instantiating if it will not get loaded these exact params from your private sources - RAISE!  
# but you could not use it and however keep access to all existed params in used section!
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

class MyPrivateJson(PrivateJson):
    NAME: str
    PWD: str

name = MyPrivateJson().NAME


# ===================================================================
# in example above you could simply use existed classes
name = PrivateAuthJson().NAME


# ===================================================================
### 1. Env

class Cls:
   user = PrivateEnv["NAME"]
   user = PrivateEnv.NAME


# ===================================================================
### 2. IniFile
# Use different sections
class Cls:
   user = PrivateIni(_section="CustomSection").NAME


# ===================================================================
# Change full settings
class CustomIniValues(PrivateIni):
   DIRPATH = "new/path/"
   DIRPATH = pathlib.Path("new/path/")
   FILENAME = "my.ini"
   SECTION = "CustomSection"

class Cls:
   user = CustomIniValues.NAME

# ===================================================================
# Without creating new class
class Cls:
   pv1 = PrivateIni(_filename="otherFilename").pv1


# ===================================================================
### 3. JsonFile
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}
class MyPrivateJson(PrivateJson):
    SECTION = "AUTH"
    NAME: str
    PWD: str

class Cls:
    data = MyPrivateJson()
    def connect(self):
        name = self.data.NAME

# ===================================================================
# use already created templates (PrivateAuthJson/PrivateTgBotAddressJson) for standard attributes
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data.NAME

# ===================================================================
### 4. Auto  
# you can use universal class  
# it will trying get all your annotated params from one source of Json/Ini/Env (in exact order)  
# in this case you cant use FileName and must use annotations!

# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

class MyPrivate(PrivateAuto):
    SECTION = "AUTH"
    NAME: str
    PWD: str

name = MyPrivate().NAME

# ===================================================================
