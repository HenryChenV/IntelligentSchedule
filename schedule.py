# !/usr/bin/env python
#  -*- coding: utf-8 -*-

import math
import time

R = 6378137
# 一天支付工资/元
courier_pay_one_day = 200
# 最大配送单数
max_courier_delivery_order = 7
# 骑手配送速度 m/s
courier_delivery_speed = 3
# 最大骑手数
max_courier_count = math.pow(10, 4)
# 最大餐厅数
max_rst_count = math.pow(10, 3)


def point_distance(lat1, lng1, lat2, lng2):
    lat_diff = (lat1 - lat2) / 2
    lng_diff = (lng1 - lng2) / 2
    return 2 * R * math.asin(math.sqrt(math.pow(math.sin(math.pi / 180 * lat_diff), 2) + math.cos(math.pi / 180 * lat1)
                                       * math.cos(math.pi / 180 * lat2) * math.pow(math.sin(math.pi / 180 * lng_diff),
                                                                                   2)))


class Courier(object):
    OPT_TYPE_DICT = {0: 'take', 1: 'delivery'}

    def __init__(self, courier_id, courier_lat, courier_lng):
        self.courier_id = courier_id
        self.courier_lat = courier_lat
        self.courier_lng = courier_lng
        self.opt_seq = 0
        self.opt_type = 'take'

    def increase_opt_seq(self):
        self.opt_seq += 1

    def switch_opt_status(self, opt_type):
        self.increase_opt_seq()
        self.opt_type = self.OPT_TYPE_DICT[opt_type]


class Rst(object):
    def __init__(self, rst_id, lng, lat):
        if not isinstance(rst_id, int) or not isinstance(lng, float) or not isinstance(lat, float):
            print("Check rst input parameter")
            return
        self.rst_id = rst_id
        self.lng = lng
        self.lat = lat


class Order(object):
    def __init__(self, order_id, rst_id, customer_lng, customer_lat, make_order_time, promise_at, created_at):
        if not isinstance(order_id, int) or not isinstance(rst_id, int) or not isinstance(customer_lat, float) \
                or not isinstance(customer_lng, float) or not isinstance(customer_lat, float) \
                or not isinstance(make_order_time, int) or not isinstance(promise_at, basestring) \
                or not isinstance(created_at, basestring):
            print("Check order input parameter")

            # 内部控制
            self.tick = time.time()

            # 订单信息
            self.order_id = order_id
            self.rst_id = rst_id
            self.customer_lng = customer_lng
            self.customer_lat = customer_lat
            self.make_order_time = make_order_time
            self.promise_at = promise_at
            self.created_at = created_at

            # 骑手信息
            # 骑手接单时间
            self.courier_activate_at = None
            # 骑手接单位置， 当决定雇佣一个新骑手送这单时候，这个点就是取餐位置---瞬移
            self.courier_info = None

    def overtime_compensate(self, cost_time):
        # 分钟
        overtime = math.ceil((cost_time - (self.promise_at - self.created_at)) / 60)

        if overtime <= 0:
            return 0

        # 元
        return overtime * math.log10(overtime + 1) + 5

    def dispatch_courier(self, courier_info):
        self.courier_activate_at = time.time()
        self.courier_info = courier_info

    def __courier_service_time(self):
        rst_info = Schedule.get_rst_info(self.order_id)
        if not rst_info:
            print("Can not cal service time because of can not find rst")
            return 0

        rst_info = Schedule.get_rst_info(self.rst_id)

        # 取餐时长
        # m / m/s = s
        take_time = point_distance(self.courier_info.lat, self.courier_info.lng, rst_info.lat,
                                   rst_info.lng) / courier_delivery_speed
        # 如果取餐时长小于出餐时长，则相当于骑手在餐馆等候出餐，取餐时间等于出餐时间
        if take_time < self.make_order_time:
            take_time = self.make_order_time

        # 送餐时长
        delivery_time = point_distance(rst_info.lat, rst_info.lng, self.customer_lat,
                                       self.customer_lng) / courier_delivery_speed

        return take_time + delivery_time


class Schedule(object):
    rst_map = dict()

    @classmethod
    def get_rst_info(cls, rst_id):
        return cls.rst_map.get(rst_id)


if __name__ == '__main__':
    print point_distance(100, 200, 88.999, 37)
