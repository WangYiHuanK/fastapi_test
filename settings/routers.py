# -*- coding: utf-8 -*-
# from apps.advertiser.views import AdvertiserRouter
from settings.base import configs
from fastapi import FastAPI


def router_init(app: FastAPI):
    from apps.user.views import StudentRouter, ClassroomRouter

    # 注册路由
    # 财务管理
    app.include_router(StudentRouter, prefix=f'/student')
    app.include_router(ClassroomRouter, prefix=f'/classroom')

