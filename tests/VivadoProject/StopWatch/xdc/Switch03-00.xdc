set_property PACKAGE_PIN  J15      [ get_ports NexysA7_GPIO_Switch[0] ]
set_property PACKAGE_PIN  L16      [ get_ports NexysA7_GPIO_Switch[1] ]
set_property PACKAGE_PIN  M13      [ get_ports NexysA7_GPIO_Switch[2] ]
set_property PACKAGE_PIN  R15      [ get_ports NexysA7_GPIO_Switch[3] ]
set_property IOSTANDARD   LVCMOS33 [ get_ports -regexp {NexysA7_GPIO_Switch\[\d+\]} ]  ; # set I/O standard
set_false_path               -from [ get_ports -regexp {NexysA7_GPIO_Switch\[\d+\]} ]  ; # Ignore timings on async I/O pins
