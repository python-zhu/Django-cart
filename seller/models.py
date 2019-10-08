from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
#自玩，更改头像
class TouXiang(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return '<obj name{}>'.format(self.name)





#卖家模型类
class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)
    nickname=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    picture=models.ImageField() #头像
    def __str__(self):
        return '<obj name{}>'.format(self.name)
#商品类型模型类
class Goods_Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    def __str__(self):
        return '<obj name{}>'.format(self.name)

#商品模型类
class Goods(models.Model):
    goods_num=models.CharField(max_length=32)#编号
    goods_name=models.CharField(max_length=32)#名称
    goods_oprice=models.CharField(max_length=32)#原价
    goods_cprice=models.CharField(max_length=32)#现价
    goods_kucun=models.CharField(max_length=32)#库存
    goods_desc = models.CharField(max_length=100)#描述
    goods_detail=RichTextField()#详情
    #设置关系
    #类型和商品  一对多
    type = models.ForeignKey(to='Goods_Type', on_delete=models.CASCADE)
    #卖家和商品 一对多
    seller = models.ForeignKey(to='Seller', on_delete=models.CASCADE)
    #商品和图片一对多
    def __str__(self):
        return '<obj goods_name:{}>'.format(self.goods_name)
class GoodsImage(models.Model):
    image_address = models.CharField(max_length=64)
    goods = models.ForeignKey(to='Goods', on_delete=models.CASCADE)

    def __str__(self):
        return '<obj image_address:{}>'.format(self.image_address)
















