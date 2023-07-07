library IEEE;
use     IEEE.std_logic_1164.all;

library libCommon;
use     libCommon.P2.all;

entity A2 is
	port (
		signal Clock : in std_logic
	);
end entity;

architecture rtl of A2 is

begin
  a : entity work.A1
    port map (
			Clock => Clock
    );
end architecture;
