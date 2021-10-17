library IEEE;
use     IEEE.std_logic_1164.all;
use     IEEE.numeric_std.all;

use     work.Utilities.all;
use     work.StopWatch_pkg.all;


entity seg7_Display is
	generic (
		CLOCK_FREQ    : freq := 100 MHz;
		REFRESH_RATE  : time := 1000 us;
		DIGITS        : positive
	);
	port (
		Clock         : in  std_logic;
		
		DigitValues   : in  T_BCD_Vector(DIGITS - 1 downto 0);
		DotValues     : in  std_logic_vector(DIGITS - 1 downto 0) := (others => '0');
		
		Seg7_Segments : out std_logic_vector(7 downto 0);
		Seg7_Selects  : out std_logic_vector(DIGITS - 1 downto 0)
	);
end entity;


architecture rtl of seg7_Display is
	constant TIMEBASE_COUNTER_MAX : positive := TimingToCycles(REFRESH_RATE, CLOCK_FREQ); -- * ite(IS_SIMULATION, 1_000, 1));
	
	signal Timebase_Tick    : std_logic;
	signal Digit_Select     : unsigned(log2(DIGITS) - 1 downto 0);
	
	signal Digit            : T_BCD;
	signal Dot              : std_logic;
begin
	-- refresh rate
	cnt1khZ: entity work.Counter
		generic map (
			MODULO => TIMEBASE_COUNTER_MAX
		)
		port map (
			Clock      => Clock,
			Reset      => '0',
			Enable     => '1',
			Value      => open,
			WrapAround => Timebase_Tick
		);
	
	-- counter to select digits (time multiplexing)
	cntDigitSelect: entity work.Counter
		generic map (
			MODULO => DIGITS,
			BITS   => Digit_Select'length
		)
		port map (
			Clock      => Clock,
			Reset      => '0',
			Enable     => Timebase_Tick,
			Value      => Digit_Select,
			WrapAround => open
		);
	
	-- multiplexer
	Digit <= DigitValues(to_index(Digit_Select, DigitValues'high));
	Dot   <= DotValues(to_index(Digit_Select, DotValues'high));
	
	-- 7-segment encoder
	enc: entity work.seg7_Encoder
		port map (
			BCDValue  => Digit,
			Dot       => Dot,
			
			Seg7Code  => Seg7_Segments
		);
	
	Seg7_Selects <= bin2onehot(Digit_Select, DIGITS);
end architecture;
