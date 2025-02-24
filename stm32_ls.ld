ENTRY(Reset_handler)

MEMORY
{
	FLASH(rx):ORIGIN =0x08000000,LENGTH =1024K
	SRAM(rwx):ORIGIN =0x20000000,LENGTH =128K
}

SECTIONS
{
	.text :
	{
		*(.isr_vector)
		*(.text)
		*(.rodata)
		_end_of_text = .;
	}> FLASH
	
	.data :
	{
		_start_of_data = .;
		*(.data)
		_end_of_data = .;
	}> SRAM AT> FLASH
	
	.bss :
	{
		_start_of_bss = .;
		*(.bss)
		_end_of_bss = .;
	}> SRAM
	
}
