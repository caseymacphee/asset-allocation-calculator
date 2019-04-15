from decimal import Decimal
from asset_allocation import *

total_investment = AssetCategory(
    'Total Investment',
    Decimal('1.0'),
    amount=Decimal('100'))

bonds = AssetCategory(
    'Bonds',
    Decimal('.30'))

stock = AssetCategory(
    'Stocks',
    Decimal('.70'))

total_investment.sub_nodes = {
    bonds,
    stock}

us_bonds = AssetCategory(
    'US Bonds',
    Decimal('.90'))

int_bonds = AssetCategory(
    'International Bonds',
    Decimal('.10'))

bonds.sub_nodes = {
    us_bonds,
    int_bonds}

muni_bonds = AssetCategory(
    'Municiple Bonds',
    Decimal('.50'))

treasury_bonds = AssetCategory(
    'Treasury Bonds',
    Decimal('.40'))

corporate_bonds = AssetCategory(
    'Corporate Bonds',
    Decimal('.10'))

us_bonds.sub_nodes = {
    muni_bonds,
    treasury_bonds,
    corporate_bonds}

us_stock = AssetCategory(
    'US Stock',
    Decimal('.90'))

int_stock = AssetCategory(
    'International Stock',
    Decimal('.10'))

stock.sub_nodes = {
    us_stock,
    int_stock}

managed_funds = AssetCategory(
    'Managed Funds',
    Decimal('0.0'))

index_funds = AssetCategory(
    'Index Funds',
    Decimal('.90'))

small_cap_index = AssetCategory(
    'Small Cap Index Funds',
    Decimal('.05'))

medium_cap_index = AssetCategory(
    'Medium Cap Index Funds',
    Decimal('.10'))

large_cap_index = AssetCategory(
    'Large Cap Index Funds',
    Decimal('.15'))

total_market_index = AssetCategory(
    'Total Market Index Funds',
    Decimal('.20'))

select_index = AssetCategory(
    'Select Index Funds',
    Decimal('.30'))

individual_stocks = AssetCategory(
    'Individual Stock',
    Decimal('.10'))

apple = Asset(
    'Apple',
    percentage=Decimal('.70'),
    allocation_type='PERCENTAGE')

msoft = Asset(
    'Microsoft',
    allocation_type='REMAINDER')

amzn = Asset(
    'Amazon',
    allocation_type='REMAINDER')

individual_stocks.sub_nodes = {
    apple,
    amzn,
    msoft}

us_stock.sub_nodes = {
    individual_stocks,
    index_funds,
    managed_funds}

index_funds.sub_nodes = {
    small_cap_index,
    medium_cap_index,
    large_cap_index,
    total_market_index,
    select_index}

total_market_index_fidel = Asset(
    'Fidelity total market',
    allocation_type='EVEN')

total_market_index_vguard = Asset(
    'Vanguard total market',
    allocation_type='EVEN')

total_market_index.sub_nodes = {
    total_market_index_fidel,
    total_market_index_vguard}

if __name__ == '__main__':
    allocations = AllocationTree(total_investment)
    results = allocations.calculate_amounts()
