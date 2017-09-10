#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"

import redis
redis_cli = redis.StrictRedis()
redis_cli.incr("jobbole_count")