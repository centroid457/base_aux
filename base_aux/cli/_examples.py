from base_aux.cli.m1_cli_user import *

print()
print()
print()
print()
victim = CliUser()
victim.send("ping localhost", timeout=0.1)
print()
# victim.print_state()
"""
[CLI_SEND] [ping localhost]
....
==================================================
[#####################ERROR#####################]
self.counter=1
self.counter_in_list=0
self.last_cmd='ping localhost'
self.last_duration=1.041
self.last_finished=True
self.last_finished_success=False
self.last_retcode=None
--------------------------------------------------
self.last_stdout=
	|''
	|'Обмен пакетами с starichenko.corp.element-t.ru [::1] с 32 байтами данных:'
	|'Ответ от ::1: время<1мс '
	|'Ответ от ::1: время<1мс '
	|''
--------------------------------------------------
self.last_stderr=
--------------------------------------------------
self.last_exc_timeout=Exc_CliTimeout()
==================================================
"""

print()
print()
print()
print()
victim.send(["python --version", ("ping localhost", 0.1), ])
"""
[CLI_SEND] [python --version]
.
[CLI_SEND] [('ping localhost', 0.1)]
....
==================================================
[#####################ERROR#####################]
self.counter=3
self.counter_in_list=2
self.last_cmd='ping localhost'
self.last_duration=1.042
self.last_finished=True
self.last_finished_success=False
self.last_retcode=None
--------------------------------------------------
self.last_stdout=
	|''
	|'Обмен пакетами с starichenko.corp.element-t.ru [::1] с 32 байтами данных:'
	|'Ответ от ::1: время<1мс '
	|'Ответ от ::1: время<1мс '
	|''
--------------------------------------------------
self.last_stderr=
--------------------------------------------------
self.last_exc_timeout=Exc_CliTimeout()
==================================================
[ERROR] cmd_item=('ping localhost', 0.1) in full sequence cmd=['python --version', ('ping localhost', 0.1)]
"""