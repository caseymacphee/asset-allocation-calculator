# asset-allocation-calculator

python -m test_allocation

You can either define an asset as a 'PERCENTAGE' combined with 'REMAINDER's or just 'EVEN' sub assets.

Assets Categories take a label and percentage represented as a decimal value.
The root node needs an amount but don't pass that to others or else it will override the calculated amount.

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

bond_fund_1 = Asset(
  'Bond Fund 1',
  allocation_type='EVEN')
  
bond_fund_2 = Asset(
  'Bond Fund 2',
  allocation_type='EVEN')
  
bonds.sub_nodes = {
  bond_fund_1,
  bond_fund_2}

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

stock.sub_nodes = {
    apple,
    amzn,
    msoft}


allocations = AllocationTree(total_investment)
allocations.calculate_amounts()
