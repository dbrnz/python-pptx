20.1.10.56 ST_ShapeType (Preset Shape Types)

This simple type specifies the preset shape geometry that is to be used for a shape. An enumeration of this simple type is used so that a custom geometry does not have to be specified but instead can be constructed automatically by the generating application. For each enumeration listed there is also the corresponding DrawingML code that would be used to construct this shape were it a custom geometry. Within the construction code for each of these preset shapes there are predefined guides that the generating application shall maintain for calculation purposes at all times. The necessary guides should have the following values. Formula syntax components are defined in the fmla attribute of the gd element (§20.1.9.11).

3/4 of a Circle ('3cd4') - Constant value of "16200000.0"
The units here are in 60,000ths of a degree. This is equivalent to 270 degrees.

3/8 of a Circle ('3cd8') - Constant value of "8100000.0"
The units here are in 60,000ths of a degree. This is equivalent to 135 degrees.

5/8 of a Circle ('5cd8') - Constant value of "13500000.0"
The units here are in 60,000ths of a degree. This is equivalent to 225 degrees.

7/8 of a Circle ('7cd8') - Constant value of "18900000.0"
The units here are in 60,000ths of a degree. This is equivalent to 315 degrees.

Shape Bottom Edge ('b') - Constant value of "h"
This is the bottom edge of the shape and since the top edge of the shape is considered the 0 point, the bottom edge is thus the shape height.

1/2 of a Circle ('cd2') - Constant value of "10800000.0"
The units here are in 60,000ths of a degree. This is equivalent to 180 degrees.

1/4 of a Circle ('cd4') - Constant value of "5400000.0"
The units here are in 60,000ths of a degree. This is equivalent to 90 degrees.

1/8 of a Circle ('cd8') - Constant value of "2700000.0"
The units here are in 60,000ths of a degree. This is equivalent to 45 degrees.

Shape Height ('h')
This is the variable height of the shape defined in the shape properties. This value is received from the shape transform listed within the <spPr> element.

Horizontal Center ('hc') - Calculated value of "*/ w 1.0 2.0"
This is the horizontal center of the shape which is just the width divided by 2.

1/2 of Shape Height ('hd2') - Calculated value of "*/ h 1.0 2.0"
This is 1/2 the shape height.

1/3 of Shape Height ('hd3') - Calculated value of "*/ h 1.0 3.0"
This is 1/3 the shape height.

1/4 of Shape Height ('hd4') - Calculated value of "*/ h 1.0 4.0"
This is 1/4 the shape height.

1/5 of Shape Height ('hd5') - Calculated value of "*/ h 1.0 5.0"
This is 1/5 the shape height.

1/6 of Shape Height ('hd6') - Calculated value of "*/ h 1.0 6.0"
This is 1/6 the shape height.

1/8 of Shape Height ('hd8') - Calculated value of "*/ h 1.0 8.0"
This is 1/8 the shape height.

Shape Left Edge ('l') - Constant value of "0"
This is the left edge of the shape and the left edge of the shape is considered the horizontal 0 point.

Longest Side of Shape ('ls') - Calculated value of "max w h"
This is the longest side of the shape. This value is either the width or the height depending on which is greater.

Shape Right Edge ('r') - Constant value of "w"
This is the right edge of the shape and since the left edge of the shape is considered the 0 point, the right edge is thus the shape width.

Shortest Side of Shape ('ss') - Calculated value of "min w h"
This is the shortest side of the shape. This value is either the width or the height depending on which is smaller.

1/2 Shortest Side of Shape ('ssd2') - Calculated value of "*/ ss 1.0 2.0"
This is 1/2 the shortest side of the shape.

1/4 Shortest Side of Shape ('ssd4') - Calculated value of "*/ ss 1.0 4.0"
This is 1/4 the shortest side of the shape.

1/6 Shortest Side of Shape ('ssd6') - Calculated value of "*/ ss 1.0 6.0"
This is 1/6 the shortest side of the shape.

1/8 Shortest Side of Shape ('ssd8') - Calculated value of "*/ ss 1.0 8.0"
This is 1/8 the shortest side of the shape.

1/16 Shortest Side of Shape ('ssd16') - Calculated value of "*/ ss 1.0 16.0"
This is 1/16 the shortest side of the shape.

1/32 Shortest Side of Shape ('ssd32') - Calculated value of "*/ ss 1.0 32.0"
This is 1/32 the shortest side of the shape.

Shape Top Edge ('t') - Constant value of "0"
This is the top edge of the shape and the top edge of the shape is considered the vertical 0 point.

Vertical Center of Shape ('vc') - Calculated value of "*/ h 1.0 2.0"
This is the vertical center of the shape which is just the height divided by 2.

Shape Width ('w')
This is the variable width of the shape defined in the shape properties. This value is received from the shape transform listed within the <spPr> element.

1/2 of Shape Width ('wd2') - Calculated value of "*/ w 1.0 2.0"
This is 1/2 the shape width.

1/3 of Shape Width ('wd3') - Calculated value of "*/ w 1.0 3.0"
This is 1/3 the shape width.

1/4 of Shape Width ('wd4') - Calculated value of "*/ w 1.0 4.0"
This is 1/4 the shape width.

1/5 of Shape Width ('wd5') - Calculated value of "*/ w 1.0 5.0"
This is 1/5 the shape width.

1/6 of Shape Width ('wd6') - Calculated value of "*/ w 1.0 6.0"
This is 1/6 the shape width.

1/8 of Shape Width ('wd8') - Calculated value of "*/ w 1.0 8.0"
This is 1/8 the shape width.

1/10 of Shape Width ('wd10') - Calculated value of "*/ w 1.0 10.0"
This is 1/10 the shape width.
