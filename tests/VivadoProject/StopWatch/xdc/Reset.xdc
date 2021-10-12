set_property PACKAGE_PIN  C12      [ get_ports NexysA7_GPIO_Button_Reset_n ]
set_property IOSTANDARD   LVCMOS33 [ get_ports NexysA7_GPIO_Button_Reset_n ]  ; # set I/O standard
set_false_path               -from [ get_ports NexysA7_GPIO_Button_Reset_n ]  ; # Ignore timings on async I/O pins
