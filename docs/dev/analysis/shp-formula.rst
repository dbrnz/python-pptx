Shape Guide Formula
===================

Specifies the formula that is used to calculate the value for a guide. Each formula has a certain number of arguments and a specific set of operations to perform on these arguments in order to generate a value for a guide. There are a total of 17 different formulas available. These are shown below with the usage for each defined.

::

    ('*/') - Multiply Divide Formula
    Arguments: 3 (fmla="*/ x y z")
    Usage: "*/ x y z" = ((x * y) / z) = value of this guide

    ('+-') - Add Subtract Formula
    Arguments: 3 (fmla="+- x y z")
    Usage: "+- x y z" = ((x + y) - z) = value of this guide

    ('+/') - Add Divide Formula
    Arguments: 3 (fmla="+/ x y z")
    Usage: "+/ x y z" = ((x + y) / z) = value of this guide

    ('?:') - If Else Formula
    Arguments: 3 (fmla="?: x y z")
    Usage: "?: x y z" = if (x > 0), then y = value of this guide, else z = value of this guide

    ('abs') - Absolute Value Formula
    Arguments: 1 (fmla="abs x")
    Usage: "abs x" = if (x < 0), then (-1) * x = value of this guide else x = value of this guide

    ('at2') - ArcTan Formula
    Arguments: 2 (fmla="at2 x y")
    Usage: "at2 x y" = arctan(y / x) = value of this guide

    ('cat2') - Cosine ArcTan Formula
    Arguments: 3 (fmla="cat2 x y z")
    Usage: "cat2 x y z" = (x*(cos(arctan(z / y))) = value of this guide

    ('cos') - Cosine Formula
    Arguments: 2 (fmla="cos x y")
    Usage: "cos x y" = (x * cos( y )) = value of this guide

    ('max') - Maximum Value Formula
    Arguments: 2 (fmla="max x y")
    Usage: "max x y" = if (x > y), then x = value of this guide else y = value of this guide

    ('min') - Minimum Value Formula
    Arguments: 2 (fmla="min x y")
    Usage: "min x y" = if (x < y), then x = value of this guide else y = value of this guide

    ('mod') - Modulo Formula
    Arguments: 3 (fmla="mod x y z")
    Usage: "mod x y z" = sqrt(x^2 + b^2 + c^2) = value of this guide   ## ERROR...

    ('pin') - Pin To Formula
    Arguments: 3 (fmla="pin x y z")
    Usage: "pin x y z" = if (y < x), then x = value of this guide else if (y > z), then z = value of this guide
    else y = value of this guide

    ('sat2') - Sine ArcTan Formula
    Arguments: 3 (fmla="sat2 x y z")
    Usage: "sat2 x y z" = (x*sin(arctan(z / y))) = value of this guide

    ('sin') - Sine Formula
    Arguments: 2 (fmla="sin x y")
    Usage: "sin x y" = (x * sin( y )) = value of this guide

    ('sqrt') - Square Root Formula
    Arguments: 1 (fmla="sqrt x")
    Usage: "sqrt x" = sqrt(x) = value of this guide

    ('tan') - Tangent Formula
    Arguments: 2 (fmla="tan x y")
    Usage: "tan x y" = (x * tan( y )) = value of this guide

    ('val') - Literal Value Formula
    Arguments: 1 (fmla="val x")
    Usage: "val x" = x = value of this guide


[Note: Guides that have a literal value formula specified via fmla="val x" above should only be used within the avLst as an adjust value for the shape. This however is not strictly enforced. end note]


Shape Guide Name
================

Specifies the name that is used to reference to this guide. This name can be used just as a variable would within an equation. That is this name can be substituted for literal values within other guides or the specification of the shape path.
