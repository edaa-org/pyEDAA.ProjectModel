set_property PACKAGE_PIN  M18      [ get_ports NexysA7_GPIO_Button[0] ]
set_property IOSTANDARD   LVCMOS33 [ get_ports -regexp {NexysA7_GPIO_Button\[\d+\]} ]  ; # set I/O standard
set_false_path               -from [ get_ports -regexp {NexysA7_GPIO_Button\[\d+\]} ]  ; # Ignore timings on async I/O pins
