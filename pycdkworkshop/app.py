#!/usr/bin/env python3

import aws_cdk as cdk

from pycdkworkshop.pycdkworkshop_stack import PycdkworkshopStack


app = cdk.App()
PycdkworkshopStack(app, "pycdkworkshop")

app.synth()
