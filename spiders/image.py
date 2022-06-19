import scrapy
from items import ImageItem


class ImageSpider(scrapy.Spider):
    name = 'image'

    custom_settings = {
        'IMAGES_STORE': 'images',  # 图片保存路径
        'ITEM_PIPELINES': {
            'scrapy.pipelines.images.ImagesPipeline': 300,  # 图片管道
        },
    }

    start_urls = ['https://bbsweb.xyz/scrapy/img/']

    def parse(self, response, **kwargs):
        # 当前页面的图片列表
        items = response.xpath('//*[@id="__docusaurus"]/div[2]/div')
        # 获取列表内所有图片地址
        images = items.xpath('div/img/@src').extract()

        # 遍历图片并下载
        for image in images:
            yield ImageItem(image_urls=[response.urljoin(image)])
