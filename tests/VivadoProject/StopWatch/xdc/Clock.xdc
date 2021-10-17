set_property PACKAGE_PIN  E3       [ get_ports NexysA7_SystemClock ]
set_property IOSTANDARD   LVCMOS33 [ get_ports NexysA7_SystemClock ]                        ; # set I/O standard
create_clock -name PIN_SystemClock_100MHz -period 10.000 [ get_ports NexysA7_SystemClock ]  ; # specify a 100 MHz clock
