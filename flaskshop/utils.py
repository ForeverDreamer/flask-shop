# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""

import logging
from logging.handlers import RotatingFileHandler
from urllib.parse import urlencode

from flask import current_app, flash, request
from flask_sqlalchemy import get_debug_queries

from flaskshop.checkout.models import Cart
from flaskshop.constant import SiteDefaultSettings
from flaskshop.dashboard.models import Setting
from flaskshop.plugin.utils import template_hook
from flaskshop.public.models import MenuItem


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def log_slow_queries(app):
    formatter = logging.Formatter(
        "[%(asctime)s]{%(pathname)s:%(lineno)d}\n%(levelname)s - %(message)s"
    )
    handler = RotatingFileHandler(
        "slow_queries.log", maxBytes=10_000_000, backupCount=10
    )
    handler.setLevel(logging.WARN)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    @app.after_request
    def after_request(response):
        for query in get_debug_queries():
            if query.duration >= app.config["DATABASE_QUERY_TIMEOUT"]:
                app.logger.warn(
                    f"Context: {query.context}\n"
                    f"SLOW QUERY: {query.statement}\n"
                    f"Parameters: {query.parameters}\n"
                    f"Duration: {query.duration}"
                )
        return response


def jinja_global_varibles(app):
    """Register global varibles for jinja2"""

    @app.context_processor
    def inject_cart():
        current_user_cart = Cart.get_current_user_cart()
        return dict(current_user_cart=current_user_cart)

    @app.context_processor
    def inject_menus():
        top_menu = (
            MenuItem.query.filter(MenuItem.position == 1)
            .filter(MenuItem.parent_id == 0)
            .order_by(MenuItem.order)
            .all()
        )
        bottom_menu = (
            MenuItem.query.filter(MenuItem.position == 2)
            .filter(MenuItem.parent_id == 0)
            .order_by(MenuItem.order)
            .all()
        )
        return dict(top_menu=top_menu, bottom_menu=bottom_menu)

    @app.context_processor
    def inject_site_setting():
        settings = {}
        for key, value in SiteDefaultSettings.items():
            obj = Setting.query.filter_by(key=key).first()
            if not obj:
                obj = Setting.create(key=key, **value)
            settings[key] = obj
        return dict(settings=settings)

    def get_sort_by_url(field, descending=False):
        request_get = request.args.copy()
        if descending:
            request_get["sort_by"] = "-" + field
        else:
            request_get["sort_by"] = field
        return f"{request.path}?{urlencode(request_get)}"

    app.add_template_global(current_app, "current_app")
    app.add_template_global(get_sort_by_url, "get_sort_by_url")
    app.add_template_global(template_hook, "run_hook")


def jinja_global_filters(app):
    """Register global varibles for jinja2"""

    categories = {
        'Apparel': '服装',
        'Accessories': '配件',
        'Groceries': '杂货',
        'Coffees': '咖啡',
        'Candies': '糖果',
        'Books': '书籍',
        'Collections': '精选',
        'Summer collection': '夏季新品',
        'Winter sale': '冬季特卖',
        'Saleor': '在线商城',
        'About': '关于我们',
        'Style guide': '风格指南',
    }

    attrs = {
        'Color': '颜色',
        'Collar': '领口',
        'Brand': '品牌',
        'Size': '尺码',
        'Coffee Genre': '咖啡类型',
        'Box Size': '盒子大小',
        'Flavor': '口味',
        'Candy Box Size': '糖果盒子大小',
        'Author': '作者',
        'Publisher': '出版社',
        'Language': '语言',
        'Cover': '封面',
    }

    attr_values = {
        'Blue': '蓝色',
        'White': '白色',
        'Round': '圆领',
        'V-Neck': 'V领',
        'Polo': 'Polo领',
        'Saleor': '在线商城',
        'XS': 'XS',
        'S': 'S',
        'M': 'M',
        'L': 'L',
        'XL': 'XL',
        'XXL': 'XXL',
        'Arabica': '阿拉比卡',
        'Robusta': '罗布斯塔',
        '100g': '100g',
        '250g': '250g',
        '500g': '500g',
        '1kg': '1kg',
        'Sour': '酸',
        'Sweet': '甜',
        'John Doe': 'John Doe',
        'Milionare Pirate': 'Milionare Pirate',
        'Mirumee Press': '米鲁米出版社',
        'Saleor Publishing': '在线出版社',
        'English': '英语',
        'Pirate': '海盗',
        'Soft': '软封面',
        'Hard': '硬封面',
    }

    produtc_fields = {
        'title': '名称',
        'price': '价格',
    }

    @app.template_filter('category_zh')
    def category_zh(s):
        s = str(s)
        return categories.get(s, s)

    @app.template_filter('attr_zh')
    def attr_zh(s):
        s = str(s)
        return attrs.get(s, s)

    @app.template_filter('attr_value_zh')
    def attr_value_zh(s):
        s = str(s)
        return attr_values.get(s, s)

    @app.template_filter('produtc_field_zh')
    def produtc_field_zh(s):
        s = str(s)
        return produtc_fields.get(s, s)
