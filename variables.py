import logging


abbreviation_sets = {
    'nouns': ['NN', 'NNS', 'NNP', 'NNPS'],
    'verbs': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
}
loglevel = logging.INFO
# loglevel = logging.DEBUG
logger = logging.getLogger("")
logger.setLevel(loglevel)
logging.basicConfig(
    filename='./logs.log',
    level=loglevel,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
maxfilenames = 100
Path = ''
repos_local_path = './repos/'
repos_to_clone_urls = [
    ['https://github.com/VladimirFilonov/wsdl2soaplib.git', 'git'],
    ['https://github.com/VladimirFilonov/discogs_client.git', 'git'],
    ['https://github.com/Nicolache/goipsend.git', 'git'],
]
top_size = 200
