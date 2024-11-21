

def parse(self, response):
   
    property_urls = response.xpath('//a[@class="listing-link"]/@href').getall()
    for url in property_urls:
        yield response.follow(url, self.parse_property)
    
  
    next_page = response.xpath('//a[@title="Next"]/@href').get()
    if next_page:
        yield response.follow(next_page, self.parse)


def parse_property(self, response):
    item = {
        'property_id': response.xpath('//div[@class="property-id"]/text()').get(),
        'property_url': response.url,
        'purpose': response.xpath('//span[@class="purpose"]/text()').get(),
        'type': response.xpath('//span[@class="property-type"]/text()').get(),
        'added_on': response.xpath('//span[@class="date-added"]/text()').get(),
        'furnishing': response.xpath('//span[@class="furnishing"]/text()').get(),
        'price': {
            "currency": "AED",
            "amount": response.xpath('//span[@class="price"]/text()').get()
        },
        'location': response.xpath('//div[@class="location"]/text()').get(),
        'bed_bath_size': {
            'bedrooms': response.xpath('//span[@class="bedrooms"]/text()').get(),
            'bathrooms': response.xpath('//span[@class="bathrooms"]/text()').get(),
            'size': response.xpath('//span[@class="size"]/text()').get()
        },
        'permit_number': response.xpath('//div[@class="permit-number"]/text()').get(),
        'agent_name': response.xpath('//span[@class="agent-name"]/text()').get(),
        'primary_image_url': response.xpath('//img[@class="primary-image"]/@src').get(),
        'breadcrumbs': " > ".join(response.xpath('//ul[@class="breadcrumbs"]/li/a/text()').getall()),
        'amenities': response.xpath('//ul[@class="amenities"]/li/text()').getall(),
        'description': response.xpath('//div[@class="description"]/text()').get(),
        'property_image_urls': response.xpath('//div[@class="property-images"]/img/@src').getall()
    }
    yield item


# In settings.py
FEEDS = {
    'output/bayut_data.json': {'format': 'json', 'overwrite': True},
    'output/bayut_data.csv': {'format': 'csv', 'overwrite': True},
}
