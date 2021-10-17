library IEEE;
use     IEEE.std_logic_1164.all;
use     IEEE.numeric_std.all;
use     IEEE.math_real.all;

package Utilities is
	type freq is range integer'low to integer'high units
		Hz;
		kHz = 1000 Hz;
		MHz = 1000 kHz;
		GHz = 1000 MHz;
		THz = 1000 GHz;
	end units;

	-- deferred constant
	constant IS_SIMULATION : boolean;
	
	function ite(condition : boolean; ThenValue : time; ElseValue : time) return time;
	
	function log2(Value : positive) return positive;
	
	function bin2onehot(binary : std_logic_vector; bits : natural := 0) return std_logic_vector;
	function bin2onehot(binary : unsigned;         bits : natural := 0) return std_logic_vector;
	
	function to_index(value : unsigned; max : positive) return natural;
	function to_index(value : natural;  max : positive) return natural;
	
	function TimingToCycles(Timing : time; Clock_Period : time) return natural;
	function TimingToCycles(Timing : time; Clock_Frequency: freq) return natural;
end package;


package body Utilities is
	function simulation return boolean is
		variable result : boolean := FALSE;
	begin
		-- synthesis translate_off
		result := TRUE;
		-- synthesis translate_on
		return result;
	end function;

	-- deferred constant initialization
	constant IS_SIMULATION : boolean := simulation;
	
	function ite(condition : boolean; ThenValue : time; ElseValue : time) return time is
	begin
		if condition then
			return ThenValue;
		else
			return ElseValue;
		end if;
	end function;
	
	function log2(Value : positive) return positive is
		variable twosPower : natural := 1;
		variable result    : natural := 0;
	begin
		while (twosPower < Value) loop
			twosPower := twosPower * 2;
			result    := result + 1;
		end loop;
		return result;
	end function;
	
	function bin2onehot(binary : std_logic_vector; bits : natural := 0) return std_logic_vector is
	begin
		return bin2onehot(unsigned(binary), bits);
	end function;
	
	function bin2onehot(binary : unsigned; bits : natural := 0) return std_logic_vector is
		variable result : std_logic_vector(2**binary'length - 1 downto 0) := (others => '0');
	begin
		result(to_integer(binary)) := '1';
		
		if (bits = 0) then
			return result;
		else
			return result(bits - 1 downto 0);
		end if;
	end function;
	
	function to_index(value : unsigned; max : positive) return natural is
	begin
		return to_index(to_integer(value), max);
	end function;
	
	function to_index(value : natural; max : positive) return natural is
	begin
		if (value <= max) then
			return value;
		else
			return max;
		end if;
		-- return minimum(value, max);
	end function;
	
	function to_time(f : freq) return time is
		function div(a : freq; b : freq) return real is
		begin
			return real(a / 1 Hz) / real(b / 1 Hz);
		end function;
	begin
		return div(1000 MHz, f) * 1 ns;
	end function;
	
	function TimingToCycles(Timing : time; Clock_Period : time) return natural is
		function div(a : time; b : time) return real is
		begin
			return real(a / 1 fs) / real(b / 1 fs);
		end function;
	begin
		return natural(ceil(div(Timing, Clock_Period)));
	end;

	function TimingToCycles(Timing : time; Clock_Frequency : freq) return natural is
	begin
		return TimingToCycles(Timing, to_time(Clock_Frequency));
	end function;
end package body;
