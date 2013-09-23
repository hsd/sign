# (c) Copyright 2008-today Marcel van der Boom. All Rights Reserved.
#
# Meta information about the signs module
{
    "name"       : "Signs",
    "version"    : "1.0",
    "author"     : "HSD",
    "category"   : "Generic",
    "website"    : "http://www.hsdev.com",
    "url"        : "http://www.hsdev.com",
    "sequence"   : 2,
    'description': """
Electronic signs, to be linked to other objects
===============================================
Create a model for electronic signs to be attached to other objects.

Typical usage:
--------------
* legislative labeling products
* safety and warnings signs for substances
* trafic signs for planning

Envisioned functionality:
-------------------------
* dynamic image generation
* image manipulation depending on object linkage
* proper linking to legislative reference documents

All relevant documentation is included in the doc directory of this module.
    """,
    "depends"    : ["base","web", "product","stock"],
    "init_xml"   : [],
    "update_xml" : [
        "sign_view.xml",
        "security/ir.model.access.csv",
        "data/sign.category.csv",
        "data/sign.sign-wms.csv",
        "data/sign.sign-ghs.csv"
    ],
    "images" : [],
    "qweb" : [],
    "js" : [
        'static/src/js/view_list.js'
    ],
    "css" : [],
    "active"     : False,
    "installable": True
}
