from django.db import models

class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    # 基表的声明  不会在数据库为其创建对应的表
    class Meta:
        abstract = True


class Book(BaseModel):
    """boo_name price pic authors publish is_delete create_time status"""
    book_name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pic = models.ImageField(upload_to="img", default="img/1.jpg")
    publish = models.ForeignKey(
        to="Press",  # 关联的表
        on_delete=models.CASCADE,  # 级联删除
        db_constraint=False,  # 删除后对应字段可以为空
        related_name="books")  # 反向查询的名称
    authors = models.ManyToManyField(to="Author", db_constraint=False, related_name="books")

    # 自定义字段  可以再序列化器中指定此字段是否显示
    # def example(self):
    #     return "expmple"

    # 自定义返回出版社的名字
    @property
    def publish_name(self):
        return self.publish.press_name

    # 自定义作者查询
    @property
    def author_list(self):
        return self.authors.values("author_name", "age", "detail__phone")

    class Meta:
        db_table = "bz_book"
        verbose_name = "图书"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name


class Press(BaseModel):
    press_name = models.CharField(max_length=128)
    pic = models.ImageField(upload_to="img", default="img/1.jpg")
    address = models.CharField(max_length=256)

    class Meta:
        db_table = "bz_press"
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name


class Author(BaseModel):
    author_name = models.CharField(max_length=128)
    age = models.IntegerField()

    class Meta:
        db_table = "bz_author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name


class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)
    author = models.OneToOneField(to="Author", on_delete=models.CASCADE, related_name="detail")

    class Meta:
        db_table = "bz_author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s的详情" % self.author.author_name

