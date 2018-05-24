# (c) Copyright 2008-today Marcel van der Boom. All Rights Reserved.
#
# Meta information about the signs module
{
    "name"       : "Signs",
    "version"    : "2.0",
    "author"     : "HSD",
    "category"   : "Generic",
    "website"    : "https://www.hsdev.com",
    "url"        : "https://www.hsdev.com",
    'summary'    : "Signs / Images / Labels related to legislation",
    'description': """
Electronic signs, to be linked to other objects
===============================================
Create a model for electronic signs to be attached to other objects.

Typical usage:
--------------
* legislative labeling products
* safety and warnings signs for substances
* trafic signs for planning

Signs can be linked to other objects. A link between products and signs
is included in this modules as well as the standard safety signs for GHS/REACH.

Envisioned functionality:
-------------------------
* dynamic image generation (resize, black/white for labelling etc.)
* image manipulation depending on object linkage
* proper linking to legislative reference documents (link to what?)


    """,
    "depends"    : [
        "base","product","stock",
        "web_tree_image"
    ],
    "data" : [
        "views/sign.xml",
        "views/sign_type.xml",
        "views/product.xml",
        "security/ir.model.access.csv",
        "data/sign.type.csv",
        "data/sign.sign-wms.csv",
        "data/sign.sign-ghs.csv"
    ],
}
