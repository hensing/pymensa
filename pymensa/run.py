#!/usr/bin/env python
activate_this = '/home/cg/.virtualenvs/pymensa/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import pymensa
CONF = pymensa.parse_config()
pymensa.send_xmpp(CONF)
