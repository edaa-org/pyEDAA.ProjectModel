set_property PACKAGE_PIN  T10      [ get_ports NexysA7_GPIO_Seg7_Cathode_n[0] ]
set_property PACKAGE_PIN  R10      [ get_ports NexysA7_GPIO_Seg7_Cathode_n[1] ]
set_property PACKAGE_PIN  K16      [ get_ports NexysA7_GPIO_Seg7_Cathode_n[2] ]
set_property PACKAGE_PIN  K13      [ get_ports NexysA7_GPIO_Seg7_Cathode_n[3] ]
set_property PACKAGE_PIN  P15      [ get_ports NexysA7_GPIO_Seg7_Cathode_n[4] ]
set_property PACKAGE_PIN  T11      [ get_ports NexysA7_GPIO_Seg7_Cathode_n[5] ]
set_property PACKAGE_PIN  L18      [ get_ports NexysA7_GPIO_Seg7_Cathode_n[6] ]
set_property PACKAGE_PIN  H15      [ get_ports NexysA7_GPIO_Seg7_Cathode_n[7] ]
set_property IOSTANDARD   LVCMOS33 [ get_ports -regexp {NexysA7_GPIO_Seg7_Cathode_n\[\d+\]} ]  ; # set I/O standard
set_false_path                 -to [ get_ports -regexp {NexysA7_GPIO_Seg7_Cathode_n\[\d+\]} ]  ; # Ignore timings on async I/O pins

set_property PACKAGE_PIN  J17      [ get_ports NexysA7_GPIO_Seg7_Anode_n[0] ]
set_property PACKAGE_PIN  J18      [ get_ports NexysA7_GPIO_Seg7_Anode_n[1] ]
set_property PACKAGE_PIN  T9       [ get_ports NexysA7_GPIO_Seg7_Anode_n[2] ]
set_property PACKAGE_PIN  J14      [ get_ports NexysA7_GPIO_Seg7_Anode_n[3] ]
set_property PACKAGE_PIN  P14      [ get_ports NexysA7_GPIO_Seg7_Anode_n[4] ]
set_property PACKAGE_PIN  T14      [ get_ports NexysA7_GPIO_Seg7_Anode_n[5] ]
set_property PACKAGE_PIN  K2       [ get_ports NexysA7_GPIO_Seg7_Anode_n[6] ]
set_property PACKAGE_PIN  U13      [ get_ports NexysA7_GPIO_Seg7_Anode_n[7] ]
set_property IOSTANDARD   LVCMOS33 [ get_ports -regexp {NexysA7_GPIO_Seg7_Anode_n\[\d+\]} ]  ; # set I/O standard
set_false_path                 -to [ get_ports -regexp {NexysA7_GPIO_Seg7_Anode_n\[\d+\]} ]  ; # Ignore timings on async I/O pins
