import re
import scrapy


class Top250Spider(scrapy.Spider):
    name = 'top250'

    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response, **kwargs):
        # 当前页面的所有电影
        items = response.xpath('//div[@id="content"]/div/div/ol/li')

        for item in items:
            content = item.xpath('div/div[2]/div[2]/p[1]').get()
            result = re.findall(r'导演: (.*?) .*?\s+(\d+).*?\xa0/\xa0(.*?)\xa0/\xa0(.*?)\n', content)[0]
            yield {
                'name': item.xpath('div/div/div/a/span/text()').get(),  # 电影名称
                'rate': item.xpath('div/div[2]/div[2]/div/span[2]/text()').get(),  # 评分
                'rate_count': re.findall(r'\d+', item.xpath('div/div[2]/div[2]/div/span[4]/text()').get())[0],  # 评分人数
                'quote': item.xpath('div/div[2]/div[2]/p[2]/span/text()').get(),  # 短评
                'director': result[0],  # 导演
                'year': result[1],  # 时间
                'region': result[2],  # 地区
                'tag': result[3],  # 标签
            }

        next_page = response.xpath('//div[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').get()
        if next_page:
            yield response.follow(next_page)
