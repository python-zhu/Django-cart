from django.db import models

# Create your models here.
class Buyer(models.Model):
    name=models.CharField(max_length=32)#用户名
    nickname=models.CharField(max_length=64)#昵称
    password = models.CharField(max_length=64)#密码
    def __str__(self):
        return '<obj name:{}>'.format(self.name)

# 用户地址
class Address(models.Model):
    receiver = models.CharField(max_length=32)  # 收货人
    phone = models.CharField(max_length=32)  # 电话
    address = models.CharField(max_length=128)  # 地址
    # 用户和地址 一对多 关系
    buyer = models.ForeignKey(to='Buyer', on_delete=models.CASCADE)

    def __str__(self):
        return "<obj receiver:{}>".format(self.receiver)
# 购物车模型类
class BuyerCar(models.Model):
    goods_id = models.IntegerField()  # 商品id
    goods_name = models.CharField(max_length=32)  # 商品名称
    goods_picture = models.CharField(max_length=64)  # 商品缩略图路径
    goods_price = models.IntegerField()  # 商品单价
    goods_num = models.IntegerField()  # 商品数量
    # 商品小计 不需要写，可以使用 单价* 数量来获取
    # 买家和购物车的商品是一个一对多的关系
    buyer = models.ForeignKey(to='Buyer', on_delete=models.CASCADE)

# 订单表
class Order(models.Model):
    order_num = models.CharField(max_length=64)  # 订单号 日期+随机数
    order_time = models.DateTimeField()  # 订单日期
    order_status = models.CharField(max_length=32)  # 订单状态
    order_total = models.IntegerField()  # 商品总价
    # 设置关系
    buyer = models.ForeignKey(to='Buyer', on_delete=models.CASCADE)
    address = models.ForeignKey(to='Address', on_delete=models.CASCADE)


# 订单商品详情表
class OrderGoods(models.Model):
    goods_id = models.IntegerField()  # 商品id
    goods_name = models.CharField(max_length=32)  # 商品名称
    goods_picture = models.CharField(max_length=64)  # 商品缩略图
    goods_price = models.IntegerField()  # 商品单价
    goods_num = models.IntegerField()  # 商品数量
    # 设置关系
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE)


# 邮箱模型类
class EmailValid(models.Model):
    email_name = models.CharField(max_length=32)  # 邮箱账号，用来发送验证码，和注册使用
    value = models.CharField(max_length=32)  # 保存验证码
    time = models.DateTimeField()  # 时间戳 用来判断时间