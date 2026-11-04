"""Old industry slug -> current slug (pages were renamed to the client's SEO list). Import in any tool that builds an industries-*.html path from the old short slug."""
NEW = {'construction': 'construction-and-infrastructure', 'renewable-energy': 'renewable-energy-and-power', 'mining': 'mining-and-minerals',
       'manufacturing': 'industrial-manufacturing', 'chemicals': 'chemicals-and-dangerous-goods', 'data-centers': 'data-centers', 'marine': 'marine-and-offshore',
       'aviation': 'aviation-and-aerospace', 'healthcare': 'healthcare-and-pharmaceuticals', 'electronics-telecom': 'electronics-and-semiconductors',
       'agriculture': 'agriculture-and-fisheries', 'food-beverage': 'fast-moving-consumer-goods', 'automotive': 'automotive', 'retail': 'retail-and-e-commerce'}
def ind(slug): return NEW.get(slug, slug)
