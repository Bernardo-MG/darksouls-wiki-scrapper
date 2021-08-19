# -*- coding: utf-8 -*-

from scrapper.list_description import *
from scrapper.name_list import *
from scrapper.relation import *
from scrapper.misc import *
import logging
import configparser
import os

logging.basicConfig(
    filename='scrapper.log',
    filemode='w',
    level=logging.DEBUG,
    format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
)

# for handler in logging.root.handlers:
#     handler.addFilter(logging.Filter(['base', 'list', 'relation']))

config_path = 'config/urls.cfg'

url_config = configparser.ConfigParser()
url_config.read(config_path)

url_root = url_config['common']['root']

if not os.path.exists('output'):
    os.makedirs('output')

scrappers = []

scrappers.append(AmmunitionScrapper(url_root))
scrappers.append(ArmorScrapper(url_root))
scrappers.append(CatalystScrapper(url_root))
scrappers.append(EmberScrapper(url_root))
scrappers.append(KeyItemScrapper(url_root))
scrappers.append(MiracleScrapper(url_root))
scrappers.append(MiscellaneousItemScrapper(url_root))
scrappers.append(PyromancyScrapper(url_root))
scrappers.append(RingScrapper(url_root))
scrappers.append(ShieldScrapper(url_root))
scrappers.append(SorceryScrapper(url_root))
scrappers.append(SoulScrapper(url_root))
scrappers.append(TalismanScrapper(url_root))
scrappers.append(UpgradeMaterialScrapper(url_root))
scrappers.append(WeaponScrapper(url_root))

# for scrapper in scrappers:
#     scrapper.scrap()

# parser = WeaponTypeScrapper(url_root)
# parser.scrap()

parser = EnemyScrapper(url_root)
parser.scrap()
