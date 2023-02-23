SOFTWARE CONTROL IN G-CODE

For User Interface Buttons:

Input box for increment movement (mm): allow values as precise as 0.1mm
(from this point forward, input referenced as 'Q')

Homing: 'G28 X Y\n'

Switch Mode to Relative Position: 'G91\n'
Up Button (must be in RELATIVE): 	'G0 YQ\n'
Down Button (must be in RELATIVE): 	'G0 Y-Q\n'
Left Button (must be in RELATIVE): 	'G0 X-Q\n'
Right Button (must be in RELATIVE): 	'G0 XQ\n'

Switch Mode to Absolute Position: 'G90\n'

To move to absolute position: 'G0 Xx Yx'

SURFACE LAYOUT

0,400	-----------------------	400,400
	|				|
	|				|
	|				|
	|				|
	|	  200,200		|
	|		`		|
	|				|
	|				|
	|				|
	|				|
0,0	-----------------------	400,0

